import faiss
import os
import pickle
import numpy as np

FAISS_INDEX_PATH = "faiss/index.faiss"
FAISS_META_PATH = "faiss/meta.pkl"


class FaissStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, vectors, metadatas):
        vectors = np.array(vectors).astype("float32")
        self.index.add(vectors)
        self.metadata.extend(metadatas)

    def save(self):
        os.makedirs("faiss", exist_ok=True)
        faiss.write_index(self.index, FAISS_INDEX_PATH)
        with open(FAISS_META_PATH, "wb") as f:
            pickle.dump(self.metadata, f)

    @classmethod
    def load(cls):
        index = faiss.read_index(FAISS_INDEX_PATH)
        with open(FAISS_META_PATH, "rb") as f:
            metadata = pickle.load(f)

        store = cls(index.d)
        store.index = index
        store.metadata = metadata
        return store
