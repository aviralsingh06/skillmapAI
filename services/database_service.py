from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


def save_resume(file_name, parsed_text):
    """
    Save uploaded resume to PostgreSQL
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


def save_extracted_skills(
    resume_id,
    skills
):
    """
    Save extracted skills
    """

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