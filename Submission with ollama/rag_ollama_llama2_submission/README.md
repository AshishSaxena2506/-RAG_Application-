# Generative AI Fundamentals – RAG Assignment (Ollama + LLaMA 2)

This repository contains a complete implementation of the RAG (Retrieval-Augmented Generation) application as described in the assignment, using **Ollama** with the **LLaMA 2** model as the open-source language model.

Features:

- PDF ingestion from 5 research papers (as specified in the assignment)
- Text preprocessing and chunking
- Vector database with FAISS
- Open-source LLM integration via **Ollama (llama2)**
- Conversational bot with memory (last 4 turns)
- Automatic evaluation with RAGAS on 10 questions

## 1. Project Structure

```text
rag_ollama_llama2/
├── data/                # Downloaded PDFs (populated by ingest.py)
├── artifacts/           # Chunks, FAISS index, evaluation JSON
├── report/              # Final report (PDF/Markdown)
├── screenshots/         # Architecture & console screenshots
├── config.py            # Paths, model names, PDF URLs
├── ingest.py            # PDF download + extraction + chunking
├── vector_store.py      # FAISS index build + load helpers
├── chatbot.py           # RAG bot with conversational memory (Ollama + LLaMA 2)
├── run_chat.py          # CLI entrypoint for chatting with the bot
├── evaluation.py        # 10-question evaluation with RAGAS
├── questions.json       # Predefined evaluation questions
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## 2. Setup

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

> Note: `sentence-transformers`, `transformers`, and `torch` are used for embeddings and evaluation; the LLM itself is served by Ollama.

## 3. Install and Configure Ollama (with LLaMA 2)

1. Download and install Ollama from: https://ollama.com

2. Pull the **llama2** model:

```bash
ollama pull llama2
```

3. (Optional) Test that Ollama works:

```bash
ollama run llama2
```

4. The model name is configured in `config.py`:

```python
OLLAMA_MODEL_NAME = "llama2"
```

You can change it to another model available in Ollama (e.g., `"llama2:7b"`, `"llama2:13b"`) if your hardware supports it.

## 4. Steps to Run the Project

### 4.1 Ingest PDFs & Chunk Text

```bash
python ingest.py
```

This will:

- Download the 5 assignment PDFs into `data/`
- Extract text with `PyPDFLoader`
- Chunk the text using `RecursiveCharacterTextSplitter`
- Persist chunks and embedding configuration into `artifacts/chunks.pkl`

### 4.2 Build FAISS Vector Store

```bash
python vector_store.py
```

This will:

- Load chunks from `artifacts/chunks.pkl`
- Build a FAISS index using `all-MiniLM-L6-v2` embeddings
- Save the index in `artifacts/faiss_index/`

### 4.3 Run the Conversational Bot (Ollama + LLaMA 2)

Make sure Ollama is installed and the `llama2` model has been pulled.

```bash
python run_chat.py
```

- Uses an Ollama-backed `llama2` model as the LLM.
- Performs retrieval from FAISS.
- Maintains conversational memory over the **last 4 turns**.

### 4.4 Run RAGAS Evaluation (10 Questions)

```bash
python evaluation.py
```

This will:

- Load the bot and ask all 10 questions from `questions.json`
- Collect answers and retrieved contexts
- Compute RAGAS metrics:
  - `answer_relevancy`
  - `faithfulness`
  - `context_precision`
  - `context_recall`
- Save everything into `artifacts/eval_results.json`
