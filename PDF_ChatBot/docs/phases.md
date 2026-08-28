# Project Phases
# PDF ChatBot — Phase-by-Phase Development Plan

---

## Overview

The project is structured into **9 sequential phases**, each building on the previous. Every phase has a clear objective, deliverables, and completion criteria.

```
Phase 1 ──▶ Phase 2 ──▶ Phase 3 ──▶ Phase 4 ──▶ Phase 5
 Setup      PDF Load    Chunking    Embeddings     RAG
                                        │
                                        ▼
Phase 9 ◀── Phase 8 ◀── Phase 7 ◀── Phase 6
  Docs       Pro UI     Streamlit    Chatbot
```

---

## Phase Status Dashboard

| # | Phase | Status | Deliverable |
|---|-------|--------|-------------|
| 1 | Project Setup | ✅ Complete | Env, directories, library check |
| 2 | PDF Loading & Extraction | ✅ Complete | `extracted_text.csv` |
| 3 | Text Cleaning & Chunking | ✅ Complete | `chunked_documents.csv` |
| 4 | Embeddings & FAISS | ✅ Complete | `vectorstore/faiss_index/` |
| 5 | RAG Pipeline | ✅ Complete | Working `qa_chain` in notebook |
| 6 | Conversational Chatbot | ✅ Complete | Multi-turn chain with memory |
| 7 | Streamlit Deployment | ✅ Complete | `app.py` running at `localhost:8501` |
| 8 | Professional UI | ✅ Complete | Dark glassmorphism theme |
| 9 | Documentation | ✅ Complete | `docs/` folder, `README.md` |

---

## Phase 1 — Project Setup

**Objective:** Bootstrap the development environment and verify all dependencies.

### Tasks
- [x] Create project directory structure (`dataset/`, `model/`, `vectorstore/`, `charts/`, `reports/`)
- [x] Create and activate Python virtual environment
- [x] Install all required libraries from `requirements.txt`
- [x] Load and validate `GOOGLE_API_KEY` from `.env`
- [x] Verify imports: Streamlit, LangChain, FAISS, PyMuPDF, Google GenAI

### Deliverables
- `requirements.txt` — all project dependencies
- `.env` — API key configuration
- `.gitignore` — security exclusions
- Verified library versions printed in notebook

### Notebook Cells
- Cell 1: Print banner
- Cell 2: Create project directories
- Cell 3: Load `.env` + validate API key format
- Cell 4: Import and version-check all libraries

### Completion Criteria
```
✅ All directories exist
✅ GOOGLE_API_KEY loaded and format-validated
✅ Streamlit, LangChain, FAISS, fitz, google.generativeai all importable
```

---

## Phase 2 — PDF Loading & Text Extraction

**Objective:** Load PDF files and extract raw text from every page.

### Tasks
- [x] Scan `dataset/` folder for `.pdf` files
- [x] Open each PDF with PyMuPDF (`fitz`)
- [x] Extract text page-by-page
- [x] Build a DataFrame with columns: `Document`, `Page`, `Text`
- [x] Compute text statistics (characters, words per page)
- [x] Save to `reports/extracted_text.csv`

### Key Decisions
| Decision | Choice | Reason |
|----------|--------|--------|
| PDF library | PyMuPDF (`fitz`) | Fastest, most accurate text extraction |
| Storage | CSV (pandas) | Human-readable, easy to inspect |
| Page granularity | One row per page | Preserves page metadata for citations |

### Deliverables
- `reports/extracted_text.csv` — columns: `Document`, `Page`, `Text`, `Characters`, `Words`

### Notebook Cells
- Cell 5: Scan `dataset/` and list PDFs
- Cell 6: Extract text from all pages with PyMuPDF
- Cell 7: Create DataFrame + compute statistics
- Cell 8: Save to CSV + print Phase 2 summary

### Completion Criteria
```
✅ All PDF pages extracted without errors
✅ extracted_text.csv saved with correct schema
✅ Character/word statistics computed
```

---

## Phase 3 — Text Cleaning & Chunking

**Objective:** Normalise extracted text and split it into retrieval-ready chunks.

