"""
OxdMem is a in memory cashe database presisted with flush
inheritance of the dict to implement additional features
"""

import os
from typing import Any
from oxdb_lite.oxdoc_lite.dp import DBIN_METHODS, DBin
from oxdb_lite.oxdoc_lite.utils import doc_validator


class OxdMem(dict):
    def __init__(self, doc: str, data_encoding="oxdbin"):
        """
        Initialize instances of the Oxdld class to handle log data storage and retrieval.

        Args:
            doc (str): The name of the oxd document or its path (e.g., "note" or "/home/user/note.oxdmem.bin").
            data_encoding (str, optional): The encoding method to use for storing data. Defaults to .
                - data encoding methods ["oxdbin", "json", "oxdbin"]
        """
        self.doc, self.doc_path = doc_validator(doc, extention=".oxdmem.bin")
        self.dbin = DBin(method=data_encoding)
        self.load()

    def load(self) -> None:
        """Load the data from the oxdmem data file or build a new one if it does not exist."""
        if os.path.exists(self.doc_path):
            try:
                with open(self.doc_path, "rb") as docfile:
                    self.update(self.dbin.decode(docfile.read()))
            except Exception as e:
                print(
                    f"Decoding with method '{self.dbin.method}' failed with error: {e} \n\nUse correct method from: {DBIN_METHODS}"
                )
                raise ValueError(
                    f"Failed to load data: incompatible encoding method '{self.dbin.method}' \n\nUse correct methods: '{DBIN_METHODS}'"
                ) from e

    def flush(self) -> None:
        """Persist the current oxdmem data to the file."""
        with open(self.doc_path, "wb") as docfile:
            docfile.write(self.dbin.encode(dict(self)))

    def __setitem__(self, key: str, value: Any) -> None:
        """Override set item to persist changes."""
        super().__setitem__(key, value)

    def __delitem__(self, key: str) -> None:
        """Override delete item to persist changes."""
        super().__delitem__(key)

    def set(self, key: str, value: Any) -> None:
        """Override set item to persist changes."""
        super().__setitem__(key, value)

    def delete(self, key):
        """Delete a key-value pair and persist the change."""
        super().__delitem__(key)

    def clear(self) -> None:
        """Clear the data and persist the empty data to the file."""
        super().clear()

    def display(self):
        """Display the current state of the in-memory data."""
        print("Current data:", dict(self))
        return dict(self)
