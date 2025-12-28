# agent_runtime.py
from collections import deque
from threading import Lock
import uuid

pending_requests = deque()
results_store = {}

queue_lock = Lock()
results_lock = Lock()

def add_request(data):
    request_id = str(uuid.uuid4())
    with queue_lock:
        pending_requests.append((request_id, data))
    return request_id

def get_request():
    with queue_lock:
        if pending_requests:
            return pending_requests.popleft()
    return None

def save_result(request_id, result):
    with results_lock:
        results_store[request_id] = result

def get_result(request_id):
    with results_lock:
        return results_store.get(request_id)
