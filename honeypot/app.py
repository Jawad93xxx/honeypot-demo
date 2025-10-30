import json
import os
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
LOG_DIR = "/app/logs"
LOG_FILE = os.path.join(LOG_DIR, "requests.log")

os.makedirs(LOG_DIR, exist_ok=True)

def log_request(req):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "remote_addr": req.remote_addr,
        "method": req.method,
        "path": req.path,
        "args": req.args.to_dict(flat=True),
        "headers": {k: v for k, v in req.headers.items()},
        "body": req.get_data(as_text=True)
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def catch_all(path):
    try:
        log_request(request)
    except Exception:
        pass
    return jsonify({"status": "ok", "message": "service running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)