### Tasks
- [x] Load `extracted_text.csv`
- [x] Clean text: remove extra whitespace, newlines, tabs
- [x] Filter out empty / near-empty pages (< 1 word)
- [x] Split each page's text using `RecursiveCharacterTextSplitter`
- [x] Attach metadata: `Chunk_ID`, `Document`, `Page`
- [x] Save to `reports/chunked_documents.csv`

### Chunking Parameters
| Parameter | Value | Reason |
|-----------|-------|--------|
| `chunk_size` | 1000 chars | Fits within LLM context without losing coherence |
| `chunk_overlap` | 200 chars | Prevents information loss at boundaries |
| `separators` | `\n\n`, `\n`, `.`, ` `, `` | Tries natural boundaries first |

### Why Chunking?
LLMs have limited context windows. Splitting documents into chunks allows:
1. **Selective retrieval** — only relevant chunks go into the prompt
2. **Memory efficiency** — no need to load the whole document
3. **Better answers** — focused context = less noise

### Deliverables
- `reports/chunked_documents.csv` — columns: `Chunk_ID`, `Document`, `Page`, `Chunk`

### Notebook Cells
- Cell 9: Load extracted text + display head
- Cell 10: Apply `clean_text()` function, filter empties
- Cell 11: Run `RecursiveCharacterTextSplitter`, build `chunk_df`
- Cell 12: Save chunks CSV + print Phase 3 summary

### Completion Criteria
```
✅ Text cleaned (no extra spaces/newlines)
✅ Empty pages removed
✅ Chunks created with correct overlap
✅ chunked_documents.csv saved
```

---

## Phase 4 — Embeddings & FAISS Vector Database

**Objective:** Convert text chunks into numerical vectors and build a searchable vector index.

### Tasks
- [x] Load `chunked_documents.csv`
- [x] Load `sentence-transformers/all-MiniLM-L6-v2` embedding model
- [x] Generate vector embeddings for all chunks
- [x] Build FAISS `IndexFlatL2` vector store
- [x] Wrap each chunk as a `langchain_core.documents.Document` with metadata
- [x] Save FAISS index to `vectorstore/faiss_index/`
- [x] Test semantic search with a sample query

### Embedding Model Choice
| Model | Dims | Speed | Quality | Chosen |
|-------|------|-------|---------|--------|
| `all-MiniLM-L6-v2` | 384 | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | ✅ Yes |
| `all-mpnet-base-v2` | 768 | ⚡⚡ Medium | ⭐⭐⭐⭐ Better | ❌ Slower |
| `text-embedding-ada-002` | 1536 | ⚡ API-only | ⭐⭐⭐⭐⭐ Best | ❌ Paid |

### Deliverables
- `vectorstore/faiss_index/index.faiss` — binary FAISS index
- `vectorstore/faiss_index/index.pkl` — metadata mapping

### Notebook Cells
- Cell 13: Load chunks DataFrame
- Cell 14: Load HuggingFace embedding model
- Cell 15: Build FAISS index + save locally
- Cell 16: Load index + run semantic search test + print Phase 4 summary

### Completion Criteria
```
✅ Embedding model loaded (384-dim)
✅ FAISS index built with 54 documents
✅ Semantic search returns relevant top-3 chunks
✅ vectorstore/faiss_index/ saved to disk
```

---

## Phase 5 — RAG Pipeline

**Objective:** Connect the vector retriever to the Gemini LLM to build a working Q&A system.

### Tasks
- [x] Load FAISS index with embedding model
- [x] Load Gemini LLM with API key (multi-model fallback)
- [x] Build prompt template with context + question slots
- [x] Create `answer_with_context()` RAG function
- [x] Wrap in `RunnableLambda` chain
- [x] Test with a sample question

### RAG Flow
```
User Query
    │
    ▼
[FAISS Retriever] — similarity_search(query, k=4)
    │
    ▼ top-4 chunks
[Prompt Template] — format(context=chunks, question=query)
    │
    ▼ formatted prompt
[Gemini LLM] — generate response
    │
    ▼
Answer + Source Documents
```

