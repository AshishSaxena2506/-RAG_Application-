"""
Configuration constants for the RAG assignment project using Ollama + LLaMA 2.
"""

from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
REPORT_DIR = BASE_DIR / "report"

# Make sure key folders exist (safe, idempotent)
for p in (DATA_DIR, ARTIFACTS_DIR, REPORT_DIR):
    p.mkdir(exist_ok=True)

# PDF sources from the assignment
PDF_URLS = [
    "https://arxiv.org/pdf/1706.03762.pdf",
    "https://arxiv.org/pdf/1810.04805.pdf",
    "https://arxiv.org/pdf/2005.14165.pdf",
    "https://arxiv.org/pdf/1907.11692.pdf",
    "https://arxiv.org/pdf/1910.10683.pdf",
]

# Local filenames (same order as URLs)
PDF_FILES = [
    DATA_DIR / "1706.03762.pdf",
    DATA_DIR / "1810.04805.pdf",
    DATA_DIR / "2005.14165.pdf",
    DATA_DIR / "1907.11692.pdf",
    DATA_DIR / "1910.10683.pdf",
]

# Embedding model (lightweight, widely used)
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Ollama model name (must be pulled with `ollama pull`)
OLLAMA_MODEL_NAME = "llama2"

# Artifacts
CHUNKS_PATH = ARTIFACTS_DIR / "chunks.pkl"
FAISS_INDEX_PATH = ARTIFACTS_DIR / "faiss_index"
EVAL_RESULTS_PATH = ARTIFACTS_DIR / "eval_results.json"

# Final PDF report path
REPORT_PATH = REPORT_DIR / "report.pdf"
