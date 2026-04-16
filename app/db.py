# Database connection helper
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Return a new psycopg connection using DATABASE_URL from .env."""
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError(
            "DATABASE_URL is not set. Copy .env.example to .env and fill it in."
        )
    return psycopg.connect(db_url)