### Model Fallback List (Fixed in Phase 6)
```python
# v1.0 (corrected — deprecated models removed)
MODEL_LIST = [
    "gemini-2.0-flash",       # Primary (fast, free tier)
    "gemini-2.0-flash-lite",  # Fallback 1
    "gemini-1.5-flash",       # Fallback 2 (stable alias)
    "gemini-1.5-pro",         # Fallback 3 (higher quality)
]
```

> ⚠️ **Note:** `gemini-1.5-flash-latest` and `gemini-2.5-flash` were removed — both return 404 for new users.

### Deliverables
- Working `qa_chain` in notebook
- Single-question test demonstrating accurate retrieval + answer

### Notebook Cells
- Cell 17: Load FAISS + embedding model
- Cell 18: Load Gemini LLM with model fallback loop
- Cell 19: Build RAG prompt + `answer_with_context()` function
- Cell 20: Test query + print Phase 5 summary

### Completion Criteria
```
✅ LLM loads successfully (at least one model from fallback list)
✅ RAG chain returns grounded answer
✅ Source documents listed with answer
```

---

## Phase 6 — Conversational PDF Chatbot

**Objective:** Add multi-turn conversational memory to the RAG pipeline.

### Tasks
- [x] Implement rolling conversation history (last 6 exchanges)
- [x] Inject history into RAG prompt as `{history}` slot
- [x] Build `answer_with_memory()` wrapping prior history + retrieval + LLM
- [x] Create `ask()` helper with pretty-printed output and citations
- [x] Test 3-turn conversation demonstrating follow-up resolution
- [x] Add graceful error handling (quota, invalid key, model not found)

### Memory Architecture
```
conversation_history = [q1, a1, q2, a2, q3, a3, ...]  # rolling list

For each new query:
  history_window = last 12 items (6 exchanges)
  history_str = "Human: q1\nAssistant: a1\n\nHuman: q2\nAssistant: a2..."
  
  Prompt = system_prompt.format(
      history=history_str,
      context=retrieved_chunks,
      question=new_query
  )
```

### API Error Handling
| Error | Message Shown |
|-------|--------------|
| `RESOURCE_EXHAUSTED` / `429` | "Free-tier quota exhausted — try again in 24h" |
| `NOT_FOUND` / `404` | "Model deprecated — skipping to next fallback" |
| `API_KEY_INVALID` / `401` | "Invalid API key — get one at AI Studio" |
| Other | Full error message displayed |

### Deliverables
- 10 Phase 6 cells appended to `notebook/chatbot.ipynb`
- Demonstrated 3-turn multi-topic conversation

### Completion Criteria
```
✅ Turn 1: Answers initial question accurately
✅ Turn 2: Remembers context from Turn 1
✅ Turn 3: Resolves "the first one you mentioned" correctly
✅ API errors produce friendly messages, not stack traces
```

---

## Phase 7 — Streamlit Deployment

**Objective:** Package the RAG chatbot into a production-ready Streamlit web app.

### Tasks
- [x] Create `app.py` at project root
- [x] Build sidebar: API key input, PDF uploader, index button
- [x] Implement full indexing pipeline in `index_pdfs()` with progress bar
- [x] Auto-load existing FAISS index on startup
- [x] Implement `get_answer()` with history injection
- [x] Build chat form with send button + session state
- [x] Display source citations in expandable section
- [x] Handle quota / model errors with user-friendly messages

### App Architecture
```
app.py
├── init_session()          — initialise Streamlit session state
├── validate_api_key_format() — format check before API call
├── load_llm()              — Gemini with 4-model fallback
├── load_vectordb()         — cached FAISS loader
├── index_pdfs()            — full pipeline: extract→clean→chunk→embed→save
├── get_answer()            — RAG with conversation history
│
├── SIDEBAR
│   ├── API key input + Connect button
│   ├── PDF uploader (multi-file)
│   ├── Dataset PDFs checkbox
│   ├── Index Documents button
│   └── Stats grid + Clear Chat
│
└── MAIN CONTENT
    ├── App header with status badge
    ├── Welcome screen (when not ready)
    ├── Chat message rendering
    ├── Source citations expander
    └── Chat input form
```

