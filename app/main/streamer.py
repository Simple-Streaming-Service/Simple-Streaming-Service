

from app.main import bp
from flask import render_template, current_app


@bp.get("/<streamer>")
def stream_watch(streamer):
    config = current_app.config
    return render_template(
        "stream.html",
        streamer=streamer,
        path=streamer,
        live_path=config["STREAMS_REDIRECT"],
        configurator="")