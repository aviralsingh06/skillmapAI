import json
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _get_secret(key, default=""):
    try:
        return st.secrets.get(key, default)
    except Exception:
        return os.getenv(key, default)


FIREBASE_API_KEY = _get_secret("FIREBASE_API_KEY")
FIREBASE_PROJECT_ID = _get_secret("FIREBASE_PROJECT_ID")

FIREBASE_AUTH_DOMAIN = _get_secret(
    "FIREBASE_AUTH_DOMAIN",
    f"{FIREBASE_PROJECT_ID}.firebaseapp.com"
    if FIREBASE_PROJECT_ID
    else ""
)

FIREBASE_STORAGE_BUCKET = _get_secret(
    "FIREBASE_STORAGE_BUCKET",
    f"{FIREBASE_PROJECT_ID}.appspot.com"
    if FIREBASE_PROJECT_ID
    else ""
)

# Firebase service account JSON from Streamlit Secrets
FIREBASE_SERVICE_ACCOUNT = _get_secret(
    "FIREBASE_SERVICE_ACCOUNT",
    ""
)

FIREBASE_AUTH_URL = (
    "https://identitytoolkit.googleapis.com/v1/accounts"
)

FIREBASE_TOKEN_URL = (
    "https://securetoken.googleapis.com/v1/token"
)


def get_firebase_credentials():
    """Return Firebase credentials dict"""
    if FIREBASE_SERVICE_ACCOUNT:
        try:
            return json.loads(FIREBASE_SERVICE_ACCOUNT)
        except json.JSONDecodeError:
            return None

    # fallback for local development
    local_path = PROJECT_ROOT / "firebase-service-account.json"
    if local_path.exists():
        with open(local_path, "r", encoding="utf-8") as f:
            return json.load(f)

    return None


def is_firebase_configured():
    return bool(
        FIREBASE_API_KEY
        and FIREBASE_PROJECT_ID
        and get_firebase_credentials()
    )