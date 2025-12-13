import joblib
import pandas as pd

def load_model():
    bundle = joblib.load("models/rf_model.joblib")
    return bundle["model"], bundle["scaler"], bundle["features"]

def predict(model, scaler, features, data: dict):
    X = pd.DataFrame([data])

    # poravnaj feature-e
    X = X.reindex(columns=features, fill_value=0)

    X_scaled = scaler.transform(X)
    proba = model.predict_proba(X_scaled)[0][1]
    pred = int(proba >= 0.5)

    return {
        "prediction": pred,
        "probability": float(proba)
    }

def get_feature_importance(model, features):
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        return sorted(
            zip(features, importances),
            key=lambda x: x[1],
            reverse=True
        )
    return []
