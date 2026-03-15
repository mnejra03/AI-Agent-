# agent_runner.py
import time
import os
import subprocess
import sys

from agent_runtime import (
    get_request, save_result, fail_request,
    get_feedback,
    get_retrain_job, save_retrain_result
)
from model_utils import load_model
from health_agent import HealthRiskAgent

# ─── Retry/backoff konstante ──────────────────────────────────────────────────
MAX_RETRIES  = 3    # max pokušaja po zadatku
BACKOFF_BASE = 1.0  # eksponencijalni backoff: 1s, 2s, 4s
IDLE_SLEEP   = 0.2  # sleep kad nema posla u queueu

model, scaler, features = load_model()
agent = HealthRiskAgent(model, scaler, features)


def _backoff(attempt: int):
    """Čeka BACKOFF_BASE * 2^attempt sekundi između pokušaja."""
    wait = BACKOFF_BASE * (2 ** attempt)
    print(f"⏳ BACKOFF: čekam {wait:.1f}s (pokušaj {attempt + 1}/{MAX_RETRIES})")
    time.sleep(wait)


def _handle_prediction(request_id: str, data: dict):
    """
    Status tranzicija: queued → processing → done | failed
    Retry do MAX_RETRIES puta s eksponencijalnim backoffom.
    """
    for attempt in range(MAX_RETRIES):
        try:
            percept     = agent.sense(data)
            risk        = agent.think(percept, request_id)
            agent.predictions_log[request_id] = risk
            decision    = agent.act(risk, data)
            explanation = agent.explain(data, decision)

            save_result(request_id, {
                "risk":        risk,
                "decision":    decision,
                "explanation": explanation
            })

            print(f"✅ PREDICT [done]: id={request_id} "
                  f"bias={agent.risk_bias:.4f} risk={risk:.4f} decision={decision}")
            return  # uspjeh

        except Exception as e:
            print(f"❌ PREDICT [pokušaj {attempt + 1}/{MAX_RETRIES}]: id={request_id} greška: {e}")
            if attempt < MAX_RETRIES - 1:
                _backoff(attempt)
            else:
                fail_request(request_id, str(e))
                print(f"💀 PREDICT [failed]: id={request_id} — status postavljen na 'failed'")


def _handle_feedback(request_id: str, true_label: int):
    """
    Learn s retry/backoffom.
    """
    for attempt in range(MAX_RETRIES):
        try:
            agent.learn(request_id, true_label)
            print(f"✅ LEARN [done]: id={request_id} label={true_label}")
            return

        except Exception as e:
            print(f"❌ LEARN [pokušaj {attempt + 1}/{MAX_RETRIES}]: id={request_id} greška: {e}")
            if attempt < MAX_RETRIES - 1:
                _backoff(attempt)
            else:
                print(f"💀 LEARN [failed]: id={request_id} — preskačem nakon {MAX_RETRIES} pokušaja")


def _handle_retrain(job_id: str):
    """
    Status tranzicija: queued → processing → success | error
    Retry do MAX_RETRIES puta s eksponencijalnim backoffom.
    """
    save_retrain_result(job_id, {"status": "processing"})
    script_path = os.path.join(os.path.dirname(__file__), "train_model.py")

    for attempt in range(MAX_RETRIES):
        try:
            proc = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True
            )

            if proc.returncode == 0:
                save_retrain_result(job_id, {
                    "status":     "success",
                    "message_bs": "Model je uspješno retreniran.",
                    "message_en": "Model retraining completed successfully."
                })
                print(f"✅ RETRAIN [success]: job_id={job_id}")
                return

            else:
                err = (proc.stderr or proc.stdout or "")[-500:]
                print(f"❌ RETRAIN [pokušaj {attempt + 1}/{MAX_RETRIES}]: returncode={proc.returncode}")
                if attempt < MAX_RETRIES - 1:
                    _backoff(attempt)
                else:
                    save_retrain_result(job_id, {
                        "status":     "error",
                        "message_bs": "Greška prilikom retreniranja.",
                        "message_en": "Retraining failed after retries.",
                        "details":    err
                    })
                    print(f"💀 RETRAIN [failed]: job_id={job_id}")

        except Exception as e:
            print(f"❌ RETRAIN [pokušaj {attempt + 1}/{MAX_RETRIES}]: iznimka: {e}")
            if attempt < MAX_RETRIES - 1:
                _backoff(attempt)
            else:
                save_retrain_result(job_id, {
                    "status":     "error",
                    "message_bs": "Greška prilikom retreniranja.",
                    "message_en": "Retraining error after retries.",
                    "details":    str(e)
                })
                print(f"💀 RETRAIN [failed]: job_id={job_id}")


# ─── Glavni loop ──────────────────────────────────────────────────────────────

def agent_loop():
    print("🧠 HealthAgent runner started")
    print(f"   MAX_RETRIES={MAX_RETRIES} | BACKOFF_BASE={BACKOFF_BASE}s | IDLE_SLEEP={IDLE_SLEEP}s")

    while True:
        # 1) Feedback (learn) — najviši prioritet
        fb = get_feedback()
        if fb is not None:
            request_id, true_label = fb
            _handle_feedback(request_id, int(true_label))
            continue

        # 2) Retrain job
        job_id = get_retrain_job()
        if job_id is not None:
            _handle_retrain(job_id)
            continue

        # 3) Predikcija
        item = get_request()
        if item is None:
            time.sleep(IDLE_SLEEP)
            continue

        request_id, data = item
        _handle_prediction(request_id, data)