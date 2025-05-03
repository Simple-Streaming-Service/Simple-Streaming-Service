import base64

from flask import render_template, current_app

from app.main import bp
from app.models.account import User
from app.services.user import is_authenticated, get_current_user, get_user


@bp.get("/<streamer>")
def stream_watch(streamer):
    user = User.nodes.first_or_none(username=streamer)
    if not user: return {"ok": False, "error": "Streamer does not exist!"}
    streamer = user.profile.single()
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}
    config = current_app.config
    return render_template(
        "stream.html",
        authenticated=is_authenticated(),
        user=get_current_user(),
        streamer=user.username,
        stream_name = streamer.stream_name,
        path=base64.urlsafe_b64encode(user.username.encode()).decode().replace('=', '~'),
        live_path=config["STREAMS_REDIRECT"])


@bp.get("/<streamer>/chat")
def stream_chat(streamer):
    user = User.nodes.first_or_none(username=streamer)
    if not user: return {"ok": False, "error": "Streamer does not exist!"}
    streamer = user.profile.single()
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}
    return render_template(
        "chat.html",
        authenticated=is_authenticated(),
        user=get_current_user(),
        streamer=user.username,
        chat_initializer=str.join("\n", [service.initializer_code for service in streamer.services]),
        chat_converter=str.join("\n", [service.formatting_code for service in streamer.services]))


@bp.context_processor
def utility_processor():
    return dict(
        is_authenticated=is_authenticated,
        get_current_user=get_current_user,
        get_user=get_user
    )