import requests

from app import app, render_template


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
