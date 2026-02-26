import os
import json

STATE_FILE = os.path.join(os.path.dirname(__file__), "data", "agent_state.json")
class HealthRiskAgent:
    def __init__(self, model, scaler, features):
        self.model = model
        self.scaler = scaler
        self.features = features
        self.predictions_log = {}#dodano
        
        self.risk_bias = 0.0#dodano
        self.load_state()

    def sense(self, data):
        return data

    def think(self, data, request_id=None):#dodan id
        import pandas as pd
        X = pd.DataFrame([data])
        X = X.reindex(columns=self.features, fill_value=0)
        X_scaled = self.scaler.transform(X)
        base_risk = float(self.model.predict_proba(X_scaled)[0][1])#dodano
        adjusted_risk = min(max(base_risk + self.risk_bias, 0), 1)#dodano
        if request_id:#dodano
            self.predictions_log[request_id] = adjusted_risk#dodano
        return adjusted_risk


    def act(self, risk, data):
        critical = 0

        if data.get("age", 0) >= 60: critical += 1
        if data.get("cp") == "asymptomatic": critical += 1
        if data.get("trestbps", 0) >= 150: critical += 1
        if data.get("chol", 0) >= 300: critical += 1
        if data.get("exang") in [1, True, "1"]: critical += 1
        if data.get("oldpeak", 0) >= 2.5: critical += 1
        if data.get("slope") == "downsloping": critical += 1
        if data.get("ca", 0) >= 2: critical += 1
        if data.get("thal") == "reversable defect": critical += 1

        if critical >= 3:
            return "HIGH_RISK"
        if risk >= 0.7:
            return "HIGH_RISK"
        if risk <= 0.3:
            return "LOW_RISK"
        return "REVIEW"

    def explain(self, data, decision):
        reasons = []

        if data.get("trestbps", 0) >= 150:
            reasons.append("povišen krvni pritisak")
        if data.get("chol", 0) >= 300:
            reasons.append("visok holesterol")
        if data.get("exang") in [1, True, "1"]:
            reasons.append("angina pri naporu")
        if data.get("ca", 0) >= 2:
            reasons.append("više zahvaćenih arterija")

        if not reasons:
            return "Nisu uočeni značajni klinički faktori rizika."

        if decision == "HIGH_RISK":
            return "Visok rizik zbog: " + ", ".join(reasons) + "."
        if decision == "REVIEW":
            return "Potrebna dodatna procjena zbog: " + ", ".join(reasons) + "."
        return "Nizak rizik bez značajnih faktora."
    def learn(self, request_id, true_label):
        if request_id not in self.predictions_log:
            print("❌ LEARN: request_id nije u predictions_log:", request_id)
            return

        predicted_risk = self.predictions_log[request_id]
        error = float(true_label) - float(predicted_risk)

        old_bias = self.risk_bias
        #self.risk_bias += 0.3 * error  # policy update
        self.risk_bias += 0.1 * error
        self.save_state()   # ← BITNO
        

        print(f"✅ LEARN: request_id={request_id} true_label={true_label} "
          f"pred={predicted_risk:.4f} error={error:.4f} bias {old_bias:.4f}->{self.risk_bias:.4f}")
        
    



    def save_state(self):
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"risk_bias": float(self.risk_bias)}, f, indent=2)

    def load_state(self):
        try:
            if not os.path.exists(STATE_FILE):
                self.risk_bias = 0.0
                return

            # ako je fajl prazan → tretiraj kao da ne postoji
            if os.path.getsize(STATE_FILE) == 0:
                self.risk_bias = 0.0
                return

            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.risk_bias = float(data.get("risk_bias", 0.0))

        except Exception:
            # bilo kakav problem (prazan/pokvaren json) → reset na 0
            self.risk_bias = 0.0