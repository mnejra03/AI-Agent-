# model_utils.py
import joblib
import pandas as pd

MODEL_PATH = "models/rf_model.joblib"

def load_model(path=MODEL_PATH):
    data = joblib.load(path)
    return data["model"], data["scaler"], data["features"]

def predict(model, scaler, features, input_dict):
    X = pd.DataFrame([input_dict])
    X = X[features]
    X_scaled = scaler.transform(X)
    proba = model.predict_proba(X_scaled)[0][1]
    pred = model.predict(X_scaled)[0]
    return {"probability": float(proba), "prediction": int(pred)}

def get_feature_importance(model, features):
    if hasattr(model, "feature_importances_"):
        imp = model.feature_importances_
        return sorted(zip(features, imp), key=lambda x: x[1], reverse=True)
    return []
