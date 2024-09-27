import json
from typing import Any, Union, List, Dict

from oxdb_lite.oxdoc.oxdbin import Oxdbin

DBIN_METHODS = [ "json", "oxdbin"]


class DBin:
    def __init__(self, method: str = "oxdbin") -> None:
        """
        Initialize the DBin object with the desired encoding/decoding method.

        Args:
        method (str): The encoding method to use. Must be either oxdbinz 'oxdbin' or 'json'.
                      Defaults to 'oxdbin'.

        Raises:
        ValueError: If the provided method is not valid.
        """
        if method not in DBIN_METHODS:
            raise ValueError(
                f"method = {method} is not valid. It should be one of these: {DBIN_METHODS}"
            )
        self.method: str = method  # Assign the method to the instance attribute

    def encode(
        self, data: Union[Dict[str, Any], List[Any], Any], method: str = None,ctype:str=None
    ) -> bytes:
        """
        Encode the given data using either JSON or encoding.

        Args:
        data (Union[Dict[str, Any], List[Any]]): The data to encode.
        method (str, optional): The encoding method to use. Can be either 'oxdbin' or 'json' .
                                If not provided, the default method of the instance is used.

        Returns:
        bytes: The encoded data in the specified format (oxdbin or or JSON).
        """
        method = method or self.method
        if method == "json":
            en_data = json.dumps(data).encode("utf-8")  # JSON encoding
        elif method == "oxdbin":
            en_data = Oxdbin.encode(data,ctype)
        # else:  # Default is
        #     en_data = bson.encode(data)
        return en_data

    def decode(
        self, data: bytes, method: str = None
    ) -> Union[Dict[str, Any], List[Any], Any]:
        """
        Decode the given encoded data using either JSON,, or byte decoding.

        Args:
            data (bytes): The encoded data to decode.
            method (str, optional): The decoding method to use. Can be either 'oxdbin' or 'json'.
                                    If not provided, the default method of the instance is used.

        Returns:
            Union[Dict[str, Any], List[Any]]: The decoded data as a dictionary, list, or any valid format.

        Raises:
            ValueError: If decoding fails for all provided methods.
        """
        method = method or self.method

        # Try decoding with the specified method first, if provided
        decoding_methods = []
        if method == "json":
            decoding_methods = ["json", "oxdbin"]
        elif method == "oxdbin":
            decoding_methods = ["oxdbin", "json"]
        else:
            decoding_methods = ["oxdbin", "json"]  # Default to first
        

        for decoding_method in decoding_methods:
            try:
                if decoding_method == "json":
                    return json.loads(data.decode("utf-8"))  # JSON decoding
                elif decoding_method == "oxdbin":
                    return Oxdbin.decode(data)  # Custom byte decoding
                # elif decoding_method == ":
                #     return bson.decode(data)  # decoding
            except Exception as e:
                print(
                    f"Decoding with method '{decoding_method}' failed with error: {e} \nusing other methods"
                )
                continue  # Try the next method if decoding fails

        # Raise an error if all methods fail
        raise ValueError(
                    f"Failed to load data: all methods incompatible"
                ) 



