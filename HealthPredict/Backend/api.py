from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread

from agent_runtime import (
    enqueue_predict,
    enqueue_feedback,
    enqueue_retrain,
    get_result
)

from agent_runner import agent_loop

from data_processing import load_data
import pandas as pd


app = Flask(__name__)
CORS(app)

# ---------- START AGENT ----------
runner_thread = Thread(target=agent_loop, daemon=True)
runner_thread.start()

# ---------- PREDICT ----------
@app.route("/predict", methods=["POST"])
def predict_endpoint():
    data = request.json or {}
    request_id = enqueue_predict(data)
    return jsonify({"request_id": request_id, "status": "queued"})


# ---------- RESULT ----------
@app.route("/result/<request_id>")
def get_prediction_result(request_id):
    result = get_result(request_id)
    if result is None:
        return jsonify({"status": "processing"})
    return jsonify(result)


# ---------- ADD PATIENT ----------
@app.route("/add", methods=["POST"])
def add_data():
    try:
        data = request.json or {}

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
        return jsonify({"status": "error", "message": str(e)}), 500


# ---------- FEEDBACK ----------
@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.json or {}
    request_id = data.get("request_id")
    true_label = data.get("true_label")

    if not request_id or true_label is None:
        return jsonify({
            "status": "error",
            "message": "request_id and true_label are required"
        }), 400

    enqueue_feedback(request_id, int(true_label))
    return jsonify({"status": "success"})


# ---------- RETRAIN ----------
@app.route("/retrain", methods=["POST"])
def retrain():
    job_id = enqueue_retrain()
    return jsonify({
        "status": "queued",
        "job_id": job_id
    })


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)