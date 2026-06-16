from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# Neon database credentials
DB_USER = "neondb_owner"
DB_PASSWORD = quote_plus("npg_56CclADGzZdn")
DB_HOST = "ep-dawn-bar-ahz05xs0.c-3.us-east-1.aws.neon.tech"
DB_PORT = "5432"
DB_NAME = "neondb"

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    f"?sslmode=require"
)

engine = create_engine(DATABASE_URL)

with open("database/schema.sql", "r") as file:
    sql_script = file.read()

with engine.connect() as connection:
    connection.execute(text(sql_script))
    connection.commit()

print("✅ Database tables created successfully!")