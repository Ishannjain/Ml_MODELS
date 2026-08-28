# =============================================================================
# PDF Chatbot – Streamlit Application
# Phase 7 & 8 : Deployment + Professional UI
# =============================================================================

import os
import re
import time
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="PDF ChatBot | AI-Powered Document Q&A",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load .env (key may be overridden via sidebar) ─────────────────────────────
load_dotenv()

# =============================================================================
# Custom CSS – Dark Glassmorphism Theme
# =============================================================================
CUSTOM_CSS = """
<style>
/* ── Google Font ─────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;700&display=swap');

/* ── Root Variables ──────────────────────────────────────── */
:root {
    --bg-primary:    #0a0e1a;
    --bg-secondary:  #0f1629;
    --bg-card:       rgba(255,255,255,0.04);
    --glass-border:  rgba(255,255,255,0.08);
    --accent-1:      #6c63ff;
    --accent-2:      #4fc3f7;
    --accent-grad:   linear-gradient(135deg, #6c63ff 0%, #4fc3f7 100%);
    --user-bubble:   linear-gradient(135deg, #6c63ff 0%, #8b5cf6 100%);
    --ai-bubble:     rgba(255,255,255,0.05);
    --text-primary:  #e8eaf6;
    --text-secondary:#9ca3af;
    --text-muted:    #6b7280;
    --success:       #10b981;
    --warning:       #f59e0b;
    --error:         #ef4444;
    --radius-lg:     16px;
    --radius-md:     12px;
    --radius-sm:     8px;
    --shadow-glow:   0 0 40px rgba(108,99,255,0.15);
}

/* ── Global Reset ────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* ── Hide default Streamlit chrome ───────────────────────── */
#MainMenu, footer, header { display: none !important; }
.block-container { padding: 0 1.5rem 2rem !important; max-width: 100% !important; }

/* ── Scrollbar ───────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--accent-1); border-radius: 3px; }

/* ── TOP HEADER ──────────────────────────────────────────── */
.app-header {
    background: linear-gradient(135deg, rgba(108,99,255,0.15) 0%, rgba(79,195,247,0.08) 100%);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
}
.app-header::before {
    content: '';
    position: absolute; top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(108,99,255,0.08) 0%, transparent 60%);
    animation: pulse-bg 4s ease-in-out infinite;
}
@keyframes pulse-bg {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50%       { opacity: 1;   transform: scale(1.05); }
}
.app-header-title {
    font-family: 'Outfit', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    background: var(--accent-grad);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin: 0 !important;
    line-height: 1.2 !important;
}
.app-header-sub {
    color: var(--text-secondary) !important;
    font-size: 0.9rem !important;
    margin-top: 0.3rem !important;
}
.status-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem; font-weight: 600;
    border: 1px solid;
}
.status-ready   { background: rgba(16,185,129,0.12); color: #10b981; border-color: rgba(16,185,129,0.3); }
.status-loading { background: rgba(245,158,11,0.12); color: #f59e0b; border-color: rgba(245,158,11,0.3); }
.status-error   { background: rgba(239,68,68,0.12);  color: #ef4444; border-color: rgba(239,68,68,0.3); }
.pulse-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: currentColor;
    animation: dot-pulse 1.5s ease-in-out infinite;
}
@keyframes dot-pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.6); }
}

/* ── SIDEBAR ─────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--glass-border) !important;
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--text-primary) !important;
}

.sidebar-section {
    background: var(--bg-card);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-md);
    padding: 1rem;
    margin-bottom: 1rem;
}
.sidebar-label {
    font-size: 0.7rem; font-weight: 600; letter-spacing: 1.5px;
    color: var(--text-muted); text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.pdf-chip {
    display: flex; align-items: center; gap: 8px;
    background: rgba(108,99,255,0.1);
    border: 1px solid rgba(108,99,255,0.25);
    border-radius: 8px;
    padding: 6px 10px; margin-bottom: 6px;
    font-size: 0.8rem; color: var(--text-primary);
}
.stat-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 8px; margin-top: 8px;
}
.stat-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--glass-border);
    border-radius: 8px;
    padding: 8px 10px; text-align: center;
}
.stat-number {
    font-size: 1.4rem; font-weight: 700;
    background: var(--accent-grad);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-label {
    font-size: 0.68rem; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.8px;
}

/* ── INPUT FIELDS ────────────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent-1) !important;
    box-shadow: 0 0 0 2px rgba(108,99,255,0.2) !important;
}

/* ── BUTTONS ─────────────────────────────────────────────── */
.stButton > button {
    background: var(--accent-grad) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(108,99,255,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(108,99,255,0.5) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── PROGRESS BAR ────────────────────────────────────────── */
[data-testid="stProgress"] > div > div {
    background: var(--accent-grad) !important;
}

/* ── CHAT MESSAGES ───────────────────────────────────────── */
.chat-container {
    display: flex; flex-direction: column;
    gap: 1rem; padding: 0.5rem 0;
}
.chat-msg {
    display: flex; gap: 12px;
    animation: msg-in 0.3s ease-out;
}
@keyframes msg-in {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.chat-msg.user { flex-direction: row-reverse; }
.avatar {
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0;
    border: 2px solid var(--glass-border);
}
.avatar-user { background: var(--user-bubble); border-color: rgba(108,99,255,0.5); }
.avatar-ai   { background: rgba(79,195,247,0.15); border-color: rgba(79,195,247,0.3); }
.bubble {
    max-width: 75%;
    padding: 0.85rem 1.1rem;
    border-radius: var(--radius-md);
    font-size: 0.9rem; line-height: 1.6;
    position: relative;
}
.bubble-user {
    background: var(--user-bubble);
    color: #fff;
    border-bottom-right-radius: 4px;
    box-shadow: 0 4px 20px rgba(108,99,255,0.3);
}
.bubble-ai {
    background: var(--ai-bubble);
    border: 1px solid var(--glass-border);
    color: var(--text-primary);
    border-bottom-left-radius: 4px;
    backdrop-filter: blur(10px);
}
.bubble-timestamp {
    font-size: 0.68rem; color: var(--text-muted);
    margin-top: 4px; text-align: right;
}
.chat-msg.user .bubble-timestamp { text-align: left; }

/* ── SOURCE CARDS ────────────────────────────────────────── */
.source-header {
    font-size: 0.75rem; font-weight: 600;
    color: var(--text-muted); text-transform: uppercase;
    letter-spacing: 1px; margin: 0.5rem 0 0.4rem;
}
.source-card {
    background: rgba(108,99,255,0.06);
    border: 1px solid rgba(108,99,255,0.2);
    border-left: 3px solid var(--accent-1);
    border-radius: 0 8px 8px 0;
    padding: 8px 12px; margin-bottom: 6px;
    font-size: 0.8rem;
}
.source-meta {
    display: flex; gap: 12px;
    color: var(--text-muted); font-size: 0.72rem;
    margin-bottom: 4px;
}
.source-text { color: var(--text-secondary); line-height: 1.5; }

/* ── TYPING INDICATOR ────────────────────────────────────── */
.typing-indicator {
    display: flex; align-items: center; gap: 6px;
    padding: 10px 16px;
    background: var(--ai-bubble);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-md);
    border-bottom-left-radius: 4px;
    width: fit-content;
}
.typing-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--accent-2);
    animation: typing 1.2s ease-in-out infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing {
    0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
    40%           { opacity: 1;   transform: scale(1.1); }
}

/* ── WELCOME SCREEN ──────────────────────────────────────── */
.welcome-card {
    background: var(--bg-card);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    padding: 3rem 2rem;
    text-align: center;
    margin: 2rem auto;
    max-width: 600px;
    backdrop-filter: blur(20px);
}
.welcome-icon {
    font-size: 4rem;
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-10px); }
}
.welcome-title {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    margin: 1rem 0 0.5rem !important;
}
.welcome-sub { color: var(--text-secondary) !important; line-height: 1.6 !important; }

.feature-chips {
    display: flex; flex-wrap: wrap; justify-content: center;
    gap: 8px; margin-top: 1.5rem;
}
.feature-chip {
    background: rgba(108,99,255,0.12);
    border: 1px solid rgba(108,99,255,0.25);
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.78rem; color: var(--text-secondary);
}

/* ── ALERTS ──────────────────────────────────────────────── */
.custom-alert {
    padding: 10px 16px;
    border-radius: var(--radius-sm);
    font-size: 0.85rem;
    margin-bottom: 12px;
    border-left: 3px solid;
}
.alert-error   { background: rgba(239,68,68,0.1);  border-color: #ef4444; color: #fca5a5; }
.alert-success { background: rgba(16,185,129,0.1); border-color: #10b981; color: #6ee7b7; }
.alert-info    { background: rgba(79,195,247,0.1); border-color: #4fc3f7; color: #93c5fd; }

/* ── FILE UPLOADER ───────────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02) !important;
    border: 2px dashed rgba(108,99,255,0.3) !important;
    border-radius: var(--radius-md) !important;
    transition: border-color 0.3s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent-1) !important;
}

/* ── EXPANDER ────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius-sm) !important;
}
[data-testid="stExpander"] summary {
    color: var(--text-secondary) !important;
}

/* ── SELECT BOX ──────────────────────────────────────────── */
[data-testid="stSelectbox"] select,
[data-baseweb="select"] {
    background: rgba(255,255,255,0.05) !important;
    border-color: var(--glass-border) !important;
    color: var(--text-primary) !important;
}

/* ── DIVIDER ─────────────────────────────────────────────── */
hr { border-color: var(--glass-border) !important; }

/* ── Streamlit label text ────────────────────────────────── */
label, .stMarkdown p { color: var(--text-primary) !important; }

/* ── Chat input area ─────────────────────────────────────── */
.chat-input-area {
    position: sticky; bottom: 0;
    background: linear-gradient(to top, var(--bg-primary) 80%, transparent);
    padding: 1rem 0 0.5rem;
    backdrop-filter: blur(10px);
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# =============================================================================
# Session State Initialisation
# =============================================================================
def init_session():
    defaults = {
        "messages":        [],       # list of {role, content, sources, ts}
        "vector_db":       None,
        "llm":             None,
        "chat_history":    [],       # LangChain message objects
        "indexed_files":   [],
        "chunks_count":    0,
        "api_key_valid":   False,
        "active_model":    None,
        "error_msg":       None,
        "processing":      False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# =============================================================================
# Helper – Validate Gemini API key format
# =============================================================================
def validate_api_key_format(key: str) -> tuple[bool, str]:
    """Returns (is_valid, message)."""
    key = key.strip()
    if not key:
        return False, "API key is empty."
    if not key.startswith("AIza"):
        return False, (
            "Key doesn't start with 'AIza'. "
            "Please use a valid Gemini API key from https://aistudio.google.com/app/apikey"
        )
    if len(key) < 30:
        return False, "API key is too short."
    return True, "Format looks valid."


# =============================================================================
# Helper – Load LLM (with fallback model list)
# =============================================================================
def load_llm(api_key: str):
    """Try Gemini models in order, return (llm, model_name) or raise."""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
    except ImportError as e:
        raise ImportError("langchain-google-genai not installed.") from e

    # Updated model list – removed deprecated aliases
    model_names = [
       "gemini-3.1-flash-lite"
    ]

    last_error = None
    for model_name in model_names:
        try:
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=0.3,
                convert_system_message_to_human=True,
            )
            # Lightweight probe to confirm the key+model work
            llm.invoke("Hello in one word.")
            return llm, model_name
        except Exception as exc:
            last_error = exc
            continue

    raise RuntimeError(
        f"All Gemini models failed. Last error: {last_error}\n\n"
        "Possible causes:\n"
        "• Free-tier quota exhausted – wait 24h or upgrade billing\n"
        "• Invalid API key – get one at https://aistudio.google.com/app/apikey"
    )


# =============================================================================
# Helper – Load FAISS + Embeddings
# =============================================================================
@st.cache_resource(show_spinner=False)
def load_vectordb(faiss_path: str):
    """Load existing FAISS index from disk."""
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
    except ImportError:
        from langchain_community.embeddings import HuggingFaceEmbeddings

    from langchain_community.vectorstores import FAISS

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    db = FAISS.load_local(
        faiss_path,
        embedding_model,
        allow_dangerous_deserialization=True,
    )
    return db, embedding_model


# =============================================================================
# Helper – Index uploaded PDFs → FAISS
# =============================================================================
def index_pdfs(pdf_paths: list[str], progress_bar, status_text) -> tuple:
    """Extract, chunk, embed PDFs and return (vector_db, embedding_model, n_chunks)."""
    import fitz  # PyMuPDF
    import pandas as pd
    import re as _re

    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
    except ImportError:
        from langchain.text_splitter import RecursiveCharacterTextSplitter

    try:
        from langchain_huggingface import HuggingFaceEmbeddings
    except ImportError:
        from langchain_community.embeddings import HuggingFaceEmbeddings

    from langchain_community.vectorstores import FAISS
    from langchain_core.documents import Document

    total_steps = len(pdf_paths) + 3
    step = 0

    # ── Extract ────────────────────────────────────────────────────────────────
    status_text.markdown("📖 **Extracting text from PDFs…**")
    raw_docs = []
    for pdf_path in pdf_paths:
        doc = fitz.open(pdf_path)
        for pg_num in range(len(doc)):
            text = doc.load_page(pg_num).get_text()
            raw_docs.append({
                "Document": Path(pdf_path).name,
                "Page":     pg_num + 1,
                "Text":     text,
            })
        doc.close()
        step += 1
        progress_bar.progress(step / total_steps)

    # ── Clean ──────────────────────────────────────────────────────────────────
    status_text.markdown("🧹 **Cleaning text…**")
    def clean_text(text):
        if pd.isna(text):
            return ""
        text = str(text)
        text = _re.sub(r"\s+", " ", text)
        text = text.replace("\n", " ").replace("\t", " ")
        return text.strip()

    df = pd.DataFrame(raw_docs)
    df["Clean_Text"] = df["Text"].apply(clean_text)
    df = df[df["Clean_Text"].str.strip() != ""]
    step += 1
    progress_bar.progress(step / total_steps)

    # ── Chunk ──────────────────────────────────────────────────────────────────
    status_text.markdown("✂️ **Chunking documents…**")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    documents = []
    chunk_id = 1
    for _, row in df.iterrows():
        chunks = splitter.split_text(row["Clean_Text"])
        for chunk in chunks:
            documents.append(Document(
                page_content=chunk,
                metadata={
                    "document": row["Document"],
                    "page":     int(row["Page"]),
                    "chunk_id": chunk_id,
                },
            ))
            chunk_id += 1
    step += 1
    progress_bar.progress(step / total_steps)

    # ── Embed ──────────────────────────────────────────────────────────────────
    status_text.markdown("🔢 **Generating embeddings (this may take a moment)…**")
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_db = FAISS.from_documents(documents, embedding_model)

    # Save to disk
    save_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "vectorstore", "faiss_index"
    )
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    vector_db.save_local(save_path)

    step += 1
    progress_bar.progress(1.0)
    return vector_db, embedding_model, len(documents)


# =============================================================================
# Helper – RAG answer
# =============================================================================
def get_answer(query: str, vector_db, llm, chat_history: list) -> dict:
    """Run RAG pipeline with conversational memory."""
    from langchain_core.prompts import ChatPromptTemplate

    # Build history string (last 6 exchanges)
    history_str = ""
    if chat_history:
        history_pairs = []
        for i in range(0, min(len(chat_history), 12), 2):
            if i + 1 < len(chat_history):
                history_pairs.append(
                    f"Human: {chat_history[i]}\nAssistant: {chat_history[i+1]}"
                )
        history_str = "\n\n".join(history_pairs)

    docs = vector_db.similarity_search(query, k=4)
    context = "\n\n".join(doc.page_content for doc in docs)

    system_template = """You are an expert AI assistant that answers questions based on the provided document context.

