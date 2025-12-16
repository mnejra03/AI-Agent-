import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

DATA_PATH = "data/heart.csv"
MODEL_PATH = "models/rf_model.joblib"

def load_data():
    df = pd.read_csv(DATA_PATH)
    df = df.copy()  
    if "target" not in df.columns:
        if "num" in df.columns:
            df.loc[:, "target"] = df["num"].apply(lambda x: 1 if x > 0 else 0)
        else:
            raise ValueError("Ne postoji ni 'target' ni 'num' kolona u CSV-u.")
    return df

def preprocess(df: pd.DataFrame):
    df = df.dropna(how="all")

    X = df.drop(columns=["target"], errors="ignore")
    y = df["target"]

    numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    cat_cols = X.select_dtypes(include=["object"]).columns.tolist()

    imputer = SimpleImputer(strategy="mean")
    X_numeric = pd.DataFrame(imputer.fit_transform(X[numeric_cols]), columns=numeric_cols)

    X_cat = pd.get_dummies(X[cat_cols], drop_first=True)

    X_processed = pd.concat([X_numeric, X_cat], axis=1)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_processed)

    feature_names = X_processed.columns.tolist()
    return X_scaled, y, scaler, feature_names

def split_data(X, y, test_size=0.2, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)[:,1]
    else:
        y_proba = y_pred
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()
    }

def main():
    print("Učitavanje podataka...")
    df = load_data()

    print("Preprocesiranje...")
    X, y, scaler, feature_names = preprocess(df)

    print("Dijeljenje na trening i test set...")
    X_train, X_test, y_train, y_test = split_data(X, y)

    print("Treniranje LogisticRegression...")
    log = LogisticRegression(max_iter=1000)
    log.fit(X_train, y_train)
    print("Logistic Regression metrics:", evaluate_model(log, X_test, y_test))

    print("Treniranje RandomForest sa GridSearch...")
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

    os.makedirs("models", exist_ok=True)
    joblib.dump({"model": best_rf, "scaler": scaler, "features": feature_names}, MODEL_PATH)
    print(f"Model spremljen u {MODEL_PATH}")

if __name__ == "__main__":
    main()
