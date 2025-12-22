class HealthRiskAgent:
    def __init__(self, model, scaler, features):
        self.model = model
        self.scaler = scaler
        self.features = features

        # agent memory (Learn)
        self.total_predictions = 0
        self.uncertain_cases = 0

    # ---------- SENSE ----------
    def sense(self, patient_data: dict):
        return patient_data

    # ---------- THINK ----------
    def think(self, percept: dict):
        import pandas as pd

        X = pd.DataFrame([percept])
        X = X.reindex(columns=self.features, fill_value=0)
        X_scaled = self.scaler.transform(X)

        return float(self.model.predict_proba(X_scaled)[0][1])

    # ---------- ACT ----------
    def act(self, risk: float):
        self.total_predictions += 1

        if risk >= 0.7:
            return "HIGH_RISK"
        elif risk <= 0.3:
            return "LOW_RISK"
        else:
            self.uncertain_cases += 1
            return "REVIEW"

    # ---------- LEARN ----------
    def needs_human_review(self, risk: float):
        return 0.45 <= risk <= 0.55
