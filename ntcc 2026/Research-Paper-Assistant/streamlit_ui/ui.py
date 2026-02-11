import streamlit as st
import os
import sys

# Add app folder to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import processing and LLM functions
from app.ingestion import process_pdf
from app.llm_agent import process_query
from app.arxiv_lookup import search_arxiv  # Keep using the same file

# Streamlit config
st.set_page_config(
    page_title="Enterprise Document Intelligence Platform", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enterprise look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .doc-type-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin: 0.25rem;
        background-color: #dbeafe;
        color: #1e40af;
        border-radius: 0.375rem;
        font-size: 0.875rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🏢 Enterprise Document Intelligence Platform</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced semantic search and contextual Q&A for enterprise documents using AI-powered retrieval</p>', unsafe_allow_html=True)

# Document types info
st.markdown("""
<div style="background-color: #f3f4f6; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1.5rem;">
    <strong>📋 Supported Document Types:</strong><br>
    <span class="doc-type-badge">Legal Contracts</span>
    <span class="doc-type-badge">Insurance Policies</span>
    <span class="doc-type-badge">Compliance Manuals</span>
    <span class="doc-type-badge">Operational Guidelines</span>
    <span class="doc-type-badge">Technical Documentation</span>
    <span class="doc-type-badge">Research Papers</span>
</div>
""", unsafe_allow_html=True)

# Initialize session state for uploaded files
if "pdf_files" not in st.session_state:
    st.session_state.pdf_files = []

# --- Sidebar ---
st.sidebar.title("📂 Document Management")

# Upload PDFs Section
st.sidebar.header("1️⃣ Upload Documents")
st.sidebar.markdown("Upload your enterprise documents for semantic indexing and intelligent retrieval.")

uploaded_files = st.sidebar.file_uploader(
    "Select PDF files",
    type=["pdf"],
    accept_multiple_files=True,
    help="Upload legal contracts, policies, manuals, or technical documentation"
)

if uploaded_files:
    for file in uploaded_files:
        file_path = f"./data/sample_papers/{file.name}"
        # ✅ Only process if not already processed
        if file_path not in st.session_state.pdf_files:
            with st.spinner(f"Processing {file.name}..."):
                with open(file_path, "wb") as f:
                    f.write(file.read())
                process_pdf(file_path)
                st.session_state.pdf_files.append(file_path)
            st.sidebar.success(f"✅ {file.name}")

# Show uploaded documents
if st.session_state.pdf_files:
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**📊 Documents Indexed:** {len(st.session_state.pdf_files)}")
    with st.sidebar.expander("View indexed documents"):
        for idx, file_path in enumerate(st.session_state.pdf_files, 1):
            st.markdown(f"{idx}. `{os.path.basename(file_path)}`")

# Document Lookup (renamed from ArXiv)
st.sidebar.markdown("---")
st.sidebar.header("2️⃣ Document Lookup")
st.sidebar.markdown("Search external document repositories and legal databases.")

search_query = st.sidebar.text_input(
    "Search documents",
    placeholder="e.g., 'contract law precedents' or 'compliance frameworks'"
)

if st.sidebar.button("🔍 Search Documents", use_container_width=True):
    with st.spinner("🔍 Searching document repository..."):
        result = search_arxiv(search_query)  # Still uses same function
        if result and "error" not in result:
            st.sidebar.success("✅ Document Found!")
            
            # Display in Main Area
            st.markdown("---")
            st.markdown("### 📄 External Document")
            st.markdown(f"#### {result['title']}")
            st.markdown(f"**👤 Authors:** {result['authors']}")
            st.markdown(f"**📅 Published:** {result['published']}")
            st.markdown("**📝 Abstract:**")
            st.info(result['summary'])
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"📄 [View Full Document]({result['arxiv_url']})")
            with col2:
                st.markdown(f"⬇️ [Download PDF]({result['pdf_url']})")
            
            # Compact Sidebar View
            st.sidebar.markdown("---")
            st.sidebar.markdown("**📌 Top Result:**")
            st.sidebar.markdown(f"_{result['title'][:60]}..._")
            st.sidebar.markdown(f"[📄 PDF]({result['pdf_url']})")
            
        elif result and "error" in result:
            st.sidebar.error(f"❌ {result['error']}")
        else:
            st.sidebar.warning("⚠️ No results found.")

# --- Main Query Section ---
st.markdown("---")
st.header("💬 Intelligent Document Query")
st.markdown("Ask questions about your uploaded documents. Our AI agent performs **semantic search** across your document corpus to retrieve contextually relevant information.")

# Query interface
col1, col2 = st.columns([3, 1])

with col1:
    query_text = st.text_area(
        "Enter your question",
        placeholder="e.g., What are the liability clauses in the insurance policy? What compliance requirements are mentioned?",
        height=100
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.button("🚀 Submit Query", use_container_width=True, type="primary")

# Example queries
with st.expander("💡 Example Queries"):
    st.markdown("""
    - What are the key terms and conditions in the contract?
    - Summarize the compliance requirements mentioned in the manual
    - What are the operational guidelines for incident management?
    - List all liability clauses in the insurance policy
    - What technical specifications are mentioned for the system?
    - What are the indemnification provisions?
    """)

# --- Submit Query ---
if submit_button:
    if not query_text:
        st.warning("⚠️ Please enter a question to proceed.")
    elif not st.session_state.pdf_files:
        st.warning("⚠️ Please upload at least one document before querying.")
    else:
        with st.spinner("🤖 Processing your query using AI-powered semantic search..."):
            result = process_query(query_text)
        
        st.markdown("---")
        st.success("✅ Query Response")
        st.markdown("### 📋 Answer")
        st.markdown(result)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 0.875rem; padding: 1rem;">
    <strong>Enterprise Document Intelligence Platform</strong> | 
    Powered by Advanced RAG Architecture | 
    Semantic Search • Context-Aware Retrieval • Domain-Specific Understanding
</div>
""", unsafe_allow_html=True)