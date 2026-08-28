# 📄 PDF ChatBot — AI-Powered Document Q&A

> **Ask questions about any PDF using Retrieval-Augmented Generation (RAG), FAISS vector search, and Google Gemini.**

---

## 🗺️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         PDF ChatBot                             │
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  PDF     │───▶│ Text     │───▶│ Chunking │───▶│Embeddings│  │
│  │ Loader   │    │Extractor │    │(1000 ch) │    │(MiniLM)  │  │
│  │(PyMuPDF) │    │          │    │          │    │          │  │
│  └──────────┘    └──────────┘    └──────────┘    └────┬─────┘  │
│                                                        │        │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌────▼─────┐  │
│  │  Answer  │◀───│  Gemini  │◀───│  RAG     │◀───│  FAISS   │  │
│  │ + Sources│    │   LLM    │    │ Pipeline │    │ VectorDB │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                                 │
│                    🎨 Streamlit UI (Dark Glass)                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Project Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Project Setup & Library Verification | ✅ Done |
| 2 | PDF Loading & Text Extraction (PyMuPDF) | ✅ Done |
| 3 | Text Cleaning & Chunking (LangChain Splitter) | ✅ Done |
| 4 | Embeddings & FAISS Vector Database | ✅ Done |
| 5 | RAG Pipeline (Gemini LLM + Retrieval) | ✅ Done |
| 6 | Conversational PDF Chatbot (Memory) | ✅ Done |
| 7 | Streamlit Deployment | ✅ Done |
| 8 | Professional Dark Glassmorphism UI | ✅ Done |
| 9 | Documentation | ✅ Done |

---

## 🚀 Quick Start

### 1. Clone / Open the Project

```bash
cd c:\Users\G\Desktop\Languages\AI-MLMODELS\PDF_ChatBot
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get a Valid Gemini API Key

> ⚠️ **Important:** The API key must start with `AIza...`
>
> Standard keys that look like `AQ.Ab8…` are **OAuth tokens, not API keys** and will fail.

1. Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign in with a Google account
3. Click **Create API Key**
4. Copy the key (it starts with `AIza`)

Add it to `.env`:

```env
GOOGLE_API_KEY=AIzaSy...your_actual_key_here
```

*Or simply paste it into the sidebar API key field when the app is running.*

### 5. Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🎮 Usage

### Via Streamlit UI

1. **Paste your Gemini API key** in the sidebar → click **Connect to Gemini**
2. **Upload PDFs** via the sidebar file uploader, or tick *"Also use dataset/ PDFs"*
3. Click **⚡ Index Documents** — wait for embeddings to complete
4. **Ask questions** in the chat box — answers include source citations

### Via Notebook

Open `notebook/chatbot.ipynb` in Jupyter and run cells phase by phase.

---

## 🏗️ Project Structure

```
PDF_ChatBot/
│
├── app.py                      ← Streamlit application (Phases 7 & 8)
├── requirements.txt            ← Python dependencies
├── .env                        ← API keys (never commit this!)
├── .gitignore
│
├── dataset/                    ← Place your PDFs here
│   └── CN (4).pdf
│
├── notebook/
│   └── chatbot.ipynb           ← Development notebook (Phases 1-6)
│
├── vectorstore/
│   └── faiss_index/            ← Auto-generated FAISS index
│       ├── index.faiss
│       └── index.pkl
│
├── reports/                    ← Auto-generated CSV reports
│   ├── extracted_text.csv
│   └── chunked_documents.csv
│
├── model/                      ← (Reserved for local model weights)
└── charts/                     ← (Reserved for visualisation outputs)
```

---

## ⚙️ Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `GOOGLE_API_KEY` | – | Gemini API key from AI Studio |
| `chunk_size` | 1000 | Characters per chunk |
| `chunk_overlap` | 200 | Overlap between chunks |
| `k` (retrieval) | 4 | Number of chunks retrieved per query |
| `temperature` | 0.3 | LLM response randomness |

### Model Fallback Order

The app automatically tries these models in order (stops at first success):

1. `gemini-2.0-flash`
2. `gemini-2.0-flash-lite`
3. `gemini-1.5-flash`
4. `gemini-1.5-pro`

---

## 🛠️ Tech Stack

| Component | Library |
|-----------|---------|
| UI | [Streamlit](https://streamlit.io/) |
| LLM | [Google Gemini](https://ai.google.dev/) via LangChain |
| Embeddings | [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) |
| Vector DB | [FAISS](https://github.com/facebookresearch/faiss) |
| PDF Parsing | [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) |
| Orchestration | [LangChain](https://www.langchain.com/) |
| Env Config | [python-dotenv](https://pypi.org/project/python-dotenv/) |

---

## 🐛 Troubleshooting

### ❌ `RESOURCE_EXHAUSTED` / `429` Error

**Cause:** Free-tier quota exceeded.

**Solutions:**
- Wait 24 hours for the daily quota reset
- Enable [billing on Google Cloud](https://console.cloud.google.com/billing)
- Use a different Google account's API key

### ❌ `NOT_FOUND` / `404` for Model

**Cause:** Deprecated model alias (e.g., `gemini-1.5-flash-latest`, `gemini-2.5-flash`).

**Solution:** Already fixed — the app uses stable model names with automatic fallback.

### ❌ API Key Format Error

**Cause:** Key does not start with `AIza`.

**Solution:** Go to [AI Studio](https://aistudio.google.com/app/apikey) and create a proper API key.

### ❌ `ModuleNotFoundError`

```bash
pip install -r requirements.txt
```

### ❌ FAISS index not found

Run the notebook up to Phase 4, or upload & index a PDF via the Streamlit sidebar.

---

## 📝 Development Notebook

`notebook/chatbot.ipynb` contains all 6 development phases:

| Cell Block | Phase |
|------------|-------|
| Phase 1 | Environment setup, directory creation, library check |
| Phase 2 | PDF loading with PyMuPDF, text extraction |
| Phase 3 | Cleaning, chunking with RecursiveCharacterTextSplitter |
| Phase 4 | Embeddings via HuggingFace, FAISS index build & save |
| Phase 5 | RAG pipeline: Gemini LLM + retriever + prompt template |
| Phase 6 | Conversational memory with `ConversationBufferMemory` |

---

## 🔒 Security Notes

- Never commit `.env` to version control
- The `.gitignore` should exclude `.env` and `vectorstore/`
- API keys entered via the sidebar are stored only in Streamlit session state (not persisted)

---

## 📜 License

MIT License — see `LICENSE` for details.

---

*Built with ❤️ using LangChain · FAISS · Google Gemini · Streamlit*
