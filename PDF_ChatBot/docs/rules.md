# Development Rules & Standards
# PDF ChatBot — Engineering Guidelines

---

## 1. Purpose

This document defines the coding standards, architectural rules, and operational guidelines for the PDF ChatBot project. All contributors must follow these rules to maintain code quality, security, and consistency.

---

## 2. Project Rules

### 2.1 Golden Rules

```
R1. Never commit secrets         — .env must always be in .gitignore
R2. Fail gracefully              — every API call must have try/except
R3. Stay grounded                — LLM must only answer from context
R4. Validate before calling      — check API key format before any request
R5. Cache aggressively           — use @st.cache_resource for heavy loads
R6. Keep phases decoupled        — each phase must work independently
R7. Document everything          — every function needs a docstring
```

---

## 3. Code Style

### 3.1 Python Standards

```python
# ✅ CORRECT — Descriptive names, type hints, docstring
def validate_api_key_format(key: str) -> tuple[bool, str]:
    """
    Validates the format of a Gemini API key.

    Args:
        key: The API key string to validate.

    Returns:
        Tuple of (is_valid: bool, message: str).
    """
    key = key.strip()
    if not key:
        return False, "API key is empty."
    if not key.startswith("AIza"):
        return False, "Key must start with 'AIza'."
    if len(key) < 30:
        return False, "Key is too short."
    return True, "Format looks valid."


# ❌ INCORRECT — No hints, no docstring, cryptic name
def chk(k):
    return k.startswith("AIza") and len(k) > 30
```

### 3.2 Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Variables | `snake_case` | `vector_db`, `chunk_df` |
| Functions | `snake_case` | `load_vectordb()`, `get_answer()` |
| Constants | `UPPER_SNAKE` | `CUSTOM_CSS`, `MODEL_LIST` |
| Classes | `PascalCase` | (not used in v1.0) |
| Files | `snake_case.py` | `app.py` |
| Notebooks | `snake_case.ipynb` | `chatbot.ipynb` |

### 3.3 Import Order

```python
# 1. Standard library
import os
import re
import time
from pathlib import Path

# 2. Third-party libraries
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# 3. LangChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI

# 4. Local modules (if any)
# from utils import helper_fn
```

### 3.4 Section Headers

All major code sections must use 60-char separator comments:

```python
# ==========================================================
# Section Name
# ==========================================================
```

Sub-sections use 58-char separators:

```python
# ── Sub-section Name ──────────────────────────────────────
```

---

## 4. Error Handling Rules

### 4.1 API Calls Must Be Wrapped

```python
# ✅ CORRECT — Classify and handle every error type
try:
    llm.invoke("test")
except Exception as exc:
    err = str(exc)
    if "RESOURCE_EXHAUSTED" in err or "429" in err:
        # Quota exhausted — user-friendly message
        st.error("⏳ Free-tier quota exhausted. Wait 24h or upgrade billing.")
    elif "NOT_FOUND" in err or "404" in err:
        # Deprecated model — try next in fallback list
        continue
    elif "API_KEY_INVALID" in err or "401" in err:
        # Bad key — stop immediately, no point retrying
        st.error("❌ Invalid API key.")
        break
    else:
        # Unknown error — show full message for debugging
        st.error(f"❌ Unexpected error: {exc}")

# ❌ INCORRECT — Swallow errors silently
try:
    llm.invoke("test")
except Exception:
    pass
```

### 4.2 Never Show Raw Stack Traces to Users

```python
# ✅ CORRECT — Show in expander, not directly
st.error("Connection failed.")
with st.expander("Error details"):
    st.code(str(e), language="text")

# ❌ INCORRECT — Raw traceback in UI
st.error(traceback.format_exc())
```

### 4.3 Validate All User Inputs

```python
# ✅ CORRECT — Validate before processing
api_key = st.text_input("API Key")
is_valid, msg = validate_api_key_format(api_key)
if not is_valid:
    st.warning(f"⚠️ {msg}")
    st.stop()

# ❌ INCORRECT — Pass unvalidated input to API
llm = ChatGoogleGenerativeAI(google_api_key=api_key)
```

---

## 5. Security Rules

### 5.1 API Keys

```
RULE: Never hardcode API keys in source code.
RULE: Never log API keys (no print(api_key), no logging.info(key)).
RULE: Never store API keys in session storage or localStorage.
RULE: Always load keys from environment variables or user input.
RULE: Validate key format BEFORE making any API request.
```

```python
# ✅ CORRECT
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

# ❌ INCORRECT — Hardcoded (NEVER DO THIS)
GOOGLE_API_KEY = "AIzaSyABCDEFGHIJKLMNOP12345678"
```

