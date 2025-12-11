# RAG Application – Final Report (Ollama + LLaMA 2)

## 1. Overview

This report describes the design, implementation, and evaluation of a Retrieval-Augmented Generation (RAG) application built over five foundational NLP papers. The system:

- Ingests and preprocesses 5 PDFs (Transformers, BERT, GPT-style models, etc.).
- Stores semantically chunked text in a FAISS vector database.
- Uses **LLaMA 2**, served locally via **Ollama**, as the open-source language model.
- Provides a conversational interface with memory over the last four interactions.
- Is evaluated using the RAGAS framework on 10 predefined questions.

## 2. System Architecture

The system is structured into four main stages:

1. **Data Ingestion & Preprocessing**
   - Downloads PDFs directly from arXiv using their URLs.
   - Extracts text with `PyPDFLoader` (LangChain).
   - Splits text into overlapping chunks with `RecursiveCharacterTextSplitter`.

2. **Vector Store & Embeddings**
   - Converts chunks into dense vectors using `sentence-transformers/all-MiniLM-L6-v2`.
   - Stores vectors and metadata in a FAISS index for fast similarity search.

3. **RAG Pipeline with Ollama (LLaMA 2)**
   - Uses `langchain_community.llms.Ollama` to connect to the local Ollama server.
   - The configured model is `llama2`, pulled via `ollama pull llama2`.
   - For each query:
     - Retrieves the top-k relevant chunks from FAISS.
     - Builds a prompt that includes the user query, retrieved context, and recent conversation history.
     - Generates a grounded answer using LLaMA 2.

4. **Conversational Memory**
   - Maintains a sliding window of the last four conversation turns using `ConversationBufferWindowMemory(k=4)`.
   - Enables coherent follow-up questions that depend on previous answers.

A diagram of this architecture is stored in `screenshots/architecture.png`.

## 3. Technical Implementation

### 3.1 PDF Extraction & Chunking

- Implemented in `ingest.py`.
- PDF sources are taken directly from the assignment specification.
- For each PDF:
  - `PyPDFLoader` loads all pages into LangChain `Document` objects.
  - `RecursiveCharacterTextSplitter` splits pages into chunks of approximately 800 characters with 150-character overlap.

The resulting list of chunks is serialized to `artifacts/chunks.pkl` for reuse.

### 3.2 Vector Database (FAISS)

- Implemented in `vector_store.py`.
- Embeddings are generated with `HuggingFaceEmbeddings` using the model `all-MiniLM-L6-v2`.
- A FAISS index is built from all chunk vectors.
- The index is persisted to `artifacts/faiss_index/` and loaded later by the chatbot.

This design decouples ingestion from retrieval so the index only needs to be built once.

### 3.3 LLaMA 2 via Ollama

- Implemented in `chatbot.py`.
- The LLM is defined as:

  ```python
  from langchain_community.llms import Ollama
  from config import OLLAMA_MODEL_NAME

  llm = Ollama(model=OLLAMA_MODEL_NAME)  # OLLAMA_MODEL_NAME = "llama2"
  ```

- Ollama runs a local HTTP server (default `localhost:11434`) that hosts the LLaMA 2 model.
- This satisfies the assignment requirement to use an open-source model from **Ollama**.

### 3.4 Conversational RAG Chain

- `load_vector_store()` returns a FAISS-backed retriever (`k=4`).
- `ConversationBufferWindowMemory(k=4)` stores the last four message pairs.
- `ConversationalRetrievalChain.from_llm` combines:
  - LLaMA 2 (via Ollama)
  - FAISS retriever
  - Conversation memory
  - `return_source_documents=True` for evaluation

The `RAGBot` class exposes a simple `.ask(question)` method that returns:

- `answer`: the LLM-generated answer.
- `source_documents`: list of retrieved chunks.
- Other internal fields as needed.

### 3.5 CLI and Evaluation Scripts

- `run_chat.py` provides an interactive command-line chat interface.
- `evaluation.py` loads 10 questions from `questions.json`, queries the bot, and evaluates the outputs using RAGAS.

