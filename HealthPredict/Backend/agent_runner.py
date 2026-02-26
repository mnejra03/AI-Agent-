import time
import os

from agent_runtime import dequeue_next, mark_done, mark_failed, save_result
from model_utils import load_model
from health_agent import HealthRiskAgent


model, scaler, features = load_model()
agent = HealthRiskAgent(model, scaler, features)


def agent_loop():
    print("🧠 HealthAgent runner started")

    while True:
        job = dequeue_next()
        if not job:
            time.sleep(0.5)
            continue

        job_id, kind, payload = job

        try:
            # -------------------------
            # FEEDBACK → LEARN
            # -------------------------
            if kind == "feedback":
                fb_request_id = payload.get("request_id")
                true_label = payload.get("true_label")

                if fb_request_id is None or true_label is None:
                    raise ValueError("Feedback payload must contain request_id and true_label")

                agent.learn(fb_request_id, int(true_label))
                print(f"🧠 LEARN: req={fb_request_id} label={true_label} bias={agent.risk_bias:.4f}")

                mark_done(job_id)
                continue

            # -------------------------
            # RETRAIN (agent radi u pozadini)
            # -------------------------
            if kind == "retrain":
                os.system("python train_model.py")

                # reload model after retrain
                new_model, new_scaler, new_features = load_model()
                agent.model = new_model
                agent.scaler = new_scaler
                agent.features = new_features

                print("🔁 RETRAIN DONE: model reloaded")
                mark_done(job_id)
                continue

            # -------------------------
            # PREDICT
            # -------------------------
            if kind == "predict":
                request_id = job_id  # enqueue_predict koristi id kao request_id
                data = payload

                percept = agent.sense(data)
                risk = agent.think(percept, request_id)
                decision = agent.act(risk, data)
                explanation = agent.explain(data, decision)

                save_result(request_id, {
                    "risk": risk,
                    "decision": decision,
                    "explanation": explanation
                })

                print(f"🧠 PREDICT: id={request_id} risk={risk:.4f} decision={decision}")
                mark_done(job_id)
                continue

            raise ValueError(f"Unknown job kind: {kind}")

        except Exception as e:
            mark_failed(job_id, str(e))
            print(f"❌ JOB FAILED: id={job_id}, kind={kind}, err={e}")