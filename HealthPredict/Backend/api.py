from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd

from model_utils import load_model, get_feature_importance
from data_processing import load_data
from health_agent import HealthRiskAgent

app = Flask(__name__)
CORS(app)

model, scaler, features = load_model()
agent = HealthRiskAgent(model, scaler, features)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    percept = agent.sense(data)
    risk = agent.think(percept)
    decision = agent.act(risk)
    review = agent.needs_human_review(risk)

    top = get_feature_importance(model, features)[:5]

    return jsonify({
        "risk": risk,
        "decision": decision,
        "needs_review": review,
        "top_features": top
    })


@app.route("/add", methods=["POST"])
def add_data():
    df = load_data()
    data = request.json

    data.setdefault("id", len(df) + 1)
    data.setdefault("dataset", "new")
    data.setdefault("num", 0)

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv("data/heart.csv", index=False)

    return jsonify({"status": "success"})


@app.route("/retrain", methods=["POST"])
def retrain():
    os.system("python train_model.py")

    global model, scaler, features, agent
    model, scaler, features = load_model()
    agent = HealthRiskAgent(model, scaler, features)

    return jsonify({"status": "model retrained"})


if __name__ == "__main__":
    app.run(debug=True)
