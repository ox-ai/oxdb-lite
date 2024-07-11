from typing import List, Union
import uuid


def gen_uid() -> str:
    """
    Generates a unique ID for a log entry.

    Returns:
        str: The unique ID.
    """
    uid = str(uuid.uuid4())
    return uid

def join_list(lists:List[str],delimiter:str="||"):
    listoutput = [delimiter.join(lists)]

    return listoutput



def strorlist_to_list(arg: Union[str, List[str]]) -> List[List[str]]:
    """
    Converts input arguments to lists if they are strings else list or None

    Args:
        args (Union[str, List[str]]): The input arguments.

    Returns:
        List[List[str]]: The converted arguments. or None
    """
    return [arg] if isinstance(arg, str) else arg or [] 
