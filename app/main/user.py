import requests

from app.main import bp
from flask import render_template, current_app


@bp.get("/<user>")
def stream_watch(user):
    config = current_app.config
    return render_template("stream.html", path=user, live_path=config["STREAMS_REDIRECT"])

@bp.get("/<user>/msg/list")
def msg_list():
    pass
@bp.post("/<user>/msg/send")
def msg_send():
    pass
