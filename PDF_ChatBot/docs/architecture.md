# Technical Architecture
# PDF ChatBot — System Design & Component Reference

---

## 1. System Overview

PDF ChatBot is a **client-side RAG (Retrieval-Augmented Generation)** application. All heavy computation (embedding, vector search) runs locally on the user's machine. Only the final LLM generation step requires an external API call to Google Gemini.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          PDF ChatBot System                                  │
│                                                                              │
│   ┌───────────┐   ┌──────────────────────────────────────────────────────┐   │
│   │  Browser  │   │                  app.py (Streamlit)                  │   │
│   │    UI     │◀──│                                                      │   │
│   │           │──▶│   Sidebar           │        Main Content            │   │
│   └───────────┘   │  ┌──────────────┐  │   ┌───────────────────────┐    │   │
│                   │  │  API Key     │  │   │   Chat Interface      │    │   │
│                   │  │  PDF Upload  │  │   │   Message History     │    │   │
│                   │  │  Index Btn   │  │   │   Source Citations    │    │   │
│                   │  │  Stats       │  │   │   Welcome Screen      │    │   │
│                   │  └──────────────┘  │   └───────────────────────┘    │   │
│                   └──────────────────────────────────────────────────────┘   │
│                                │                   │                         │
│                   ┌────────────▼───────────────────▼──────────────────────┐  │
│                   │              Core Pipeline Layer                       │  │
│                   │                                                        │  │
│                   │  index_pdfs()              get_answer()                │  │
│                   │  ┌──────────┐              ┌──────────┐               │  │
│                   │  │ Extract  │              │ Retrieve │               │  │
│                   │  │ Clean    │              │ Format   │               │  │
│                   │  │ Chunk    │              │ Generate │               │  │
│                   │  │ Embed    │              └────┬─────┘               │  │
│                   │  │ Save     │                   │                     │  │
│                   │  └────┬─────┘                   │                     │  │
│                   └───────┼───────────────────────── │ ───────────────────┘  │
│                           │  LOCAL                   │  EXTERNAL             │
│                   ┌───────▼──────────┐     ┌─────────▼──────────┐           │
│                   │   FAISS Index    │     │   Google Gemini    │           │
│                   │  (vectorstore/)  │◀───▶│       API          │           │
│                   │  index.faiss     │     │  (gemini-2.0-flash)│           │
│                   │  index.pkl       │     └────────────────────┘           │
│                   └──────────────────┘                                       │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Architecture

### 2.1 Ingestion Pipeline

```
PDF Files (dataset/ + uploads)
         │
         ▼
┌─────────────────────┐
│   PyMuPDF (fitz)    │  ← Open PDF, iterate pages, call page.get_text()
│   Text Extractor    │
└────────┬────────────┘
         │  raw text per page
         ▼
┌─────────────────────┐
│   Text Cleaner      │  ← re.sub(r"\s+", " ", text)
│   (clean_text())    │     remove \n, \t, strip
└────────┬────────────┘
         │  clean text per page
         ▼
┌─────────────────────┐
│  RecursiveCharacter │  ← chunk_size=1000, chunk_overlap=200
│   TextSplitter      │     separators: ["\n\n", "\n", ".", " ", ""]
└────────┬────────────┘
         │  chunks with metadata
         ▼
┌─────────────────────┐
│  HuggingFaceEmbed.  │  ← sentence-transformers/all-MiniLM-L6-v2
│  (all-MiniLM-L6-v2) │     384-dimensional dense vectors
└────────┬────────────┘
         │  (text, vector, metadata) tuples
         ▼
┌─────────────────────┐
│    FAISS Index      │  ← IndexFlatL2 (exact L2 search)
│    (save_local)     │     saved to vectorstore/faiss_index/
└─────────────────────┘
```

### 2.2 Query Pipeline (RAG)

```
User Query (string)
         │
         ▼
┌─────────────────────┐
│  HuggingFaceEmbed.  │  ← embed query with same model as index
│   (query embed)     │     384-dim vector
└────────┬────────────┘
         │  query vector
         ▼
┌─────────────────────┐
│    FAISS Search     │  ← similarity_search(query, k=4)
│   (IndexFlatL2)     │     returns top-4 Documents by L2 distance
└────────┬────────────┘
         │  [Document(page_content, metadata), ...]
         ▼
┌─────────────────────┐
│   Prompt Builder    │  ← ChatPromptTemplate.from_template()
│                     │     injects: history + context + question
└────────┬────────────┘
         │  formatted prompt string
         ▼
┌─────────────────────┐
│  ChatGoogleGenAI    │  ← Gemini model via LangChain wrapper
│  (Gemini LLM)       │     temperature=0.3, streaming=False
└────────┬────────────┘
         │  AIMessage(content="...")
         ▼
┌─────────────────────┐
│   Response Parser   │  ← extract .content, pass source docs
└────────┬────────────┘
         │
         ▼
    {answer: str, sources: [Document, ...]}
```

