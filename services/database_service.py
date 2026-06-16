import os
from urllib.parse import quote_plus

import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

# -------------------------------
# DATABASE CONFIG
# -------------------------------

DB_USER = st.secrets.get("DB_USER", "")
DB_HOST = st.secrets.get("DB_HOST", "")
DB_PORT = st.secrets.get("DB_PORT", "5432")
DB_NAME = st.secrets.get("DB_NAME", "")
DB_PASSWORD = quote_plus(
    st.secrets.get("DB_PASSWORD", "")
)

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    f"?sslmode=require"
)

# -------------------------------
# DATABASE ENGINE
# -------------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10,
    connect_args={
        "sslmode": "require",
        "connect_timeout": 15
    }
)


# -------------------------------
# SAVE RESUME
# -------------------------------

def save_resume(file_name, parsed_text):
    """
    Save uploaded resume
    to PostgreSQL
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

    try:
        with engine.connect() as connection:

            result = connection.execute(
                query,
                {
                    "file_name": file_name,
                    "parsed_text": parsed_text
                }
            )

            connection.commit()

            return result.scalar()

    except Exception as e:
        print(
            f"Database save error: {e}"
        )

        # Don't crash app
        return None


# -------------------------------
# SAVE EXTRACTED SKILLS
# -------------------------------

def save_extracted_skills(
    resume_id,
    skills
):
    """
    Save extracted skills
    """

    if resume_id is None:
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

    try:
        with engine.connect() as connection:

            for skill in skills:
                connection.execute(
                    query,
                    {
                        "resume_id": resume_id,
                        "skill_name": skill
                    }
                )

            connection.commit()

    except Exception as e:
        print(
            f"Skill save error: {e}"
        )

