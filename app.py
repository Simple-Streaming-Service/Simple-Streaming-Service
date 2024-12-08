import os

from flask import Flask, session, send_file, render_template
from flask import request, jsonify, redirect
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.getenv("SECRET_KEY", "secret")

# MediaMTX
app.mtx_api_host = os.getenv("MTX_API_HOST", "localhost")
app.mtx_api_host_port = os.getenv("MTX_API_HOST_PORT", "9997")
app.mtx_api_uri = "http://" + app.mtx_api_host + ":" + app.mtx_api_host_port

# MediaMTX HLS
app.mtx_hls_host = os.getenv("MTX_LIVE_HOST", "localhost")
app.mtx_hls_host_port = os.getenv("MTX_LIVE_HOST_PORT", "8888")
app.mtx_hls_uri = app.mtx_hls_host + ":" + app.mtx_hls_host_port

app.streams_redirect = "https://" + app.mtx_hls_host


# MongoDB
app.mongo_host = os.getenv("MONGO_HOST", "localhost")
app.mongo_port = os.getenv("MONGO_PORT", "27017")
app.mongo_user = os.getenv("MONGO_USER", "root")
app.mongo_password = os.getenv("MONGO_PASSWORD", "root")


def get_mongo_uri():
    return f"mongodb://{app.mongo_user}:{app.mongo_password}@{app.mongo_host}:{app.mongo_port}"


@app.get("/")
def index():
    r = requests.get(app.mtx_api_uri + "/v3/paths/list")
    if r.status_code == 200:
        data = r.json()
        if "items" in data:
            res = [x["name"] for x in data["items"]]
            return render_template("index.html", paths=res, live_path=app.streams_redirect)
    return {"error": f"MediaMTX API on {app.mtx_api_uri} not available"}


if __name__ == '__main__':
    app.run()
