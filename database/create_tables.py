from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

DB_USER = "postgres"
DB_PASSWORD = quote_plus("Aviral66605@")
DB_NAME = "skillmap_ai"

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@127.0.0.1:5432/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

with open("database/schema.sql", "r") as file:
    sql_script = file.read()

with engine.connect() as connection:
    connection.execute(text(sql_script))
    connection.commit()

print("✅ Database tables created successfully!")