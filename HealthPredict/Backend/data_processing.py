import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer


def load_data(path="data/heart.csv"):
    return pd.read_csv(path)


def preprocess(df):
    df = df.dropna(how="all")

    if "target" not in df.columns:
        df["target"] = df["num"].apply(lambda x: 1 if x > 0 else 0)

    y = df["target"]
    X = df.drop(columns=["target", "num", "id", "dataset"], errors="ignore")

    numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns
    cat_cols = X.select_dtypes(include=["object"]).columns

    imputer = SimpleImputer(strategy="mean")
    X_numeric = pd.DataFrame(
        imputer.fit_transform(X[numeric_cols]),
        columns=numeric_cols
    )

    X_cat = pd.get_dummies(X[cat_cols], drop_first=True)

    X_processed = pd.concat([X_numeric, X_cat], axis=1)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_processed)

    return X_scaled, y, scaler, X_processed.columns.tolist()
