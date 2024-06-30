"""
log handles the database work flow
"""

import os
import uuid
import bson
import json
from datetime import datetime
from typing import TypeAlias, Union, List, Optional, Any
from pydantic import BaseModel
from ox_db.ai.vector import Model
from ox_doc.ld import OxDoc


# Type Alias for key, uid, or date queries
SLBUnion: TypeAlias = Union[str, List[str], bool]
SLUnion: TypeAlias = Union[str, List[str]]


class Log:
    def __init__(self, db: str = "", db_path: Optional[str] = None):
        """
        Initialize instances of the Log class

        Args:
            db (str, optional): The name of the database. Defaults to "".
            db_path (Optional[str], optional): The path to the database directory. Defaults to None.
        """
        self.set_db(db, db_path)
        self.doc: Optional[str] = None
        self.vec = Model()
        self.set_doc()

    def set_db(self, db: str, db_path: Optional[str] = None) -> str:
        """
        Sets the database path.

        Args:
            db (str): The database name.
            db_path (Optional[str]): The database path.

        Returns:
            str: The path to the database.
        """
        self.db = db
        self.db_path = (
            db_path if db_path else os.path.join(os.path.expanduser("~"), db + ".ox-db")
        )
        os.makedirs(self.db_path, exist_ok=True)
        return self.db_path

    def get_db(self) -> str:
        """
        Returns the current database path.

        Returns:
            str: The database path.
        """
        return self.db_path

    def set_doc(self, doc: Optional[str] = None) -> str:
        """
        Sets the current document.

        Args:
            doc (Optional[str], optional): The document name. Defaults to None.

        Returns:
            str: The document name.
        """
        if doc is None:
            self.doc = self.doc or "log-" + datetime.now().strftime("[%d_%m_%Y]")
        elif self.doc != doc:
            self.doc = doc
        else:
            return self.doc

        self.doc_path = os.path.join(self.db_path, self.doc)
        os.makedirs(self.doc_path, exist_ok=True)

        self.data_oxd = self._create_oxd("data.oxd")
        self.vec_oxd = self._create_oxd("vec.oxd")

        doc_index_data = self.load_index(self.doc + ".index")
        self.doc_entry = doc_index_data["ox-db_init"]["doc_entry"]
        doc_index_data["ox-db_init"]["vec_model"] = self.vec.md_name
        self.save_index(self.doc, doc_index_data)

        return self.doc

    def _create_oxd(self, oxd_doc_name):
        oxd_doc_path = os.path.join(self.doc_path, oxd_doc_name)
        return OxDoc(oxd_doc_path)

    def get_doc(self) -> str:
        """
        Returns the current document.

        Returns:
            str: The document name.
        """
        return self.doc or self.set_doc()

    def push(
        self,
        data: Any,
        embeddings: SLBUnion = True,
        description: Optional[any] = None,
        metadata: Optional[dict] = None,
        key: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Pushes data to the log file. Can be called with either data or both key and data.

        Args:
            data (Any): The data to be logged.
            embeddings (bool, optional): Whether to generate embeddings. Defaults to True.
            description (Optional[any], optional): Description related to the data. Defaults to None.
            metadata (Optional[dict], optional): metadata related to the data. Defaults to None.
            key (Optional[str], optional): The key for the log entry. Defaults to None.
            doc (Optional[str], optional): The doc for the log entry. Defaults to None.
            data_type (Optional[str], optional): The data_type of log entry. Defaults to None.

        Returns:
            str: The unique ID of the log entry.
        """
        doc = self.get_doc()
        uid = self.gen_uid()

        if data == "" or data is None:
            raise ValueError("ox-db : No data provided for logging")
        doc_unit = {"data": data, "description": description}

        index_unit = {
            "uid": uid,
            "key": key or "key",
            "doc": doc,
            "time": datetime.now().strftime("%I:%M:%S_%p"),
            "date": datetime.now().strftime("%d_%m_%Y"),
            "metadata": metadata,
            "data_type": kwargs.get("data_type", type(data).__name__),
        }

        self.push_index(uid, index_unit, doc + ".index")
        self.data_oxd.set(uid, doc_unit)
        if embeddings:
            encoded_embeddings = (
                encoded_embeddings if embeddings != True else self.vec.encode(data)
            )
            self.vec_oxd.set(uid, encoded_embeddings)

        return uid

    def pull(
        self,
        uid: Optional[SLUnion] = None,
        key: Optional[str] = None,
        time: Optional[str] = None,
        date: Optional[str] = None,
        docfile: Optional[str] = "data.oxd",
        where={"metadata_key": "is_equal_to_this"},
        where_data={"$contains": "search_string"},
    ) -> List[dict]:
        """
        Retrieves log entries based on unique ID, key, time, or date.

        Args:
            uid (Optional[SLUnion], optional): The unique ID of the log entry. Defaults to None.
            key (Optional[str], optional): The key of the log entry. Defaults to None.
            time (Optional[str], optional): The time of the log entry. Defaults to None.
            date (Optional[str], optional): The date of the log entry. Defaults to None.
            docfile (Optional[str], optional): The specific file within the document. Defaults to None.
                eg : ["data.oxd","vec.oxd",".index"]
            where={"metadata_key": "value"},
            where_data={"$contains":"search_string"} ,
        Returns:
            List[dict]: The log entries matching the criteria.
        """
        if docfile not in ["data.oxd", "vec.oxd", ".index"]:
            raise ValueError(
                f"""ox-db : docfile should be ["data.oxd","vec.oxd",".index"] not {docfile} """
            )

        all_none = all(var is None for var in [key, uid, time, date])

        log_entries = []
        if all_none:
            content = self._retrive_doc_all(docfile)
            for uidx, unit in content.items():
                log_entries.append(
                    {
                        "uid": uidx,
                        "unit": unit,
                    }
                )
            return log_entries

        if uid is not None:
            uids = Log._convert_input(uid)[0]

            if docfile == ".index":
                file_content = self.load_index(self.doc + ".index")
                content = file_content["index"]
                for u in uids:
                    if u in content:
                        unit = content[u]
                        log_entries.append(
                            {
                                "uid": u,
                                "unit": unit,
                            }
                        )
                return log_entries
            else:
                return self._pull_oxd_by_uid(uid, docfile)

        if any([key, time, date]):
            uids = self.search_uid(key, time, date)
            log_entries_data = self.pull(uid=uids, docfile=docfile)
            log_entries.extend(log_entries_data)
            return log_entries

    def _pull_oxd_by_uid(self, uids, docfile):
        log_entries = []
        oxd_doc = self.vec_oxd if docfile == "vec.oxd" else self.data_oxd
        for u in uids:
            unit = oxd_doc.get(u)
            if not unit:
                continue
            log_entries.append(
                {
                    "uid": u,
                    "unit": unit,
                }
            )
        return log_entries

    def search(
        self,
        query: str,
        topn: int = 10,
        uid: Optional[SLUnion] = None,
        key: Optional[str] = None,
        time: Optional[str] = None,
        date: Optional[str] = None,
        log_entries: Optional[List[dict]] = None,
        by: Optional[str] = "dp",
    ) -> List[dict]:
        """
        Searches log entries based on a query and retrieves the top matching results.

        Args:
            query (str): The search query.
            topn (int, optional): Number of top results to return. Defaults to 10.
            uid (Optional[SLUnion], optional): The unique ID(s) of the log entry. Defaults to None.
            key (Optional[str], optional): The key of the log entry. Defaults to None.
            time (Optional[str], optional): The time of the log entry. Defaults to None.
            date (Optional[str], optional): The date of the log entry. Defaults to None.
            log_entries (Optional[List[dict]], optional): The log entry [{"uid":uid,unit:{"data":data,"description":description}}]  Defaults to None.
            by (Optional[str], optional): method of search
                dp : Dot Product (default)
                ed : Euclidean Distance
                cs : Cosine Similarity


        Returns:
            List[dict]: The log entries matching the search query.
        """
        log_entries = log_entries or self.pull(uid, key, time, date, docfile="vec.oxd")
        dataset = [entry["unit"] for entry in log_entries]
        top_idx = self.vec.search(query, dataset, topn=topn, by=by)
        if len(top_idx) == 0:
            return [{"uid": None, "unit": {"data": None, "description": None}}]
        uids = [log_entries[idx]["uid"] for idx in top_idx]
        res_data = self.pull(uid=uids)

        return res_data

    def show(
        self,
        key: Optional[str] = None,
        uid: Optional[SLUnion] = None,
        time: Optional[str] = None,
        doc: Optional[str] = None,
        date: Optional[str] = None,
    ):
        # Placeholder for future implementation
        pass

    def embed_all(self, doc: str):
        # Placeholder for future implementation
        pass

    @classmethod
    def gen_uid(cls) -> str:
        """
        Generates a unique ID for a log entry.

        Returns:
            str: The unique ID.
        """
        uid = str(uuid.uuid4())
        return uid

    def load_index(self, log_file: str) -> dict:
        """
        Loads data from a BSON or JSON file.

        Args:
            log_file (str): The log file name.

        Returns:
            dict: The loaded data.
        """
        log_file_path = self._get_logfile_path(log_file)
        try:
            with open(log_file_path, "rb+") as file:
                file_content = file.read()
                return bson.decode_all(file_content)[0] if file_content else {}

        except FileNotFoundError:
            file_content = {"ox-db_init": {"doc_entry": 0}, "index": {}}
            self.save_index(log_file, file_content)
            return file_content

    def save_index(self, log_file: str, file_content: dict):
        """
        Saves data to a BSON or JSON file.

        Args:
            log_file (str): The log file name.
            file_content (dict): The data to save.
        """
        log_file_path = self._get_logfile_path(log_file)

        def write_file(file, content):
            file.seek(0)
            file.truncate()
            file.write(bson.encode(content))

        try:
            mode = "rb+"
            with open(log_file_path, mode) as file:
                write_file(file, file_content)
        except FileNotFoundError:
            mode = "wb"
            with open(log_file_path, mode) as file:
                write_file(file, file_content)

    def search_uid(
        self,
        key: Optional[str] = None,
        time: Optional[str] = None,
        date: Optional[str] = None,
    ) -> List[str]:
        """
        Searches for UIDs based on key, time, or date.

        Args:
            key (Optional[str], optional): The key to search. Defaults to None.
            time (Optional[str], optional): The time to search. Defaults to None.
            date (Optional[str], optional): The date to search. Defaults to None.

        Returns:
            List[str]: The matching UIDs.
        """
        doc = self.get_doc()
        file_content = self.load_index(doc + ".index")
        content = file_content["index"]
        uids = []

        time_parts = self._parse_time(time) if time else [None, None, None, None]
        date_parts = self._parse_date(date) if date else [None, None, None]

        for uid, data in content.items():
            log_it = (
                self._match_time(data["time"], time_parts)
                or self._match_date(data["date"], date_parts)
                or key == data["key"]
            )

            if log_it:
                uids.append(uid)

        return uids

    def _get_logfile_path(self, log_file: str) -> str:
        """
        Constructs the full path to a log file.

        Args:
            log_file (str): The log file name.

        Returns:
            str: The full path to the log file.
        """
        self.doc_path = self.doc_path or os.path.join(self.db_path, self.doc)
        return os.path.join(self.doc_path, f"{log_file}.bson")

    def push_index(self, uid: str, index_unit: Any, log_file: str):
        """
        Pushes data to a specified log file.

        Args:
            uid (str): The unique ID for the log entry.
            data (Any): The data to be logged.
            log_file (str): The log file name.
        """
        if index_unit == "" or index_unit is None:
            raise ValueError("ox-db: No data provided for logging")

        file_content = self.load_index(log_file)
        file_content["index"][uid] = index_unit
        file_content["ox-db_init"]["doc_entry"] += 1
        self.doc_entry = file_content["ox-db_init"]["doc_entry"]

        self.save_index(log_file, file_content)
        print(f"ox-db: Logged data: {uid} in {log_file}")

    def _retrive_doc_all(self, docfile)->dict:
        """
        Retrieves all the content key value pairs as dict

        Args:
        docfile (Optional[str], optional): The specific file within the document. Defaults to None.
            eg : ["data.oxd","vec.oxd",".index"]

        Returns:
            dict: dict of the docfile
        """
        content = {}
        if docfile == ".index":
            file_content = self.load_index(self.doc + ".index")
            content = file_content["index"]
        elif docfile == "vec.oxd":
            content = self.vec_oxd.load_data()
        else:
            content = self.data_oxd.load_data()
        return content

    @staticmethod
    def _convert_input(*args: Union[str, List[str]]) -> List[List[str]]:
        """
        Converts input arguments to lists if they are strings.

        Args:
            args (Union[str, List[str]]): The input arguments.

        Returns:
            List[List[str]]: The converted arguments.
        """
        return [[arg] if isinstance(arg, str) else arg or [] for arg in args]

    @staticmethod
    def _parse_time(time: str) -> List[Optional[str]]:
        """
        Parses a time string into components.

        Args:
            time (str): The time string.

        Returns:
            List[Optional[str]]: The time components.
        """
        time_parts, period = (
            time.split("_") if "_" in time else (time, datetime.now().strftime("%p"))
        )
        return time_parts.split(":") + [period]

    @staticmethod
    def _parse_date(date: str) -> List[Optional[str]]:
        """
        Parses a date string into components.

        Args:
            date (str): The date string.

        Returns:
            List[Optional[str]]: The date components.
        """
        return date.split("_")

    @staticmethod
    def _match_time(log_time: str, query_time: List[Optional[str]]) -> bool:
        """
        Checks if the log time matches the query time.

        Args:
            log_time (str): The log time.
            query_time (List[Optional[str]]): The query time components.

        Returns:
            bool: Whether the log time matches the query time.
        """
        log_time_parts = log_time.split("_")[0].split(":") + [log_time.split("_")[1]]
        return (
            log_time_parts[: len(query_time) - 1] == query_time[:-1]
            and log_time_parts[-1] == query_time[-1]
        )

    @staticmethod
    def _match_date(log_date: str, query_date: List[Optional[str]]) -> bool:
        """
        Checks if the log date matches the query date.

        Args:
            log_date (str): The log date.
            query_date (List[Optional[str]]): The query date components.

        Returns:
            bool: Whether the log date matches the query date.
        """
        log_date_parts = log_date.split("_")
        return log_date_parts[: len(query_date)] == query_date
