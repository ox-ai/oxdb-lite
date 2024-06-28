import json
import bson
import os
import zipfile


class OxDoc:
    def __init__(self, doc):
        """
        Initialize instances of the OxDoc class to handle log data storage and retrieval.

        Args:
            db (str): The name of the oxd doc or its path eg : (note) (/home/user/note.oxd)

        """
        self.doc, self.doc_path = self._doc_validator(doc)
        if not os.path.exists(self.doc_path):
            os.makedirs(self.doc_path)
        self.index = {}  # Store index as {key: (file_position, document_length)}
        self.free_list = []  # List of reusable spaces as (file_position, length)
        self.index_name = f"{self.doc}.index.oxdi"
        self.free_list_name = f"{self.doc}.free_list.oxdfl"
        self.data_doc_name = f"{self.doc}.doc.oxdd"
        self.load_index()
        self.set("oxd-init", f"{self.doc}")

    def _get_file_path(self, file_name):
        return os.path.join(self.doc_path, file_name)

    def load_index(self):
        # Load index from file or build if not exists
        index_file_path = self._get_file_path(self.index_name)
        free_list_file_path = self._get_file_path(self.free_list_name)

        if os.path.exists(index_file_path):
            with open(index_file_path, "rb") as index_file:
                self.index = bson.decode(index_file.read())
        else:
            self.index = {}
        # Load free list from file or build if not exists
        if os.path.exists(free_list_file_path):
            with open(free_list_file_path, "rb") as free_list_file:
                free_list_dict = bson.decode(free_list_file.read())
                self.free_list = [
                    (entry["position"], entry["length"])
                    for entry in free_list_dict.values()
                ]
        else:
            self.free_list = []

    def save_index(self):
        # Save the index to a file
        index_file_path = self._get_file_path(self.index_name)
        free_list_file_path = self._get_file_path(self.free_list_name)

        with open(index_file_path, "wb") as index_file:
            index_file.write(bson.encode(self.index))

        # Convert the free list to a dictionary for BSON encoding
        free_list_dict = {
            str(i): {"position": position, "length": length}
            for i, (position, length) in enumerate(self.free_list)
        }

        # Save the free list to a file
        with open(free_list_file_path, "wb") as free_list_file:
            free_list_file.write(bson.encode(free_list_dict))

    def set(self, key: str, value):
        """set new key-value pair in the doc"""
        data = {key: value}
        bson_data = bson.encode(data)
        bson_data_len = len(bson_data)  # Length of the BSON valuee
        set_status = False
        # Check if key exists for update
        if key in self.index:
            file_position, existing_bson_data_len = self.index[key]

            if bson_data_len <= existing_bson_data_len:
                # If the new document is smaller or equal, overwrite in place
                with open(self._get_file_path(self.data_doc_name), "r+b") as file:
                    file.seek(file_position)
                    file.write(bson_data)
                    self.index[key] = (file_position, bson_data_len)
                    set_status = True
            else:
                # If the new document is larger, delete the old entry and append the new one
                self.delete(key)
                file_position = self._find_space_or_append(bson_data_len)
                with open(self._get_file_path(self.data_doc_name), "r+b") as file:
                    file.seek(file_position)
                    file.write(bson_data)
                    self.index[key] = (file_position, bson_data_len)
                    set_status = True
        else:
            # New key, find space in the free list or append
            file_position = self._find_space_or_append(bson_data_len)
            with open(self._get_file_path(self.data_doc_name), "r+b") as file:
                file.seek(file_position)
                file.write(bson_data)
                self.index[key] = (file_position, bson_data_len)
                set_status = True

        self.save_index()
        return set_status

    def add(self, data_dict: dict):
        for key, value in data_dict.items():
            self.set(key, value)

    def get(self, key: str):
        """the the value in the doc by using key"""
        if key not in self.index:
            return None
        file_position, document_length = self.index[key]
        with open(self._get_file_path(self.data_doc_name), "rb") as file:
            file.seek(file_position)
            bson_data = file.read(document_length)  # Read only the BSON document
            data = bson.decode(bson_data)
            val = data.get(key)
            print(f"ox-db : {val}")
            return val

    def delete(self, key):
        if key not in self.index:
            return False
        file_position, document_length = self.index[key]
        self.free_list.append(
            (file_position, document_length)
        )  # Add space to free list
        del self.index[key]
        self.save_index()  # Save updated index and free list
        return True

    def compact(self):
        """Optional: Compact the file to remove all unused spaces."""
        data_dict = {}
        new_file_path = self._get_file_path("compact.oxdd")
        with open(self._get_file_path(self.data_doc_name), "rb") as old_file, open(
            new_file_path, "wb"
        ) as new_file:
            new_index = {}
            for key, (old_position, length) in self.index.items():
                old_file.seek(old_position)
                bson_data = old_file.read(length)
                document = bson.decode(bson_data)
                data_dict.update(document)
                new_position = new_file.tell()
                new_file.write(bson_data)
                new_index[key] = (new_position, length)

        # Replace old file with the compacted file
        os.replace(new_file_path, self._get_file_path(self.data_doc_name))
        self.index = new_index
        self.free_list = []
        self.save_index()

        return data_dict

    def load_data(self):
        """Load all key-value pairs from the BSON file and return them as a Python dictionary."""
        data = self.compact()
        del data["oxd-init"]
        return data
        data_dict = {}
        with open(self._get_file_path(self.data_doc_name), "rb") as file:
            while True:
                try:
                    # Read the length of the next BSON document
                    length_bytes = file.read(4)
                    if not length_bytes:
                        break  # End of file
                    length = int.from_bytes(length_bytes, byteorder="little")

                    # Read the BSON document based on the length
                    bson_data = length_bytes + file.read(length - 4)
                    document = bson.decode(bson_data)
                    data_dict.update(document)
                except Exception:
                    break  # End of file or error in reading, stop the loop
        return data_dict

    def zip(self, output_path: str = None):
        """
        Compresses the given folder into a ZIP file.

        Parameters:
        output_path (str) or None : The path to the output ZIP file.
        """
        if output_path != None:
            if not os.path.exists(output_path):
                raise ValueError(f"oxd : given path {output_path} does not exist")
        folder_path = self.doc_path
        output_path = (
            os.path.join(output_path, self.doc + ".oxd")
            if output_path
            else self.doc_path
        )
        output_path += ".zip"
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Add file to zip, using relative path
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))

        return output_path

    @classmethod
    def unzip(cls, zip_path: str, output_path: str = None):
        """
        Extracts the given ZIP file to the specified folder.

        Parameters:
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
        Converts a dictionary to a JSON file.

        Parameters:
        output_path (str): The path to the output JSON file.
        """
        if output_path != None:
            if not os.path.exists(output_path):
                raise ValueError(f"oxd : given path {output_path} does not exist")
        output_path = (
            os.path.join(output_path, self.doc + ".json")
            if output_path
            else os.path.join(".", self.doc + ".json")
        )

        data = self.compact()
        with open(output_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

    def _find_space_or_append(self, size):
        """Find a suitable space from the free list or append to the end of the file."""
        for i, (position, length) in enumerate(self.free_list):
            if length >= size:
                # Use this free space and adjust the free list entry
                self.free_list.pop(i)
                if length > size:
                    # Add the remaining space back to the free list
                    self.free_list.append((position + size, length - size))
                return position
        # If no suitable space is found, append to the end of the file
        with open(self._get_file_path(self.data_doc_name), "ab") as file:
            return file.tell()

    def _doc_validator(self, doc: str):
        if not isinstance(doc, str):
            raise ValueError("oxd : The doc must be a string.")
        doc_path = doc

        path_to_doc, doc_name_full = os.path.split(doc)
        if path_to_doc == "":
            path_to_doc = "."
        elif not os.path.exists(path_to_doc):
            raise ValueError(f"oxd : given path {path_to_doc} does not exist")

        doc_name, ext = os.path.splitext(doc_name_full)

        if ext not in ["", ".oxd"]:
            raise ValueError("oxd : Invalid file extension. Only '.oxd' is allowed.")

        # Determine doc and doc_path based on the input
        if ext == ".oxd":
            doc_path = doc
        else:
            doc_path = doc + ".oxd"

        return doc_name, doc_path
