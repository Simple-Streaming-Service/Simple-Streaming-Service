import requests

from app.main import bp
from flask import render_template, current_app


@bp.get("/")
def index():
    config = current_app.config

    r = requests.get(config["MTX_API_URI"] + "/v3/paths/list")
    if r.status_code == 200:
        data = r.json()
        if "items" in data:
            res = [x["name"] for x in data["items"]]
            return render_template("index.html", paths=res)
    return {"error": f"MediaMTX API on {config["MTX_API_URI"]} not available"}
