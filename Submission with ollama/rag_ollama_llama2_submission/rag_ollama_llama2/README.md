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



====================================================Task 1==================================================================
Run the bat file names as "run_task1_ingestion" in below location :
C:\AI_Project\Submission with ollama\rag_ollama_llama2_submission\rag_ollama_llama2

Defination : It will perform the task 1 of assignment as below :

1. PDF Ingestion & Data Sourcing (20 Marks) 
• PDF Sources: 
Use these PDFs as your data sources for ingestion and embedding in your RAG 
application. They are readily accessible, and provide diverse content for evaluating 
your system's retrieval and conversational abilities -  
a) https://arxiv.org/pdf/1706.03762.pdf 
b) https://arxiv.org/pdf/1810.04805.pdf 
c) https://arxiv.org/pdf/2005.14165.pdf 
d) https://arxiv.org/pdf/1907.11692.pdf 
e) https://arxiv.org/pdf/1910.10683.pdf 
• Data Extraction (10 Marks): 
Implement a pipeline to extract text from each PDF. Consider handling layout, 
tables, or figures if needed, but focus primarily on ensuring that the text is correctly 
segmented for embedding. 
• Preprocessing & Chunking (10 Marks): 
Effective preprocessing of text into meaningful chunks for embedding.

It will:

Activate venv
Run ingest.py
Download PDFs
Extract text
Chunk
Create vector embeddings
Save vector DB into /artifacts

Expected Output Files After Running Task-1

Inside:
rag_ollama_llama2_submission\rag_ollama_llama2\artifacts\

You should see files like:

vectorstore.pkl
chroma.sqlite3
Document chunking artifacts

And inside:

rag_ollama_llama2_submission\rag_ollama_llama2\data\
You should see the 5 PDFs downloaded.


=============================================Task 1 completed ====================================================

=============================================Task 2 Started ======================================================
Run the bat file names as "task2_vector_db" in below location :
C:\AI_Project\Submission with ollama\rag_ollama_llama2_submission\rag_ollama_llama2

Defination : It will perform the task 2 of assignment as below :

2. Vector Database Creation (20 Marks) 
• Requirement: 
Create a vector database to store and retrieve text embeddings from your extracted 
PDF content. 
• Suggested Tools: 
You may use an open-source vector store such as FAISS, or any alternative that 
meets the assignment requirements. 
• Implementation: 
o Process the text from the PDFs into meaningful chunks. (5 Marks) 
o Generate embeddings for these chunks using your chosen model. (5 Marks) 
o Proper setup and configuration for vector DB to store these for efficient 
similarity search. (10 Marks) 

Goal: Build a vector database (FAISS) using embeddings for all text chunks extracted in Task 1.

STEP-BY-STEP EXPLANATION OF TASK 2 :

Step 1 — Virtual environment is activated

Your BAT file activates:
.venv\Scripts\activate
This ensures the correct Python packages & dependencies are used.

Step 2 — Check if sentence-transformers is installed

log shows:
[OK] sentence-transformers already installed.

This is needed because you are using:

sentence-transformers/all-MiniLM-L6-v2
This library generates vector embeddings.

Step 3 — Load chunks.pkl created in Task 1
Task 1 produced:

artifacts/chunks.pkl
This file contains 976 processed text chunks extracted and cleaned from all 5 PDFs.

Task 2 loads this file:
These chunks are the input for your vector database.

Step 4 — Generate embeddings for each chunk

Task 2 prints:
[build_vector_store] Using embedding model: sentence-transformers/all-MiniLM-L6-v2
So for every chunk (976 chunks):

The text is fed to the embedding model
The model converts text → a vector of 384 floating-point numbers
This is how semantic search becomes possible.

Step 5 — Build FAISS index

This is the actual Vector Database step:
[build_vector_store] Building FAISS index...

FAISS is extremely fast for similarity search.
It stores embeddings in an efficient format for:
cosine similarity
top-k search
nearest neighbor retrieval

Step 6 — Save FAISS vector database

Output message:
Saved FAISS index to artifacts/faiss_index
Inside this folder you now have:
faiss_index/index.faiss – binary file storing all embeddings
faiss_index/index.pkl – metadata mapping embeddings → text chunks

This is our complete vector database.

=======================================Task 2 completed ===========================================================
WHAT DOES THIS ENABLE NOW?

After Task 2 completes:

We can perform semantic search

Example:
"What is self-attention?"
The system will retrieve the correct PDF paragraphs based on meaning, not keywords.

======================================Task 3 Started ===============================================================
Run the bat file names as "task3_model_integration" in below location :
C:\AI_Project\Submission with ollama\rag_ollama_llama2_submission\rag_ollama_llama2

Defination : It will perform the task 3 of assignment as below :

3. Open Source Language Model Integration (20 Marks) 
• Model Requirement: 
Integrate an open-source language model from Hugging Face or Ollama to generate 
responses based on retrieved context. 
• Usage: 
o The model should be used to generate answers by combining retrieved text 
chunks with the user’s query. 
o Ensure that your model and embedding generator are compatible.

