# Product Requirements Document (PRD)
# PDF ChatBot — AI-Powered Document Q&A System

---

## 1. Document Information

| Field | Value |
|-------|-------|
| **Project Name** | PDF ChatBot |
| **Version** | 1.0.0 |
| **Status** | ✅ Complete |
| **Author** |Ishan Jain |
| **Last Updated** | August 2026 |
| **Tech Stack** | Python · LangChain · FAISS · Gemini · Streamlit |

---

## 2. Executive Summary

PDF ChatBot is an AI-powered, Retrieval-Augmented Generation (RAG) application that enables users to **have natural conversations with PDF documents**. Instead of manually reading and searching through large documents, users can ask plain-English questions and receive accurate, context-grounded answers with full source citations.

The system is built entirely on open-source components (FAISS, SentenceTransformers) combined with Google Gemini as the LLM backbone, making it cost-effective and reproducible.

---

## 3. Problem Statement

### The Core Problem
> **PDFs are static, unsearchable knowledge silos.** Users waste significant time manually skimming documents to find specific information.

### Pain Points
- 📄 **Large documents** — Lab manuals, textbooks, and reports can span 50–500+ pages
- 🔍 **Ctrl+F is insufficient** — Keyword search misses semantic context
- 🧠 **No memory** — Users must re-read context on every session
- 📌 **No citations** — Traditional chatbots don't tell you *where* the answer came from
- 💬 **Not conversational** — PDFs don't understand follow-up questions

---

## 4. Goals & Non-Goals

### ✅ Goals
- Allow users to upload any PDF and immediately chat with it
- Return answers grounded strictly in document content (no hallucination)
- Display source citations (document name, page number, chunk ID) with every answer
- Support multi-turn conversations with memory of prior exchanges
- Run on a standard laptop without GPU (CPU-only FAISS + local embeddings)
- Deploy as a single-command Streamlit app

### ❌ Non-Goals (v1.0)
- Real-time document collaboration / multi-user support
- OCR for scanned / image-only PDFs
- Support for non-PDF formats (Word, Excel, PowerPoint)
- Cloud deployment or containerisation (Docker/K8s)
- Fine-tuning the embedding model on domain data
- Authentication / user accounts

---

## 5. Target Users

| Persona | Description | Primary Use |
|---------|-------------|-------------|
| **Student** | B.Tech / M.Tech student with lab manuals, notes | Quick answers from course material |
| **Researcher** | Academic reading papers and literature | Summarise & cross-reference papers |
| **Engineer** | Developer reading API / system docs | Find specific configurations |
| **Analyst** | Business user with reports & contracts | Extract data, summarise findings |

---

## 6. Functional Requirements

### 6.1 PDF Ingestion
| ID | Requirement | Priority |
|----|-------------|----------|
| F1 | System shall accept one or more PDF files via file uploader | P0 |
| F2 | System shall also load PDFs from the `dataset/` directory | P0 |
| F3 | System shall extract full text from all pages using PyMuPDF | P0 |
| F4 | System shall display extraction progress to the user | P1 |
| F5 | System shall handle empty / blank pages gracefully | P1 |

### 6.2 Text Processing
| ID | Requirement | Priority |
|----|-------------|----------|
| F6 | System shall clean extracted text (remove extra whitespace, tabs) | P0 |
| F7 | System shall chunk text into 1000-character segments with 200-character overlap | P0 |
| F8 | System shall attach metadata (document name, page, chunk ID) to every chunk | P0 |

### 6.3 Embeddings & Vector Store
| ID | Requirement | Priority |
|----|-------------|----------|
| F9 | System shall embed all chunks using `sentence-transformers/all-MiniLM-L6-v2` | P0 |
| F10 | System shall persist the FAISS index to `vectorstore/faiss_index/` | P0 |
| F11 | System shall auto-load existing FAISS index on startup if available | P1 |

### 6.4 RAG Pipeline
| ID | Requirement | Priority |
|----|-------------|----------|
| F12 | System shall retrieve the top-4 most relevant chunks per query | P0 |
| F13 | System shall inject retrieved context into the LLM prompt | P0 |
| F14 | System shall instruct the LLM to answer only from provided context | P0 |
| F15 | System shall return source document citations with every answer | P0 |

