import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def init_db():
    """Initializes CockroachDB tables and vector indexes from schema.sql."""
    if not DATABASE_URL:
        print("❌ DATABASE_URL missing from environment variables.")
        return

    print("🔌 Connecting to CockroachDB Cloud...")
    try:
        with psycopg.connect(DATABASE_URL) as conn:
            schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
            with open(schema_path, "r") as f:
                schema_sql = f.read()
            
            with conn.cursor() as cur:
                cur.execute(schema_sql)
                conn.commit()
            print("✅ CockroachDB Schema & Distributed Vector Index created successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize CockroachDB: {str(e)}")

if __name__ == "__main__":
    init_db()
