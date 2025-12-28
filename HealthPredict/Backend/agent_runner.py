# agent_runner.py
import time

from agent_runtime import get_request, save_result
from model_utils import load_model
from health_agent import HealthRiskAgent

model, scaler, features = load_model()
agent = HealthRiskAgent(model, scaler, features)

def agent_loop():
    print("🧠 HealthAgent runner started")

    while True:
        item = get_request()
        if item is None:
            time.sleep(0.5)
            continue

        request_id, data = item

        # ---- AGENT TICK ----
        percept = agent.sense(data)
        risk = agent.think(percept)
        decision = agent.act(risk, data)
        explanation = agent.explain(data, decision)

        save_result(request_id, {
            "risk": risk,
            "decision": decision,
            "explanation": explanation
        })
