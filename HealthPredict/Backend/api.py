# api.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd
from model_utils import load_model, predict, get_feature_importance
from data_processing import load_data

app = Flask(__name__)
CORS(app) 

model, scaler, features = load_model()

@app.route("/predict", methods=["POST"])
def predict_endpoint():
    try:
        data = request.json
        result = predict(model, scaler, features, data)
        top = get_feature_importance(model, features)[:5]
        return jsonify({"result": result, "top_features": top})
    except Exception as e:
        print("Predict Error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/add", methods=["POST"])
def add_data():
    try:
        df = load_data() 
        data = request.json
        
        numeric_fields = ["age","sex","trestbps","chol","fbs","thalch","exang","oldpeak","ca"]
        for field in numeric_fields:
            if field not in data or data[field] in ["", None]:
                return jsonify({"status": "error",
                                "message_bs": "Molimo popunite sva obavezna polja.",
                                "message_en": "Please fill all required fields."}), 400
            data[field] = float(data[field])  
        
        string_fields = ["cp","restecg","slope","thal"]
        for field in string_fields:
            if field not in data or data[field] in ["", None]:
                return jsonify({"status": "error",
                                "message_bs": "Molimo popunite sva obavezna polja.",
                                "message_en": "Please fill all required fields."}), 400

        data.setdefault("id", len(df) + 1)
        data.setdefault("dataset", "new")
        data.setdefault("num", 0)
        
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv("data/heart.csv", index=False)

        return jsonify({"status": "success",
                        "message_bs": "Pacijent uspješno dodan.",
                        "message_en": "Patient added successfully."})

    except Exception as e:
        print("Add Data Error:", e)
        return jsonify({"status": "error",
                        "message_bs": f"Greška: {str(e)}",
                        "message_en": f"Error: {str(e)}"}), 500



@app.route("/retrain", methods=["POST"])
def retrain():
    try:
       
        df = load_data()
        df = df.dropna()  
        if df.empty:
            return jsonify({
        "status": "error",
        "message_bs": "Nije moguće retrenirati model jer nema validnih korisnika.",
        "message_en": "Cannot retrain the model because there are no valid users."
            })


        os.system("python train_model.py") 
        global model, scaler, features
        model, scaler, features = load_model() 

        return jsonify({
            "status": "success",
            "message_bs": "Model je uspješno retreniran i ponovno učitan.",
            "message_en": "Model retrained and reloaded successfully."
        })

    except Exception as e:
        print("Retrain Error:", e)
        return jsonify({
            "status": "error",
            "message_bs": f"Greška prilikom retreniranja: {str(e)}",
            "message_en": f"Error retraining model: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
