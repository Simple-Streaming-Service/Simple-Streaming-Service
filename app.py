import os

from flask import Flask, session, send_file, render_template
from flask import request, jsonify, redirect
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = "super secret key"
app.api_host = os.getenv("API_HOST", "http://localhost:9997")
app.live_host = os.getenv("LIVE_HOST", "http://localhost:8888")


@app.get("/")
def index():
    r = requests.get(app.api_host + "/v3/paths/list")
    if r.status_code == 200:
        data = r.json()
        if "items" in data:
            res = [x["name"] for x in data["items"]]
            return render_template("index.html", paths=res, live_path=app.live_host)
    return {"error": f"API {app.api_host} not available"}


if __name__ == '__main__':
    app.run()
