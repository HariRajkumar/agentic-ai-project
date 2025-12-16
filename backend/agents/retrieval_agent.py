from rag.retrieval import retrieve_similar_chunks

def retrieve_context(question: str, top_k: int = 5):
    results = retrieve_similar_chunks(question, top_k=top_k)
    return [item["chunk"] for item in results]