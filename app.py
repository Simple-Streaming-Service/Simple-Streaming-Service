import os

from flask import Flask, session, send_file, render_template
from flask import request, jsonify, redirect
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = "super secret key"
app.api_host = os.getenv("API_HOST", "http://localhost:9997")
if len(app.api_host) == 0:
    app.api_host = "http://localhost:9997"

app.live_host = os.getenv("LIVE_HOST", "https://localhost:8888")
if len(app.live_host) == 0:
    app.live_host = "https://localhost:8888"


@app.get("/")
def index():
    r = requests.get(app.api_host + "/v3/paths/list")
    if r.status_code == 200:
        data = r.json()
        if "items" in data:
            res = [x["name"] for x in data["items"]]
            return render_template("index.html", paths=res)
    return {"error": f"API {app.api_host} not available"}

@app.get("/<user>")
def stream_watch(user):
    return render_template("stream.html", path=user, live_path=app.live_host)

@app.get("/msg/list")
def msg_list():
    pass
@app.post("/msg/send")
def msg_send():
    pass

if __name__ == '__main__':
    app.run()
