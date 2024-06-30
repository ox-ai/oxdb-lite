from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np


class Model:
    def __init__(self) -> None:
        self.md_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.model = SentenceTransformer(self.md_name)

    def load(self, md_name:str):
        self.md_name = md_name
        self.model = SentenceTransformer(self.md_name)

    def encode(self, data):
        embeddings = self.model.encode(data,normalize_embeddings=True, convert_to_numpy=True).tolist()
        return embeddings
    

    def search(self,query:str,doc_embed:list=[],doc_data:list=[],topn=5,by:str="dp")->List[int]:
        
        query_embed = np.array(self.encode(query))
        if len(doc_data)>0 :
            doc_embed = self.encode(doc_data)
        elif len(doc_embed)>0:
            doc_embed = np.array(doc_embed)
        else:
            return []

        # need to implement all 3 sim metrics
        # Dot Product (default)
        sim = np.dot(doc_embed, query_embed.T)
        topn_idx = np.argsort(sim, axis=0)[-topn:][::-1].tolist()


        return topn_idx



    @classmethod
    def sim(cls, veca, vecb, sim_format=1):
        """
        Calculates similarity between two vectors based on the specified format.

        Args:
            veca: First vector.
            vecb: Second vector.
            sim_format: Integer specifying the similarity metric.
                1: Euclidean Distance
                2: Cosine Similarity
                3: Dot Product (default)

        Returns:
            The similarity value based on the chosen format.
        """
     
        veca = np.array(veca).flatten()
        vecb = np.array(vecb).flatten()

        if sim_format == 1:
            # Euclidean Distance
            euclidean_distance = np.linalg.norm(veca - vecb)
            return euclidean_distance
        elif sim_format == 2:
            # Cosine Similarity
            cosine_similarity = np.dot(veca, vecb) / (
                np.linalg.norm(veca) * np.linalg.norm(vecb)
            )
            return cosine_similarity
        else:
            # Dot Product (default)
            dot_product = np.dot(veca, vecb)
            return dot_product