### Deliverables
- `app.py` (700+ lines, fully functional)

### Completion Criteria
```
✅ streamlit run app.py starts without errors
✅ API key input validates format
✅ PDF indexing completes with progress feedback
✅ Chat history renders correctly
✅ Source citations appear for last AI message
```

---

## Phase 8 — Professional UI

**Objective:** Apply a premium dark glassmorphism design system.

### Tasks
- [x] Define CSS custom properties (color palette, radii, shadows)
- [x] Style `.stApp` background — deep navy `#0a0e1a`
- [x] Style sidebar — slightly lighter `#0f1629`
- [x] Build app header with gradient text + animated background
- [x] Build chat bubbles — purple gradient (user) / translucent glass (AI)
- [x] Build typing indicator — 3-dot animation
- [x] Build welcome card — floating robot animation
- [x] Build PDF chips, stat grid, source cards
- [x] Style all Streamlit widgets (inputs, buttons, progress, expanders)
- [x] Load Google Fonts: Inter + Outfit
- [x] Add micro-animations (message entrance, button hover, pulse dot)

### Design Tokens
| Token | Value | Usage |
|-------|-------|-------|
| `--bg-primary` | `#0a0e1a` | Main background |
| `--bg-secondary` | `#0f1629` | Sidebar |
| `--accent-1` | `#6c63ff` | Purple accent (buttons, borders) |
| `--accent-2` | `#4fc3f7` | Cyan accent (AI avatar, typing dots) |
| `--accent-grad` | `135deg, #6c63ff → #4fc3f7` | Gradient (header, buttons) |
| `--glass-border` | `rgba(255,255,255,0.08)` | Card borders |
| `--text-primary` | `#e8eaf6` | Main text |
| `--text-secondary` | `#9ca3af` | Subtitles, descriptions |

### Deliverables
- `CUSTOM_CSS` constant in `app.py` (~350 lines of CSS)

### Completion Criteria
```
✅ Dark background with no white flash
✅ All Streamlit default colours overridden
✅ Chat bubbles visually distinct (user vs AI)
✅ Typing indicator animates while LLM responds
✅ Welcome screen displays when setup incomplete
✅ Status badge updates (Ready / Indexing / Setup Required)
```

---

## Phase 9 — Documentation

**Objective:** Create comprehensive project documentation for all stakeholders.

### Tasks
- [x] Write `README.md` — public-facing quick start guide
- [x] Write `docs/prd.md` — product requirements document
- [x] Write `docs/phases.md` — this document
- [x] Write `docs/architecture.md` — technical architecture deep-dive
- [x] Write `docs/rules.md` — development rules and standards
- [x] Update `requirements.txt` — add missing packages, version pins
- [x] Update `.gitignore` — proper security exclusions

### Deliverables
```
docs/
├── prd.md          ← Product Requirements Document
├── phases.md       ← This document
├── architecture.md ← Technical Architecture
└── rules.md        ← Development Rules & Standards

README.md           ← Quick start guide (public-facing)
requirements.txt    ← Updated with all dependencies
.gitignore          ← Updated security exclusions
```

### Completion Criteria
```
✅ All 4 docs/ files created with full content
✅ README.md covers setup, usage, and troubleshooting
✅ requirements.txt includes all transitive dependencies
✅ .gitignore excludes .env, venv, vectorstore, reports
```

---

## Future Phases (v2.0 Roadmap)

| Phase | Feature | Priority |
|-------|---------|---------|
| 10 | OCR support for scanned PDFs (Tesseract) | P1 |
| 11 | Multi-user session isolation | P1 |
| 12 | Chat export (PDF / Markdown) | P2 |
| 13 | Document comparison mode | P2 |
| 14 | Docker containerisation | P2 |
| 15 | Cloud deployment (Streamlit Cloud / HuggingFace Spaces) | P3 |
| 16 | Fine-tune embedding model on domain corpus | P3 |

---

*PDF ChatBot — phases.md v1.0 — August 2026*
