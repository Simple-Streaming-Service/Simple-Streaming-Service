import base64

import requests

from app.main import bp
from flask import render_template, current_app

from app.models.account import StreamingProfile, User


@bp.get("/")
def index():
    config = current_app.config

    r = requests.get(config["MTX_API_URI"] + "/v3/paths/list")
    if r.status_code == 200:
        print(r.content, flush=True)
        data = r.json()
        if "items" in data:
            streams = []
            for x in data["items"]:
                username = base64.urlsafe_b64decode(x["name"].replace('~', '=').encode()).decode()
                profile = StreamingProfile.objects(user=User.objects(username=username).first()).first()
                if not profile:
                    return {"error": f"Streamer {username} not found!"}
                streams.append({
                    "streamer": username,
                    "name": profile.stream_name
                })

            return render_template("index.html", streams=streams)
    return {"error": f"MediaMTX API on {config["MTX_API_URI"]} not available"}
