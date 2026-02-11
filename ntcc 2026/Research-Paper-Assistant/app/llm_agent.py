import os
import faiss
import json
import numpy as np
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from sentence_transformers import SentenceTransformer

# File paths
VECTOR_STORE_DIR = "./vector_store"
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "faiss_store.index")
METADATA_PATH = os.path.join(VECTOR_STORE_DIR, "metadata.json")

# Load or initialize FAISS index
if os.path.exists(INDEX_PATH):
    faiss_index = faiss.read_index(INDEX_PATH)
else:
    print("FAISS index not found. Creating a new one.")
    faiss_index = faiss.IndexFlatL2(384)
    faiss.write_index(faiss_index, INDEX_PATH)

# Load or initialize metadata
if os.path.exists(METADATA_PATH):
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
else:
    metadata = []
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump([], f)

# Load embedding model
embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")


class LlmAgent:
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key='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', 
            temperature=0.1,
            model_name='llama3-70b-8192'
        )

    def ask(self, prompt_text):
        prompt_template = PromptTemplate(
            input_variables=["prompt_text"],
            template="{prompt_text}"
        )
        chain = prompt_template | self.llm
        response = chain.invoke({"prompt_text": prompt_text})
        return response.content


def retrieve_context(query, top_k=4):
    query_vector = embedding_model.encode(query).astype("float32")
    D, I = faiss_index.search(np.array([query_vector]), top_k)

    retrieved_chunks = []
    for idx in I[0]:
        if idx < len(metadata):
            retrieved_chunks.append(metadata[idx]["content"])
    return retrieved_chunks


def process_query(query_text):
    agent = LlmAgent()
    relevant_chunks = retrieve_context(query_text)
    context = "\n\n".join(relevant_chunks)

    prompt = f"""
You are an intelligent research assistant specializing in scientific literature.

Below is context extracted from research papers. Use it to provide a relevant, accurate, and helpful response to the user's query.
Handle queries asking for theory, metrics, image interpretation, or summaries.

Context from academic documents:
{context}

User Query:
{query_text}

Give a complete and helpful answer:
"""
    return agent.ask(prompt)
