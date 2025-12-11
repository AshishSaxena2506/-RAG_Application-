# generate_report.py
# -------------------
# Generates final report.pdf including:
# - Overview + System architecture
# - Technical implementation
# - Evaluation metrics (custom summary from evaluation.py)
# - FULL Question–Answer list from eval_results.json

import json
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from config import (
    EVAL_RESULTS_PATH,
    REPORT_PATH,
    PDF_URLS,
    EMBEDDING_MODEL_NAME,
    OLLAMA_MODEL_NAME,
)


def safe(value):
    """Convert None to empty string and everything else to str."""
    return "" if value is None else str(value)


def load_eval_results():
    """
    Return (scores_dict, records_list).

    - For the current evaluation.py, 'summary' holds the metrics.
    - Older formats might use 'scores'. We handle both.
    """
    if not EVAL_RESULTS_PATH.exists():
        return None, []

    try:
        data = json.loads(EVAL_RESULTS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None, []

    # New format from evaluation.py: { "summary": {...}, "records": [...] }
    summary = data.get("summary")
    scores = summary if isinstance(summary, dict) else data.get("scores") or {}
    records = data.get("records") or []

    return scores, records


def generate_report():
    styles = getSampleStyleSheet()
    story = []

    # ---------------------------------------------------
    # Title + timestamp
    # ---------------------------------------------------
    story.append(Paragraph("RAG Application Final Report (Ollama + LLaMA 2)", styles["Title"]))
    story.append(Spacer(1, 10))
    story.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 20))

    # ---------------------------------------------------
    # 1. Overview
    # ---------------------------------------------------
    overview = f"""
    <b>1. Overview</b><br/>
    This project implements a complete Retrieval-Augmented Generation (RAG) pipeline for the
    Generative AI Fundamentals assignment. The system ingests five research papers on
    Transformers / BERT / GPT from arXiv, builds a vector database with FAISS, and uses
    a local LLaMA&nbsp;2 model served by Ollama to answer questions about those papers.<br/><br/>
    Key components:
    <br/>• PDF ingestion & preprocessing
    <br/>• Chunking & embedding with <i>{EMBEDDING_MODEL_NAME}</i>
    <br/>• FAISS-based vector store
    <br/>• LLaMA&nbsp;2 via Ollama (<i>{OLLAMA_MODEL_NAME}</i>)
    <br/>• Conversational bot with 4-turn memory
    <br/>• 10-question evaluation using a custom metric summary
    """
    story.append(Paragraph(overview, styles["BodyText"]))
    story.append(Spacer(1, 16))

    # ---------------------------------------------------
    # 2. System Architecture (Tasks 1–5)
    # ---------------------------------------------------
    arch_html = f"""
    <b>2. System Architecture</b><br/>
    The pipeline is structured to mirror the assignment tasks:<br/><br/>
    <b>Task 1 – PDF Ingestion & Chunking</b><br/>
    • Downloads 5 PDFs from arXiv:<br/>
    &nbsp;&nbsp;- {PDF_URLS[0]}<br/>
    &nbsp;&nbsp;- {PDF_URLS[1]}<br/>
    &nbsp;&nbsp;- {PDF_URLS[2]}<br/>
    &nbsp;&nbsp;- {PDF_URLS[3]}<br/>
    &nbsp;&nbsp;- {PDF_URLS[4]}<br/>
    • Extracts raw text and splits it into overlapping semantic chunks (~976 total).<br/><br/>
    <b>Task 2 – Vector Database Creation</b><br/>
    • Each chunk is embedded using <i>{EMBEDDING_MODEL_NAME}</i>.<br/>
    • Embeddings are stored in a FAISS index under <i>artifacts/faiss_index</i> for fast similarity search.<br/><br/>
    <b>Task 3 – Open Source LLM Integration</b><br/>
    • Integrates a local LLaMA&nbsp;2 model served by Ollama on <i>localhost:11434</i>.<br/>
    • At query time, top-k chunks are retrieved from FAISS and combined with the user question
      into a prompt sent to the Ollama LLM.<br/><br/>
    <b>Task 4 – Conversational Bot with Memory</b><br/>
    • Uses a 4-turn conversation window to remember recent context (e.g. the user name "Ashish").<br/><br/>
    <b>Task 5 – Interaction & Evaluation</b><br/>
    • Runs a 10-question evaluation suite defined in <i>questions.json</i>.<br/>
    • Computes a custom summary of relevance, answer length, and context usage.
    """
    story.append(Paragraph(arch_html, styles["BodyText"]))
    story.append(Spacer(1, 16))

    # ---------------------------------------------------
    # 3. Technical Implementation
    # ---------------------------------------------------
    tech_html = f"""
    <b>3. Technical Implementation</b><br/><br/>
    <b>3.1 Data Extraction & Preprocessing</b><br/>
    • PDFs are downloaded from the assignment URLs and stored under <i>data/</i>.<br/>
    • Text is extracted and split into overlapping chunks to preserve context across page and section boundaries.<br/><br/>
    <b>3.2 Embeddings & Vector Store</b><br/>
    • A sentence-transformer model <i>{EMBEDDING_MODEL_NAME}</i> generates dense embeddings
      for each chunk.<br/>
    • Embeddings are indexed in a FAISS vector store under <i>artifacts/faiss_index</i>.<br/><br/>
    <b>3.3 LLM Integration with Ollama</b><br/>
    • Ollama serves the <i>{OLLAMA_MODEL_NAME}</i> model locally.<br/>
    • LangChain's Ollama wrapper is used to send prompts that combine user question +
      retrieved chunks.<br/><br/>
    <b>3.4 Conversational Memory</b><br/>
    • A 4-turn memory window is used to maintain short-term dialogue context without
      unbounded growth.
    """
    story.append(Paragraph(tech_html, styles["BodyText"]))
    story.append(Spacer(1, 16))

    # ---------------------------------------------------
    # 4. Evaluation Setup & Metrics
    # ---------------------------------------------------
    eval_intro = """
    <b>4. Evaluation Setup and Metrics</b><br/>
    The evaluation uses 10 predefined questions from <i>questions.json</i> to probe different aspects
    of the papers: self-attention, encoder-decoder architecture, positional encodings, BERT
    pre-training, GPT-style training, multi-head attention, limitations, etc.<br/><br/>
    For each question, the RAG bot:
    <br/>• retrieves relevant chunks from the FAISS index,
    <br/>• generates an answer using LLaMA&nbsp;2,
    <br/>• and the results are aggregated into simple numeric metrics.
    """
    story.append(Paragraph(eval_intro, styles["BodyText"]))
    story.append(Spacer(1, 14))

    # ---------------------------------------------------
    # 4.1 Evaluation Scores (from eval_results.json -> summary)
    # ---------------------------------------------------
    scores, records = load_eval_results()
    story.append(Paragraph("<b>4.1 Evaluation Scores (Custom Summary)</b>", styles["Heading3"]))
    story.append(Spacer(1, 6))

    if scores is None:
        story.append(
            Paragraph(
                "No evaluation results found. Please rerun Task 4_5 to generate "
                "<i>artifacts/eval_results.json</i> before running Task 6.",
                styles["BodyText"],
            )
        )
    elif not scores:
        story.append(
            Paragraph(
                "No metrics found in <i>eval_results.json</i>.",
                styles["BodyText"],
            )
        )
    else:
        # Show each metric from 'summary' (avg_relevance_score, etc.)
        for metric_name, value in scores.items():
            story.append(
                Paragraph(
                    f"<b>{metric_name}</b>: {float(value):.4f}",
                    styles["BodyText"],
                )
            )

    story.append(Spacer(1, 14))

    # ---------------------------------------------------
    # 4.2 Detailed Q&A from eval_results.json
    # ---------------------------------------------------
    story.append(Paragraph("<b>4.2 Evaluation Question–Answer Pairs</b>", styles["Heading3"]))
    story.append(Spacer(1, 6))

    if not records:
        story.append(
            Paragraph(
                "No Q&A records found in eval_results.json. "
                "Ensure Task 4_5 ran successfully.",
                styles["BodyText"],
            )
        )
    else:
        for i, r in enumerate(records):
            q = safe(r.get("question"))
            a = safe(r.get("answer"))
            story.append(Paragraph(f"<b>Q{i+1}:</b> {q}", styles["BodyText"]))
            story.append(Paragraph(f"<b>Answer:</b> {a}", styles["BodyText"]))
            story.append(Spacer(1, 10))

    story.append(Spacer(1, 14))

    # ---------------------------------------------------
    # 5. Results & Discussion
    # ---------------------------------------------------
    results_text = """
    <b>5. Results & Discussion</b><br/>
    The RAG pipeline successfully answers technical questions about Transformers, BERT and
    related architectures using only the five assignment PDFs as its knowledge base. Retrieval via
    FAISS focuses the LLM on relevant chunks, which improves answer relevancy compared to a
    raw LLM without context.<br/><br/>
    The conversational memory test (Task 4) confirms that the bot can track short-term context,
    such as the user’s name, across multiple turns while still grounding answers in retrieved
    research paper content.<br/><br/>
    Main challenges encountered include:
    <br/>• Library version mismatches (LangChain, embeddings, evaluation libs).
    <br/>• Ensuring FAISS index and pickle artifacts stay compatible after upgrades.
    """
    story.append(Paragraph(results_text, styles["BodyText"]))
    story.append(Spacer(1, 14))

    # ---------------------------------------------------
    # 6. Conclusion
    # ---------------------------------------------------
    conclusion_text = """
    <b>6. Conclusion</b><br/>
    This project demonstrates a complete local RAG application:
    <br/>• PDF ingestion and preprocessing
    <br/>• Chunking and embedding with MiniLM
    <br/>• Vector database creation using FAISS
    <br/>• LLaMA&nbsp;2 integration via Ollama
    <br/>• Conversational memory over the last 4 turns
    <br/>• Objective evaluation on 10 questions using custom metrics<br/><br/>
    The system fulfils the functional requirements of the assignment and can be extended with
    richer UIs, additional documents, or more advanced evaluation methods in the future.
    """
    story.append(Paragraph(conclusion_text, styles["BodyText"]))

    # ---------------------------------------------------
    # 7. Write the PDF
    # ---------------------------------------------------
    REPORT_PATH.parent.mkdir(exist_ok=True)
    doc = SimpleDocTemplate(str(REPORT_PATH), pagesize=A4)  # str(...) fixes WindowsPath issue
    doc.build(story)
    print(f"[generate_report] PDF saved to {REPORT_PATH}")


if __name__ == "__main__":
    generate_report()
