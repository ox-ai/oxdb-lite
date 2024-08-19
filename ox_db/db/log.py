"""
# ox-db
"""

import os
import bson
from datetime import datetime
from typing import Dict, ForwardRef, Union, List, Optional, Any

from ox_doc.ld import OxDoc

from ox_db.db.types import embd, hids, DOCFILE_LIST
from ox_db.ai.vector import Model
from ox_db.utils.dp import (
    gen_hid,
    get_immediate_subdirectories,
    strorlist_to_list,
    to_json_string,
)

dbDoc = ForwardRef("dbDoc")
Default_vec_model = Model()


class Oxdb:
    def __init__(self, db: str = "", db_path: Optional[str] = None,vec_model:Model = None):
        """
        Initializes an instance of the Oxdb class.

        Args:
            db (str, optional): The name of the database. Defaults to an empty string.
            db_path (Optional[str], optional): The path to the database directory. Defaults to None.
        """
        self.db: str = db
        self.vec: Model = vec_model or Default_vec_model
        self.doc: Optional[dbDoc] = None
        self.doc_list: List[str] = []

        self.db_path: str = None
        self.get_db(db, db_path)

    
    def get_db(self, db: str = "", db_path: Optional[str] = None) -> str:
        """
        Returns the current database path, optionally updating the database name and path.

        Args:
            db (str, optional): The name of the database. Defaults to an empty string.
            db_path (Optional[str], optional): The path to the database directory. Defaults to None.

        Returns:
            str: The validated and potentially updated path to the database.
        """
        self.db = db
        self.db_path = self._db_path_validator(db, db_path)
        os.makedirs(self.db_path, exist_ok=True)
        self.get_doc()
    
        return self.info

    def _db_path_validator(self, db: str = "", db_path: Optional[str] = None) -> str:
        """
        Validates and potentially updates the database path, appending the '.oxdb' extension if missing.

        Args:
            db (str, optional): The name of the database. Defaults to an empty string.
            db_path (Optional[str], optional): The path to the database directory. Defaults to None.

        Returns:
            str: The validated and potentially updated path to the database.
        """
        if db_path:
            dir_name = os.path.basename(db_path)
            if not dir_name.endswith(".oxdb"):
                new_dir_name = dir_name + ".oxdb"
                final_path = os.path.join(os.path.dirname(db_path), new_dir_name)
            else:
                final_path = db_path
        else:
            final_path = os.path.join(os.path.expanduser("~"), "ox-db", db + ".oxdb")

        return final_path

    def get_doc(self, doc: Optional[str] = None) -> dbDoc:  # type: ignore # Forward reference
        """
        Returns an instance of the OxDoc class, connecting it to the database.

        Args:
            doc (Optional[str], optional): The document name. Defaults to None.

        Returns:
            dbDoc: An instance of the dbDoc class.
        """
        self.doc = dbDoc(doc)
        self.doc.connect_db(self.db_path, self.vec)
        return self.doc

    def get_docs(self) -> List[str]:
        """
        Returns a list of all document names in the current database directory.

        Returns:
            List[str]: A list of document names.
        """
        self.doc_list = get_immediate_subdirectories(self.db_path)
        return self.doc_list

    def info(self) -> Dict[str, Any]:
        """
        Returns detailed information about the current database and the active document.

        Returns:
            Dict[str, Any]: A dictionary containing information about the database, document, and vector model.
        """
        res = {
            "db": self.db,
            "db_path": self.db_path,
            "doc_name": self.doc.doc_name if self.doc else None,
            "doc_path": self.doc.doc_path if self.doc else None,
            "doc_list": self.get_docs(),
            "vec_model": self.vec.md_name,
        }
        return res


