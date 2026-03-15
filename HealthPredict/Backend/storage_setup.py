# storage_setup.py
import sqlite3
import os
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")
print("DATABASE PATH:", DB_PATH)
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def db_conn():
    """Use this for safe auto-commit + auto-close in one line."""
    conn = get_conn()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    conn = get_conn()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        request_id TEXT PRIMARY KEY,
        data TEXT,
        status TEXT,
        created_at TEXT,
        retry_count INTEGER DEFAULT 0,
        error TEXT
    )
    """)
    
    cols = {r[1] for r in conn.execute("PRAGMA table_info(requests)").fetchall()}
    if "retry_count" not in cols:
        conn.execute("ALTER TABLE requests ADD COLUMN retry_count INTEGER DEFAULT 0")
    if "error" not in cols:
        conn.execute("ALTER TABLE requests ADD COLUMN error TEXT")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS results (
        request_id TEXT PRIMARY KEY,
        risk REAL,
        decision TEXT,
        explanation TEXT,
        created_at TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_id TEXT,
        true_label INTEGER,
        created_at TEXT,
        processed   INTEGER DEFAULT 0
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS retrain_jobs (
        job_id TEXT PRIMARY KEY,
        status TEXT,
        message_bs TEXT,
        message_en TEXT,
        details TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()