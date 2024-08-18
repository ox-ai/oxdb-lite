import json
import os
import socket
import uuid
import hashlib
from typing import List, Union

def gen_uid() -> str:
    """
    Generates a unique ID for a log entry.

    Returns:
        str: The unique ID.
    """
    uid = str(uuid.uuid4())
    return uid


def gen_hid(data):
  """Calculates the SHA-256 hash of the given data.

  Args:
    data: The data to be hashed.

  Returns:
    str: The SHA-256 hash in hexadecimal format.
  """

  if isinstance(data, str):
    encoded_data = data.encode('utf-8')
  else:
    encoded_data = data

  sha256_hash = hashlib.sha256(encoded_data)
  return sha256_hash.hexdigest()


def join_list(lists: List[str], delimiter: str = "||"):
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


def get_immediate_subdirectories(path: str):
    """Returns a list of immediate subdirectories in the given path."""
    doc_list = []
    if  os.path.isdir(os.path.join(path)):
        for doc in os.listdir(path):
            if os.path.isdir(os.path.join(path, doc)) :
                doc_list.append(doc)

    return doc_list


def to_json_string(data):
    """Converts any data type to a JSON string.

    Args:
      data: The data to be converted.

    Returns:
      str: The JSON string representation of the data.
    """
    if isinstance(data,str):
        return data
    try:
        json_string = json.dumps(data)
    except TypeError as e:
        # Handle unsupported data types or errors
        print(f"Error converting data to JSON: {e}")
        json_string = str(data)  # Fallback to string representation
    return json_string


def get_local_ip():
    # Create a socket to find the local IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # This IP address doesn't need to be reachable; it's just used to determine the local IP
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"  # Fallback to localhost if unable to determine IP
    finally:
        s.close()
    
    return local_ip