Guidelines:
- Answer ONLY from the provided context. If the answer is not in the context, clearly say "I don't have enough information in the documents to answer this."
- Be concise, accurate, and well-structured. Use bullet points or numbered lists where appropriate.
- Reference the document and page number when possible.
- Maintain the conversation context shown in the chat history.

Chat History:
{history}

Context from Documents:
{context}

Question: {question}

Answer:"""

    prompt = ChatPromptTemplate.from_template(system_template)
    response = llm.invoke(
        prompt.format(history=history_str, context=context, question=query)
    )
    answer = response.content if hasattr(response, "content") else str(response)
    return {"answer": answer, "sources": docs}


# =============================================================================
# Helper – Format timestamp
# =============================================================================
def fmt_time():
    return time.strftime("%H:%M")


# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown(
        """
        <div style='text-align:center; padding: 0.5rem 0 1rem;'>
          <div style='font-size:2.5rem;'>📄</div>
          <div style='font-family:Outfit,sans-serif; font-size:1.2rem; font-weight:700;
               background: linear-gradient(135deg,#6c63ff,#4fc3f7);
               -webkit-background-clip:text; -webkit-text-fill-color:transparent;
               background-clip:text;'>PDF ChatBot</div>
          <div style='font-size:0.72rem; color:#6b7280; margin-top:2px;'>
               AI-Powered Document Q&A
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── API Key Section ────────────────────────────────────────────────────────
    st.markdown(
        "<div class='sidebar-label'>🔑 Gemini API Key</div>",
        unsafe_allow_html=True,
    )

    env_key = os.getenv("GOOGLE_API_KEY", "").strip()
    # Prefer sidebar input; pre-fill with env key only if it looks valid
    pre_fill = env_key if env_key.startswith("AIza") else ""

    api_key_input = st.text_input(
        "Gemini API Key",
        value=pre_fill,
        type="password",
        placeholder="AIzaSy…",
        label_visibility="collapsed",
        help="Get your free API key at https://aistudio.google.com/app/apikey",
        key="api_key_input",
    )

    active_key = api_key_input.strip() or env_key

    fmt_valid, fmt_msg = validate_api_key_format(active_key)
    if active_key and not fmt_valid:
        st.markdown(
            f"<div class='custom-alert alert-error'>⚠️ {fmt_msg}</div>",
            unsafe_allow_html=True,
        )
    elif active_key and fmt_valid:
        st.markdown(
            "<div class='custom-alert alert-success'>✅ Key format valid</div>",
            unsafe_allow_html=True,
        )

    connect_btn = st.button(
        "🔌 Connect to Gemini",
        use_container_width=True,
        disabled=not fmt_valid,
    )

    if connect_btn and fmt_valid:
        with st.spinner("Testing connection…"):
            try:
                llm, model_name = load_llm(active_key)
                st.session_state.llm = llm
                st.session_state.api_key_valid = True
                st.session_state.active_model = model_name
                st.session_state.error_msg = None
                st.success(f"Connected ✅  •  Model: `{model_name}`")
            except Exception as e:
                st.session_state.api_key_valid = False
                st.session_state.error_msg = str(e)
                st.error("Connection failed. See details below.")
                with st.expander("Error details"):
                    st.code(str(e), language="text")

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── PDF Upload Section ─────────────────────────────────────────────────────
    st.markdown(
        "<div class='sidebar-label'>📂 Document Library</div>",
        unsafe_allow_html=True,
    )

    # Show pre-existing PDFs in dataset folder
    dataset_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "dataset"
    )
    existing_pdfs = list(Path(dataset_path).glob("*.pdf")) if os.path.isdir(dataset_path) else []

    if existing_pdfs:
        for pdf in existing_pdfs:
            size_kb = pdf.stat().st_size // 1024
            st.markdown(
                f"<div class='pdf-chip'>📄 <span style='flex:1;overflow:hidden;"
                f"text-overflow:ellipsis;white-space:nowrap'>{pdf.name}</span>"
                f"<span style='color:#6b7280;font-size:0.7rem'>{size_kb}KB</span></div>",
                unsafe_allow_html=True,
            )

    uploaded_files = st.file_uploader(
        "Upload PDF(s)",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    use_existing = st.checkbox(
        "Also use dataset/ PDFs",
        value=bool(existing_pdfs),
        disabled=not existing_pdfs,
    )

    index_btn = st.button("⚡ Index Documents", use_container_width=True)

    if index_btn:
        pdf_paths_to_index = []

        # Gather uploaded files → temp files
        if uploaded_files:
            for uf in uploaded_files:
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                tmp.write(uf.getbuffer())
                tmp.flush()
                pdf_paths_to_index.append(tmp.name)

        # Gather existing dataset PDFs
        if use_existing and existing_pdfs:
            pdf_paths_to_index.extend([str(p) for p in existing_pdfs])

        if not pdf_paths_to_index:
            st.warning("Please upload at least one PDF or enable 'use dataset PDFs'.")
        else:
            st.session_state.processing = True
            prog = st.progress(0)
            status = st.empty()
            try:
                vdb, emb_model, n_chunks = index_pdfs(pdf_paths_to_index, prog, status)
                st.session_state.vector_db = vdb
                st.session_state.chunks_count = n_chunks
                st.session_state.indexed_files = [
                    (uf.name if hasattr(uf, "name") else Path(p).name)
                    for uf, p in zip(uploaded_files or [], pdf_paths_to_index[:len(uploaded_files or [])])
                ] + ([pdf.name for pdf in existing_pdfs] if use_existing else [])
                st.session_state.messages = []
                st.session_state.chat_history = []
                status.markdown(
                    "<div class='custom-alert alert-success'>✅ Indexing complete!</div>",
                    unsafe_allow_html=True,
                )
                st.session_state.processing = False
            except Exception as e:
                status.markdown(
                    f"<div class='custom-alert alert-error'>❌ Indexing failed: {e}</div>",
                    unsafe_allow_html=True,
                )
                st.session_state.processing = False

    # Also try to load existing FAISS index if not yet loaded
    if st.session_state.vector_db is None:
        faiss_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "vectorstore", "faiss_index"
        )
        if os.path.isdir(faiss_path):
            try:
                vdb, _ = load_vectordb(faiss_path)
                st.session_state.vector_db = vdb
                if not st.session_state.indexed_files and existing_pdfs:
                    st.session_state.indexed_files = [p.name for p in existing_pdfs]
            except Exception:
                pass

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Stats Section ──────────────────────────────────────────────────────────
    if st.session_state.vector_db or st.session_state.chunks_count:
        total_chunks = st.session_state.chunks_count or "–"
        total_docs   = len(st.session_state.indexed_files) or len(existing_pdfs) or "–"
        total_msgs   = len([m for m in st.session_state.messages if m["role"] == "user"])
        model_name   = st.session_state.active_model or "–"

        st.markdown(
            f"""
            <div class='sidebar-section'>
              <div class='sidebar-label'>📊 Stats</div>
              <div class='stat-grid'>
                <div class='stat-card'>
                  <div class='stat-number'>{total_docs}</div>
                  <div class='stat-label'>PDFs</div>
                </div>
                <div class='stat-card'>
                  <div class='stat-number'>{total_chunks}</div>
                  <div class='stat-label'>Chunks</div>
                </div>
                <div class='stat-card'>
                  <div class='stat-number'>{total_msgs}</div>
                  <div class='stat-label'>Queries</div>
                </div>
                <div class='stat-card'>
                  <div class='stat-number' style='font-size:0.75rem;'>
                    {model_name.replace('gemini-','') if model_name != '–' else '–'}
                  </div>
                  <div class='stat-label'>Model</div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Clear chat ─────────────────────────────────────────────────────────────
    if st.session_state.messages:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.rerun()

    # ── About ──────────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style='font-size:0.7rem; color:#4b5563; text-align:center; margin-top:1rem;'>
          Built with LangChain · FAISS · Gemini · Streamlit<br>
          <span style='color:#6c63ff;'>PDF ChatBot v1.0</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# MAIN CONTENT
# =============================================================================

# ── Header ─────────────────────────────────────────────────────────────────────
if st.session_state.api_key_valid and st.session_state.vector_db:
    badge = "<span class='status-badge status-ready'><span class='pulse-dot'></span>Ready</span>"
elif st.session_state.processing:
    badge = "<span class='status-badge status-loading'><span class='pulse-dot'></span>Indexing…</span>"
else:
    badge = "<span class='status-badge status-error'><span class='pulse-dot'></span>Setup Required</span>"

st.markdown(
    f"""
    <div class='app-header'>
      <div style='display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1rem;'>
        <div>
          <h1 class='app-header-title'>📄 PDF ChatBot</h1>
          <p class='app-header-sub'>
            Ask anything about your documents — powered by RAG, FAISS &amp; Gemini
          </p>
        </div>
        <div>{badge}</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Chat Area ──────────────────────────────────────────────────────────────────
chat_col, _ = st.columns([1, 0.001])

with chat_col:
    # Welcome screen (no messages yet)
    if not st.session_state.messages:
        ready = st.session_state.vector_db is not None
        api_ok = st.session_state.api_key_valid

        setup_steps = []
        if not api_ok:
            setup_steps.append("🔑 Connect your Gemini API key in the sidebar")
        if not ready:
            setup_steps.append("📂 Upload / index a PDF document")

        if setup_steps:
            steps_html = "".join(
                f"<div style='color:#9ca3af; font-size:0.85rem; margin:6px 0;'>→ {s}</div>"
                for s in setup_steps
            )
            st.markdown(
                f"""
                <div class='welcome-card'>
                  <div class='welcome-icon'>🤖</div>
                  <h2 class='welcome-title'>Welcome to PDF ChatBot</h2>
                  <p class='welcome-sub'>
                    Chat with your PDFs using AI. Ask questions, get summaries,
                    find specific information — all powered by RAG.
                  </p>
                  <div style='margin:1.2rem 0 0.5rem; color:#6b7280; font-size:0.78rem;
                       text-transform:uppercase; letter-spacing:1px;'>To get started</div>
                  {steps_html}
                  <div class='feature-chips'>
                    <span class='feature-chip'>⚡ Semantic Search</span>
                    <span class='feature-chip'>🧠 Conversational Memory</span>
                    <span class='feature-chip'>📑 Source Citations</span>
                    <span class='feature-chip'>🔒 Local Embeddings</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            # API + index ready but no messages yet
            st.markdown(
                """
                <div class='welcome-card'>
                  <div class='welcome-icon'>✨</div>
                  <h2 class='welcome-title'>Ready to Chat!</h2>
                  <p class='welcome-sub'>
                    Your documents are indexed and Gemini is connected.<br>
                    Ask your first question below!
                  </p>
                  <div class='feature-chips'>
                    <span class='feature-chip'>💬 "Summarize this document"</span>
                    <span class='feature-chip'>🔍 "What is covered in week 3?"</span>
                    <span class='feature-chip'>📊 "List all practicals"</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        # ── Render conversation ────────────────────────────────────────────────
        chat_html_parts = ["<div class='chat-container'>"]

        for msg in st.session_state.messages:
            role    = msg["role"]
            content = msg["content"]
            ts      = msg.get("ts", "")

            if role == "user":
                chat_html_parts.append(
                    f"""
                    <div class='chat-msg user'>
                      <div class='avatar avatar-user'>👤</div>
                      <div>
                        <div class='bubble bubble-user'>{content}</div>
                        <div class='bubble-timestamp'>{ts}</div>
                      </div>
                    </div>
                    """
                )
            else:
                # Escape for HTML display (preserve newlines)
                safe_content = content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                safe_content = safe_content.replace("\n", "<br>")

                chat_html_parts.append(
                    f"""
                    <div class='chat-msg ai'>
                      <div class='avatar avatar-ai'>🤖</div>
                      <div>
                        <div class='bubble bubble-ai'>{safe_content}</div>
                        <div class='bubble-timestamp'>{ts}</div>
                      </div>
                    </div>
                    """
                )

        chat_html_parts.append("</div>")
        st.markdown("".join(chat_html_parts), unsafe_allow_html=True)

        # ── Source citations (for last AI message) ─────────────────────────────
        last_ai = next(
            (m for m in reversed(st.session_state.messages) if m["role"] == "assistant"),
            None,
        )
        if last_ai and last_ai.get("sources"):
            with st.expander("📎 Source Documents", expanded=False):
                for i, doc in enumerate(last_ai["sources"], 1):
                    meta   = doc.metadata
                    d_name = meta.get("document", "Unknown")
                    page   = meta.get("page", "?")
                    chunk  = meta.get("chunk_id", "?")
                    snip   = doc.page_content[:200].replace("\n", " ")
                    st.markdown(
                        f"""
                        <div class='source-card'>
                          <div class='source-meta'>
                            <span>📄 {d_name}</span>
                            <span>Page {page}</span>
                            <span>Chunk #{chunk}</span>
                          </div>
                          <div class='source-text'>"{snip}…"</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    # ── Chat Input ─────────────────────────────────────────────────────────────
    st.markdown("<div class='chat-input-area'>", unsafe_allow_html=True)

    can_chat = st.session_state.api_key_valid and st.session_state.vector_db is not None

    with st.form("chat_form", clear_on_submit=True):
        input_col, btn_col = st.columns([6, 1])
        with input_col:
            user_query = st.text_input(
                "Question",
                placeholder=(
                    "Ask a question about your documents…"
                    if can_chat
                    else "Connect API key and index a PDF first…"
                ),
                label_visibility="collapsed",
                disabled=not can_chat,
                key="user_query_input",
            )
        with btn_col:
            send_btn = st.form_submit_button(
                "Send ➤",
                use_container_width=True,
                disabled=not can_chat,
            )

    if not can_chat:
        hints = []
        if not st.session_state.api_key_valid:
            hints.append("Connect Gemini API key")
        if st.session_state.vector_db is None:
            hints.append("Index a PDF")
        st.markdown(
            f"<div class='custom-alert alert-info'>ℹ️ To start chatting: {' → '.join(hints)}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Process query ──────────────────────────────────────────────────────────
    if send_btn and user_query.strip() and can_chat:
        query = user_query.strip()
        ts = fmt_time()

        # Append user message
        st.session_state.messages.append({
            "role":    "user",
            "content": query,
            "ts":      ts,
        })

        # Typing indicator placeholder
        typing_ph = st.empty()
        typing_ph.markdown(
            """
            <div style='display:flex; gap:12px; align-items:flex-start; margin-top:1rem;'>
              <div class='avatar avatar-ai'>🤖</div>
              <div class='typing-indicator'>
                <span class='typing-dot'></span>
                <span class='typing-dot'></span>
                <span class='typing-dot'></span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        try:
            result = get_answer(
                query,
                st.session_state.vector_db,
                st.session_state.llm,
                st.session_state.chat_history,
            )
            answer  = result["answer"]
            sources = result["sources"]

            # Update chat history (last 12 turns for memory)
            st.session_state.chat_history.append(query)
            st.session_state.chat_history.append(answer)
            if len(st.session_state.chat_history) > 24:
                st.session_state.chat_history = st.session_state.chat_history[-24:]

            # Append AI message
            st.session_state.messages.append({
                "role":    "assistant",
                "content": answer,
                "sources": sources,
                "ts":      fmt_time(),
            })
            st.session_state.error_msg = None

        except Exception as e:
            err_msg = str(e)
            if "RESOURCE_EXHAUSTED" in err_msg or "429" in err_msg:
                friendly = (
                    "⏳ **Quota exceeded.** Your free-tier API quota is exhausted.\n\n"
                    "• Wait ~24 hours for daily reset, OR\n"
                    "• Enable billing at [Google AI Studio](https://aistudio.google.com)"
                )
            elif "API_KEY_INVALID" in err_msg or "401" in err_msg:
                friendly = "❌ **Invalid API key.** Please check your key in the sidebar."
            else:
                friendly = f"❌ **Error:** {err_msg}"

            st.session_state.messages.append({
                "role":    "assistant",
                "content": friendly,
                "sources": [],
                "ts":      fmt_time(),
            })

        typing_ph.empty()
        st.rerun()
