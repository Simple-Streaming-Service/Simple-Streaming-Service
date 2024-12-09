from datetime import datetime

from mongoengine import ValidationError

from app.main import bp
from flask import render_template, current_app, request, json

from app.models.account import User, StreamingProfile
from app.models.messaging import Message


@bp.get("/<streamer>")
def stream_watch(streamer):
    config = current_app.config
    return render_template(
        "stream.html",
        streamer=streamer,
        path=streamer,
        live_path=config["STREAMS_REDIRECT"])

@bp.post("/<streamer>/create")
def create(streamer):
    data = request.data
    data = json.loads(data)
    try:
        user = User(username=streamer, email=data["email"], password=data["password"])
        user.validate()
        user.save()
    except ValidationError as e:
        return {"ok": False, "error": "Registration error!", "exception": str(e)}
    return {"ok": True, "msg": "User created successfully!"}

@bp.post("/<streamer>/stream")
def stream(streamer):
    try:
        streamer = User.objects(username=streamer).first()
        if not streamer: return {"ok": False, "error": "User does not exist!"}
        if "stream_name" not in request.args:
            return {"ok": False, "error": "Stream without name!"}
        streamer = StreamingProfile(
            user=streamer,
            stream_name=request.args.get("stream_name"))
        streamer.validate()
        streamer.save()
    except ValidationError as e:
        return {"ok": False, "error": "Streamer profile error!", "exception": str(e)}
    return {"ok": True, "msg": "User created successfully!"}

@bp.get("/<streamer>/chat/list")
def msg_list(streamer):
    limit = int(request.args.get("limit", 10))

    timestamp = int(request.args.get("timestamp", datetime.now().timestamp()))
    timestamp = datetime.fromtimestamp(timestamp)

    streamer = User.objects(username=streamer).first()
    streamer = StreamingProfile.objects(user=streamer).first()
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}

    filtered_messages = [msg for msg in streamer.messages if msg.timestamp <= timestamp]
    sorted_messages = sorted(filtered_messages, key=lambda x: x.timestamp, reverse=True)
    return [
        {
            "user": msg.user.username,
            "content": msg.content,
            "timestamp": msg.timestamp
        } for msg in sorted_messages[:limit]
    ]

anonym = User.objects(username="Anonym").first()
if not anonym:
    anonym = User(username="Anonym", email="anonym@anonym.com", password="pass")
    anonym.validate()
    anonym.save()

@bp.post("/<streamer>/chat/send")
def msg_send(streamer):
    data = request.data
    data = json.loads(data)

    user = anonym # TODO: Get user
    if not user: return {"ok": False, "error": "User does not exist!"}

    timestamp = request.args.get("timestamp", datetime.now().timestamp())
    timestamp = datetime.fromtimestamp(timestamp)
    if "message" not in data: return {"ok": False, "error": "Content field is required!"}

    streamer = User.objects(username=streamer).first()
    streamer = StreamingProfile.objects(user=streamer).first()
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}

    try:
        msg = Message(user=user, content=data["message"], timestamp=timestamp)
        msg.validate()
        streamer.messages.append(msg)
        streamer.save()
    except ValidationError as e:
        return {"ok": False, "error": "Message sent error!", "exception": str(e)}
    return {"ok": True, "msg": "Message sent!", "timestamp": timestamp}
