import base64

from app.main import bp
from flask import render_template, current_app

from app.models.account import User, StreamingProfile
from app.services.user import is_authenticated, get_current_user


@bp.get("/<streamer>")
def stream_watch(streamer):
    streamer = User.objects(username=streamer).first()
    streamer = StreamingProfile.objects(user=streamer).first()
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}
    config = current_app.config
    return render_template(
        "stream.html",
        streamer=streamer.user.username,
        path=base64.urlsafe_b64encode(streamer.user.username.encode()).decode().replace('=', '~'),
        live_path=config["STREAMS_REDIRECT"],
        chat_initializer=str.join("\n", [service.initializer_code for service in streamer.services]),
        chat_converter=str.join("\n", [service.converter_code for service in streamer.services]),
        authenticated=is_authenticated(),
        user=get_current_user())