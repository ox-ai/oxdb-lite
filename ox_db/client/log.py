import requests
from typing import Any, Dict, Optional, List, Union


class OxdbClient:
    def __init__(
        self,
        base_url: str,
        api_key: str = "ox-db-prime",
        db_name: str = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.db_name = db_name
        self.headers = {"x-api-key": api_key, "Content-Type": "application/json"}

    def get_db(self, db: str = None) -> dict:
        self.db_name = db or self.db_name
        url = f"{self.base_url}/get-db/{self.db_name}"
        response = requests.post(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_doc(self, doc_name: str) -> "dbDoc":
        self.get_db()  # Ensure the database is selected before accessing docs
        self.doc = dbDoc(self.base_url, doc_name, self.headers)
        return self.doc


class dbDoc:
    def __init__(self, base_url: str, doc_name: str, headers: Dict[str, str]):
        self.base_url = base_url
        self.doc_name = doc_name
        self.headers = headers

    def get_doc(self) -> dict:
        url = f"{self.base_url}/get-doc/{self.doc_name}"
        response = requests.post(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def push(
        self,
        data: Optional[Union[List[str], str]] = None,
        datax: Optional[Any] = None,
        uid: Optional[str] = None,
        embeddings: bool = True,
        description: Optional[Union[str, List[str]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> dict:
        """
        Sends a push request to the server to log the provided data.

        Args:
            data (Optional[Union[List[str], str]], optional): The data to be logged. Must not be empty or None.
            datax (Optional[Any], optional): Additional data that can be converted to a string and logged. Defaults to None.
            uid (Optional[str], optional): A unique ID for the log entry. Defaults to None.
            embeddings (bool, optional): Whether to generate embeddings for the data. Defaults to True.
            description (Optional[Union[str, List[str]]], optional): A description related to the data. Defaults to None.
            metadata (Optional[Dict[str, Any]], optional): Additional metadata related to the data. Defaults to None.

        Returns:
            dict: The server's response as a JSON object.

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
            "description": description,
            "metadata": metadata,
            "uid": uid,
        }
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def pull(
        self,
        hid: Optional[Union[str, List[str]]] = None,
        uid: Optional[str] = None,
        time: Optional[str] = None,
        date: Optional[str] = None,
        docfile: Optional[str] = "data.oxd",
        where: Optional[Dict[str, Any]] = None,
        where_data: Optional[Dict[str, Any]] = None,
        search_all_filter: bool = False,
        apply_filter: bool = True,
    ) -> dict:
        url = f"{self.base_url}/pull"
        payload = {
            "hid": hid,
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
        hid: Optional[Union[str, List[str]]] = None,
        uid: Optional[str] = None,
        time: Optional[str] = None,
        date: Optional[str] = None,
        where: Optional[Dict[str, Any]] = None,
        where_data: Optional[Dict[str, Any]] = None,
        includes: Optional[List[str]] = None,
        search_all_filter: bool = False,
        apply_filter_last: bool = False,
        where_data_before_vec_search: bool = False,
    ) -> dict:
        url = f"{self.base_url}/search"
        payload = {
            "query": query,
            "topn": topn,
            "by": by,
            "hid": hid,
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
