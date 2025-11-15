"""Simple DB connectivity tester for MycoScan.
Reads `DATABASE_URL` from environment (or .env) and prints DB version and tables.

Run:
    python tools/test_mysql.py
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

load_dotenv()

def main():
    url = os.getenv("DATABASE_URL")
    if not url:
        print("DATABASE_URL not set. Create a .env or set the env var first.")
        return

    print(f"Using DATABASE_URL={url}")

    try:
        engine = create_engine(url, future=True)
        with engine.connect() as conn:
            version = conn.execute(text("SELECT VERSION()")).scalar()
            insp = inspect(conn)
            tables = insp.get_table_names()
            print(f"Connected to DB. Version: {version}")
            print(f"Tables: {tables}")
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == '__main__':
    main()
