import os
import json
import sqlite3
import uuid
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "agent_db.sqlite")


def _utc_now():
    return datetime.utcnow().isoformat()


def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)

    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS queue (
            id TEXT PRIMARY KEY,
            kind TEXT NOT NULL,            -- predict | feedback | retrain
            payload TEXT NOT NULL,         -- JSON string
            status TEXT NOT NULL,          -- queued | processing | done | failed
            error TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            request_id TEXT PRIMARY KEY,
            payload TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id TEXT NOT NULL,
            true_label INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
        """)

        con.commit()


# ---------- API: enqueue ----------
def enqueue_predict(data: dict) -> str:
    init_db()
    req_id = str(uuid.uuid4())
    payload = json.dumps(data)

    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            INSERT INTO queue (id, kind, payload, status, created_at, updated_at)
            VALUES (?, 'predict', ?, 'queued', ?, ?)
        """, (req_id, payload, _utc_now(), _utc_now()))
        con.commit()

    return req_id


def enqueue_feedback(request_id: str, true_label: int) -> str:
    init_db()
    fb_job_id = str(uuid.uuid4())
    payload = json.dumps({"request_id": request_id, "true_label": int(true_label)})

    with sqlite3.connect(DB_PATH) as con:
        # trajno spremi feedback (prof traži)
        con.execute("""
            INSERT INTO feedback (request_id, true_label, created_at)
            VALUES (?, ?, ?)
        """, (request_id, int(true_label), _utc_now()))

        # stavi job u queue da agent uradi learn
        con.execute("""
            INSERT INTO queue (id, kind, payload, status, created_at, updated_at)
            VALUES (?, 'feedback', ?, 'queued', ?, ?)
        """, (fb_job_id, payload, _utc_now(), _utc_now()))
        con.commit()

    return fb_job_id


def enqueue_retrain() -> str:
    init_db()
    job_id = str(uuid.uuid4())

    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            INSERT INTO queue (id, kind, payload, status, created_at, updated_at)
            VALUES (?, 'retrain', '{}', 'queued', ?, ?)
        """, (job_id, _utc_now(), _utc_now()))
        con.commit()

    return job_id


# ---------- Agent: dequeue ----------
def dequeue_next():
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute("""
            SELECT id, kind, payload
            FROM queue
            WHERE status='queued'
            ORDER BY created_at ASC
            LIMIT 1
        """)
        row = cur.fetchone()

        if not row:
            return None

        cur.execute("""
            UPDATE queue SET status='processing', updated_at=?
            WHERE id=?
        """, (_utc_now(), row["id"]))
        con.commit()

        return row["id"], row["kind"], json.loads(row["payload"])


def mark_done(job_id: str):
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            UPDATE queue SET status='done', updated_at=?
            WHERE id=?
        """, (_utc_now(), job_id))
        con.commit()


def mark_failed(job_id: str, error: str):
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            UPDATE queue SET status='failed', error=?, updated_at=?
            WHERE id=?
        """, (str(error), _utc_now(), job_id))
        con.commit()


# ---------- Results ----------
def save_result(request_id: str, result: dict):
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            INSERT OR REPLACE INTO results (request_id, payload, created_at)
            VALUES (?, ?, ?)
        """, (request_id, json.dumps(result), _utc_now()))
        con.commit()


def get_result(request_id: str):
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT payload FROM results WHERE request_id=?", (request_id,))
        row = cur.fetchone()
        if not row:
            return None
        return json.loads(row["payload"])