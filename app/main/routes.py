import requests

from app.main import bp
from flask import render_template


@bp.get("/")
def index():
    r = requests.get(bp.mtx_api_uri + "/v3/paths/list")
    if r.status_code == 200:
        data = r.json()
        if "items" in data:
            res = [x["name"] for x in data["items"]]
            return render_template("index.html", paths=res, live_path=bp.streams_redirect)
    return {"error": f"MediaMTX API on {bp.mtx_api_uri} not available"}
