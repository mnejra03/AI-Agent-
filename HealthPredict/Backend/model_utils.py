import joblib
import pandas as pd


def load_model():
    bundle = joblib.load("models/rf_model.joblib")
    return bundle["model"], bundle["scaler"], bundle["features"]


def predict_raw(model, scaler, features, data: dict):
    X = pd.DataFrame([data])
    X = X.reindex(columns=features, fill_value=0)
    X_scaled = scaler.transform(X)
    return model.predict_proba(X_scaled)[0][1]


def get_feature_importance(model, features):
    if not hasattr(model, "feature_importances_"):
        return []

    return sorted(
        zip(features, model.feature_importances_),
        key=lambda x: x[1],
        reverse=True
    )
