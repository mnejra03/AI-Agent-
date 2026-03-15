import uuid
import json
from datetime import datetime
from storage_setup import get_conn


# ---------------- REQUEST QUEUE ----------------

def add_request(data):
    request_id = str(uuid.uuid4())

    conn = get_conn()
    conn.execute(
        "INSERT INTO requests (request_id, data, status, created_at) VALUES (?, ?, ?, ?)",
        (
            request_id,
            json.dumps(data),
            "queued",
            datetime.utcnow().isoformat()
        )
    )
    conn.commit()
    conn.close()

    return request_id


def get_request():
    conn = get_conn()

    row = conn.execute(
        "SELECT request_id, data FROM requests WHERE status='queued' LIMIT 1"
    ).fetchone()

    if not row:
        conn.close()
        return None

    request_id = row["request_id"]
    data = json.loads(row["data"])

    conn.execute(
        "UPDATE requests SET status='processing' WHERE request_id=?",
        (request_id,)
    )

    conn.commit()
    conn.close()

    return request_id, data

def fail_request(request_id: str, error_msg: str):
    """Označava zahtjev kao 'failed' nakon svih retry pokušaja."""
    conn = get_conn()
    conn.execute(
        "UPDATE requests SET status='failed', error=? WHERE request_id=?",
        (error_msg, request_id)
    )
    conn.commit()
    conn.close()
# ---------------- RESULTS ----------------

def save_result(request_id, result):
    conn = get_conn()

    conn.execute(
        """INSERT OR REPLACE INTO results
        (request_id, risk, decision, explanation, created_at)
        VALUES (?, ?, ?, ?, ?)""",
        (
            request_id,
            result["risk"],
            result["decision"],
            result["explanation"],
            datetime.utcnow().isoformat()
        )
    )

    conn.execute(
        "UPDATE requests SET status='done' WHERE request_id=?",
        (request_id,)
    )

    conn.commit()
    conn.close()


def get_result(request_id):
    conn = get_conn()

    row = conn.execute(
        "SELECT risk, decision, explanation FROM results WHERE request_id=?",
        (request_id,)
    ).fetchone()

    conn.close()

    if not row:
        return None

    return {
        "risk": row["risk"],
        "decision": row["decision"],
        "explanation": row["explanation"]
    }


# ---------------- FEEDBACK ----------------

def add_feedback(request_id, true_label):
    conn = get_conn()

    conn.execute(
        "INSERT INTO feedback (request_id, true_label, created_at) VALUES (?, ?, ?)",
        (
            request_id,
            true_label,
            datetime.utcnow().isoformat()
        )
    )

    conn.commit()
    conn.close()

    return True

def get_feedback():
    conn = get_conn()

    row = conn.execute(
        """SELECT id, request_id, true_label FROM feedback
           WHERE processed = 0
           ORDER BY created_at
           LIMIT 1"""
    ).fetchone()

    if not row:
        conn.close()
        return None

    # označi kao obrađeno umjesto brisanja
    conn.execute(
        "UPDATE feedback SET processed=1 WHERE id=?",
        (row["id"],)
    )

    conn.commit()
    conn.close()

    return row["request_id"], row["true_label"]

from storage_setup import DB_PATH, db_conn
from datetime import datetime
from storage_setup import db_conn

def save_feedback(request_id: str, true_label: int):
    """
    Sprema feedback u SQLite tabelu 'feedback'.
    Ne dira agent_state.json.
    """
    created_at = datetime.utcnow().isoformat() + "Z"

    with db_conn() as conn:
        conn.execute("""
            INSERT INTO feedback (request_id, true_label, created_at)
            VALUES (?, ?, ?)
        """, (request_id, true_label, created_at))

    print(f"✅ FEEDBACK SPREMLJEN U BAZU: {request_id} -> {true_label}")

# ---------------- RETRAIN JOBS ----------------

def add_retrain_job():
    job_id = str(uuid.uuid4())

    conn = get_conn()

    conn.execute(
        """INSERT INTO retrain_jobs
        (job_id, status, created_at)
        VALUES (?, ?, ?)""",
        (
            job_id,
            "queued",
            datetime.utcnow().isoformat()
        )
    )

    conn.commit()
    conn.close()

    return job_id


def get_retrain_job():
    conn = get_conn()

    row = conn.execute(
        "SELECT job_id FROM retrain_jobs WHERE status='queued' LIMIT 1"
    ).fetchone()

    if not row:
        conn.close()
        return None

    job_id = row["job_id"]

    conn.execute(
        "UPDATE retrain_jobs SET status='processing' WHERE job_id=?",
        (job_id,)
    )

    conn.commit()
    conn.close()

    return job_id


def save_retrain_result(job_id, result):
    conn = get_conn()

    conn.execute(
        """UPDATE retrain_jobs
        SET status=?, message_bs=?, message_en=?, details=?
        WHERE job_id=?""",
        (
            result.get("status"),
            result.get("message_bs"),
            result.get("message_en"),
            result.get("details"),
            job_id
        )
    )

    conn.commit()
    conn.close()


def get_retrain_result(job_id):
    conn = get_conn()

    row = conn.execute(
        "SELECT status, message_bs, message_en, details FROM retrain_jobs WHERE job_id=?",
        (job_id,)
    ).fetchone()

    conn.close()

    if not row:
        return None

    return dict(row)