### 2.3 Conversational Memory

```
conversation_history: list[str]  (alternating user/ai)
= [q1, a1, q2, a2, q3, a3, ...]

On each new query:
  window = last 12 items (6 exchanges)
  history_str = join pairs as "Human: {q}\nAssistant: {a}"

Prompt template receives:
  {history}  ← conversation_history window
  {context}  ← FAISS retrieved chunks
  {question} ← current user query
```

---

## 3. Data Flow Diagram

```
┌──────────────────────────────────────────────────────┐
│                    INDEXING FLOW                      │
│                                                      │
│  PDF File ─▶ fitz.open() ─▶ page.get_text()         │
│                ─▶ clean_text() ─▶ splitter.split()   │
│                ─▶ Document(page_content, metadata)   │
│                ─▶ HuggingFaceEmbeddings.embed()      │
│                ─▶ FAISS.from_documents()             │
│                ─▶ vector_db.save_local()             │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│                    QUERY FLOW                         │
│                                                      │
│  User Input ─▶ vector_db.similarity_search(k=4)     │
│             ─▶ Build prompt(history, context, q)     │
│             ─▶ llm.invoke(prompt)                    │
│             ─▶ Parse response.content                │
│             ─▶ Display answer + sources in UI        │
│             ─▶ Append (query, answer) to history     │
└──────────────────────────────────────────────────────┘
```

---

## 4. File Structure

```
PDF_ChatBot/
│
├── app.py                          ← Streamlit app entry point
│   ├── CUSTOM_CSS                  ← Injected dark-theme styles (~350 lines)
│   ├── init_session()              ← Session state initialisation
│   ├── validate_api_key_format()   ← Pre-API key format check
│   ├── load_llm()                  ← Gemini model with 4-model fallback
│   ├── load_vectordb()             ← @st.cache_resource FAISS loader
│   ├── index_pdfs()                ← Full ingestion pipeline
│   └── get_answer()                ← RAG with conversation history
│
├── notebook/
│   └── chatbot.ipynb               ← Jupyter development notebook
│       ├── Phase 1 (cells 1-4)     ← Setup
│       ├── Phase 2 (cells 5-8)     ← PDF extraction
│       ├── Phase 3 (cells 9-12)    ← Cleaning & chunking
│       ├── Phase 4 (cells 13-16)   ← Embeddings & FAISS
│       ├── Phase 5 (cells 17-20)   ← RAG pipeline
│       └── Phase 6 (cells 29-39)   ← Conversational chatbot
│
├── dataset/                        ← Input PDFs
│   └── CN (4).pdf
│
├── vectorstore/
│   └── faiss_index/
│       ├── index.faiss             ← Binary FAISS index (vectors)
│       └── index.pkl               ← Metadata mapping (chunk → doc/page)
│
├── reports/                        ← Auto-generated analysis CSVs
│   ├── extracted_text.csv          ← Raw text per page
│   └── chunked_documents.csv       ← Text chunks with metadata
│
├── docs/                           ← Project documentation
│   ├── prd.md                      ← Product Requirements Document
│   ├── phases.md                   ← Phase breakdown
│   ├── architecture.md             ← This file
│   └── rules.md                    ← Development rules & standards
│
├── charts/                         ← (Reserved) EDA visualisations
├── model/                          ← (Reserved) Local model weights
├── venv/                           ← Python virtual environment
├── README.md                       ← Public-facing documentation
├── requirements.txt                ← Python dependencies
├── .env                            ← API keys (never commit)
└── .gitignore                      ← VCS exclusions
```

---

## 5. Technology Decisions

### 5.1 Why FAISS over ChromaDB / Pinecone?

| Aspect | FAISS | ChromaDB | Pinecone |
|--------|-------|----------|---------|
| **Cost** | Free, local | Free (local) | Paid (cloud) |
| **Speed** | ⚡⚡⚡ Fastest | ⚡⚡ Fast | ⚡⚡ Fast |
| **No internet** | ✅ Yes | ✅ Yes | ❌ Cloud |
| **Persistence** | ✅ `save_local` | ✅ SQLite | ✅ Cloud |
| **Production-ready** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Chosen** | ✅ | ❌ | ❌ |

**Decision:** FAISS chosen for zero cost, maximum speed, and offline capability.

### 5.2 Why `all-MiniLM-L6-v2` for Embeddings?

| Model | Dims | Size | Speed | Quality |
|-------|------|------|-------|---------|
| `all-MiniLM-L6-v2` | 384 | 22MB | ⚡⚡⚡ | ⭐⭐⭐ |
| `all-mpnet-base-v2` | 768 | 420MB | ⚡⚡ | ⭐⭐⭐⭐ |
| `text-embedding-3-small` | 1536 | API | ⚡ | ⭐⭐⭐⭐⭐ |

