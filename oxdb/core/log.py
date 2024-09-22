"""
# ox-db
"""

import os
from datetime import datetime
from typing import Dict, ForwardRef, Union, List, Optional, Any

from oxdoc.db import Oxdld, OxdMem
from oxdoc.dp import DBin

from oxdb.core.types import idxdata, embd, DOCFILE_LIST
from oxdb.ai.embed import VectorModel
from oxdb.settings import settings
from oxdb.utils.dp import (
    UIDX,
    delete_folder_and_contents,
    gen_hid,
    get_immediate_subdirectories,
    strorlist_to_list,
    to_json_string,
)

dbDoc = ForwardRef("dbDoc")
Default_vec_model = VectorModel()
dbin = DBin(method=settings.DBIN_METHOD)


class Oxdb:
    def __init__(
        self,
        db: str = None,
        db_path: Optional[str] = None,
        vec_model: Optional[VectorModel] = None,
    ):
        """
        Initializes an instance of the Oxdb class.

        Args:
            db (str, optional): The name of the database. Defaults to an empty string.
            db_path (Optional[str], optional): The path to the database directory. Defaults to None.
            vec_model (Optional[VectorModel], optional): A vector model instance for document operations. Defaults to None.
        """
        if db is not None and db_path is not None:
            raise ValueError(
                "Either `db` or `db_path` can be provided, but not both. Both can also be empty."
            )
        self.db: str = db
        self.vec: VectorModel = vec_model or Default_vec_model
        self.doc: Optional[dbDoc] = None
        self.doc_list: List[str] = []
        self.db_list: List[str] = []
        self.db_path: Optional[str] = None
        self.current_doc: Optional[str] = None
        self.get_db(db, db_path)

    def get_db(self, db: Optional[str] = None, db_path: Optional[str] = None) -> str:
        """
        Returns the current database path, optionally updating the database name and path.

        Args:
            db (Optional[str], optional): The name of the database. Defaults to None.
            db_path (Optional[str], optional): The path to the database directory. Defaults to None.

        Returns:
            str: The validated and potentially updated path to the database.
        """
        if db is not None and db_path is not None:
            raise ValueError(
                "Either `db` or `db_path` can be provided, but not both. Both can also be empty."
            )

        db = db or "" if not db_path else None
        self.db, self.db_path = self._db_path_validator(db, db_path)
        os.makedirs(self.db_path, exist_ok=True)
        self.get_doc()

        return self.info()

    def _db_path_validator(
        self, db: Optional[str] = None, db_path: Optional[str] = None
    ) -> str:
        """
        Validates and potentially updates the database path, appending the '.oxdb' extension if missing.

        Args:
            db (Optional[str], optional): The name of the database. Defaults to None.
            db_path (Optional[str], optional): The path to the database directory. Defaults to None.

        Returns:
            set(db,db_path): The validated and potentially updated path to the database.
        """
        if (db is None and db_path is None) or (db is not None and db_path is not None):
            raise ValueError(
                "Either `db` or `db_path` must be provided, but not both. Both must not be empty"
            )

        if db_path:
            dir_name = os.path.basename(db_path)
            db = dir_name.split(".oxdb")[0] if dir_name.endswith(".oxdb") else dir_name
            final_path = db_path if dir_name.endswith(".oxdb") else db_path + ".oxdb"
        elif db:
            db = db.split(".oxdb")[0] if db.endswith(".oxdb") else db
            final_path = os.path.join(os.path.expanduser("~"), "ox-db", db + ".oxdb")
        else:
            db, final_path = (
                "",
                os.path.join(os.path.expanduser("~"), "ox-db", ".oxdb"),
            )

        return db, final_path

    def get_doc(
        self, doc: Optional[str] = None, time_log: Optional[bool] = False
    ) -> dbDoc:
        """
        Returns an instance of the dbDoc class, connecting it to the database.

        Args:
            doc (Optional[str], optional): The document name. Defaults to None.
            time_log (Optional[bool], optional): The time as doc name. Defaults to False.

        Returns:
            dbDoc: An instance of the dbDoc class.
        """
        self.doc = dbDoc(doc)
        self.doc.connect_db(self.db_path, self.vec)
        self.current_doc = self.doc.doc_name
        return self.doc

    def get_docs(self) -> List[str]:
        """
        Returns a list of all document names in the current database directory.

        Returns:
            List[str]: A list of document names.
        """
        self.doc_list = get_immediate_subdirectories(self.db_path)
        return self.doc_list

    def get_dbs(self) -> List[str]:
        """
        Returns a list of all database names in the default database directory.

        Returns:
            List[str]: A list of database names.
        """
        db_root_path = os.path.join(os.path.expanduser("~"), "ox-db")
        self.db_list = get_immediate_subdirectories(db_root_path)
        return self.db_list

    def clean_up(self, db: Optional[str] = None, db_path: Optional[str] = None) -> bool:
        """
        Cleans up empty documents from the specified database or from all databases.

        Args:
            db (Optional[str], optional): The name of the database to clean. Defaults to None.
            db_path (Optional[str], optional): The path to the database. Defaults to None.

        Returns:
            bool: True if the cleanup was successful.
        """
        if db is not None and db_path is not None:
            raise ValueError(
                "Either `db` or `db_path` can be provided, but not both. Both can also be empty."
            )

        self.get_dbs()
        dbs_to_check = self.db_list
        path_given = False

        if db:
            dbs_to_check = [db]
        elif db_path:
            dbs_to_check = [db_path]
            path_given = True

        for db_pointer in dbs_to_check:
            if path_given:
                self.get_db(db_path=db_pointer)
            else:
                self.get_db(db=db_pointer)
            self.get_docs()

            is_db_empty = True
            for doc in self.doc_list:
                self.get_doc(doc)
                if not self.doc.data_oxd.index:
                    self.del_doc(doc)
                else:
                    self.doc.index_oxd.compact()
                    self.doc.data_oxd.compact()
                    self.doc.vec_oxd.compact()
                    is_db_empty = False
            if is_db_empty and self.db_path != db_path:
                self.del_db(db_path=self.db_path)

        return True

    def del_doc(self, doc: str) -> bool:
        """
        Deletes the specified document from the database.

        Args:
            doc (str): The name of the document to delete.

        Returns:
            bool: True if the document was successfully deleted.
        """
        self.get_docs()
        if doc in self.doc_list:
            doc_path = os.path.join(self.db_path, doc)
            delete_folder_and_contents(doc_path)
            if doc == self.current_doc:
                self.get_doc()

        return True

    def del_db(self, db: Optional[str] = None, db_path: Optional[str] = None) -> bool:
        """
        Deletes the specified database.

        Args:
            db (Optional[str], optional): The name of the database to delete. Defaults to None.
            db_path (Optional[str], optional): The path to the database to delete. Defaults to None.

        Returns:
            bool: True if the database was successfully deleted.
        """
        if (db is None and db_path is None) or (db is not None and db_path is not None):
            raise ValueError(
                "Either `db` or `db_path` must be provided, but not both. Both must not be empty"
            )

        db, del_path = self._db_path_validator(db=db, db_path=db_path)
        delete_folder_and_contents(del_path)

        if del_path == self.db_path:
            self.get_db()

        return True

    def info(self) -> Dict[str, Any]:
        """
        Returns detailed information about the current database and the active document.

        Returns:
            Dict[str, Any]: A dictionary containing information about the database, document, and VectorModel model.
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
    def __init__(self, doc: Optional[str] = None, time_log: Optional[bool] = False):
        """
        Initializes an instance of the dbDoc class, representing a document handler or pointer object.

        Args:
            doc (Optional[str], optional): The name of the document. Defaults to a timestamped name if not provided.
            time_log (Optional[bool], optional): The time as doc name. Defaults to False.
        """
        default_doc = (
            "log-doc"
            if not time_log
            else "log-doc" + datetime.now().strftime("[%d-%m-%Y]")
        )
        self.doc_name: str = doc or default_doc
        self.db_path: Optional[str] = None
        self.vec: VectorModel = None
        self.doc_path: Optional[str] = None

    def connect_db(self, db_path: str, vec: VectorModel) -> None:
        """
        Connects the document to the database and loads the document data.

        Args:
            db_path (str): The path to the database directory.
            vec (Any): The VectorModel model associated with the document.

        Raises:
            ValueError: If the database path is invalid.
        """
        if not db_path or not os.path.isdir(db_path):
            raise ValueError("Invalid database path provided.")
        self.db = os.path.basename(db_path)
        self.db_path = db_path
        self.vec: VectorModel = vec
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

        self.index_oxd: Oxdld = self._load_oxdld("index.oxdld")
        self.data_oxd: Oxdld = self._load_oxdld("data.oxdld")
        self.vec_oxd: Oxdld = self._load_oxdld("vec.oxdld")
        idxs = self.data_oxd.keys()
        self.uidx = UIDX(idxs)
        self.hid_set = set()
        for idx in idxs:
            self.hid_set.add(self.index_oxd[idx]["hid"])
        self.index_oxd["vec_model"] = self.vec.md_name

    def save_doc(self):
        # self.index_oxd.save_index
        # self.data_oxd.save_index
        # self.vec_oxd.save_index
        pass

    def __len__(self):
        return len(self.data_oxd.index)

    def len(self):
        return len(self.data_oxd.index)

    def _load_oxdld(self, oxd_doc_name: str) -> Oxdld:
        """
        Creates an Oxdld instance for the given document name.

        Args:
            oxd_doc_name (str): The name of the .oxd document to create.

        Returns:
            Oxdld: An instance of the Oxdld class representing the .oxd document.

        Raises:
            ValueError: If the .oxd document name is invalid.
        """
        if not oxd_doc_name:
            raise ValueError("The .oxd document name cannot be empty.")

        oxd_doc_path = os.path.join(self.doc_path, oxd_doc_name)
        return Oxdld(oxd_doc_path)

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
            "doc_entry": self.len(),
            "vec_model": self.index_oxd["vec_model"],
        }
        return res

    def push(
        self,
        data: Optional[Union[List[str], str]] = None,
        datax: Optional[Any] = None,
        uid: Optional[Union[str, list[str]]] = None,
        metadata: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        embeddings: Optional[Union[bool, list[list[int]]]] = True,
        log_time: Optional[bool] = False,
        **kwargs,
    ) -> list[str]:
        """
        Pushes data to the log file, generating a unique ID for each log entry.
        Supports batch processing of data entries.

        Args:
            data (Optional[Union[List[str], str]], optional): The data to be logged. Must not be empty or None.
            datax (Optional[Any], optional): Additional data that can be converted to a string and logged. Defaults to None.
            uid (Optional[Union[str, List[str]]], optional): A unique ID for each log entry. Defaults to None.
            metadata (Optional[Union[Dict[str, Any], List[Dict[str, Any]]]], optional): Additional metadata related to the data.
                Defaults to None.
            embeddings (Optional[Union[bool, List[List[int]]]], optional): If True, embeddings are generated for the data.
                If a list of embeddings is provided, they will be used instead. Defaults to True.
            log_time (Optional[bool,optional]) if need to include time and date as metadata then True,Defaults to False
        Returns:
            list[str]: A list of unique IDs for the log entries.

        Raises:
            ValueError: If the `data` argument is empty or None.
        """

        # Validation to ensure only one of `data` or `datax` is provided and neither is empty.
        if (data is None and datax is None) or (data is not None and datax is not None):
            raise ValueError("Either `data` or `datax` must be provided, but not both.")

        # Convert datax to a JSON string if provided
        datax = [to_json_string(datax)] if datax else None

        # Ensure all inputs are lists to facilitate batch processing
        data_list = datax or (data if isinstance(data, list) else [data])
        data_len = len(data_list)

        uid_list = uid if isinstance(uid, list) else [uid] * data_len
        metadata_list = (
            metadata if isinstance(metadata, list) else [metadata] * data_len
        )

        # Handle embeddings if required
        if embeddings is True:
            embedding_list: list[list[int]] = self.vec.generate(data_list)
        elif isinstance(embeddings, list):
            embedding_list = embeddings
        else:
            embedding_list = [[]] * data_len

        # Ensure all lists are the same length
        uid_list = uid_list + [None] * (data_len - len(uid_list))
        metadata_list = metadata_list + [None] * (data_len - len(metadata_list))
        embedding_list = embedding_list + [[]] * (data_len - len(embedding_list))

        oxd_index_dict = {}
        oxd_embedding_dict = {}
        oxd_data_dict = {}
        idx_list = []

        # Get the document name
        doc: str = self.get_doc_name()

        for i in range(data_len):
            hid: str = gen_hid(data_list[i])
            idx = None
            if hid in self.hid_set:

                for idxi in self.data_oxd.keys():
                    if hid == self.index_oxd[idxi]["hid"]:
                        if data_list[i] == self.data_oxd[idxi]:
                            idx = idxi
                            break

            if not idx:
                idx=self.uidx.gen()
                

            # Prepare the document unit and index metadata
            index_metadata: Dict[str, Any] = {
                # "uid": uid_list[i] or "uid",
                "doc": doc,
                "hid": hid,
            }
            if log_time:
                index_metadata["time"] = datetime.now().strftime("%H:%M:%S")
                index_metadata["date"] = datetime.now().strftime("%d-%m-%Y")

            if uid_list[i]:
                index_metadata["uid"] = uid_list[i]

            # Update index metadata with any additional metadata provided
            if metadata_list[i]:
                index_metadata.update(metadata_list[i])

            oxd_index_dict[idx] = index_metadata
            oxd_embedding_dict[idx] = embedding_list[i]
            oxd_data_dict[idx] = data_list[i]

            idx_list.append(int(idx))

        # Add the data and embeddings to the storage
        self.index_oxd.add(oxd_index_dict)
        self.data_oxd.add(oxd_data_dict)
        self.vec_oxd.add(oxd_embedding_dict)
        self.save_doc()

        return idx_list

    def pull(
        self,
        idx: idxdata = None,
        uid: Optional[str] = None,
        time: Optional[str] = None,
        date: Optional[str] = None,
        docfile: Optional[str] = "data.oxd",
        where: Optional[Dict[str, Any]] = None,
        where_data: Optional[Dict[str, Any]] = None,
        search_all_filter: Optional[bool] = False,
        apply_filter: Optional[bool] = True,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Retrieves log entries based on unique ID, uid, time, date, or additional filter criteria.

        Args:
            idx (Optional[List[int]], optional): The unique ID(s) of the log entry. Defaults to None.
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
        all_none = all(var is None for var in [uid, idx, time, date, where, where_data])
        if not apply_filter:
            all_none = True

        # If no filters are applied, retrieve all entries from the specified docfile
        if all_none:
            log_entries = self._retrive_doc_all(docfile)
            return log_entries

        # If `idx` is provided, retrieve entries by unique ID
        where = where or {}
        idx = idx or where.get(idx)
        if idx is not None:
            idxs_list = strorlist_to_list(idx)
            return self.pull_idx(idxs_list, docfile, where_data)

        # If any other filter criteria are provided, search for matching idxs and retrieve the corresponding entries
        if any([uid, time, date, where, where_data]):
            idxs_list = self.search_idx(
                hid=kwargs.get("hid", None),
                uid=uid,
                time=time,
                date=date,
                where=where,
                where_data=where_data,
                search_all_filter=search_all_filter,
            )
            log_entries = self.pull_idx(
                idxs=idxs_list, docfile=docfile, where_data=where_data
            )
            return log_entries

        return log_entries

    def pull_idx(
        self,
        idxs: idxdata,
        docfile: str,
        where_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Retrieves log entries based on a list of unique IDs (`idxs`) from a specified document file (`docfile`).

        Args:
            idxs (List[str]): A list of unique IDs representing the log entries to retrieve.
            docfile (str): The specific subfile within the document to search. Must be one of ["data.oxd", "vec.oxd", ".index"].
            where_data (Optional[Dict[str, Any]], optional): Data filter criteria for the log entry, particularly used for searching within "data.oxd". Defaults to None.

        Returns:
            Dict[str, Any]: A dictionary containing the log entries that match the given `idxs`.

        Raises:
            ValueError: If `docfile` is not a valid subfile within the document.
        """
        log_entries: Dict[str, Any] = {}
        content: Union[Dict[str, Any], Oxdld] = {}

        # Validate the `docfile` argument
        if docfile not in DOCFILE_LIST:
            raise ValueError(
                f"ox-db: `docfile` should be one of {DOCFILE_LIST}, not '{docfile}'"
            )

        # Determine which content to search based on `docfile`

        if docfile == "data.oxd" and where_data:
            search_string = where_data.get("search_string")
            if not search_string:
                return log_entries
            content = self.data_oxd

            # Search within the data using the provided `idxs` and `search_string`
            for idx in idxs:
                idx = str(idx)
                unit = content.get(idx)
                if unit:
                    if search_string in unit:
                        log_entries[idx] = unit
            return log_entries
        else:
            if docfile == "vec.oxd":
                content = self.vec_oxd

            elif docfile == ".index":
                content = self.index_oxd

            else:
                content = self.data_oxd

        # Retrieve log entries using the provided `idxs`
        for idx in idxs:
            idx = str(idx)
            unit = content.get(idx)
            if unit:
                log_entries[idx] = unit

        return log_entries

    def search(
        self,
        query: str,
        topn: int = 10,
        by: Optional[str] = settings.SIM_FORMAT,
        idx: idxdata = None,
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
            by (Optional[str], optional): The search method. Defaults to "dp".
                - "dp": Dot Product (default)
                - "ed": Euclidean Distance
                - "cs": Cosine Similarity
            idx (Optional[idxs], optional): The unique ID(s) of the log entry. Defaults to None.
            uid (Optional[str], optional): The uid of the log entry. Defaults to None.
            time (Optional[str], optional): The time of the log entry. Defaults to None.
            date (Optional[str], optional): The date of the log entry. Defaults to None.
            where (Optional[Dict[str, Any]], optional): Additional metadata filter criteria for the log entry. Defaults to None.
            where_data (Optional[Dict[str, Any]], optional): Data filter criteria, such as a specific search string within the log entries. Defaults to None.
            includes (Optional[List[str]], optional): Fields to include in the search results. Defaults to ["idx", "data", "description"].
            search_all_filter (Optional[bool], optional): Whether to apply all filters across all entries. Defaults to False.
            apply_filter_last (Optional[bool], optional): Whether to apply filters after VectorModel search. Defaults to False.
            where_data_before_vec_search (Optional[bool], optional): Whether to apply `where_data` filter before performing VectorModel search. Defaults to False.

        Returns:
            Dict[str, Any]: The search results, including matched log entries and their similarity scores.

        Raises:
            ValueError: If an invalid search method is provided for the `by` argument.
        """
        # Initialize the includes list if it's None
        if includes is None:
            includes = ["idx", "data", "metadata"]

        # Validate the search method
        if by not in settings.SIM_FORMATS:
            raise ValueError(
                f"Invalid search method '{by}'. Must be one of {settings.SIM_FORMATS}."
            )

        # Prepare the search query for pulling entries
        search_query = {
            "idx": idx,
            "uid": uid,
            "time": time,
            "date": date,
            "docfile": "vec.oxd",
            "where": where,
            "where_data": where_data,
            "search_all_filter": search_all_filter,
            "apply_filter": not apply_filter_last,
        }

        # Control whether `where_data` is applied before Vector search
        if not where_data_before_vec_search:
            search_query["where_data"] = None

        # Pull Vec log entries for the search
        vec_log_entries = self.pull(**search_query)
        dataset_idxs = list(vec_log_entries.keys())
        dataset = list(vec_log_entries.values())

        # Perform the search on the Vec data
        search_scores = self.vec.search(query, embeds=dataset, by=by)
        search_res = {
            "entries": 0,
            "idx": [],
            "data": [],
            "sim_score": [],
            "index": [],
            "embeddings": [],
        }

        # If no results found, return empty search results
        if len(search_scores["idx"]) == 0:
            return search_res

        # Retrieve the top matching embds
        top_idxs = [dataset_idxs[idx] for idx in search_scores["idx"][:topn]]

        # Apply additional filters if specified
        if apply_filter_last:
            search_query["idx"] = top_idxs
            search_query["apply_filter"] = True
            search_query["docfile"] = "data.oxd"
            search_query["where_data"] = where_data
            res_data = self.pull(**search_query)
        else:
            res_data = self.pull_idx(
                idxs=top_idxs, docfile="data.oxd", where_data=where_data
            )

        res_idxs = list(res_data.keys())
        res_len = len(res_idxs)
        search_res["entries"] = res_len
        search_res["idx"] = res_idxs

        # Populate the search results with data, descriptions, and other requested fields
        for idxi in res_idxs:
            search_res["data"].append(res_data[idxi])
            search_res["sim_score"].append(
                search_scores["sim_score"][
                    search_scores["idx"].index(dataset_idxs.index(idxi))
                ]
            )
            search_res["index"].append(self.index_oxd.get(idxi))
            if "embeddings" in includes:
                search_res["embeddings"].append(vec_log_entries[idxi])

        return search_res

    def delete(
        self,
        idx: Optional[Union[str, list[str]]] = None,
    ) -> list[str]:
        """
        delete data of the given idxs

        Args:
            idx (Optional[Union[str, List[str]]], optional): idx or list of idxs that need to be deleted

        Returns:
            list[str]: given input that got deleted

        Raises:
            ValueError: If `idx` is None
        """

        # Validation to ensure only one of `idx` or `doc` is provided and neither is empty.
        if idx is None:
            raise ValueError("Either `idx` or `doc` must be provided, but not both.")

        # Ensure all inputs are lists to facilitate batch processing

        idx_list = idx if isinstance(idx, list) else [idx]
        idx_list = [str(i) for i in idx_list]
        self.index_oxd.delete(idx_list)
        self.data_oxd.delete(idx_list)
        self.vec_oxd.delete(idx_list)
        self.uidx.delete(idx_list)

        self.save_doc()

        return idx_list

    def show(
        self,
        uid: Optional[str] = None,
        idx: Optional[str] = None,
        time: Optional[str] = None,
        doc: Optional[str] = None,
        date: Optional[str] = None,
    ) -> None:
        """
        Placeholder method to show specific log entries based on provided criteria.

        Args:
            uid (Optional[str], optional): The uid of the log entry. Defaults to None.
            idx (Optional[str], optional): The unique ID of the log entry. Defaults to None.
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
            content = self.index_oxd.load_data()
        elif docfile == "vec.oxd":
            content = self.vec_oxd.load_data()
        elif docfile == "data.oxd":
            content = self.data_oxd.load_data()
        else:
            raise ValueError(
                f"ox-db: Unknown document file '{docfile}' docfile should be {DOCFILE_LIST}"
            )
        return content

    def search_idx(
        self,
        hid: Optional[str] = None,
        uid: Optional[str] = None,
        time: Optional[str] = None,
        date: Optional[str] = None,
        where: Optional[Dict[str, Any]] = None,
        where_data: Optional[Dict[str, Any]] = None,
        search_all_filter: bool = False,
    ) -> List[str]:
        """
        Searches for IDXs based on uid, time, date, or additional filtering criteria.

        Args:
            uid (Optional[str], optional): The uid to search. Defaults to None.
            time (Optional[str], optional): The time to search. Defaults to None.
            date (Optional[str], optional): The date to search. Defaults to None.
            where (Optional[Dict[str, Any]], optional): Additional metadata filters, e.g., {"metadata_key": "value"}.
            where_data (Optional[Dict[str, Any]], optional): Additional data filters, e.g., {"in_data": "search_string"}.
            search_all_filter (bool, optional): If True, requires all filters to match. Defaults to False.

        Returns:
            List[str]: The list of matching IDXs.
        """
        where = where or {}

        iskey = uid or where.get("uid")
        ishid = hid or where.get("hid")
        istime = time or where.get("time")
        isdate = date or where.get("date")

        if iskey:
            where["uid"] = iskey
        if ishid:
            where["hid"] = ishid
        if istime:
            where["time"] = istime
        if isdate:
            where["date"] = isdate

        idxs = []

        for idx in self.data_oxd.keys():
            idx = str(idx)
            log_it = self._metadata_filter(
                where, self.index_oxd.get(idx), search_all_filter
            )
            if log_it:
                idxs.append(idx)

        return idxs

    @staticmethod
    def search_data(
        search_string: str, doc_data: Oxdld, output: str = "data"
    ) -> List[str]:
        """
        Searches through the document data for a specific string.

        Args:
            search_string (str): The string to search for within the data.
            doc_data (Dict[str, Dict[str, str]]): The dictionary containing IDXs and their corresponding data.
            output (str): out put list [idx,values]
        Returns:
            List[str]: The IDXs where the search string was found.
        """
        out = []
        for idx in doc_data.keys():
            data = doc_data.get(idx, "")
            if search_string in data:
                if output == "data":
                    out.append(data)
                else:
                    out.append(idx)
        return out

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