### 5.2 `.env` File

The `.env` file must:
- Always be in `.gitignore`
- Never be committed to version control
- Contain only environment-specific configuration

```
# .env template (safe to commit as .env.example)
GOOGLE_API_KEY=your_key_here
```

### 5.3 FAISS Deserialization

```python
# The allow_dangerous_deserialization flag is required by LangChain
# ONLY use it on FAISS indexes YOU generated — not on external files.
vector_db = FAISS.load_local(
    "vectorstore/faiss_index",
    embedding_model,
    allow_dangerous_deserialization=True  # ← only safe for own indexes
)
```

---

## 6. LangChain Rules

### 6.1 Use Modern Imports

```python
# ✅ CORRECT — Use split packages (LangChain 0.3+)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

# ❌ INCORRECT — Legacy monolith imports (deprecated)
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
```

### 6.2 Import Fallback Pattern

When supporting older environments, use try/except:

```python
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings
```

### 6.3 Prompt Templates

Always use `ChatPromptTemplate` — never f-string the prompt directly:

```python
# ✅ CORRECT — Template with named slots
prompt = ChatPromptTemplate.from_template(
    "Context: {context}\n\nQuestion: {question}\n\nAnswer:"
)
formatted = prompt.format(context=ctx, question=q)
response = llm.invoke(formatted)

# ❌ INCORRECT — Direct f-string (no reuse, no validation)
response = llm.invoke(f"Context: {ctx}\n\nQuestion: {q}\n\nAnswer:")
```

---

## 7. Gemini Model Rules

### 7.1 Approved Model Names

```python
# ✅ APPROVED — Stable model names as of August 2026
MODEL_LIST = [
    "gemini-2.0-flash",       # Primary
    "gemini-2.0-flash-lite",  # Fallback 1
    "gemini-1.5-flash",       # Fallback 2 (NOT "gemini-1.5-flash-latest")
    "gemini-1.5-pro",         # Fallback 3
]

# ❌ BANNED — Deprecated aliases (return 404)
BANNED_MODELS = [
    "gemini-1.5-flash-latest",  # 404 — use "gemini-1.5-flash"
    "gemini-2.5-flash",         # 404 — not available to new users
    "gemini-pro",               # 404 — use "gemini-1.5-pro"
]
```

### 7.2 Model Initialization

Always use `convert_system_message_to_human=True` with Gemini:

```python
# ✅ CORRECT — Gemini requires this for system messages
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=api_key,
    temperature=0.3,
    convert_system_message_to_human=True,  # ← Required for Gemini
)

# ❌ INCORRECT — Will error if system messages are in the prompt
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)
```

### 7.3 Temperature Guidelines

| Use Case | Temperature | Reason |
|----------|-------------|--------|
| Factual Q&A (RAG) | 0.2–0.4 | Accuracy over creativity |
| Summarisation | 0.3–0.5 | Slightly more paraphrase |
| Creative writing | 0.7–1.0 | Not applicable here |

**Default for this project:** `temperature=0.3`

---

## 8. Streamlit Rules

### 8.1 Session State

Always initialise all session state keys at app startup:

```python
# ✅ CORRECT — Centralised initialisation
def init_session():
    defaults = {
        "messages":      [],
        "vector_db":     None,
        "llm":           None,
        "api_key_valid": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()  # Call at top of app

# ❌ INCORRECT — Scattered, uninitialized access
if st.button("Send"):
    st.session_state.messages.append(...)  # KeyError if not initialised
```

### 8.2 Caching

Use `@st.cache_resource` for objects that are expensive to load and shared across sessions:

```python
# ✅ CORRECT — FAISS index loaded once, cached
@st.cache_resource(show_spinner=False)
def load_vectordb(faiss_path: str):
    embedding_model = HuggingFaceEmbeddings(...)
    return FAISS.load_local(faiss_path, embedding_model, ...)

# ❌ INCORRECT — Reloads FAISS on every interaction
def load_vectordb(faiss_path: str):  # No cache decorator
    ...
```

Do NOT cache: LLM objects (they hold user-specific API keys), session-specific state.

### 8.3 `st.rerun()` Usage

Call `st.rerun()` sparingly — only after state-changing actions that require a full re-render:

```python
# ✅ CORRECT — Only after adding message + getting answer
st.session_state.messages.append({"role": "user", "content": query})
# ... get answer ...
st.session_state.messages.append({"role": "assistant", "content": answer})
st.rerun()  # Re-render with new messages

# ❌ INCORRECT — Rerun in a loop (infinite loop)
while not done:
    st.rerun()
```

---

## 9. Notebook Rules

