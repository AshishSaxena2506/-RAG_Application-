"""
ingest.py
----------
1. Downloads the 5 assignment PDFs if not already present.
2. Extracts text using LangChain's PyPDFLoader.
3. Splits into semantic chunks.
4. Saves chunks and embedding model config to disk.
"""

import requests
import pickle

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import PDF_URLS, PDF_FILES, DATA_DIR, CHUNKS_PATH, EMBEDDING_MODEL_NAME


def download_pdfs() -> None:
    DATA_DIR.mkdir(exist_ok=True, parents=True)
    for url, path in zip(PDF_URLS, PDF_FILES):
        if path.exists():
            print(f"[download_pdfs] Already present: {path.name}")
            continue
        print(f"[download_pdfs] Downloading {url} -> {path}")
        resp = requests.get(url)
        resp.raise_for_status()
        path.write_bytes(resp.content)
    print("[download_pdfs] All PDFs ready.")


def load_and_chunk() -> None:
    """
    Loads the 5 PDFs, turns them into LangChain Documents, and chunks them.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    docs = []
    for path in PDF_FILES:
        print(f"[load_and_chunk] Loading {path.name}")
        loader = PyPDFLoader(str(path))
        pages = loader.load()
        chunks = splitter.split_documents(pages)
        print(f"  -> {len(chunks)} chunks")
        docs.extend(chunks)

    print(f"[load_and_chunk] Total chunks: {len(docs)}")

    payload = {
        "docs": docs,
        "embedding_model_name": EMBEDDING_MODEL_NAME,
    }
    CHUNKS_PATH.parent.mkdir(exist_ok=True, parents=True)
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(payload, f)

    print(f"[load_and_chunk] Saved chunks to {CHUNKS_PATH}")


def preview_chunks(n: int = 3) -> None:
    """
    Utility to print a quick preview of a few chunks.
    """
    import textwrap

    with open(CHUNKS_PATH, "rb") as f:
        payload = pickle.load(f)

    docs = payload["docs"]
    for i, d in enumerate(docs[:n]):
        print("=" * 80)
        print(f"Chunk {i}")
        print(textwrap.shorten(d.page_content.replace("\n", " "), width=400))


if __name__ == "__main__":
    download_pdfs()
    load_and_chunk()
    preview_chunks(3)
