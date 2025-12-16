import os
from rag.embeddings import EmbeddingModel
from rag.vector_store import FaissStore
from rag.retrieval_chunking import chunk_for_retrieval


def index_document(
    document_id: str,
    text: str,
    filename: str
):
    chunks = chunk_for_retrieval(text)

    embeddings = EmbeddingModel.embed_texts(chunks)

    store = (
        FaissStore.load()
        if exists_faiss()
        else FaissStore(dim=len(embeddings[0]))
    )

    metadatas = [
        {
            "document_id": document_id,
            "filename": filename,
            "chunk": chunk
        }
        for chunk in chunks
    ]

    store.add(embeddings, metadatas)
    store.save()
    print(f"Indexed {len(chunks)} chunks for document {document_id}")

def exists_faiss():
    return (
        os.path.exists("faiss/index.faiss")
        and os.path.exists("faiss/meta.pkl")
    )
