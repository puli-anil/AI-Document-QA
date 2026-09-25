import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class RAGEngine:

    def __init__(self):
        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.index = None
        self.chunks = []

        print("Embedding model loaded.")

    def build_index(self, chunks):

        self.chunks = chunks

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        print("Creating embeddings...")

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True
        )

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.index = faiss.IndexFlatL2(
            embeddings.shape[1]
        )

        self.index.add(embeddings)

        print(
            f"FAISS vectors: {self.index.ntotal}"
        )

    def search(self, question, top_k=5):

        if self.index is None:
            return []

        question_embedding = self.model.encode(
            [question]
        )

        question_embedding = np.asarray(
            question_embedding,
            dtype="float32"
        )

        distances, indices = self.index.search(
            question_embedding,
            top_k
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):

            if index == -1:
                continue

            result = self.chunks[index].copy()

            result["distance"] = float(distance)

            results.append(result)

        return results