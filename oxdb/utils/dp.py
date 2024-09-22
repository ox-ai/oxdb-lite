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



def delete_folder_and_contents(folder_path: str):
    """
    Delete all files and subfolders inside the specified folder, and then delete the folder itself.

    Args:
        folder_path (str): The path to the folder to be deleted.
    """
    if os.path.exists(folder_path):
        # Remove all contents inside the folder
        for root, dirs, files in os.walk(folder_path, topdown=False):
            # Remove files
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)

            # Remove subdirectories
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                os.rmdir(dir_path)

        # Finally, remove the folder itself
        os.rmdir(folder_path)

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

def intorstrorlist_to_liststr(arg: Union[str, List[str]]) -> List[List[str]]:
    """
    Converts input arguments to lists if they are strings else list or None

    Args:
        args (Union[str, List[str]]): The input arguments.

    Returns:
        List[List[str]]: The converted arguments. or None
    """
    return [int(arg)] if isinstance(arg, int) or isinstance(arg, str)  else arg or []

intorstrorlist_to_liststr


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


class UIDX:

    def __init__(self, uidxs):
        # Normalize all items in uidxs to integers, but store original types
        self.uidxs = set(self._to_int(uidx) for uidx in uidxs)
        self.dellist = []
        self.max_uidx = max(self.uidxs) if self.uidxs else 0
        self.original_is_str = all(isinstance(uidx, str) for uidx in uidxs)

    def _to_int(self, uidx):
        # Convert uidx to an integer for comparison
        return int(uidx) if isinstance(uidx, str) else uidx

    def _to_original_type(self, uidx):
        # Convert uidx back to its original type if needed
        return str(uidx) if self.original_is_str else uidx

    def gen(self):
        # Return the last uidxber from dellist if available
        if self.dellist:
            return self._to_original_type(self.dellist.pop())
        else:
            # Increment the max uidxber and return it
            self.max_uidx += 1
            self.uidxs.add(self.max_uidx)
            return self._to_original_type(self.max_uidx)

    def delete(self, uidx):
        # Handle single str, int or list of them
        if isinstance(uidx, list):
            # Convert list of uidx to integers and delete each
            for n in uidx:
                self._delete_single(n)
        else:
            # Handle single uidxber
            self._delete_single(uidx)

    def _delete_single(self, uidx):
        """Internal method to delete a single uidxber."""
        uidx = self._to_int(uidx)  # Ensure it's treated as an integer
        if uidx in self.uidxs:
            self.uidxs.remove(uidx)
            self.dellist.append(uidx)

    def __len__(self):
        # Return the count of available uidx (excluding dellist)
        return len(self.uidxs)

