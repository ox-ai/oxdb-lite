


import struct
from typing import Any


class Oxdbin:
    def __init__(self) -> None:
        pass

    def encode(data: Any,ctype:str=None,) -> bytes:
        """
        Convert any type of data (string, list, dict, etc.) to bytes.

        Args:
            data (Any): The data to convert to bytes.

        Returns:
            bytes: The data serialized as bytes.
        """
        if ctype in ["n","delb","delbyte"]:
            totbytelen = data
            datalen= totbytelen-5
            deldata = b'\x00'*datalen
            return b"n" + datalen.to_bytes(4, "big") + deldata
        if isinstance(data, str):
            # Encode strings with a 's' prefix and UTF-8 encoding
            return b"s" + len(data).to_bytes(4, "big") + data.encode("utf-8")

        elif isinstance(data, int):
            # Encode integers with an 'i' prefix
            return b"i" + data.to_bytes(8, "big", signed=True)

        elif isinstance(data, float):
            # Encode floats with an 'f' prefix
            return b"f" + Oxdbin.float_to_bytes(data)

        elif isinstance(data, list):
            # Encode lists with an 'l' prefix and serialize each element recursively
            byte_list = b"".join([Oxdbin.encode(d) for d in data])
            return b"l" + len(data).to_bytes(4, "big") + byte_list

        elif isinstance(data, tuple):
            # Encode tuples with a 't' prefix and serialize each element recursively
            byte_tuple = b"".join([Oxdbin.encode(d) for d in data])
            return b"t" + len(data).to_bytes(4, "big") + byte_tuple

        elif isinstance(data, dict):
            # Encode dictionaries with a 'd' prefix, key-value pairs serialized recursively
            byte_datas = b"".join(
                [Oxdbin.encode(key) + Oxdbin.encode(value) for key, value in data.items()]
            )
            return b"d" + len(data).to_bytes(4, "big") + byte_datas

        else:
            raise ValueError(f"Unsupported data type: {type(data)}")


    def decode(data_bytes: bytes, data_type:str=None,length:int=None, pos: int = 0, posless: bool = True) -> Any:
        """
        Convert bytes back to the original data type (string, list, dict, etc.).

        Args:
            data_bytes (bytes): The bytes to convert back to the original data.
            pos Optional(int,optional): The current position in the stream.

        Returns:
            Any: The original data structure.
            tuple: (decoded_data, new_position)
        """

        data_type =data_type or  chr(data_bytes[pos])
        bdsize_len = 5 if not length else 0

        if data_type == "n":
            if not length:
                length = int.from_bytes(data_bytes[pos + 1 : pos + 5], "big")
            #value = int.from_bytes(data_bytes[pos + 5 : pos + 5 + length],"big")
            value = 0
            if posless:
                return value
            return value, pos + 5 + length

        elif data_type == "s":
            if not length:
                length = int.from_bytes(data_bytes[pos + 1 : pos + 5], "big")
            value = data_bytes[pos + bdsize_len : pos + bdsize_len + length].decode("utf-8")
            if posless:
                return value
            return value, pos + bdsize_len + length

        elif data_type == "i":
            value = int.from_bytes(data_bytes[pos + 1 : pos + 9], "big", signed=True)
            if posless:
                return value
            return value, pos + 9

        elif data_type == "f":
            value = Oxdbin.bytes_to_float(data_bytes[pos + 1 : pos + 9])
            if posless:
                return value
            return value, pos + 9

        elif data_type == "l":
            if not length:
                length = int.from_bytes(data_bytes[pos + 1 : pos + 5], "big")
            datas = []
            new_pos = pos + bdsize_len
            for _ in range(length):
                data, new_pos = Oxdbin.decode(data_bytes, pos=new_pos, posless=False)
                datas.append(data)
            if posless:
                return datas
            return datas, new_pos

        elif data_type == "t":
            if not length:
                length = int.from_bytes(data_bytes[pos + 1 : pos + 5], "big")
            datas = []
            new_pos = pos + bdsize_len
            for _ in range(length):
                data, new_pos = Oxdbin.decode(data_bytes, pos=new_pos, posless=False)
                datas.append(data)
            if posless:
                return tuple(datas)
            return tuple(datas), new_pos

        elif data_type == "d":
            if not length:
                length = int.from_bytes(data_bytes[pos + 1 : pos + 5], "big")
            datas = {}
            new_pos = pos + bdsize_len
            for _ in range(length):
                key, new_pos = Oxdbin.decode(data_bytes, pos=new_pos, posless=False)
                value, new_pos = Oxdbin.decode(data_bytes, pos= new_pos, posless=False)
                datas[key] = value
            if posless:
                return datas
            return datas, new_pos

        else:
            raise ValueError(f"Unsupported data type prefix: {data_type}")


    def decode_all(data_bytes:bytes):
        data = []
        data_bytes_len = len(data_bytes)
        pos = 0
        while pos<data_bytes_len :
            datai,pos = Oxdbin.decode(data_bytes,pos=pos,posless=False)
            data.append(datai)

        return data


    def bdsize_len(btype) -> Any:
        """
        Convert bytes back to the original data type (string, list, dict, etc.).

        Args:
            data_bytes (bytes): The bytes to convert back to the original data.
            pos Optional(int,optional): The current position in the stream.

        Returns:
            Any: The original data structure.
            tuple: (decoded_data, new_position)
        """

        if btype in ["n","s","l","t","d"]:
            return 4
        elif btype in ["i","f"]:
            return 8

        else:
            raise ValueError(f"Unsupported data type prefix: {btype}")
        
    def decode_bdlen(bdsize,btype):
        if btype in ["n","s","l","t","d"]:
            return int.from_bytes(bdsize[0 : 4], "big")
        elif btype in ["i","f"]:
            return 8




    def float_to_bytes(f: float) -> bytes:
        return struct.pack(">d", f)  # '>d' is for big-endian double precision floats


    def bytes_to_float(b: bytes) -> float:
        return struct.unpack(">d", b)[0]  # '>d' unpacks the 8-byte float
