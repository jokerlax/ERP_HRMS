import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/hrms")

def run_script(conn, filename):
    with open(filename, 'r', encoding='utf-8') as f:
        sql = f.read()
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()
    print(f"Executed {filename}")

if __name__ == "__main__":
    try:
        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor() as cur:
            cur.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
        conn.commit()
        print("Database reset.")

        run_script(conn, "hrms_schema.sql")
        run_script(conn, "seed.sql")
        conn.close()
    except Exception as e:
        print("Error:", e)
