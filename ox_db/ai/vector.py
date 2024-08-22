from typing import List, Optional, Dict
from ox_onnx.runtime import OnnxModel
import numpy as np

SIM_FORMAT = ["dp", "ed", "cs"]

class Model:
    def __init__(self) -> None:
        """
        Initializes the Model class with the default sentence transformer model.
        """
        self.md_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.model = OnnxModel(self.md_name).load()

    def load(self, md_name: str):
        """
        Loads a specific sentence transformer model.

        Args:
            md_name (str): The name of the model to load.
        """
        self.md_name = md_name
        self.model = OnnxModel(self.md_name).load()

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

    def search(self, query: str, doc_embed: list = [], doc_data: list = [], by: Optional[str] = "dp") -> Dict[str, List]:
        """
        Searches for the most similar documents to the query based on the specified similarity metric.

        Args:
            query (str): The query string to search for.
            doc_embed (list, optional): Precomputed embeddings for the documents. Defaults to an empty list.
            doc_data (list, optional): Raw document data that needs to be encoded. Defaults to an empty list.
            by (Optional[str], optional): The similarity metric to use. Defaults to "dp".
                - "dp" : Dot Product (default)
                - "ed" : Euclidean Distance
                - "cs" : Cosine Similarity

        Returns:
            Dict [str, List]: A dictionary containing the indices and similarity scores of the top higher to least results.
        """
        query_embed = np.array(self.generate(query))[0]
        if len(doc_data) > 0:
            doc_embed = np.array(self.generate(doc_data))
        elif len(doc_embed) > 0:
            doc_embed = np.array(doc_embed)
        else:
            return {"idx": [], "sim_score": []}

        # Vectorized similarity calculations
        if by == "dp":
            sim = np.dot(doc_embed, query_embed.T)
        elif by == "cs":
            sim = np.dot(doc_embed, query_embed.T) / (np.linalg.norm(doc_embed, axis=1) * np.linalg.norm(query_embed))
        elif by == "ed":
            sim = np.linalg.norm(doc_embed - query_embed, axis=1)

        # Get top N indices and their similarity scores
        if by == "ed":
            idx = np.argsort(sim) # For Euclidean distance, lower distance is similar
        else:
            idx = np.argsort(sim)[::-1]  # For Dot Product and Cosine Similarity, higher is similar

        idx = idx.tolist()
        sim_score = sim[idx].tolist()

        return {"idx": idx, "sim_score": sim_score}

    @staticmethod
    def sim( veca, vecb, sim_format: Optional[str] = "dp"):
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
        if sim_format not in SIM_FORMAT:
            raise ValueError(
                f"ox-db: sim_format should be one of {SIM_FORMAT}, not {sim_format}"
            )

        veca = np.array(veca)
        vecb = np.array(vecb)

        if sim_format == "dp":
            return np.dot(veca, vecb)
        if sim_format == "ed":
            return np.linalg.norm(veca - vecb)
        elif sim_format == "cs":
            return np.dot(veca, vecb) / (np.linalg.norm(veca) * np.linalg.norm(vecb))