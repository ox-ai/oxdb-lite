from typing import List, Optional, Dict
from ox_onnx.runtime import OnnxModel
import numpy as np

from oxdb_lite import config



class VectorModel:
    def __init__(self) -> None:
        """
        Initializes the Model class with the default sentence transformer model.
        """
        self.md_name = config.settings.EMBEDDING_MODEL
        self.model = OnnxModel.load(self.md_name)

    def load(self, md_name: str):
        """
        Loads a specific sentence transformer model.

        Args:
            md_name (str): The name of the model to load.
        """
        self.md_name = md_name
        self.model = OnnxModel.load(self.md_name)

    def generate(self, data:list):
        """
        Encodes the input data into embeddings using the loaded model.

        Args:
            data: The data to be encoded, typically a list of strings.

        Returns:
            A list of embeddings corresponding to the input data.
        """
        embeddings = self.model.generate(data)
        return embeddings
    def encode(self, data: str) -> List[int]:
        """
        Tokenize and encode a string into a list of token IDs.

        Args:
            data (str): The string to be tokenized and encoded.

        Returns:
            List[int]: A list of token IDs representing the encoded string.
        """
        return self.model.encode(data)

    def decode(self, encoded_data: List[int]) -> str:
        """
        Decode a list of token IDs back into a string.

        Args:
            encoded_data (List[int]): A list of token IDs to be decoded.

        Returns:
            str: The decoded string.
        """
        return self.model.decode(encoded_data)

    def search(self, query: str,  data: Optional[List[str]] = [],embeds: Optional[List[List[int]]] = [], by: Optional[str] = config.settings.SIM_FORMAT,include : Optional[List[str]]=[]) -> Dict[str, List]:
        """
        Searches for the most similar documents to the query based on the specified similarity metric.

        Args:
            query (str): The query string to search for.
            embeds (list, optional): Precomputed embeddings for the documents. Defaults to an empty list.
            data (list, optional): Raw document data that needs to be encoded. Defaults to an empty list.
            by (Optional[str], optional): The similarity metric to use. Defaults to "dp".
                - "dp" : Dot Product (default)
                - "ed" : Euclidean Distance
                - "cs" : Cosine Similarity
            include (Optional[List[str]],optional): return data format
                - "emdeds" : embeddings of the data


        Returns:
            dict[str, List]: A dictionary containing the indices, similarity scores, document data, and embeddings of the top results.
        """
        # Validate the search method
        if by not in config.settings.SIM_FORMATS:
            raise ValueError(f"Invalid search method '{by}'. Must be one of {config.settings.SIM_FORMATS}.")

        # Generate embeddings for the query
        query_embed = np.array(self.generate([query]))[0]

        # Generate embeddings for the documents if raw data is provided
        if len(data) > 0:
            embeds = np.array(self.generate(data))
        elif len(embeds) > 0:
            embeds = np.array(embeds)
        else:
            return {"idx": [], "sim_score": [], "data": [], "embeds": []}

        # Vectorized similarity calculations
        if by == "dp":
            sim = np.dot(embeds, query_embed.T)
        elif by == "cs":
            sim = np.dot(embeds, query_embed.T) / (np.linalg.norm(embeds, axis=1) * np.linalg.norm(query_embed))
        elif by == "ed":
            sim = np.linalg.norm(embeds - query_embed, axis=1)

        # Get top N indices and their similarity scores
        if by == "ed":
            idx = np.argsort(sim)  # For Euclidean distance, lower distance is more similar
        else:
            idx = np.argsort(sim)[::-1]  # For Dot Product and Cosine Similarity, higher is more similar

        idx = idx.tolist()
        sim_score = sim[idx].tolist()

        # Reorder data and embed based on the sorted indices
        data_sorted = []
        if len(data) > 0:
            data_sorted = [data[i] for i in idx]
        embeds_sorted = []
        if "embeds" in include:
            embeds_sorted = [embeds[i].tolist() for i in idx]

        return {
            "idx": idx,
            "sim_score": sim_score,
            "data": data_sorted,
            "embeds": embeds_sorted
        }

    @staticmethod
    def sim( veca, vecb, sim_format: Optional[str] = config.settings.SIM_FORMAT):
        """
        Calculates the similarity between two vectors based on the specified format.

        Args:
            veca: The first vector.
            vecb: The second vector.
            sim_format (Optional[str], optional): The similarity metric to use. Defaults to "dp".
                - "dp" : Dot Product (default)
                - "ed" : Euclidean Distance
                - "cs" : Cosine Similarity

        Returns:
            The similarity value between the two vectors based on the chosen format.
        """
        if sim_format not in config.settings.SIM_FORMATS:
            raise ValueError(
                f"ox-db: sim_format should be one of {config.settings.SIM_FORMATS}, not {sim_format}"
            )

        veca = np.array(veca)
        vecb = np.array(vecb)

        if sim_format == "dp":
            return np.dot(veca, vecb)
        if sim_format == "ed":
            return np.linalg.norm(veca - vecb)
        elif sim_format == "cs":
            return np.dot(veca, vecb) / (np.linalg.norm(veca) * np.linalg.norm(vecb))