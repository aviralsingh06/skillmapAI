from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from dotenv import load_dotenv
from urllib.parse import quote_plus
import time
import streamlit as st
import os

load_dotenv()

# ---------------------------------
# DATABASE SECRETS
# Reads from Streamlit secrets first,
# falls back to environment variables.
# ---------------------------------

def _get_secret(key, default=""):
    try:
        val = st.secrets.get(key, None)
        if val is not None:
            return val
    except Exception:
        pass
    return os.getenv(key, default)


DB_USER = _get_secret("DB_USER", "")
DB_HOST = _get_secret("DB_HOST", "")
DB_PORT = _get_secret("DB_PORT", "5432")
DB_NAME = _get_secret("DB_NAME", "")
_raw_password = _get_secret("DB_PASSWORD", "")

# URL-encode the password to handle special characters (e.g. @, !, #)
DB_PASSWORD = quote_plus(_raw_password) if _raw_password else ""

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    f"?sslmode=require"
)

# ---------------------------------
# ENGINE — created lazily so that a
# bad DATABASE_URL doesn't crash the
# app at import time.
# ---------------------------------

_engine = None


def _get_engine():
    """
    Return the shared SQLAlchemy engine,
    creating it on the first call.
    Returns None if the DB is not configured.
    """
    global _engine

    if _engine is not None:
        return _engine

    if not DB_USER or not DB_HOST or not DB_NAME:
        print("Database not configured — skipping engine creation.")
        return None

    try:
        _engine = create_engine(
            DATABASE_URL,
            # Verify connections before use (avoids stale-connection errors)
            pool_pre_ping=True,
            # Recycle connections every 5 minutes (prevents Neon idle timeouts)
            pool_recycle=300,
            # Wait up to 30 s for a connection from the pool
            pool_timeout=30,
            # Keep a small pool; Neon free tier has connection limits
            pool_size=2,
            max_overflow=3,
            connect_args={
                "sslmode": "require",
                "connect_timeout": 10,
            }
        )
        return _engine

    except Exception as e:
        print(f"Engine creation error: {e}")
        return None


# ---------------------------------
# INTERNAL HELPER — retry wrapper
# Retries up to `retries` times with
# an exponential back-off before giving
# up and returning None.
# ---------------------------------

def _execute_with_retry(query, params, retries=2, delay=1.0):
    """
    Execute a write query with retry logic.
    Returns the scalar result on success, None on failure.
    """
    engine = _get_engine()
    if engine is None:
        return None

    last_error = None
    for attempt in range(retries + 1):
        try:
            with engine.begin() as connection:
                result = connection.execute(query, params)
                # Only scalar() when the query returns rows (INSERT … RETURNING)
                try:
                    return result.scalar()
                except Exception:
                    return True  # Non-returning statements (INSERT without RETURNING)

        except (OperationalError, SQLAlchemyError) as e:
            last_error = e
            print(f"DB attempt {attempt + 1} failed: {e}")
            if attempt < retries:
                time.sleep(delay * (attempt + 1))

    print(f"All DB retries exhausted. Last error: {last_error}")
    return None


# ---------------------------------
# PUBLIC API
# ---------------------------------

def save_resume(file_name, parsed_text):
    """
    Save a resume record and return the new resume_id.
    Returns None if the database is unavailable.
    """
    query = text("""
        INSERT INTO resumes (
            file_name,
            parsed_text
        )
        VALUES (
            :file_name,
            :parsed_text
        )
        RETURNING resume_id
    """)

    resume_id = _execute_with_retry(
        query,
        {
            "file_name": str(file_name),
            "parsed_text": str(parsed_text)
        }
    )

    if resume_id is not None:
        print(f"Resume saved successfully: {resume_id}")
    else:
        print("Resume could not be saved to the database.")

    return resume_id


def save_extracted_skills(resume_id, skills):
    """
    Save extracted skills for a given resume_id.
    Silently skips if resume_id is None or skills is empty.
    """
    if not resume_id or not skills:
        return

    query = text("""
        INSERT INTO extracted_skills (
            resume_id,
            skill_name
        )
        VALUES (
            :resume_id,
            :skill_name
        )
    """)

    engine = _get_engine()
    if engine is None:
        return

    try:
        with engine.begin() as connection:
            for skill in skills:
                connection.execute(
                    query,
                    {
                        "resume_id": resume_id,
                        "skill_name": str(skill)
                    }
                )
    except Exception as e:
        print(f"Skills save error: {e}")