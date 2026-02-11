# 🤖 AI-Powered Research Paper Assistant

A cutting-edge tool that helps users intelligently **search**, **summarize**, and **interact** with academic research papers using **LLMs**, **semantic search**, **Arxiv integration**, and a clean **Streamlit UI**.

---

## 🚀 Overview

The **Research Paper Assistant** makes academic exploration easier by combining advanced Natural Language Processing (NLP) techniques with an intuitive interface. It supports:

* 🔍 Natural language paper lookup via Arxiv
* 🧠 Summarization, direct question answering, and metric extraction using LLaMA-3 from Groq
* ⚡ Semantic search using FAISS and sentence embeddings
* 📁 Metadata management for precise source tracking
* 🌐 A Streamlit web app for seamless user interaction

---

## 🧠 Why This Project Stands Out

👌 **Real-Time Semantic Search**: Uses FAISS and Sentence Transformers for fast, accurate retrieval of relevant content from papers.

🕊 **High-Performance LLM (Groq + LLaMA-3)**: Ultra-fast responses with contextual understanding for summarization and Q\&A.

🔍 **Arxiv Search API**: Allows keyword-based or descriptive paper search directly from the app.

🗁 **Metadata Management**: Links every result with its source (chunk, position), ensuring transparency and explainability.

📅 **Modular Architecture**: Clean separation between UI, retrieval logic, LLM agent, and Arxiv integration.

📊 **Extendable**: Future integration with PDF upload, citation extraction, or image caption analysis (BLIP) is possible.

---

## 🛠️ Features

| Feature              | Description                                                             |
| -------------------- | ----------------------------------------------------------------------- |
| 🔍 Arxiv Search      | Find papers using natural language queries like "transformer-based OCR" |
| 🧬 Vector Retrieval  | Retrieve context using FAISS + BAAI sentence embeddings                 |
| 📝 Summarization     | Get concise and clear summaries using LLM                               |
| ❓ Q\&A               | Ask questions and get context-aware answers                             |
| 📊 Metric Extraction | Extract numbers, statistics, or performance metrics from text           |
| 🧠 LLM-Powered       | Groq-hosted LLaMA-3 70B for speed and quality                           |
| 💡 Streamlit UI      | Easy-to-use and responsive frontend                                     |

---

## 📁 Project Structure

```
research-paper-assistant/
├── streamlit_ui/
│   └── ui.py                  # Streamlit frontend logic
├── vector_store/
│   ├── faiss_store.index      # FAISS index file for embeddings
│   └── metadata.json          # Metadata for each text chunk
├── app/
│   ├── ingestion.py           # Handles vector-based retrieval
│   └── llm_agent.py           # Prompt building and LLM invocation via Groq
│   └── arxiv_search.py        # Arxiv search integration                   
├── Streamlit_ui/
│   ├──Ui.py                   #Streamlit userinterface
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/research-paper-assistant.git
cd research-paper-assistant
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

Make sure you delete the faiss_idex , metadata.js and report.pdfs before running the server

### 3. Set API Key (Groq)

In `llm_agent.py`, replace your Groq API key:

```python
ChatGroq(groq_api_key="your_groq_api_key", ...)
```

You can also add it in an `.env` file and use `python-dotenv` to load it securely.

### 4. Run the App

```bash
streamlit run streamlit_ui/ui.py
```

---

## 🧺 Example Prompts

* “Summarize the methodology of this paper.”
* “What are the main findings from the latest transformer OCR research?”
* “Extract all numerical results from this document.”
* “Find a paper about multi-modal diffusion in vision-language models.”

---

## 🔌 Arxiv Integration Example

Search a paper using:

> "Find a paper on transformer-based OCR systems"

The app will:

1. Query Arxiv API.
2. Return top result: title, authors, abstract.
3. Provide PDF and paper links.

---

## 📂 Technologies Used

* **Groq LLaMA-3 70B** – lightning-fast LLM inference
* **FAISS** – similarity search across paper chunks
* **Sentence Transformers (BAAI/bge-small-en-v1.5)** – embedding text
* **Arxiv API** – academic paper search
* **Streamlit** – frontend UI
* **Python** – core backend and logic

---

## 📌 Why We Use Metadata?

Metadata stores the source chunk for every embedding, so when a vector is retrieved from FAISS, we can trace it back to the original content and paper. This improves:

* ✅ **Explainability** of answers
* ✅ **Traceability** of source text
* ✅ **Modular chunk-based search**

## 👍 Contributing

Contributions are welcome! Please open issues for bugs or submit a PR for improvements.

---

## 📬 Contact

**Author**: Arnav Singh
Email: toshu129@gail.com
GitHub:https://github.com/toshu134

---

## 🌟 If You Like This Project...

Give it a ⭐ on GitHub and share it with friends in research or academia!
