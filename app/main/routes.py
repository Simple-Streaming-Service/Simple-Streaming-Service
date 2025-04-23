import base64

import requests

from app.main import bp
from flask import render_template, current_app

from app.models.account import StreamingProfile, User
from app.services.user import is_authenticated, get_current_user


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
                user = User.nodes.first_or_none(username=username)
                if not user: return {"error": f"Streamer {username} not found!"}
                profile = user.profile.single()
                if not profile: return {"error": f"Streamer {username} not found!"}
                streams.append({
                    "streamer": username,
                    "name": profile.stream_name
                })

            return render_template("index.html", streams=streams)
    return {"error": f"MediaMTX API on {config["MTX_API_URI"]} not available"}

@bp.get("/<streamer>")
def stream_watch(streamer):
    user = User.nodes.first_or_none(username=streamer)
    if not user: return {"ok": False, "error": "Streamer does not exist!"}
    streamer = user.profile.single()
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}
    config = current_app.config
    return render_template(
        "stream.html",
        streamer=streamer.user.username,
        stream_name = streamer.stream_name,
        path=base64.urlsafe_b64encode(streamer.user.username.encode()).decode().replace('=', '~'),
        live_path=config["STREAMS_REDIRECT"],
        chat_initializer=str.join("\n", [service.initializer_code for service in streamer.services]),
        chat_converter=str.join("\n", [service.converter_code for service in streamer.services]),
        authenticated=is_authenticated(),
        user=get_current_user())
