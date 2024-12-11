from datetime import datetime

from flask import request, json

from mongoengine import ValidationError

from app.api import bp
from app.models.account import User, StreamingProfile
from app.models.messaging import Message
from app.services.user import get_current_user, get_user

anonym = User.objects(username="Anonym").first()
if not anonym:
    anonym = User(username="Anonym", email="anonym@anonym.com", password="pass")
    anonym.validate()
    anonym.save()


@bp.get("/<streamer>/subscribers/contains")
def is_subscribed(streamer):
    streamer = find_streamer(streamer)
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}
    return {"ok": True, "subscribed": get_user(request.args) in streamer.subscribers}

@bp.get("/<streamer>/subscribers/count")
def sub_count(streamer):
    streamer = find_streamer(streamer)
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}
    return {"ok": True, "count": len(streamer.subscribers)}

@bp.post("/<streamer>/subscribers/subscribe")
def subscribe(streamer):
    streamer = find_streamer(streamer)
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}
    streamer.subscribers.append(get_current_user(request.args))
    streamer.subscribers = list(set(streamer.subscribers))
    streamer.save()
    return {"ok": True, "msg": "Subscribed!"}

@bp.post("/<streamer>/subscribers/unsubscribe")
def unsubscribe(streamer):
    streamer = find_streamer(streamer)
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}
    streamer.subscribers.remove(get_current_user(request.args))
    streamer.save()
    return {"ok": True, "msg": "Unsubscribed!"}


@bp.get("/<streamer>/viewers/connect")
def view_count(streamer):
    streamer = find_streamer(streamer)
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}
    streamer.viewers.append(get_current_user(request.args))
    streamer.viewers = list(set(streamer.viewers))
    streamer.save()
    return {"ok": True, "msg": "Connected!"}

@bp.get("/<streamer>/viewers/disconnect")
def view_count(streamer):
    streamer = find_streamer(streamer)
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}
    streamer.viewers.remove(get_current_user(request.args))
    streamer.save()
    return {"ok": True, "msg": "Disconnected!"}

@bp.get("/<streamer>/viewers/count")
def view_count(streamer):
    streamer = find_streamer(streamer)
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}
    return {"ok": True, "count": len(streamer.viewers)}


@bp.get("/<streamer>/chat/list")
def msg_list(streamer):
    limit = int(request.args.get("limit", 10))

    timestamp = int(request.args.get("timestamp", datetime.now().timestamp()))
    timestamp = datetime.fromtimestamp(timestamp)

    streamer = find_streamer(streamer)
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}

    filtered_messages = [msg for msg in streamer.messages if msg.timestamp <= timestamp]
    sorted_messages = sorted(filtered_messages, key=lambda x: x.timestamp, reverse=True)
    return {
        "ok": True,
        "messages": [
            {
                "user": msg.user.username,
                "content": msg.content,
                "timestamp": msg.timestamp
            } for msg in sorted_messages[:limit]
        ]
    }

@bp.post("/<streamer>/chat/send")
def msg_send(streamer):
    data = request.data
    data = json.loads(data)

    user = get_current_user(data)
    if not user: return {"ok": False, "error": "User does not exist!"}

    timestamp = request.args.get("timestamp", datetime.now().timestamp())
    timestamp = datetime.fromtimestamp(timestamp)
    if "message" not in data: return {"ok": False, "error": "Content field is required!"}

    streamer = find_streamer(streamer)
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}

    try:
        msg = Message(user=user, content=data["message"], timestamp=timestamp)
        msg.validate()
        streamer.messages.append(msg)
        streamer.save()
    except ValidationError as e:
        return {"ok": False, "error": "Message sent error!", "exception": str(e)}
    return {"ok": True, "msg": "Message sent!", "timestamp": timestamp}

def find_streamer(streamer):
    streamer = User.objects(username=streamer).first()
    return StreamingProfile.objects(user=streamer).first()