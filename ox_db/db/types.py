from typing import Any, Dict, List, Optional, TypeAlias, Union
from pydantic import BaseModel

# Type Alias for uid, hid, or date queries
embd: TypeAlias = Optional[Union[str, List[Any], bool, None]]
hids: TypeAlias = Optional[Union[str, List[str], None]]


from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

DOCFILE_LIST = ["data.oxd", "vec.oxd", ".index"]

class PushModel(BaseModel):
    data: Any = Field(
        ..., description="The data to be logged. Must not be empty or None."
    )
    embeddings: embd = Field(
        True, description="Indicates whether to generate embeddings for the data."
    )
    description: Optional[Any] = Field(
        None, description="A description related to the data."
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Additional metadata related to the data."
    )
    uid: Optional[str] = Field(None, description="A uid for the log entry.")


class PushResponseModel(BaseModel):
    hid: str = Field(..., description="The unique ID of the log entry.")


class PullModel(BaseModel):
    hid: hids = Field(None, description="The unique ID(s) of the log entry.")
    uid: Optional[str] = Field(None, description="The uid of the log entry.")
    time: Optional[str] = Field(None, description="The time of the log entry.")
    date: Optional[str] = Field(None, description="The date of the log entry.")
    docfile: Optional[str] = Field(
        "data.oxd", description=f"The docfile within the doc to search {DOCFILE_LIST}."
    )
    where: Optional[Dict[str, Any]] = Field(
        None, description="Additional metadata filter criteria."
    )
    where_data: Optional[Dict[str, Any]] = Field(
        None, description="Data filter criteria for the log entry."
    )
    search_all_filter: Optional[bool] = Field(
        False, description="Whether to search all entries regardless of filters."
    )
    apply_filter: Optional[bool] = Field(
        True, description="Whether to apply filtering criteria."
    )


class PullResponseModel(BaseModel):
    entries: List[Dict[str, Any]] = Field(
        ..., description="A list of dictionaries representing the log entries."
    )


class PullHIDModel(BaseModel):
    hids: List[str] = Field(
        ...,
        description="A list of unique IDs representing the log entries to retrieve.",
    )
    docfile: str = Field(
        ..., description=f"The docfile within the doc to search {DOCFILE_LIST}."
    )
    where_data: Optional[Dict[str, Any]] = Field(
        None, description="Data filter criteria for the log entry."
    )


class PullHIDResponseModel(BaseModel):
    log_entries: Dict[str, Any] = Field(
        ...,
        description="A dictionary containing the log entries that match the given `hids`.",
    )


class SearchModel(BaseModel):
    query: str = Field(..., description="The search query string.")
    topn: int = Field(10, description="Number of top results to return.")
    log_entries: Optional[Dict[str, Dict[str, Any]]] = Field(
        None, description="Pre-fetched log entries to search within."
    )
    by: Optional[str] = Field(
        "dp", description="The search method. Must be one of ['dp', 'ed', 'cs']."
    )
    hid: Optional[Union[str, List[str]]] = Field(
        None, description="The unique ID(s) of the log entry."
    )
    uid: Optional[str] = Field(None, description="The uid of the log entry.")
    time: Optional[str] = Field(None, description="The time of the log entry.")
    date: Optional[str] = Field(None, description="The date of the log entry.")
    where: Optional[Dict[str, Any]] = Field(
        None, description="Additional metadata filter criteria."
    )
    where_data: Optional[Dict[str, Any]] = Field(
        None, description="Data filter criteria for the log entry."
    )
    includes: Optional[List[str]] = Field(
        None, description="Fields to include in the search results."
    )
    search_all_filter: Optional[bool] = Field(
        False, description="Whether to apply all filters across all entries."
    )
    apply_filter_last: Optional[bool] = Field(
        False, description="Whether to apply filters after vector search."
    )
    where_data_before_vec_search: Optional[bool] = Field(
        False,
        description="Whether to apply `where_data` filter before performing vector search.",
    )


class SearchResponseModel(BaseModel):
    entries: int = Field(..., description="Number of entries found.")
    hid: List[str] = Field(..., description="List of hids for the matched entries.")
    data: List[Any] = Field(..., description="List of data for the matched entries.")
    description: List[Any] = Field(
        ..., description="List of descriptions for the matched entries."
    )
    sim_score: List[float] = Field(
        ..., description="List of similarity scores for the matched entries."
    )
    index: List[Optional[Dict[str, Any]]] = Field(
        ..., description="List of index metadata for the matched entries."
    )
    embeddings: Optional[List[Any]] = Field(
        None, description="List of embeddings for the matched entries (if included)."
    )
