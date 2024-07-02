from datetime import datetime
from typing import List, Optional, Union


def search_uid(
    doc_index: dict,
    key: Optional[str] = None,
    time: Optional[str] = None,
    date: Optional[str] = None,
    where: Optional[dict] = None,
) -> List[str]:
    """
    Searches for UIDs based on key, time, or date.

    Args:
        key (Optional[str], optional): The key to search. Defaults to None.
        time (Optional[str], optional): The time to search. Defaults to None.
        date (Optional[str], optional): The date to search. Defaults to None.
        where={"metadata_key": "value"}.
    Returns:
        List[str]: The matching UIDs.
    """

    content = doc_index
    uids = []

    time_parts = _parse_time(time) if time else None
    date_parts = _parse_date(date) if date else None

    for uid, data in content.items():
        log_it = (
            (key == data["key"] if key else True)
            and (_metadata_filter(where, data["metadata"]) if where else True)
            and (_match_time(time_parts, data["time"]) if time_parts else True)
            and (_match_date(date_parts, data["date"]) if date_parts else True)
        )

        if log_it:
            uids.append(uid)

    return uids


def _metadata_filter(query_dict: dict, data_dict: dict):
    """
    Checks if atlest one key-value pair from the query_dict is present in the data_dict

    Args:
        query_dictd dict :  key-value
        data_dict dict :  key-value

    Returns:
        True if atlest one key-value pair or query_dict present in data_dict
    """
    if data_dict is None:
        return False
    for key in query_dict.keys():
        if query_dict[key] == data_dict.get(key):
            return True
    return False


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


def _parse_date(date: str) -> List[Optional[str]]:
    """
    Parses a date string into components.

    Args:
        date (str): The date string.

    Returns:
        List[Optional[str]]: The date components.
    """
    return date.split("_")


def _match_time(query_time: List[Optional[str]], log_time: str) -> bool:
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


def _match_date(query_date: List[Optional[str]], log_date: str) -> bool:
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
