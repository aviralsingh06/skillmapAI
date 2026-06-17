import json
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Project root is the directory that contains this file (firebase_config.py).
# When deployed to Streamlit Cloud the layout is flat (no parent directory),
# so we resolve relative to __file__ without going up a level.
PROJECT_ROOT = Path(__file__).resolve().parent


def _get_secret(key, default=""):
    """
    Read a secret from st.secrets first, then fall back to os.getenv.
    Never raises — always returns a string.
    """
    try:
        val = st.secrets.get(key, None)
        if val is not None:
            return val
    except Exception:
        pass
    return os.getenv(key, default)


FIREBASE_API_KEY = _get_secret("FIREBASE_API_KEY")
FIREBASE_PROJECT_ID = _get_secret("FIREBASE_PROJECT_ID")

FIREBASE_AUTH_DOMAIN = _get_secret(
    "FIREBASE_AUTH_DOMAIN",
    f"{FIREBASE_PROJECT_ID}.firebaseapp.com" if FIREBASE_PROJECT_ID else ""
)

FIREBASE_STORAGE_BUCKET = _get_secret(
    "FIREBASE_STORAGE_BUCKET",
    f"{FIREBASE_PROJECT_ID}.appspot.com" if FIREBASE_PROJECT_ID else ""
)

FIREBASE_AUTH_URL = (
    "https://identitytoolkit.googleapis.com/v1/accounts"
)

FIREBASE_TOKEN_URL = (
    "https://securetoken.googleapis.com/v1/token"
)


def get_firebase_credentials():
    """
    Return the Firebase service-account dict, or None if unavailable.
    Tries st.secrets first, then looks for the local JSON file.
    """
    # 1. Try Streamlit secrets (production / Streamlit Cloud)
    try:
        service_account = st.secrets.get(
            "FIREBASE_SERVICE_ACCOUNT",
            ""
        )
        if service_account:
            return json.loads(service_account)
    except Exception:
        pass

    # 2. Try local file (development)
    local_path = PROJECT_ROOT / "firebase-service-account.json"
    if local_path.exists():
        try:
            with open(local_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return None


def is_firebase_configured():
    """
    Return True only when all required Firebase config is present.
    """
    return bool(
        FIREBASE_API_KEY
        and FIREBASE_PROJECT_ID
        and get_firebase_credentials()
    )