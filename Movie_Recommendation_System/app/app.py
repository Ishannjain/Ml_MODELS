# ==========================================================
# MOVIE RECOMMENDATION SYSTEM
# app/app.py  –  Legacy entry point
# ──────────────────────────────────────────────────────────
# This file forwards to the root app.py.
# For deployment, use the ROOT app.py directly.
# ==========================================================

import os, sys

# Go up one level to the project root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_APP = os.path.join(ROOT, "app.py")

# Add root to path so relative imports work
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Execute root app.py in this process
exec(open(ROOT_APP, encoding="utf-8").read())