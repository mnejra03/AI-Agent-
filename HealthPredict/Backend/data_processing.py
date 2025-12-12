# data_processing.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_data(path="data/heart.csv"):
    df = pd.read_csv(path)
    return df

def preprocess(df):
    # uklanjamo redove sa nedostajućim vrijednostima
    df = df.dropna()

    # target: 0 = nema bolesti, 1 ako je num >0
    df["target"] = df["num"].apply(lambda x: 1 if x > 0 else 0)
    y = df["target"]

    # uklanjamo nebitne kolone
    X = df.drop(["num", "target", "id", "dataset"], axis=1)

    # Enkodiranje binarnih kategorija
    X["sex"] = X["sex"].map({"Male":1, "Female":0})
    X["fbs"] = X["fbs"].map({True:1, False:0})
    X["exang"] = X["exang"].map({True:1, False:0})

    # Enkodiranje ostalih kategorijskih varijabli
    X = pd.get_dummies(X, columns=["cp","restecg","slope","thal"], drop_first=True)

    # skaliranje numeričkih vrijednosti
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler, X.columns.tolist()

def split_data(X, y, test_size=0.2, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state)