**Decision:** `all-MiniLM-L6-v2` is the optimal CPU-friendly model — 22MB download, < 2s embedding for 54 chunks.

### 5.3 Why Gemini over OpenAI / Anthropic?

| Provider | Free Tier | Context Window | Speed |
|---------|-----------|----------------|-------|
| **Google Gemini** | ✅ Generous | 1M tokens | ⚡⚡⚡ |
| OpenAI GPT-4o | ❌ Paid | 128K tokens | ⚡⚡ |
| Anthropic Claude | ❌ Paid | 200K tokens | ⚡⚡ |

**Decision:** Gemini's free tier allows prototyping without billing.

### 5.4 Why Streamlit over Flask / FastAPI?

- Zero frontend code — pure Python
- Built-in session state, file uploader, progress bars
- One-command deployment
- Native hot-reload for development

---

## 6. Prompt Architecture

### System Prompt Template

```
You are an expert AI assistant that answers questions based on the provided 
PDF document context.

Guidelines:
- Answer ONLY from the provided context.
- If the answer is not in the context, say:
  "I don't have enough information in the documents to answer this."
- Be concise, accurate and well-structured.
- Use bullet points or numbered lists where appropriate.
- Reference the document and page number when possible.

Chat History:
{history}

Context from Documents:
{context}

Question: {question}

Answer:
```

### Prompt Design Decisions
| Decision | Rationale |
|----------|-----------|
| "Answer ONLY from context" | Prevents hallucination |
| History window = 6 exchanges | Balances context richness vs token cost |
| k=4 retrieved chunks | Enough coverage, stays under context window |
| temperature=0.3 | Factual accuracy over creativity |
| `convert_system_message_to_human=True` | Required for Gemini (no system role) |

---

## 7. API Key & Model Fallback

### Key Validation

```python
def validate_api_key_format(key: str) -> tuple[bool, str]:
    if not key:               return False, "Empty"
    if not key.startswith("AIza"):  return False, "Wrong format"
    if len(key) < 30:         return False, "Too short"
    return True, "Valid"
```

### Model Fallback Sequence

```
gemini-2.0-flash         ← Try first (fastest free-tier model)
        │ fail (429 quota / 404 deprecated)
        ▼
gemini-2.0-flash-lite    ← Try second
        │ fail
        ▼
gemini-1.5-flash         ← Try third (stable, not -latest alias)
        │ fail
        ▼
gemini-1.5-pro           ← Try fourth (highest quality)
        │ fail
        ▼
    Show error message    ← All failed: quota exhausted or bad key
```

### Error Classification

```python
if "RESOURCE_EXHAUSTED" in err or "429" in err:
    # Free-tier quota → wait 24h
elif "NOT_FOUND" in err or "404" in err:
    # Model deprecated → skip to next
elif "API_KEY_INVALID" in err or "401" in err:
    # Bad key → stop fallback loop immediately
```

---

## 8. Session State Schema

```python
st.session_state = {
    "messages":      list[dict],   # [{role, content, sources, ts}, ...]
    "vector_db":     FAISS | None, # loaded FAISS index
    "llm":           ChatGoogleGenerativeAI | None,
    "chat_history":  list[str],    # [q1, a1, q2, a2, ...] rolling
    "indexed_files": list[str],    # names of indexed PDFs
    "chunks_count":  int,          # total chunks in index
    "api_key_valid": bool,
    "active_model":  str | None,   # e.g., "gemini-2.0-flash"
    "error_msg":     str | None,
    "processing":    bool,         # True while indexing
}
```

---

## 9. Performance Characteristics

### Indexing (CN (4).pdf — 46 pages, 54 chunks)

| Step | Time (CPU) |
|------|------------|
| PDF extraction | < 1s |
| Text cleaning | < 1s |
| Chunking | < 1s |
| Embedding (54 chunks) | 5–15s |
| FAISS index build | < 1s |
| **Total** | **~10–20s** |

### Query (per question)

| Step | Time |
|------|------|
| Query embedding | < 0.5s |
| FAISS search (k=4) | < 0.1s |
| Gemini API call | 2–8s (network) |
| **Total** | **~3–10s** |

---

## 10. Security Considerations

| Concern | Mitigation |
|---------|------------|
| API key in `.env` committed | `.gitignore` excludes `.env` |
| API key in Streamlit session | Never serialised to disk; memory-only |
| Malicious PDF upload | PyMuPDF only reads text; no code execution |
| FAISS index tampering | `allow_dangerous_deserialization=True` is required by LangChain — only load indexes you generated |
| Log exposure of API key | No logging of keys at any point in code |

---

*PDF ChatBot — architecture.md v1.0 — August 2026*
