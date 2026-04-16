# All database queries for the application.
# Keep SQL in this file. Do not put queries in main.py.
from app.db import get_connection

def ping():
    # Just a test Returns the postgres version string
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            return cur.fetchone()[0]