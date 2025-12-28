from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread

from agent_runtime import add_request, get_result
from agent_runner import agent_loop

app = Flask(__name__)
CORS(app)

# ---------- START AGENT ----------
runner_thread = Thread(target=agent_loop, daemon=True)
runner_thread.start()

# ---------- ENDPOINTS ----------
@app.route("/predict", methods=["POST"])
def predict_endpoint():
    data = request.json
    request_id = add_request(data)
    return jsonify({"request_id": request_id, "status": "queued"})


@app.route("/result/<request_id>")
def get_prediction_result(request_id):
    result = get_result(request_id)
    if result is None:
        return jsonify({"status": "processing"})
    return jsonify(result)

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
