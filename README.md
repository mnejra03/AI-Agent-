# AI-Agent
# HealthPredict – AI Agent for Heart Disease Prediction

# About
HealthPredict is a web application that uses an AI agent to assess the risk of heart disease based on clinical patient parameters. The agent combines an ML model (Random Forest) with medical rules and continuous learning through a feedback mechanism.

# Features
- **Risk prediction** – the agent estimates the probability of heart disease based on 13 clinical parameters
- **Clinical decision** – the agent outputs: LOW RISK / MODERATE RISK / HIGH RISK
- **Feedback & learning** – users can correct predictions; the agent learns and updates its `risk_bias`
- **Learning persistence** – learned parameters (`risk_bias`) are saved to `agent_state.json` and survive server restarts
- **Add patients** – new data can be added to the dataset
- **Model retraining** – the model can be retrained on new data
- **Persistent storage** – all requests, results and feedback are stored in a SQLite database (`database.db`)
- **Retry/backoff mechanism** – the agent automatically retries failed tasks (max 3 attempts, exponential backoff)
- **Multilingual UI** – Bosnian and English language support

# Tech Stack
| Layer | Technology |
|-------|------------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask, Flask-CORS |
| ML Model | scikit-learn (Random Forest) |
| Storage | SQLite |
| Agent | Custom Python agent (sense → think → act → learn) |

## ⚙️ Running the Project
```bash
      python -m venv venv
      cd .\Backend\
      .\venv\Scripts\Activate.ps1
      pip install -r requirements.txt
      python api.py
```
Backend runs at: http://127.0.0.1:5000

