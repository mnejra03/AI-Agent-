# health_agent.py
import os
import json
import tempfile
from datetime import datetime

class HealthRiskAgent:
    
    def __init__(self, model, scaler, features, state_path=None):
        self.model = model
        self.scaler = scaler
        self.features = features

        self.risk_bias = 0.0  # # persisted via agent_state.json
        self.predictions_log = {}  # već imaš :contentReference[oaicite:2]{index=2}

        # --- NEW: state file path ---
        if state_path is None:
            # agent_state.json u istom folderu gdje je health_agent.py
            state_path = os.path.join(os.path.dirname(__file__), "agent_state.json")
        self.state_path = state_path

        # --- NEW: load persisted state on startup ---
        self.load_state()
       
    def sense(self, data):
        return data

    def think(self, data, request_id=None):#dodan id
        #raise Exception("TEST GREŠKA – namjerna")  # ← dodaj samo ovu liniju
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

        # klinička pravila vrijede samo ako model SLAŽE (risk > 0.6)
        # ako je agent naučio da je rizik nizak, poštuj to
        if critical >= 3 and risk > 0.6:
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
   
    # --- NEW ---
    def load_state(self):
        try:
            if not os.path.exists(self.state_path):
                print(f"ℹ️ STATE: nema fajla ({self.state_path}), startam sa bias=0.0")
                return

            with open(self.state_path, "r", encoding="utf-8") as f:
                state = json.load(f)

            rb = state.get("risk_bias", 0.0)
            self.risk_bias = float(rb)

            print(f"✅ STATE LOADED: risk_bias={self.risk_bias:.4f} from {self.state_path}")

        except Exception as e:
            # ako je fajl oštećen ili nešto pođe po zlu, ne ruši aplikaciju
            print(f"⚠️ STATE LOAD FAILED ({self.state_path}): {e}. Startam sa bias=0.0")
            self.risk_bias = 0.0
            
            
     # --- NEW ---
    
    def save_state(self):
        state = {
            "version": 1,
            "risk_bias": float(self.risk_bias),
            "updated_at": datetime.utcnow().isoformat() + "Z"
        }

        os.makedirs(os.path.dirname(self.state_path), exist_ok=True)

        # atomic write
        dir_name = os.path.dirname(self.state_path) or "."
        fd, tmp_path = tempfile.mkstemp(prefix="agent_state_", suffix=".json", dir=dir_name)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, self.state_path)
            # print(f"✅ STATE SAVED: {self.state_path}")
        except Exception as e:
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except:
                pass
            print(f"⚠️ STATE SAVE FAILED ({self.state_path}): {e}")

    def learn(self, request_id, true_label):
        if request_id not in self.predictions_log:
            print("❌ LEARN: request_id nije u predictions_log:", request_id)
            return

        predicted_risk = self.predictions_log[request_id]
        error = float(true_label) - float(predicted_risk)

        old_bias = self.risk_bias
        self.risk_bias += 0.15 * error 


        print(
            f"✅ LEARN: request_id={request_id} true_label={true_label} "
            f"pred={predicted_risk:.4f} error={error:.4f} bias {old_bias:.4f}->{self.risk_bias:.4f}"
        )

        # --- NEW: persist after every update ---
        self.save_state()