# filepath: ai-interview-assistant/app/config.py

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

EVALUATION_FILE = BASE_DIR / "data" / "evaluation_report.json"
FEEDBACK_FILE = BASE_DIR / "data" / "feedback_report.json"

PAGE_TITLE = "AI Interview Assistant"
PAGE_ICON = "🤖"
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"