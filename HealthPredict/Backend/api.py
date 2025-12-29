from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread

from agent_runtime import add_request, get_result
from agent_runner import agent_loop

from data_processing import load_data
import pandas as pd

app = Flask(__name__)
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


@app.route("/retrain", methods=["POST"])
def retrain_model():
    try:
        import os
        os.system("python train_model.py")

        return jsonify({
            "status": "success",
            "message_bs": "Model je uspješno retreniran.",
            "message_en": "Model retraining completed successfully."
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message_bs": "Greška prilikom retreniranja.",
            "message_en": "Error during retraining."
        }), 500




# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