### 9.1 Cell Organisation

Each cell must:
- Have a single, clear purpose
- Start with a section header comment (60-char `=`)
- Print a completion message at the end

```python
# ✅ CORRECT cell structure
# ===========================================================
# PHASE N : TASK NAME
# ===========================================================

# ... code ...

print("=" * 60)
print("Task Name Completed")
print("=" * 60)
print(f"Key Metric: {value}")
```

### 9.2 Defensive Loading

Each phase must check for required variables and reload if missing:

```python
# ✅ CORRECT — Defensive reload
if "df" not in globals():
    df = pd.read_csv("../reports/extracted_text.csv")

if "Clean_Text" not in df.columns:
    df["Clean_Text"] = df["Text"].apply(clean_text)
```

### 9.3 Output Every Phase

Every phase must print a summary of:
- What was generated/processed
- Key numbers (count, size, etc.)
- What the next phase is

---

## 10. Documentation Rules

### 10.1 Function Docstrings

All functions must have Google-style docstrings:

```python
def get_answer(query: str, vector_db, llm, chat_history: list) -> dict:
    """
    Runs the RAG pipeline for a single user query.

    Args:
        query:        The user's question.
        vector_db:    Loaded FAISS vector store.
        llm:          Initialised Gemini LLM instance.
        chat_history: Flat list of alternating [user, ai, user, ai, ...] strings.

    Returns:
        dict with keys:
            "answer"  (str)           — LLM-generated answer
            "sources" (list[Document]) — Retrieved source chunks
    """
```

### 10.2 Inline Comments

Comments explain **why**, not **what**:

```python
# ✅ CORRECT — Explains the design decision
# convert_system_message_to_human is required for Gemini;
# it does not support a separate system role like OpenAI does.
llm = ChatGoogleGenerativeAI(convert_system_message_to_human=True, ...)

# ❌ INCORRECT — States the obvious
# Create an LLM object
llm = ChatGoogleGenerativeAI(...)
```

### 10.3 Docs Folder

All documentation lives in `docs/`:

| File | Audience | Update Frequency |
|------|----------|-----------------|
| `prd.md` | Product / stakeholders | Per feature milestone |
| `phases.md` | Developers | Per phase completion |
| `architecture.md` | Engineers | Per architectural change |
| `rules.md` | All contributors | Per policy update |
| `../README.md` | Public / new users | Per release |

---

## 11. Git Rules

### 11.1 `.gitignore` Must Include

```gitignore
.env                        # API keys
venv/                       # Virtual environment
__pycache__/                # Python cache
*.pyc                       # Compiled bytecode
vectorstore/faiss_index/    # Regenerable from PDFs
reports/                    # Auto-generated CSVs
.ipynb_checkpoints/         # Jupyter temp files
```

### 11.2 Commit Message Format

```
<type>: <short description>

Types:
  feat:   New feature
  fix:    Bug fix
  docs:   Documentation only
  style:  Formatting, no logic change
  refactor: Code restructure, no feature change
  chore:  Maintenance (deps, gitignore, etc.)

Examples:
  feat: add conversational memory to RAG chain
  fix: remove deprecated gemini-1.5-flash-latest model
  docs: add architecture.md with system diagram
  chore: update requirements.txt with version pins
```

### 11.3 Branch Naming

```
main          ← production-ready code only
dev           ← active development
feature/<name>  ← new features
fix/<issue>     ← bug fixes
docs/<name>     ← documentation updates
```

---

## 12. Testing Checklist

Before marking any phase complete:

```
□ Code runs without errors from a clean kernel/restart
□ All error cases produce friendly messages (not stack traces)
□ API key is not hardcoded anywhere
□ .env is in .gitignore and not committed
□ All functions have docstrings
□ Section headers are present and consistent
□ Phase summary printed with correct stats
□ Deliverable files exist and have correct schema
```

---

## 13. Dependency Management

### 13.1 Adding New Dependencies

1. Install in the venv: `pip install package-name`
2. Add to `requirements.txt` with a minimum version:
   ```
   package-name>=X.Y.0
   ```
3. Test that `pip install -r requirements.txt` installs cleanly on a fresh venv
4. Update `docs/architecture.md` if it's a key dependency

### 13.2 Updating Existing Dependencies

Do NOT pin to an exact version unless there's a known incompatibility:

```
# ✅ CORRECT — Lower bound only
langchain>=0.3.0

# ❌ INCORRECT — Too restrictive (breaks with patches)
langchain==0.3.0

# ❌ INCORRECT — No bound (may break with major versions)
langchain
```

---

*PDF ChatBot — rules.md v1.0 — August 2026*