Goal : Task 3 integrates the Language Model (Ollama LLaMA2) with your Vector DB so your chatbot can answer questions using PDF-retrieved knowledge + conversation memory.

Step-by-Step Explanation of Task 3 :

Step 1 — Ensure the Language Model (Ollama) Is Running
The batch file checks if Ollama server is active:

http://localhost:11434/api/tags

If it replies successfully → ✔ Ollama is running.
If not → ❌ You would see an error.
Why?
Your RAG chatbot must query LLaMA 2 via Ollama to generate answers.

Step 2 — Load the Vector Database (FAISS) Built in Task 2

Task 3 loads:
artifacts/faiss_index
artifacts/chunks.pkl

This gives the system:
✔ All chunked PDF text
✔ Embeddings
✔ Ability to find relevant passages using similarity search.

Step 3 — Combine Vector DB with the LLM
This is the core of a Retrieval-Augmented Generation (RAG) system.
When you ask:

My name is Ashish, remember this.
What is self-attention?

The RAG pipeline does:
1. Retrieve contextual chunks from DB
FAISS finds the most relevant text from the PDFs.

2. Add conversation memory (last 4 turns)
Your chatbot tracks the last 4 messages:
✔ Your message
✔ Bot response
✔ Next user message
✔ Next bot response

So the bot knows:
Your name = Ashish
Self-attention context from PDFs
Your follow-up question

3. Send the combined prompt to LLaMA 2 via Ollama
The prompt includes:
✔ Retrieved PDF context
✔ Conversation memory
✔ Current question

Step 4 — Generate the Final Answer

The LLaMA 2 model produces:
A correct technical response
Plus it remembers your name
And maintains conversation flow

You may ask below questions to verify :
My name is Ashish. Remember this.
What is self-attention in transformers?
What is my name?

=============================================Task 3 completed =======================================================
=============================================Task 4 and 5 started ========================================================

Run the bat file names as "task4_memory_test" {For task 4 only} / "task4_memory_and_eval" {For task 4 and 5} in below location :
C:\AI_Project\Submission with ollama\rag_ollama_llama2_submission\rag_ollama_llama2
Created the memory_test.py : This does NOT change the chatbot's behaviour. It simply imports the
existing RAGBot and runs a small scripted conversation to show that
the bot remembers information across turns.

Defination : It will perform the task 4  and task 5 of assignment  as below :

4. Conversational Bot with Memory (10 Marks) 
• Conversational Memory: 
The bot should maintain context over the last 4 conversation turns. This means it 
should “remember” the past interactions and use them to inform its responses. 
• Implementation Hints: 
o Use techniques such as conversation state management or prompt 
concatenation. 
o Ensure the memory is updated and only the last 4 interactions are 
considered.

Goal  Task 4 : bot should remember the last 4 conversation turns and use them to answer the next question.
Goal Task 5 : It tests  how well  RAG system performs using a formal evaluation framework like RAGAS.

Task 4 requires only:

✅ A small script that:

Loads the existing RAG bot

Runs three fixed test messages

Ensures the bot remembers the name

Saves the output as screenshots (optional) or text

Closes

❗ NOT modifying any main bot code.

This preserves everything we already built.

Once you click the bat file it will automatically ask 3 questions to bot and with the help of that we could showcase our Task 4 objectives.

Task 5 requires only :

Loads the same RAG pipeline (same personality + same FAISS index + same Ollama llama2).

Reads 10 questions from questions.json.

For each question:

Sends the question to the bot (RAGBot).

Gets:

answer
source_documents (chunks retrieved from PDFs)

Stores these into a list of records.

Builds a HuggingFace Dataset from those 10 records.

Runs ragas.evaluate with metrics:

answer_relevancy

faithfulness

context_precision

context_recall

Saves results in:

artifacts/eval_results.json


=====================================================Task 4 and 5 completed ================================================================
======================================================Task 6 started =======================================================================
Run the bat file names as "task6_report"  in below location :
C:\AI_Project\Submission with ollama\rag_ollama_llama2_submission\rag_ollama_llama2

Defination : It will perform the task 6 as below :

6. Final Report (10 Marks) 
• Format: 
Submit a final report as a PDF document. 
• Contents: 
The report should include: 
o Overview: An introduction to your approach and system architecture. 
o Technical Implementation: Details on how you extracted data, generated 
embeddings, set up your vector database, integrated the language model, 
and implemented conversational memory. 
o Evaluation: A detailed description of the 10 test questions and the evaluation 
framework (including any metrics, scoring methods, or qualitative 
assessments used). 
o Results & Discussion: Analysis of the performance of your RAG application, 
challenges faced, and potential improvements. 
o Conclusion: A summary of your findings and overall performance.

Goal : Task 6 takes all outputs from Tasks 1–5 and automatically converts them into a clean, professional report.pdf for submission.

Task 6 requires only :

Step 1 — Activate Virtual Environment
Step 2 — Check for reportlab

reportlab is the Python library used to generate PDF files.

If missing → it installs it automatically.

Step 3 — Load evaluation results

It reads:
artifacts/eval_results.json

This file was created in Task 5, and contains:

scores
question & answer pairs
extracted contexts

======================================================Task 6 completed =======================================================================

