import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "")
FIREBASE_AUTH_DOMAIN = os.getenv(
    "FIREBASE_AUTH_DOMAIN",
    f"{FIREBASE_PROJECT_ID}.firebaseapp.com" if FIREBASE_PROJECT_ID else ""
)
FIREBASE_STORAGE_BUCKET = os.getenv(
    "FIREBASE_STORAGE_BUCKET",
    f"{FIREBASE_PROJECT_ID}.appspot.com" if FIREBASE_PROJECT_ID else ""
)

_credentials_path = os.getenv(
    "FIREBASE_CREDENTIALS_PATH",
    str(PROJECT_ROOT / "firebase-service-account.json")
)
FIREBASE_CREDENTIALS_PATH = (
    _credentials_path
    if os.path.isabs(_credentials_path)
    else str(PROJECT_ROOT / _credentials_path)
)

FIREBASE_AUTH_URL = (
    "https://identitytoolkit.googleapis.com/v1/accounts"
)
FIREBASE_TOKEN_URL = (
    "https://securetoken.googleapis.com/v1/token"
)


def is_firebase_configured():
    return bool(
        FIREBASE_API_KEY
        and FIREBASE_PROJECT_ID
        and os.path.isfile(FIREBASE_CREDENTIALS_PATH)
    )