class dbDoc:
    def __init__(self, doc: Optional[str] = None):
        """
        Initializes an instance of the dbDoc class, representing a document handler or pointer object.

        Args:
            doc (Optional[str], optional): The name of the document. Defaults to a timestamped name if not provided.
        """
        self.doc_name: str = doc or "log-" + datetime.now().strftime("[%d_%m_%Y]")
        self.db_path: Optional[str] = None
        self.vec: Model = None
        self.doc_path: Optional[str] = None
        self.doc_index_path: Optional[str] = None
        self.doc_reg: Dict[str, Any] = {}

    def connect_db(self, db_path: str, vec: Model) -> None:
        """
        Connects the document to the database and loads the document data.

        Args:
            db_path (str): The path to the database directory.
            vec (Any): The vector model associated with the document.

        Raises:
            ValueError: If the database path is invalid.
        """
        if not db_path or not os.path.isdir(db_path):
            raise ValueError("Invalid database path provided.")
        self.db = os.path.basename(db_path)
        self.db_path = db_path
        self.vec: Model = vec
        self.load_doc(self.doc_name)

    def get_doc(self, doc: str) -> str:
        """
        Loads a document by name and returns its path.

        Args:
            doc (str): The name of the document to load.

        Returns:
            str: The path to the loaded document.

        Raises:
            ValueError: If the document name is empty or invalid.
        """
        if not doc:
            raise ValueError("Document name cannot be empty.")

        self.load_doc(doc)
        return self.info()

    def load_doc(self, doc: str) -> None:
        """
        Loads the document and its associated data, creating necessary files if they don't exist.

        Args:
            doc (str): The name of the document to load.

        Raises:
            ValueError: If the document name is empty or invalid.
        """
        if not doc:
            raise ValueError("Document name cannot be empty.")

        self.doc_name = doc
        self.doc_path = os.path.join(self.db_path, self.doc_name)
        os.makedirs(self.doc_path, exist_ok=True)
        self.doc_index_path = os.path.join(self.doc_path, self.doc_name + ".index")

        self.load_index()
        self.data_oxd: OxDoc = self._create_oxd("data.oxd")
        self.vec_oxd: OxDoc = self._create_oxd("vec.oxd")
        self.doc_reg["vec_model"] = self.vec.md_name
        self.save_index()

    def _create_oxd(self, oxd_doc_name: str) -> OxDoc:
        """
        Creates an OxDoc instance for the given document name.

        Args:
            oxd_doc_name (str): The name of the .oxd document to create.

        Returns:
            OxDoc: An instance of the OxDoc class representing the .oxd document.

        Raises:
            ValueError: If the .oxd document name is invalid.
        """
        if not oxd_doc_name:
            raise ValueError("The .oxd document name cannot be empty.")

        oxd_doc_path = os.path.join(self.doc_path, oxd_doc_name)
        return OxDoc(oxd_doc_path)

    def get_doc_name(self) -> str:
        """
        Returns the current document's name.

        Returns:
            str: The name of the current document.
        """
        return self.doc_name

    def info(self) -> Dict[str, Any]:
        """
        Returns detailed information about the current document.

        Returns:
            Dict[str, Any]: A dictionary containing information about the document.
        """
        res = {
            "db": self.db,
            "db_path": self.db_path,
            "doc_name": self.doc_name,
            "doc_path": self.doc_path,
            "doc_reg": self.doc_reg,
        }
        return res

    def push(
        self,
        data: Any,
        embeddings: embd = True,
        description: Optional[Any] = None,
        metadata: Optional[Dict[str, Any]] = None,
        uid: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Pushes data to the log file. Generates a unique ID for each log entry.

        Args:
            data (Any): The data to be logged. Must not be empty or None.
            embeddings (embd, optional): Indicates whether to generate embeddings for the data. Defaults to True.
            description (Optional[Any], optional): A description related to the data. Defaults to None.
            metadata (Optional[Dict[str, Any]], optional): Additional metadata related to the data. Defaults to None.
            uid (Optional[str], optional): A uid for the log entry. Defaults to None.

            eg:
            metadata = {metadata_key:value}
        Returns:
            str: The unique ID of the log entry.

        Raises:
            ValueError: If the data is empty or None.
        """

        # Validate input data
        if not data:
            raise ValueError("ox-db: No data provided for logging.")

        data = to_json_string(data)
        # Get the document name
        doc: str = self.get_doc_name()
        hid: str = gen_hid(data)
        if hid in self.doc_index:
            return hid

        # Prepare the document unit and index metadata
        doc_unit: Dict[str, Any] = {"data": data, "description": description}
        index_metadata: Dict[str, Any] = {
            "uid": uid or "uid",
            "doc": doc,
            "time": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%d-%m-%Y"),
        }

        # Update index metadata with any additional metadata provided
        if metadata:
            index_metadata.update(metadata)

        # Push the index and data to the corresponding storage
        self.push_index(hid, index_metadata)
        self.data_oxd.set(hid, doc_unit)

        # Handle embeddings if required
        if embeddings:
            encoded_embeddings: Any = (
                embeddings
                if not isinstance(embeddings, bool)
                else self.vec.encode(data)
            )
            self.vec_oxd.set(hid, encoded_embeddings)

        return hid

    def pull(
        self,
        hid: Optional[hids] = None,
        uid: Optional[str] = None,
        time: Optional[str] = None,
        date: Optional[str] = None,
        docfile: Optional[str] = "data.oxd",
        where: Optional[Dict[str, Any]] = None,
        where_data: Optional[Dict[str, Any]] = None,
        search_all_filter: Optional[bool] = False,
        apply_filter: Optional[bool] = True,
    ) -> List[Dict[str, Any]]:
        """
        Retrieves log entries based on unique ID, uid, time, date, or additional filter criteria.

        Args:
            hid (Optional[hids], optional): The unique ID(s) of the log entry. Defaults to None.
            uid (Optional[str], optional): The uid of the log entry. Defaults to None.
            time (Optional[str], optional): The time of the log entry. Defaults to None.
            date (Optional[str], optional): The date of the log entry. Defaults to None.
            docfile (Optional[str], optional): The specific subfile within the document to search.
                Defaults to "data.oxd". Must be one of ["data.oxd", "vec.oxd", ".index"].
            where (Optional[Dict[str, Any]], optional): Additional metadata filter criteria. Defaults to None.
            where_data (Optional[Dict[str, Any]], optional): Data filter criteria for the log entry. Defaults to None.
            search_all_filter (Optional[bool], optional): Whether to search all entries regardless of filters. Defaults to False.
            apply_filter (Optional[bool], optional): Whether to apply filtering criteria. Defaults to True.

            eg :
            where={"metadata_key": "value"},
            where_data={"search_string":"query_search_string"} ,
        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the log entries matching the criteria.

        Raises:
            ValueError: If `docfile` is not a valid subfile within the document.
        """

        # Validate the `docfile` argument
        if docfile not in DOCFILE_LIST:
            raise ValueError(
                f"ox-db: `docfile` should be one of {DOCFILE_LIST}, not '{docfile}'"
            )

        log_entries: Dict[str, Any] = {}

        # Check if all filters are None
        all_none = all(var is None for var in [uid, hid, time, date, where, where_data])
        if not apply_filter:
            all_none = True

        # If no filters are applied, retrieve all entries from the specified docfile
        if all_none:
            log_entries = self._retrive_doc_all(docfile)
            return log_entries

        # If `hid` is provided, retrieve entries by unique ID
        where = where or {}
        hid = hid or where.get(hid)
        if hid is not None:
            hids_list = strorlist_to_list(hid)
            return self.pull_hid(hids_list, docfile, where_data)

        # If any other filter criteria are provided, search for matching hIDs and retrieve the corresponding entries
        if any([uid, time, date, where, where_data]):
            hids_list = self.search_hid(
                uid, time, date, where, where_data, search_all_filter
            )
            log_entries = self.pull_hid(
                hids=hids_list, docfile=docfile, where_data=where_data
            )
            return log_entries

        return log_entries

    def pull_hid(
        self,
        hids: List[str],
        docfile: str,
        where_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves log entries based on a list of unique IDs (`hids`) from a specified document file (`docfile`).

        Args:
            hids (List[str]): A list of unique IDs representing the log entries to retrieve.
            docfile (str): The specific subfile within the document to search. Must be one of ["data.oxd", "vec.oxd", ".index"].
            where_data (Optional[Dict[str, Any]], optional): Data filter criteria for the log entry, particularly used for searching within "data.oxd". Defaults to None.

        Returns:
            Dict[str, Any]: A dictionary containing the log entries that match the given `hids`.

        Raises:
            ValueError: If `docfile` is not a valid subfile within the document.
        """
        log_entries: Dict[str, Any] = {}
        content: Union[Dict[str, Any], OxDoc] = {}

        # Validate the `docfile` argument
        if docfile not in DOCFILE_LIST:
            raise ValueError(
                f"ox-db: `docfile` should be one of {DOCFILE_LIST}, not '{docfile}'"
            )

        # Determine which content to search based on `docfile`
        if docfile == ".index":
            content = self.doc_index
        elif docfile == "data.oxd" and where_data:
            search_string = where_data.get("search_string")
            if not search_string:
                return log_entries
            content = self.data_oxd

            # Search within the data using the provided `hids` and `search_string`
            for hidx in hids:
                unit = content.get(hidx)
                if unit:
                    if search_string in unit["data"]:
                        log_entries[hidx] = unit
            return log_entries
        else:
            content = self.vec_oxd if docfile == "vec.oxd" else self.data_oxd

        # Retrieve log entries using the provided `hids`
        for hidx in hids:
            unit = content.get(hidx)
            if unit:
                log_entries[hidx] = unit

        return log_entries

    def search(
        self,
        query: str,
        topn: int = 10,
        log_entries: Optional[Dict[str, Dict[str, Any]]] = None,
        by: Optional[str] = "dp",
        hid: Optional[hids] = None,
        uid: Optional[str] = None,
        time: Optional[str] = None,
        date: Optional[str] = None,
        where: Optional[Dict[str, Any]] = None,
        where_data: Optional[Dict[str, Any]] = None,
        includes: Optional[List[str]] = None,
        search_all_filter: Optional[bool] = False,
        apply_filter_last: Optional[bool] = False,
        where_data_before_vec_search: Optional[bool] = False,
    ) -> Dict[str, Any]:
        """
        Searches log entries based on a query and retrieves the top matching results.

        Args:
            query (str): The search query string.
            topn (int, optional): Number of top results to return. Defaults to 10.
            log_entries (Optional[Dict[str, Dict[str, Any]]], optional): Pre-fetched log entries to search within. Defaults to None.
            by (Optional[str], optional): The search method. Defaults to "dp".
                - "dp": Dot Product (default)
                - "ed": Euclidean Distance
                - "cs": Cosine Similarity
            hid (Optional[hids], optional): The unique ID(s) of the log entry. Defaults to None.
            uid (Optional[str], optional): The uid of the log entry. Defaults to None.
            time (Optional[str], optional): The time of the log entry. Defaults to None.
            date (Optional[str], optional): The date of the log entry. Defaults to None.
            where (Optional[Dict[str, Any]], optional): Additional metadata filter criteria for the log entry. Defaults to None.
            where_data (Optional[Dict[str, Any]], optional): Data filter criteria, such as a specific search string within the log entries. Defaults to None.
            includes (Optional[List[str]], optional): Fields to include in the search results. Defaults to ["hid", "data", "description"].
            search_all_filter (Optional[bool], optional): Whether to apply all filters across all entries. Defaults to False.
            apply_filter_last (Optional[bool], optional): Whether to apply filters after vector search. Defaults to False.
            where_data_before_vec_search (Optional[bool], optional): Whether to apply `where_data` filter before performing vector search. Defaults to False.

        Returns:
            Dict[str, Any]: The search results, including matched log entries and their similarity scores.

        Raises:
            ValueError: If an invalid search method is provided for the `by` argument.
        """
        # Initialize the includes list if it's None
        if includes is None:
            includes = ["hid", "data", "description"]

        # Validate the search method
        valid_search_methods = ["dp", "ed", "cs"]
        if by not in valid_search_methods:
            raise ValueError(
                f"Invalid search method '{by}'. Must be one of {valid_search_methods}."
            )

        # Prepare the search query for pulling entries
        search_query = {
            "hid": hid,
            "uid": uid,
            "time": time,
            "date": date,
            "docfile": "vec.oxd",
            "where": where,
            "where_data": where_data,
            "search_all_filter": search_all_filter,
            "apply_filter": not apply_filter_last,
        }

        # Control whether `where_data` is applied before vector search
        if not where_data_before_vec_search:
            search_query["where_data"] = None

        # Pull vector log entries for the search
        vec_log_entries = log_entries or self.pull(**search_query)
        dataset_hids = list(vec_log_entries.keys())
        dataset = list(vec_log_entries.values())

        # Perform the search on the vector data
        search_scores = self.vec.search(query, dataset, by=by)
        search_res = {
            "entries": 0,
            "hid": [],
            "data": [],
            "description": [],
            "sim_score": [],
            "index": [],
            "embeddings": [],
        }

        # If no results found, return empty search results
        if len(search_scores["idx"]) == 0:
            return search_res

        # Retrieve the top matching hIDs
        top_hids = [dataset_hids[idx] for idx in search_scores["idx"][:topn]]

        # Apply additional filters if specified
        if apply_filter_last:
            search_query["hid"] = top_hids
            search_query["apply_filter"] = True
            search_query["docfile"] = "data.oxd"
            search_query["where_data"] = where_data
            res_data = self.pull(**search_query)
        else:
            res_data = self.pull_hid(
                hids=top_hids, docfile="data.oxd", where_data=where_data
            )

        res_hids = list(res_data.keys())
        res_len = len(res_hids)
        search_res["entries"] = res_len
        search_res["hid"] = res_hids

        # Populate the search results with data, descriptions, and other requested fields
        for hidx in res_hids:
            search_res["data"].append(res_data[hidx]["data"])
            search_res["description"].append(res_data[hidx]["description"])
            search_res["sim_score"].append(
                search_scores["sim_score"][
                    search_scores["idx"].index(dataset_hids.index(hidx))
                ]
            )
            search_res["index"].append(self.doc_index.get(hidx))
            if "embeddings" in includes:
                search_res["embeddings"].append(vec_log_entries[hidx])

        return search_res

    def show(
        self,
        uid: Optional[str] = None,
        hid: Optional[str] = None,
        time: Optional[str] = None,
        doc: Optional[str] = None,
        date: Optional[str] = None,
    ) -> None:
        """
        Placeholder method to show specific log entries based on provided criteria.

        Args:
            uid (Optional[str], optional): The uid of the log entry. Defaults to None.
            hid (Optional[str], optional): The unique ID of the log entry. Defaults to None.
            time (Optional[str], optional): The time of the log entry. Defaults to None.
            doc (Optional[str], optional): The document name to retrieve from. Defaults to None.
            date (Optional[str], optional): The date of the log entry. Defaults to None.
        """
        pass  # Implementation will be added in the future

    def embed_all(self, doc: str) -> None:
        """
        Placeholder method to embed all data entries in a document.

        Args:
            doc (str): The document name to process.
        """
        pass  # Implementation will be added in the future

    def load_index(self) -> Dict[str, Any]:
        """
        Loads data from the index file, which may be in BSON or JSON format.

        Returns:
            Dict[str, Any]: The loaded index data.

        Raises:
            FileNotFoundError: If the index file does not exist, a new index will be initialized and saved.
        """
        try:
            with open(self.doc_index_path, "rb+") as file:
                file_content = file.read()
                if file_content:
                    content = bson.decode_all(file_content)[0]
                else:
                    content = {}
                self.doc_reg = content.get("doc_reg", {"entry": 0})
                self.doc_index = content.get("index", {})
                return content

        except FileNotFoundError:
            content = {"doc_reg": {"entry": 0}, "index": {}}
            self.doc_reg = content["doc_reg"]
            self.doc_index = content["index"]
            self.save_index()
            return content

    def save_index(self) -> None:
        """
        Saves the current state of the index to the index file in BSON format.
        """
        log_file_path = self.doc_index_path
        content = {"doc_reg": self.doc_reg, "index": self.doc_index}

        def write_file(file, content) -> None:
            file.seek(0)
            file.truncate()
            file.write(bson.encode(content))

        try:
            mode = "rb+"
            with open(log_file_path, mode) as file:
                write_file(file, content)
        except FileNotFoundError:
            mode = "wb"
            with open(log_file_path, mode) as file:
                write_file(file, content)

    def push_index(self, hid: str, index_unit: Any) -> None:
        """
        Pushes an index entry to the index file.

        Args:
            hid (str): The unique ID for the log entry.
            index_unit (Any): The index data to be logged.
            log_file (str): The log file name to save the index.

        Raises:
            ValueError: If `index_unit` is empty or None.
        """
        if not index_unit:
            raise ValueError("ox-db: No data provided for logging")
        self.doc_index[hid] = index_unit
        self.doc_reg["entry"] += 1
        self.save_index()

    def _retrive_doc_all(self, docfile: str) -> Dict[str, Any]:
        """
        Retrieves all the content indexkey-value pairs from a specified document file.

        Args:
            docfile (str): The specific file within the document, e.g., ["data.oxd", "vec.oxd", ".index"].

        Returns:
            Dict[str, Any]: A dictionary containing all the data from the specified document file.

        Raises:
            ValueError: If the specified `docfile` is not recognized.
        """
        content = {}
        if docfile == ".index":
            content = self.doc_index
        elif docfile == "vec.oxd":
            content = self.vec_oxd.load_data()
        elif docfile == "data.oxd":
            content = self.data_oxd.load_data()
        else:
            raise ValueError(
                f"ox-db: Unknown document file '{docfile}' docfile should be {DOCFILE_LIST}"
            )
        return content

    def search_hid(
        self,
        uid: Optional[str] = None,
        time: Optional[str] = None,
        date: Optional[str] = None,
        where: Optional[Dict[str, Any]] = None,
        where_data: Optional[Dict[str, Any]] = None,
        search_all_filter: bool = False,
        **kwargs,
    ) -> List[str]:
        """
        Searches for hIDs based on uid, time, date, or additional filtering criteria.

        Args:
            uid (Optional[str], optional): The uid to search. Defaults to None.
            time (Optional[str], optional): The time to search. Defaults to None.
            date (Optional[str], optional): The date to search. Defaults to None.
            where (Optional[Dict[str, Any]], optional): Additional metadata filters, e.g., {"metadata_key": "value"}.
            where_data (Optional[Dict[str, Any]], optional): Additional data filters, e.g., {"in_data": "search_string"}.
            search_all_filter (bool, optional): If True, requires all filters to match. Defaults to False.

        Returns:
            List[str]: The list of matching hIDs.
        """
        where = where or {}

        iskey = uid or where.get("uid")
        istime = time or where.get("time")
        isdate = date or where.get("date")

        if iskey:
            where["uid"] = iskey
        if istime:
            where["time"] = istime
        if isdate:
            where["date"] = isdate

        content = self.doc_index
        hids = []

        for hid, index_metadata in content.items():
            log_it = self._metadata_filter(where, index_metadata, search_all_filter)
            if log_it:
                hids.append(hid)

        return hids

    @staticmethod
    def search_data(
        search_string: str, doc_data_dict: Dict[str, Dict[str, str]]
    ) -> List[str]:
        """
        Searches through the document data for a specific string.

        Args:
            search_string (str): The string to search for within the data.
            doc_data_dict (Dict[str, Dict[str, str]]): The dictionary containing hIDs and their corresponding data.

        Returns:
            List[str]: The hIDs where the search string was found.
        """
        hids = []
        for hid, doc_data in doc_data_dict.items():
            if search_string in doc_data.get("data", ""):
                hids.append(hid)

        return hids

    @staticmethod
    def _metadata_filter(
        query_dict: Dict[str, Any],
        data_dict: Dict[str, Any],
        search_all_filter: bool = False,
    ) -> bool:
        """
        Checks if at least one metakey-value pair from the query_dict matches the data_dict.

        Args:
            query_dict (Dict[str, Any]): The metakey-value pairs to match.
            data_dict (Dict[str, Any]): The data to be checked against.
            search_all_filter (bool, optional): If True, all filters must match. Defaults to False.

        Returns:
            bool: True if the query matches the data; otherwise, False.
        """
        if data_dict is None:
            return False
        partial_filters = ["time", "date"]
        if not search_all_filter:
            for metakey in query_dict.keys():
                qvalue = query_dict.get(metakey)
                dvalue = data_dict.get(metakey)

                if dvalue is None:
                    return False
                elif (metakey in partial_filters) and (qvalue in dvalue):
                    return True
                elif query_dict[metakey] == dvalue:
                    return True
            return False
        else:

            for metakey in query_dict.keys():
                qvalue = query_dict.get(metakey)
                dvalue = data_dict.get(metakey)

                if dvalue is None:
                    return False

                elif (metakey in partial_filters) and (qvalue in dvalue):
                    continue
                elif query_dict[metakey] != dvalue:
                    return False
            return True
