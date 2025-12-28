class HealthRiskAgent:
    def __init__(self, model, scaler, features):
        self.model = model
        self.scaler = scaler
        self.features = features

    def sense(self, data):
        return data

    def think(self, data):
        import pandas as pd
        X = pd.DataFrame([data])
        X = X.reindex(columns=self.features, fill_value=0)
        X_scaled = self.scaler.transform(X)
        return float(self.model.predict_proba(X_scaled)[0][1])

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
