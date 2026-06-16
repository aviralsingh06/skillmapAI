from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import quote_plus
import streamlit as st
import os

load_dotenv()

# Database secrets
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

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_timeout=30,
    connect_args={
        "sslmode": "require",
        "connect_timeout": 10
    }
)


def save_resume(file_name, parsed_text):

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
        with engine.begin() as connection:

            result = connection.execute(
                query,
                {
                    "file_name": str(file_name),
                    "parsed_text": str(parsed_text)
                }
            )

            resume_id = result.scalar()

            print(
                f"Resume saved successfully: "
                f"{resume_id}"
            )

            return resume_id

    except Exception as e:
        print(f"Database save error: {e}")
        return None


def save_extracted_skills(
    resume_id,
    skills
):

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