"""
# Oxdld 

disk presisted key-vaue database

"""

import os
from typing import Any, Union
import zipfile

from oxdb_lite.oxdoc_lite.dp import DBIN_METHODS, DBin
from oxdb_lite.oxdoc_lite.db.cache import LRUCache
from oxdb_lite.oxdoc_lite.db.mem import OxdMem
from oxdb_lite.oxdoc_lite.db.freeindex import FreeIndex
from oxdb_lite.oxdoc_lite.utils import doc_validator




class Oxdld:
    def __init__(self, doc: str, data_encoding="oxdbin", cache_capacity=25):
        """
        Initialize instances of the Oxdld class to handle log data storage and retrieval.

        Args:
            doc (str): The name of the oxd document or its path (e.g., "note" or "/home/user/note.oxdld").
            data_encoding (str, optional): The encoding method to use for storing data. Defaults to "oxdbin"
                - data encoding methods [ "oxdbin","json"]
        """
        self.dbin = DBin(method=data_encoding)
        self.doc, self.doc_path = doc_validator(doc, extention=".oxdld")
        os.makedirs(self.doc_path, exist_ok=True)

        self.free_index = FreeIndex()
        self.lrucache = LRUCache(capacity=cache_capacity)
        self._create_data_doc()
        self.index_data = OxdMem(
            self._get_file_path("index"), data_encoding=data_encoding
        )
        self.load_index()
        self.compact()

    def _get_file_path(self, file_name: str) -> str:
        """
        Generate the full file path for a given file name.

        Args:
            file_name (str): The name of the file.

        Returns:
            str: The full file path.
        """
        return os.path.join(self.doc_path, file_name)

    def _create_data_doc(self):
        """
        Create the data document (.oxdldd.bin file) if it does not exist.
        """
        self.data_doc_name = f"{self.doc}.oxdldd.bin"
        data_doc_path = self._get_file_path(self.data_doc_name)
        if not os.path.exists(data_doc_path):
            with open(data_doc_path, "w") as f:
                pass

    def _gen_index_data(self):
        return {
            "config": self.config,
            "free_index": self.free_index.get_dict(),
            "index": self.index,
        }

    def load_index(self) -> tuple[dict, list]:
        """
        Load the index from the index file or build a new one if it does not exist.

        Returns:
            tuple: A tuple containing the index dictionary and the free list.
        """
        self.index = self.index_data.get(
            "index", {}
        )  # Store index as {key: (file_position, document_length)}
        self.free_index.set_dict(
            self.index_data.get("free_index", {})
        )  # List of reusable spaces as (file_position, length)
        self.config = self.index_data.get("config", {"data_encoding": self.dbin.method})

    def save_index(self) -> tuple[dict, list]:
        """
        Save the current index and free list to the index file.

        Returns:
            tuple: A tuple containing the updated index dictionary and free list.
        """
        self.index_data.update(self._gen_index_data())
        self.index_data.flush()

    def __len__(self):
        "len prop of db"

        return len(self.index)

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key=key, value=value)

    def __getitem__(self, key: str) -> Any:
        return self.get(key=key)

    def __delitem__(self, key: str):
        self.delete(key=key)

    def __contains__(self, key):
        if isinstance(key, str):
            return key in self.index

    def keys(self):
        """
        return all the keys in the db
        """
        return list(self.index)

    def commit(self):
        "save the in memory index to file"
        self.save_index()

    def _update_data(self, file, key: str, value: Any):
        """
        Update the data in the document with the given key-value pair.

        Args:
            file (file object): The open file object to write to.
            key (str): The key to be updated or added.
            value (Any): The value associated with the key.
        """
        data = {"": value}
        encoded_data = self.dbin.encode(data)
        encoded_data_len = len(encoded_data)  # Length of the encoded data

        set_status = False
        # Check if the key exists for update
        if key in self.index:
            if value == self.get(key=key):
                return True
            file_position, existing_encoded_data_len = self.index[key]

            if encoded_data_len <= existing_encoded_data_len:
                # If the new document is smaller or equal, overwrite in place
                file.seek(file_position)
                file.write(encoded_data)
                self.index[key] = (file_position, encoded_data_len)
                if encoded_data_len != existing_encoded_data_len:
                    self.free_index.add(
                        file_position + encoded_data_len,
                        existing_encoded_data_len - encoded_data_len,
                    )

                    file.seek(file_position + encoded_data_len)
                    del_data = self.dbin.encode( existing_encoded_data_len - encoded_data_len,ctype="n",method="oxdbin")
                    file.write(del_data)
                set_status = True
            else:
                # If the new document is larger, delete the old entry and append the new one
                self.delete(key)
                file_position = self.free_index.find_space(encoded_data_len)
                if file_position == "EOF":
                    file.seek(0, 2)  # Move to the end of the file
                    file_position = file.tell()  # end of the file position

                file.seek(file_position)
                file.write(encoded_data)
                self.index[key] = (file_position, encoded_data_len)
                set_status = True

        # key not present new data entry
        else:
            # New key, find space in the free list or append
            file_position = self.free_index.find_space(encoded_data_len)
            if file_position == "EOF":
                file.seek(0, 2)  # Move to the end of the file
                file_position = file.tell()  # end of the file position

            file.seek(file_position)
            file.write(encoded_data)
            self.index[key] = (file_position, encoded_data_len)
            set_status = True

        self.lrucache.put(key=key, value=value)

        return set_status

    def set(self, key: str, value: Any) -> bool:
        """
        Set a new key-value pair in the document.

        Args:
            key (str): The key to be added or updated.
            value (Any): The value associated with the key.

        Returns:
            bool: True if the key-value pair was set successfully, False otherwise.
        """
        set_status = False

        with open(self._get_file_path(self.data_doc_name), "r+b") as file:
            set_status = self._update_data(file, key, value)

        self.save_index()
        return set_status

    def add(self, data_dict: dict) -> bool:
        """
        Add multiple key-value pairs to the document.

        Args:
            data_dict (dict): A dictionary of key-value pairs to be added.

        Returns:
            bool: True if the key-value pairs were added successfully, False otherwise.
        """

        set_status = False
        with open(self._get_file_path(self.data_doc_name), "r+b") as file:
            for key, value in data_dict.items():
                set_status = self._update_data(file, key, value)

        self.save_index()
        return set_status

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in the document.

        Args:
            key (str): The key to be checked.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        return key in self.index

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve the value associated with a key in the document.

        Args:
            key (str): The key to look up.

        Returns:
            Any: The value associated with the key, or None if the key does not exist.
        """
        if key not in self.index:
            return None
        if key in self.lrucache:
            return self.lrucache.get(key)
        file_position, document_length = self.index[key]
        with open(self._get_file_path(self.data_doc_name), "rb") as file:
            file.seek(file_position)
            encoded_data = file.read(document_length)  # Read only the data document
            data = self.dbin.decode(encoded_data)
            val = data.get("", default)
            self.lrucache.put(key=key, value=val)
        return val

    def delete(self, key: Union[str, list[str]]) -> bool:
        """
        Delete a key or list of keys from the document.

        Args:
            key (Union[str, list[str]]): The key or list of keys to be deleted.

        Returns:
            bool: True if all specified keys were deleted successfully, False if any key was not found.
        """
        if isinstance(key, str):
            keys_to_delete = [key]
        else:
            keys_to_delete = key

        all_deleted = True
        with open(self._get_file_path(self.data_doc_name), "r+b") as file:
            for k in keys_to_delete:
                if k in self.index:
                    self.lrucache.delete(k)
                    file_position, document_length = self.index[k]
                    self.free_index.add(
                        file_position, document_length
                    )  # Add space to free index
                    file.seek(file_position)
                    del_data = del_data = self.dbin.encode(document_length ,ctype="n",method="oxdbin") 
                    file.write(del_data)
                    del self.index[k]
                else:
                    all_deleted = False

        self.save_index()  # Save updated index and free list
        return all_deleted

    def delete_all(self):
        """
        Delete all keys from the document, remove all associated files,
        and delete the document's folder.
        """
        # Clear the index and free list
        self.index.clear()
        self.free_index.set_dict({})
        self.save_index()

        # Remove the data document file
        data_doc_path = self._get_file_path(self.data_doc_name)
        if os.path.exists(data_doc_path):
            os.remove(data_doc_path)

        # Remove the index file
        index_file_path = self.index_data.doc_path
        if os.path.exists(index_file_path):
            os.remove(index_file_path)

        # Remove the document folder
        if os.path.exists(self.doc_path):
            os.rmdir(self.doc_path)

        return True

    def compact(self):
        """Compact the file to remove all unused spaces."""
        data_dict = {}
        new_index = {}
        new_file_path = self._get_file_path("compact.oxdldd")
        with open(self._get_file_path(self.data_doc_name), "rb") as old_file, open(
            new_file_path, "wb"
        ) as new_file:

            for key, (old_position, length) in self.index.items():
                old_file.seek(old_position)
                encoded_data = old_file.read(length)
                document = self.dbin.decode(encoded_data)
                data_dict[key] = document.get("")
                new_position = new_file.tell()
                new_file.write(encoded_data)
                new_index[key] = (new_position, length)

        # Replace old file with the compacted file
        os.replace(new_file_path, self._get_file_path(self.data_doc_name))
        self.index = new_index
        self.free_index.set_dict({})
        self.save_index()

        return data_dict

    def load_data(self) -> dict:
        """Load all key-value pairs from the data file and return them as a Python dictionary."""
        data = self.compact()
        return data
        # data_dict = {}
        # with open(self._get_file_path(self.data_doc_name), "rb") as file:
        #     while True:
        #         try:
        #             # Read the length of the next data document
        #             length_bytes = file.read(4)
        #             if not length_bytes:
        #                 break  # End of file
        #             length = int.from_bytes(length_bytes, byteorder="little")

        #             # Read the data document based on the length
        #             encoded_data = length_bytes + file.read(length - 4)
        #             document = self.dbin.decode(encoded_data)
        #             data_dict.update(document)
        #         except Exception:
        #             break  # End of file or error in reading, stop the loop
        # return data_dict

    @staticmethod
    def zip(doc, output_path: str = None):
        """
        Compresses the given folder into a ZIP file.

        Args:
            output_path (str) or None : The path to the output ZIP file.
        """
        if output_path != None:
            if not os.path.exists(output_path):
                raise ValueError(f"oxd : given path {output_path} does not exist")
        doc, doc_path = doc_validator(doc, extention=".oxdld")
        folder_path = doc_path
        output_path = (
            os.path.join(output_path, doc + ".oxdld") if output_path else doc_path
        )
        output_path += ".zip"
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Add file to zip, using relative path
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))

        return output_path

    @staticmethod
    def unzip(zip_path: str, output_path: str = None):
        """
        Extracts the given ZIP file to the specified folder.

        Args:
            zip_path (str): The path to the ZIP file to be extracted.
            extract_to (str): The path to the folder where files should be extracted.
        """
        if not os.path.exists(zip_path):
            raise ValueError(f"oxd : given oxd.zip path {zip_path} does not exist")
        if output_path != None:
            if not os.path.exists(output_path):
                raise ValueError(
                    f"oxd : given output path {output_path} does not exist"
                )

        extract_to_path, _ = os.path.splitext(zip_path)
        base_name = os.path.basename(extract_to_path)
        extract_to = (
            os.path.join(output_path, base_name) if output_path else extract_to_path
        )

        with zipfile.ZipFile(zip_path, "r") as zipf:
            zipf.extractall(extract_to)

        return extract_to

    def to_json(self, output_path: str = None):
        """
        Converts a database data to a JSON file.

        Args:
            output_path (str): The path to the output JSON file.
        """
        if output_path != None:
            if not os.path.exists(output_path):
                raise ValueError(f"oxd : given path {output_path} does not exist")
        output_path = (
            os.path.join(output_path, self.doc + ".oxdld.json")
            if output_path
            else os.path.join(".", self.doc + ".oxdld.json")
        )

        data = self.compact()
        with open(output_path, "wb") as json_file:
            json_file.write(self.dbin.encode(data, method="json"))

        return output_path

    def to_db(self, json_path=None):
        """
        Converts JSON file to dictnory or simply add json data to existing database

        Args:
            json_path (str): The path to the JSON file.
        """
        json_path = json_path or f"{self.doc}.oxdld.json"

        if os.path.exists(json_path):
            with open(json_path, "rb") as json_file:
                try:
                    json_data_dict = self.dbin.decode(json_file.read(), method="json")
                    self.add(json_data_dict)
                except Exception as e:
                    raise ValueError(
                        f"Failed to load json file : incompatible data '{json_path}'"
                    ) from e

        else:
            raise ValueError(
                f"Failed to load json file : path is incorrect '{json_path}'"
            )
