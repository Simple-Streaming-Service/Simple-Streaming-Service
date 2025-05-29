from datetime import datetime, timedelta, timezone

from flask import request, json

from app.api import bp
from app.models.account import User, StreamingProfile
from app.models.messaging import Message
from app.services.graphql import make_query
from app.services.user import get_current_user, get_user, find_streamer


@bp.get("/stream/<streamer>/subscribers/contains")
def is_subscribed(streamer):
    streamer = find_streamer(streamer)
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}
    return {"ok": True, "subscribed": get_user(request.args) in streamer.subscribers}

@bp.get("/stream/<streamer>/subscribers/count")
def subscribers_count(streamer):
    streamer = find_streamer(streamer)
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}
    return {"ok": True, "count": len(streamer.subscribers)}

@bp.post("/stream/<streamer>/subscribers/subscribe")
def subscribe(streamer):
    streamer = find_streamer(streamer)
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}
    streamer.subscribers.connect(user)

    return {"ok": True, "msg": "Subscribed!"}

@bp.post("/stream/<streamer>/subscribers/unsubscribe")
def unsubscribe(streamer):
    streamer = find_streamer(streamer)
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}
    streamer.subscribers.disconnect(user)
    return {"ok": True, "msg": "Unsubscribed!"}


@bp.get("/stream/<streamer>/viewers/count")
def view_count(streamer):
    streamer = find_streamer(streamer)
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}
    return {"ok": True, "count": streamer.viewer_count}


@bp.get("/stream/<streamer>/chat/list")
def msg_list(streamer):
    limit = int(request.args.get("limit", 10))

    end_timestamp = int(request.args.get("end_timestamp", datetime.now().timestamp()))
    end_timestamp = datetime.fromtimestamp(end_timestamp, tz=timezone.utc)


    start_timestamp = int(request.args.get("start_timestamp", (datetime.now() - timedelta(days=1)).timestamp()))
    start_timestamp = datetime.fromtimestamp(start_timestamp, tz=timezone.utc)

    streamer = find_streamer(streamer)
    if not streamer: return {"ok": False, "error": "Streamer does not exist!"}

    filtered_messages = [
        msg for msg in streamer.messages.all()
        if start_timestamp <= msg.timestamp <= end_timestamp
    ]
    sorted_messages = sorted(filtered_messages, key=lambda x: x.timestamp, reverse=True)
    return {
        "ok": True,
        "messages": [
            {
                "user": msg.author.single().username,
                "content": msg.content,
                "timestamp": msg.timestamp
            } for msg in sorted_messages[:limit]
        ]
    }

@bp.post("/stream/<streamer>/chat/send")
def msg_send(streamer):
    data = request.data
    data = json.loads(data)
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}

    timestamp = request.args.get("timestamp", datetime.now().timestamp())
    timestamp = datetime.fromtimestamp(timestamp)
    if "message" not in data: return {"ok": False, "error": "Content field is required!"}
    try:
        result = make_query(
            """
                mutation SendMessage {
                    sendMessage(streamer: $streamer, message: $message, timestamp: $timestamp) {
                        ok
                        error
                        msg
                        timestamp
                    }
                }
            """,
            {
                "streamer": streamer,
                "message": data["message"],
                "timestamp": timestamp.isoformat()
            },
            "http://localhost:5001",
            request.headers
        )
        if "ok" in result and result["ok"]:
            return {"ok": True, "msg": result["msg"] | "Message sent!", "timestamp": timestamp}
        else:
            return {"ok": False, "error": result["error"] | "Message sending failed!"}
    except:
        return {"ok": False, "error": "Message sending failed!"}
