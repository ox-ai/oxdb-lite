import requests
from typing import Any, Dict, ForwardRef, Optional, List, Union

from oxdb_lite.core.types import DOCFILE_LIST

dbDoc = ForwardRef("dbDoc")


class OxdbClient:
    def __init__(
        self,
        base_url: str,
        api_key: str = "ox-db-prime",
        db_name: str = None,
    ):
        """
        Initializes an instance of the OxdbClient class.

        Args:
            db (str, optional): The name of the database. Defaults to an empty string.
        """
        self.base_url = base_url.rstrip("/")
        self.db_name = db_name
        self.headers = {"x-api-key": api_key, "Content-Type": "application/json"}

    def alive(self) -> dict:
        """
        Returns the status of the Oxdb server.

        Returns:
            dict: A dictionary containing the status of the Oxdb server.
        """
        url = f"{self.base_url}/"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()  # Raise an error if the request failed
        return response.json()

    def get_db(self, db: str = None) -> dict:
        """
        Returns the current database path, optionally updating the database name and path.

        Args:
            db (str, optional): The name of the database. Defaults to an empty string.

        Returns:
            str: The validated and potentially updated path to the database.
        """
        self.db_name = db or self.db_name
        url = f"{self.base_url}/get-db/{self.db_name}"
        response = requests.post(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_doc(self, doc_name: str) -> "dbDoc":
        """
        Returns an instance of the OxDoc class, connecting it to the database.

        Args:
            doc (Optional[str], optional): The document name. Defaults to None.

        Returns:
            dbDoc: An instance of the dbDoc class.
        """
        self.get_db()  # Ensure the database is selected before accessing docs
        self.doc = dbDoc(self.base_url, doc_name, self.headers)
        return self.doc


class dbDoc:
    def __init__(self, base_url: str, doc_name: str, headers: Dict[str, str]):
        self.base_url = base_url
        self.doc_name = doc_name
        self.headers = headers

    def get_doc(self, doc: str) -> dict:
        """
        Loads a document by name and returns its path.

        Args:
            doc (str): The name of the document to load.

        Returns:
            str: The path to the loaded document.

        Raises:
            ValueError: If the document name is empty or invalid.
            HTTPError: If the server returns a 4xx/5xx status code.
        """
        url = f"{self.base_url}/get-doc/{doc}"
        response = requests.post(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def push(
        self,
        data: Optional[Union[List[str], str]] = None,
        datax: Optional[Any] = None,
        uid: Optional[Union[str, list[str]]] = None,
        description: Optional[Union[str, list[str]]] = None,
        metadata: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        embeddings: Optional[Union[bool, list[list[int]]]] = True,
    ) -> list[str]:
        """
        Sends a push request to the server to log the provided data.

        Args:
            data (Optional[Union[List[str], str]], optional): The data to be logged. Must not be empty or None.
            datax (Optional[Any], optional): Additional data that can be converted to a string and logged. Defaults to None.
            uid (Optional[Union[str, List[str]]], optional): A unique ID for each log entry. Defaults to None.
            description (Optional[Union[str, List[str]]], optional): A description related to the data. Defaults to None.
            metadata (Optional[Union[Dict[str, Any], List[Dict[str, Any]]]], optional): Additional metadata related to the data.
                Defaults to None.
            embeddings (Optional[Union[bool, List[List[int]]]], optional): If True, embeddings are generated for the data.
                If a list of embeddings is provided, they will be used instead. Defaults to True.
        Returns:
            list[str]: A list of unique IDs for the log entries.

        Raises:
            ValueError: If both `data` and `datax` are provided or if neither is provided.
            HTTPError: If the server returns a 4xx/5xx status code.
        """
        # Validation to ensure only one of `data` or `datax` is provided and neither is empty.
        if (data is None and datax is None) or (data is not None and datax is not None):
            raise ValueError("Either `data` or `datax` must be provided, but not both.")

        url = f"{self.base_url}/push"
        payload = {
            "data": data,
            "datax": datax,
            "embeddings": embeddings,
            "metadata": metadata,
            "uid": uid,
        }
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def pull(
        self,
        idx: Optional[Union[str, List[str]]] = None,
        uid: Optional[str] = None,
        time: Optional[str] = None,
        date: Optional[str] = None,
        docfile: Optional[str] = "data.oxd",
        where: Optional[Dict[str, Any]] = None,
        where_data: Optional[Dict[str, Any]] = None,
        search_all_filter: bool = False,
        apply_filter: bool = True,
    ) -> Dict[str, Any]:
        """
        Retrieves log entries based on unique ID, uid, time, date, or additional filter criteria.

        Args:
            idx (Optional[idxs], optional): The unique ID(s) of the log entry. Defaults to None.
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
            HTTPError: If the server returns a 4xx/5xx status code.
        """
        # Validate the `docfile` argument
        if docfile not in DOCFILE_LIST:
            raise ValueError(
                f"ox-db: `docfile` should be one of {DOCFILE_LIST}, not '{docfile}'"
            )

        url = f"{self.base_url}/pull"
        payload = {
            "idx": idx,
            "uid": uid,
            "time": time,
            "date": date,
            "docfile": docfile,
            "where": where,
            "where_data": where_data,
            "search_all_filter": search_all_filter,
            "apply_filter": apply_filter,
        }
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def search(
        self,
        query: str,
        topn: int = 10,
        by: Optional[str] = "dp",
        idx: Optional[List[str]] = None,
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
            apply_filter_last (Optional[bool], optional): Whether to apply filters after vector search. Defaults to False.
            where_data_before_vec_search (Optional[bool], optional): Whether to apply `where_data` filter before performing vector search. Defaults to False.

        Returns:
            Dict[str, Any]: The search results, including matched log entries and their similarity scores.

        Raises:
            ValueError: If an invalid search method is provided for the `by` argument.
        """
        url = f"{self.base_url}/search"
        payload = {
            "query": query,
            "topn": topn,
            "by": by,
            "idx": idx,
            "uid": uid,
            "time": time,
            "date": date,
            "where": where,
            "where_data": where_data,
            "includes": includes,
            "search_all_filter": search_all_filter,
            "apply_filter_last": apply_filter_last,
            "where_data_before_vec_search": where_data_before_vec_search,
        }
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