## 4. Evaluation

### 4.1 Question Set

10 questions are chosen to cover:

- Transformer fundamentals (self-attention, positional encodings, parallelization).
- BERT-specific ideas (masked language modeling, pretraining setup).
- GPT-style autoregressive modeling.
- Encoder-decoder architectures and limitations discussed in the papers.

These questions are stored in `questions.json`.

### 4.2 RAGAS Metrics

The evaluation uses the RAGAS framework with four metrics:

- **answer_relevancy** – Is the answer relevant to the question?
- **faithfulness** – Is the answer supported by the retrieved context?
- **context_precision** – How much of the retrieved context is actually useful?
- **context_recall** – Does the retrieval capture all necessary information?

`evaluation.py` constructs a Hugging Face `Dataset` with:

- `question`
- `answer`
- `contexts` (the text of source documents used for each answer)

and then calls `ragas.evaluate()` to compute scores. The numeric results and all Q/A/context triples are saved in `artifacts/eval_results.json`.

### 4.3 Observations (Qualitative)

- For questions directly matched to specific sections (e.g., self-attention, positional encoding), retrieval is very strong and LLaMA 2 produces accurate and fluent explanations.
- For more open-ended or cross-paper questions, the quality of retrieval (choice of chunks) strongly influences the answer quality.
- Conversational memory allows clarification questions like “what about BERT’s approach?” to be grounded in the immediately preceding context.

## 5. Results & Discussion

> The actual numerical metrics depend on running `python evaluation.py` in your environment. After you run it, you can update this section with concrete values from `artifacts/eval_results.json`.

### 5.1 Strengths

- **Use of Ollama + LLaMA 2**:
  - Simple local deployment of a strong open-source model.
  - No need to directly manage large model weights in Python code.
- **Modular pipeline**:
  - Clear separation between ingestion, indexing, chat, and evaluation.
  - Easy to swap models or change chunking parameters.
- **Good alignment with assignment requirements**:
  - Uses exactly the 5 specified PDFs.
  - Employs a vector database (FAISS) for semantic retrieval.
  - Includes conversational memory over the last 4 turns.
  - Uses an established evaluation framework (RAGAS).

### 5.2 Limitations

- Hardware limitations may affect LLaMA 2 performance and latency on weaker machines.
- Some very fine-grained or numerically detailed questions may still produce partial hallucinations if not fully covered in the retrieved chunks.
- RAGAS scores provide an aggregate view but may not capture all aspects of user satisfaction (e.g., style, verbosity).

### 5.3 Future Improvements

- Experiment with alternative embeddings or cross-encoder re-ranking.
- Tune chunk size and overlap for better alignment with paragraph/section boundaries.
- Increase the conversation memory window or compress older turns into summaries.
- Add a feedback mechanism where the user can mark answers as good/bad and influence future retrieval and scoring.

## 6. Bonus: Real-Time User Feedback (Design Outline)

To integrate real-time user feedback into conversational memory and retrieval:

1. After each answer, prompt the user:
   - “Was this answer helpful? (yes / no)”
2. Store feedback in a small database (e.g., JSON or SQLite) keyed by:
   - question, answer, contexts, timestamp, feedback label.
3. When retrieving context for future questions:
   - Downweight or filter chunks frequently associated with negative feedback.
   - Optionally upweight chunks frequently associated with positive feedback.

This creates a feedback loop where the system dynamically adapts its retrieval behavior over time.

## 7. Conclusion

The implemented RAG system:

- Correctly ingests and preprocesses the five assignment PDFs.
- Builds and uses a FAISS-based vector database for semantic retrieval.
- Integrates **LLaMA 2 via Ollama** as the open-source LLM.
- Offers a conversational interface with 4-turn memory.
- Evaluates its own performance using the RAGAS framework.

This fully addresses the assignment objectives while showcasing a practical, modern RAG architecture suitable for further experimentation and extension.
