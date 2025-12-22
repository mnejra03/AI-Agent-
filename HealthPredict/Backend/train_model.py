import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from data_processing import load_data, preprocess

MODEL_PATH = "models/rf_model.joblib"


def main():
    df = load_data()
    X, y, scaler, features = preprocess(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )
    model.fit(X_train, y_train)

    score = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    print("ROC AUC:", score)

    os.makedirs("models", exist_ok=True)
    joblib.dump(
        {"model": model, "scaler": scaler, "features": features},
        MODEL_PATH
    )
    print("Model saved.")


if __name__ == "__main__":
    main()
