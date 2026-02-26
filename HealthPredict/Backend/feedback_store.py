import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FEEDBACK_FILE = os.path.join(DATA_DIR, "feedback.json")

def save_feedback(request_id, true_label):
    os.makedirs(DATA_DIR, exist_ok=True)

    try:
        with open(FEEDBACK_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append({
        "request_id": request_id,
        "true_label": true_label
    })

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=2)
