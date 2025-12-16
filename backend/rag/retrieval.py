import numpy as np
from rag.vector_store import FaissStore
from rag.embeddings import EmbeddingModel


def retrieve_similar_chunks(query: str, top_k: int = 5):
    # Load FAISS store
    store = FaissStore.load()

    # Embed query
    query_vector = EmbeddingModel.embed_texts([query])
    query_vector = np.array(query_vector).astype("float32")

    # Search FAISS
    distances, indices = store.index.search(query_vector, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(store.metadata):
            results.append(store.metadata[idx])

    return results