### 6.5 Conversational Memory
| ID | Requirement | Priority |
|----|-------------|----------|
| F16 | System shall maintain a rolling conversation history (last 6 exchanges) | P0 |
| F17 | System shall inject history into the prompt for follow-up questions | P0 |
| F18 | System shall allow the user to clear conversation history | P1 |

### 6.6 API Key & Model Management
| ID | Requirement | Priority |
|----|-------------|----------|
| F19 | System shall accept Google API key via `.env` file | P0 |
| F20 | System shall accept Google API key via sidebar input (overrides `.env`) | P0 |
| F21 | System shall validate key format before making any API calls | P0 |
| F22 | System shall attempt multiple Gemini models in fallback order | P0 |
| F23 | System shall display user-friendly messages for quota / model errors | P0 |

### 6.7 User Interface
| ID | Requirement | Priority |
|----|-------------|----------|
| F24 | System shall display a professional dark-themed chat interface | P0 |
| F25 | System shall show a typing indicator while the LLM generates a response | P1 |
| F26 | System shall show a welcome screen with setup instructions when not ready | P1 |
| F27 | System shall show real-time indexing progress bar | P1 |
| F28 | System shall display document stats in the sidebar | P2 |

---

## 7. Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| **Performance** | Indexing 50-page PDF completes in < 60 seconds on CPU |
| **Latency** | LLM response returned within 10 seconds (network-dependent) |
| **Accuracy** | Answers must be grounded in retrieved chunks (no confabulation) |
| **Reliability** | App degrades gracefully on API quota errors |
| **Security** | API keys never logged, stored only in session state |
| **Portability** | Runs on Windows/macOS/Linux with Python 3.9+ |
| **Maintainability** | Each phase isolated; new models added by editing a 4-item list |

---

## 8. User Stories

```
As a student,
I want to upload my lab manual PDF and ask "What is covered in Week 3?",
So that I don't have to manually skim 46 pages.

As a researcher,
I want the chatbot to remember what I asked previously,
So that I can ask "Can you expand on the second point?" without repeating context.

As a developer,
I want to see which page and document each answer comes from,
So that I can verify the information is correct.

As a first-time user,
I want clear setup instructions in the UI,
So that I know exactly what to do if nothing is working yet.
```

---

## 9. Acceptance Criteria

| Criterion | Test |
|-----------|------|
| PDF uploads and indexes without error | Upload `CN (4).pdf`, click Index — FAISS saved |
| Answer contains document content | Ask "What practicals are in week 1?" — returns relevant content |
| Source citation shown | Answer UI shows document name + page number |
| Follow-up works | Ask "Expand on the first one" — references prior answer |
| Quota error is friendly | With exhausted key — shows "Wait 24h" message, not stack trace |
| Bad API key detected | Enter `AQ.xxx` key — immediate format warning shown |

---

## 10. Success Metrics

| Metric | Target |
|--------|--------|
| Time-to-first-answer | < 30s from upload to indexed |
| Answer relevance | Top-4 chunks contain answer for 90% of reasonable questions |
| Error rate | Zero unhandled exceptions for documented error cases |
| UI responsiveness | Page renders in < 2s on local network |

---

## 11. Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| `streamlit` | ≥ 1.32 | UI framework |
| `langchain` | ≥ 0.3 | Orchestration |
| `langchain-google-genai` | ≥ 2.0 | Gemini LLM |
| `langchain-huggingface` | ≥ 0.1 | Embedding wrapper |
| `faiss-cpu` | ≥ 1.8 | Vector search |
| `sentence-transformers` | ≥ 3.0 | Embedding model |
| `pymupdf` | ≥ 1.23 | PDF text extraction |
| `python-dotenv` | ≥ 1.0 | Env var loading |

---

## 12. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Gemini free-tier quota exhausted | High | High | Fallback model list; friendly UI error; billing upgrade docs |
| Gemini model deprecated | Medium | High | Stable model names (not `-latest` aliases); fallback list |
| PDF contains only images (no text) | Medium | High | Warn user; (OCR planned for v2) |
| Large PDFs slow indexing | Low | Medium | Progress bar; chunking keeps memory usage bounded |
| API key accidentally committed | Low | Critical | `.gitignore` excludes `.env`; sidebar input as alternative |

---

*PDF ChatBot PRD v1.0 — August 2026*
