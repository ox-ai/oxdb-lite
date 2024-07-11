from typing import Any, Dict, List, Optional, TypeAlias, Union
from pydantic import BaseModel

# Type Alias for key, uid, or date queries
embd: TypeAlias = Union[str, List[Any], bool, None]
uids: TypeAlias = Union[str, List[str], None]


class PushModel(BaseModel):
    data: Any
    embeddings: embd = True
    description: Optional[Any] = None
    metadata: Optional[Dict[str, Any]] = None
    key: Optional[str] = None
   


class PullModel(BaseModel):
    uid: uids = None
    key: Optional[str] = "key"
    time: Optional[str] = None
    date: Optional[str] = None
    docfile: Optional[str] = "data.oxd"
    where: Optional[dict] = None
    where_data: Optional[dict] = None


class SearchModel(BaseModel):
    query: str
    topn: int = 10
    log_entries: Optional[List[dict]] = None
    uid: uids = None
    by: Optional[str] = "dp"
    key: Optional[str] = None
    time: Optional[str] = None
    date: Optional[str] = None
    where: Optional[dict] = None
    where_data: Optional[dict] = None
