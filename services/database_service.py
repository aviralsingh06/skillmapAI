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
    """)

    with engine.connect() as connection:
        connection.execute(
            query,
            {
                "file_name": file_name,
                "parsed_text": parsed_text
            }
        )
        connection.commit()