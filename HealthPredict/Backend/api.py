# api.py
# .\venv\Scripts\Activate.ps1

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd
from model_utils import load_model, predict, get_feature_importance
from data_processing import load_data

app = Flask(__name__)
CORS(app)  # omogućava CORS za sve domene

model, scaler, features = load_model()

@app.route("/predict", methods=["POST"])
def predict_endpoint():
    try:
        data = request.json
        result = predict(model, scaler, features, data)
        top = get_feature_importance(model, features)[:5]
        return jsonify({"result": result, "top_features": top})
    except Exception as e:
        print("Predict Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/add", methods=["POST"])
def add_data():
    try:
        df = load_data()  # prvo učitaj postojeći DataFrame
        data = request.json

        # Dodaj default vrijednosti za polja koja frontend ne šalje
        data.setdefault("id", len(df) + 1)
        data.setdefault("dataset", "new")
        data.setdefault("num", 0)

        # Polja koja stvarno šalje frontend
        required_fields = [f for f in df.columns if f not in ["id", "dataset", "num"]]
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({"status": "error", "message": f"Missing fields: {missing}"}), 400

        # Dodavanje novog reda u DataFrame
        new_row = pd.DataFrame([data])
        df = pd.concat([df, new_row], ignore_index=True)

        # Spremanje u CSV
        df.to_csv("data/heart.csv", index=False)

        return jsonify({"status": "success", "message": "Record added successfully"})
    except Exception as e:
        print("Add Data Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500



@app.route("/retrain", methods=["POST"])
def retrain():
    try:
        os.system("python train_model.py")  # pokreni retraining
        global model, scaler, features
        model, scaler, features = load_model()  # reload model
        return jsonify({"status": "success", "message": "Model retrained and reloaded"})
    except Exception as e:
        print("Retrain Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
