# api.py
from flask import Flask, request, jsonify
import os
from model_utils import load_model, predict, get_feature_importance
from data_processing import load_data

app = Flask(__name__)

model, scaler, features = load_model()

@app.route("/predict", methods=["POST"])
def predict_endpoint():
    data = request.json
    result = predict(model, scaler, features, data)
    top = get_feature_importance(model, features)[:5]
    return jsonify({"result": result, "top_features": top})

@app.route("/add", methods=["POST"])
def add_data():
    data = request.json
    df = load_data()
    df2 = df.append(data, ignore_index=True)
    df2.to_csv("data/heart.csv", index=False)
    return jsonify({"status":"success", "message":"Record added"})

@app.route("/retrain", methods=["POST"])
def retrain():
    os.system("python train_model.py")
    global model, scaler, features
    model, scaler, features = load_model()
    return jsonify({"status":"success", "message":"Model retrained and reloaded"})

if __name__ == "__main__":
    app.run(debug=True)
