# ==========================================================
# app.py  –  Fake News Detection  |  Streamlit Web App
# ==========================================================

import os
import sys

import streamlit as st

# Make src/ importable regardless of where the app is launched from
APP_DIR  = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(APP_DIR)
SRC_DIR  = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from predict import predict  # noqa: E402  (import after path fix)

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Custom CSS  –  dark glassmorphism aesthetic
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* ── Google font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Background gradient ── */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }

    /* ── Hero header ── */
    .hero {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem;
    }
    .hero h1 {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .hero p {
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 400;
        margin-top: 0;
    }

    /* ── Glass card ── */
    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(16px);
        border-radius: 1.2rem;
        padding: 2rem 2.5rem;
        margin: 1.5rem auto;
        max-width: 780px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    }

    /* ── Result badge ── */
    .result-badge {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 1rem;
        padding: 2rem 1.5rem;
        margin: 1.5rem 0 0.5rem;
        animation: fadeIn 0.5s ease;
    }
    .result-badge.fake {
        background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(220,38,38,0.08));
        border: 1px solid rgba(239,68,68,0.4);
    }
    .result-badge.real {
        background: linear-gradient(135deg, rgba(52,211,153,0.15), rgba(16,185,129,0.08));
        border: 1px solid rgba(52,211,153,0.4);
    }
    .result-badge .icon { font-size: 3.5rem; margin-bottom: 0.4rem; }
    .result-badge .verdict {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: 0.08em;
    }
    .result-badge.fake .verdict { color: #f87171; }
    .result-badge.real .verdict { color: #34d399; }
    .result-badge .conf {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-top: 0.2rem;
    }

    /* ── Textarea styling ── */
    textarea {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.14) !important;
        border-radius: 0.75rem !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.97rem !important;
        resize: vertical;
    }
    textarea::placeholder { color: #64748b !important; }

    /* ── Primary button ── */
    .stButton > button {
        width: 100%;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 700;
        border: none;
        border-radius: 0.75rem;
        background: linear-gradient(135deg, #7c3aed, #4f46e5);
        color: #fff;
        cursor: pointer;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        letter-spacing: 0.04em;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(124,58,237,0.45);
    }
    .stButton > button:active { transform: translateY(0); }

    /* ── Stats row ── */
    .stats-row {
        display: flex;
        gap: 1rem;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 1rem;
    }
    .stat-chip {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 0.6rem;
        padding: 0.55rem 1.1rem;
        text-align: center;
        font-size: 0.85rem;
        color: #cbd5e1;
    }
    .stat-chip span {
        display: block;
        font-size: 1.1rem;
        font-weight: 700;
        color: #a78bfa;
    }

    /* ── Confidence bar ── */
    .conf-bar-wrap { margin-top: 1rem; }
    .conf-bar-label {
        font-size: 0.82rem;
        color: #94a3b8;
        margin-bottom: 0.3rem;
    }
    .conf-bar-bg {
        background: rgba(255,255,255,0.08);
        border-radius: 999px;
        height: 10px;
        overflow: hidden;
    }
    .conf-bar-fill {
        height: 100%;
        border-radius: 999px;
        transition: width 0.6s ease;
    }
    .conf-bar-fill.fake { background: linear-gradient(90deg, #ef4444, #f97316); }
    .conf-bar-fill.real { background: linear-gradient(90deg, #10b981, #34d399); }

    /* ── Footer ── */
    .footer {
        text-align: center;
        color: #475569;
        font-size: 0.78rem;
        padding: 2.5rem 0 1rem;
    }

    /* ── Fade-in animation ── */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ── Hide default Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Hero header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🔍 Fake News Detector</h1>
        <p>Paste any news article below and let AI decide — Real or Fake.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Stats chips
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="stats-row">
        <div class="stat-chip"><span>~44 K</span>Training articles</div>
        <div class="stat-chip"><span>TF-IDF</span>Vectorisation</div>
        <div class="stat-chip"><span>6</span>Models compared</div>
        <div class="stat-chip"><span>≥ 98 %</span>Best accuracy</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Clear callback – must be defined BEFORE the widget is rendered.
# Streamlit ≥1.36 forbids writing to a widget key after it is instantiated;
# on_click callbacks run before the next rerun so the key is still free.
# ---------------------------------------------------------------------------
def _clear_input():
    st.session_state["article_input"] = ""

# ---------------------------------------------------------------------------
# Input card  –  use a container with CSS class injection
# ---------------------------------------------------------------------------
# We style the container via CSS; DO NOT wrap native widgets in raw HTML <div>
# (that pattern breaks Streamlit ≥1.36 component JS hydration).
st.markdown("""
<style>
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(16px);
    border-radius: 1.2rem;
    padding: 1rem 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}
</style>
""", unsafe_allow_html=True)

with st.container(border=True):
    article_text = st.text_area(
        label="Article Text",
        placeholder="Paste the full news article text here…",
        height=260,
        label_visibility="collapsed",
        key="article_input",
    )

    col_left, col_right = st.columns([3, 1])
    with col_left:
        analyse_btn = st.button("⚡ Analyse Article", key="analyse_btn")
    with col_right:
        clear_btn = st.button("🗑 Clear", key="clear_btn", on_click=_clear_input)

# ---------------------------------------------------------------------------
# Prediction
# ---------------------------------------------------------------------------
if analyse_btn:
    text = (article_text or "").strip()
    if not text:
        st.warning("⚠️  Please paste some article text before analysing.")
    else:
        with st.spinner("Analysing…"):
            try:
                result = predict(text)
            except FileNotFoundError as exc:
                st.error(str(exc))
                st.stop()

        label      = result["prediction"]        # "FAKE" | "REAL"
        confidence = result["confidence"]        # float | None
        css_cls    = label.lower()               # "fake" | "real"
        icon       = "🚨" if css_cls == "fake" else "✅"

        conf_html = ""
        if confidence is not None:
            bar_fill = f'<div class="conf-bar-fill {css_cls}" style="width:{confidence:.1f}%"></div>'
            conf_html = f"""
            <div class="conf-bar-wrap">
                <div class="conf-bar-label">Model confidence — {confidence:.1f} %</div>
                <div class="conf-bar-bg">{bar_fill}</div>
            </div>
            """

        st.markdown(
            f"""
            <div class="glass-card" style="max-width:780px">
                <div class="result-badge {css_cls}">
                    <div class="icon">{icon}</div>
                    <div class="verdict">{label} NEWS</div>
                    <div class="conf">
                        {"Confidence: " + f"{confidence:.1f} %" if confidence is not None else ""}
                    </div>
                </div>
                {conf_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Expandable detail
        with st.expander("📋 What does this mean?", expanded=False):
            if css_cls == "fake":
                st.markdown(
                    """
                    **🚨 Fake News** — The model believes this article contains
                    misinformation or fabricated content.  
                    Always cross-check with reputable sources before sharing.
                    """
                )
            else:
                st.markdown(
                    """
                    **✅ Real News** — The model considers this article likely
                    authentic based on patterns learned from verified sources.  
                    Still good practice to verify with original reporting.
                    """
                )

# ---------------------------------------------------------------------------
# How it works sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ℹ️ How It Works")
    st.markdown(
        """
        1. **Pre-processing** – lowercase, remove URLs/HTML/digits/punctuation,
           strip stop-words, apply Porter stemming.
        2. **TF-IDF** – converts text into a 5 000-feature sparse matrix.
        3. **ML Model** – the best-performing classifier (chosen automatically
           during training) predicts the label.
        4. **Confidence** – derived from `predict_proba` or the decision
           function (sigmoid-scaled).
        """
    )
    st.markdown("---")
    st.markdown("## 📂 Project Layout")
    st.code(
        """\
Fake_News_Detection/
├── dataset/
│   ├── Fake.csv
│   ├── True.csv
│   └── processed_fake_news.csv
├── model/
│   ├── fake_news_model.pkl
│   └── tfidf_vectorizer.pkl
├── charts/
├── src/
│   ├── preprocessing.py
│   ├── train.py
│   └── predict.py
└── app/
    └── app.py          ← you are here
""",
        language="text",
    )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="footer">Fake News Detection · Built with Streamlit & Scikit-Learn</div>',
    unsafe_allow_html=True,
)
