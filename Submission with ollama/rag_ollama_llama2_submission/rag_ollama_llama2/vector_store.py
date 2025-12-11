"""
vector_store.py
----------------
Builds and loads a FAISS vector store from the preprocessed chunks.
"""

import pickle

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import CHUNKS_PATH, FAISS_INDEX_PATH, EMBEDDING_MODEL_NAME


def build_vector_store() -> None:
    with open(CHUNKS_PATH, "rb") as f:
        payload = pickle.load(f)

    docs = payload["docs"]
    model_name = payload.get("embedding_model_name", EMBEDDING_MODEL_NAME)

    print(f"[build_vector_store] Using embedding model: {model_name}")
    embeddings = HuggingFaceEmbeddings(model_name=model_name)

    print("[build_vector_store] Building FAISS index...")
    vectordb = FAISS.from_documents(docs, embeddings)
    FAISS_INDEX_PATH.mkdir(exist_ok=True, parents=True)
    vectordb.save_local(str(FAISS_INDEX_PATH))

    print(f"[build_vector_store] Saved FAISS index to {FAISS_INDEX_PATH}")


def load_vector_store() -> FAISS:
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    vectordb = FAISS.load_local(
        str(FAISS_INDEX_PATH),
        embeddings,
        allow_dangerous_deserialization=True,
    )
    return vectordb


if __name__ == "__main__":
    build_vector_store()
