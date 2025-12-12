# train_model.py
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, confusion_matrix

from data_processing import load_data, preprocess, split_data

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:,1]
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()
    }

def main():
    df = load_data()
    X, y, scaler, feature_names = preprocess(df)
    X_train, X_test, y_train, y_test = split_data(X, y)

    # Logistic Regression baseline
    log = LogisticRegression(max_iter=1000)
    log.fit(X_train, y_train)
    print("Logistic Regression metrics:", evaluate_model(log, X_test, y_test))

    # Random Forest model
    rf = RandomForestClassifier(random_state=42)
    param_grid = {
        "n_estimators": [100, 200],
        "max_depth": [None, 6, 10],
        "min_samples_split": [2, 5]
    }
    grid = GridSearchCV(rf, param_grid, cv=5, scoring="roc_auc", n_jobs=-1)
    grid.fit(X_train, y_train)
    best_rf = grid.best_estimator_
    print("Random Forest metrics:", evaluate_model(best_rf, X_test, y_test))
    print("Best RF params:", grid.best_params_)

    # spremi model + scaler
    joblib.dump({"model": best_rf, "scaler": scaler, "features": feature_names}, "models/rf_model.joblib")
    print("Model spremljen u models/rf_model.joblib")

if __name__ == "__main__":
    main()
