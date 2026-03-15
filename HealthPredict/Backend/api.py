from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread
from data_processing import load_data
from storage_setup import init_db
import pandas as pd
# Queue / storage funkcije
from agent_runtime import (
    add_request, get_result,
    add_feedback,
    add_retrain_job, get_retrain_result
)

# Runner loop
from agent_runner import agent_loop

print("agent_runtime location:", __import__('agent_runtime').__file__)
app = Flask(__name__)
init_db()
CORS(app)

# ---------- START AGENT ----------
runner_thread = Thread(target=agent_loop, daemon=True)
runner_thread.start()

# ---------- ENDPOINTS ----------
@app.route("/predict", methods=["POST"])
def predict_endpoint():
    data = request.json
    request_id = add_request(data)
    return jsonify({"request_id": request_id, "status": "queued"})

@app.route("/result/<request_id>")
def get_prediction_result(request_id):
    result = get_result(request_id)
    if result is None:
        return jsonify({"status": "processing"})
    return jsonify(result)


@app.route("/retrain_result/<job_id>")
def retrain_result(job_id):
    r = get_retrain_result(job_id)
    if r is None:
        return jsonify({"status": "processing"})
    return jsonify(r)

@app.route("/add", methods=["POST"])
def add_data():
    try:
        data = request.json

        required_fields = [
            "age", "sex", "cp", "trestbps", "chol",
            "fbs", "restecg", "thalch", "exang",
            "oldpeak", "slope", "ca", "thal"
        ]

        for field in required_fields:
            if field not in data or data[field] in ["", None]:
                return jsonify({
                    "status": "error",
                    "message_bs": "Sva polja moraju biti popunjena.",
                    "message_en": "All fields must be filled."
                }), 400

        df = load_data()

        data.setdefault("id", len(df) + 1)
        data.setdefault("dataset", "new")
        data.setdefault("num", 0)

        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv("data/heart.csv", index=False)

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/feedback", methods=["POST"])
def feedback():
    
    data = request.json or {}
    request_id = data.get("request_id")
    true_label = data.get("true_label")

    if not request_id or true_label is None:
        return jsonify({"status": "error", "message": "request_id and true_label are required"}), 400

    print(f"DEBUG: feedback endpoint pozvan {request_id=} {true_label=}")

    #save_feedback(request_id, int(true_label))      # storage (log) OK
    add_feedback(request_id, int(true_label))       # queue -> agent tick će pokupit

    return jsonify({"status": "success"})           # ili "ok" ako ti JS očekuje "ok"

@app.route("/retrain", methods=["POST"])
def retrain_model():
    job_id = add_retrain_job()
    return jsonify({
        "status": "queued",
        "job_id": job_id,
        "message_bs": "Retreniranje je stavljeno u red (queue).",
        "message_en": "Retraining has been queued."
    })

@app.route("/debug/<request_id>")
def debug(request_id):
    from storage_setup import get_conn
    conn = get_conn()
    row = conn.execute("SELECT * FROM results WHERE request_id=?", (request_id,)).fetchone()
    conn.close()
    return str(row)

from storage_setup import get_conn 
@app.route("/last_result")
def get_last_result():
    conn = get_conn()
    row = conn.execute("SELECT * FROM results ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()
    if not row:
        return jsonify({"status": "empty"})
    return jsonify({
        "request_id": row["request_id"],
        "risk": row["risk"],
        "decision": row["decision"],
        "explanation": row["explanation"]
    })

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
