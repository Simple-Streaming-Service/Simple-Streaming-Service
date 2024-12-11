from datetime import datetime

from flask import request, json

from mongoengine import ValidationError

from app.api import bp
from app.models.account import User, StreamingProfile
from app.models.messaging import Message


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
