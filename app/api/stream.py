from datetime import datetime, timedelta

from flask import request, json

from mongoengine import ValidationError

from app.api import bp
from app.models.account import User, StreamingProfile
from app.models.messaging import Message
from app.services.user import get_current_user, get_user


@bp.get("/stream/<streamer>/subscribers/contains")
def is_subscribed(streamer):
    """
    Check if the user is subscribed to the streamer or not.
    This endpoint checks if the user is subscribed to a given streamer.
    It checks if the streamer exists and if the user is authorized.
    If the user is not authorized, it returns an error message.
    :param streamer: Streamer username
    :return: JSON response with the subscription status
    """
    streamer = find_streamer(streamer)
    if not streamer:
        return {"ok": False, "error": "Streamer does not exist!"}
    return {"ok": True, "subscribed": get_user(request.args) in streamer.subscribers}


@bp.get("/stream/<streamer>/subscribers/count")
def subscribers_count(streamer):
    """
    Get the number of subscribers for a streamer.
    This endpoint returns the number of subscribers for a given streamer.
    It checks if the streamer exists and returns the count of subscribers.
    If the streamer does not exist, it returns an error message.
    :param streamer: Streamer username
    :return: JSON response with the number of subscribers
    """
    streamer = find_streamer(streamer)
    if not streamer:
        return {"ok": False, "error": "Streamer does not exist!"}
    return {"ok": True, "count": len(streamer.subscribers)}


@bp.post("/stream/<streamer>/subscribers/subscribe")
def subscribe(streamer):
    """
    Subscribe to a streamer.
    This endpoint allows a user to subscribe to a given streamer.
    It checks if the streamer exists and if the user is authorized.
    If the user is not authorized, it returns an error message.
    If the streamer does not exist, it returns an error message.
    :param streamer:
    :return: JSON response with the subscription status
    """
    streamer = find_streamer(streamer)
    if not streamer:
        return {"ok": False, "error": "Streamer does not exist!"}
    user = get_current_user(request.headers)
    if not user:
        return {"ok": False, "error": "User not authorized!"}

    user.subscriptions.append(streamer)
    user.subscriptions = list(set(user.subscriptions))
    user.save()

    streamer.subscribers.append(user)
    streamer.subscribers = list(set(streamer.subscribers))
    streamer.save()

    return {"ok": True, "msg": "Subscribed!"}


@bp.post("/stream/<streamer>/subscribers/unsubscribe")
def unsubscribe(streamer):
    """
    Unsubscribe from a streamer.
    This endpoint allows a user to unsubscribe from a given streamer.
    It checks if the streamer exists and if the user is authorized.
    If the user is not authorized, it returns an error message.
    If the streamer does not exist, it returns an error message.
    :param streamer: Streamer username
    :return: JSON response with the unsubscription status
    """
    streamer = find_streamer(streamer)
    if not streamer:
        return {"ok": False, "error": "Streamer does not exist!"}
    user = get_current_user(request.headers)
    if not user:
        return {"ok": False, "error": "User not authorized!"}

    user.subscriptions.remove(streamer)
    user.save()

    streamer.subscribers.remove(user)
    streamer.save()
    return {"ok": True, "msg": "Unsubscribed!"}


@bp.get("/stream/<streamer>/viewers/connect")
def view_connect(streamer):
    """
    Connect to a streamer's chat.
    This endpoint allows a user to connect to a streamer's chat.
    It checks if the streamer exists and if the user is authorized.
    If the user is not authorized, it returns an error message.
    If the streamer does not exist, it returns an error message.
    :param streamer: Streamer username
    :return: JSON response with the connection status
    """
    streamer = find_streamer(streamer)
    if not streamer:
        return {"ok": False, "error": "Streamer does not exist!"}
    user = get_current_user(request.headers)
    if not user:
        return {"ok": False, "error": "User not authorized!"}
    streamer.viewers.append(user)
    streamer.viewers = list(set(streamer.viewers))
    streamer.save()
    return {"ok": True, "msg": "Connected!"}


@bp.get("/stream/<streamer>/viewers/disconnect")
def view_disconnect(streamer):
    """
    Disconnect from a streamer's chat.
    This endpoint allows a user to disconnect from a streamer's chat.
    It checks if the streamer exists and if the user is authorized.
    If the user is not authorized, it returns an error message.
    If the streamer does not exist, it returns an error message.
    :param streamer: Streamer username
    :return: JSON response with the disconnection status
    """
    streamer = find_streamer(streamer)
    if not streamer:
        return {"ok": False, "error": "Streamer does not exist!"}
    user = get_current_user(request.headers)
    if not user:
        return {"ok": False, "error": "User not authorized!"}
    streamer.viewers.remove(user)
    streamer.save()
    return {"ok": True, "msg": "Disconnected!"}


@bp.get("/stream/<streamer>/viewers/count")
def view_count(streamer):
    """
    Get the number of viewers for a streamer.
    This endpoint returns the number of viewers for a given streamer.
    It checks if the streamer exists and returns the count of viewers.
    If the streamer does not exist, it returns an error message.
    :param streamer: Streamer username
    :return: JSON response with the number of viewers
    """
    streamer = find_streamer(streamer)
    if not streamer:
        return {"ok": False, "error": "Streamer does not exist!"}
    return {"ok": True, "count": len(streamer.viewers)}


@bp.get("/stream/<streamer>/chat/list")
def msg_list(streamer):
    """
    Get the list of messages from a streamer's chat.
    This endpoint retrieves the list of messages from a streamer's chat.
    It checks if the streamer exists and if the user is authorized.
    If the user is not authorized, it returns an error message.
    If the streamer does not exist, it returns an error message.
    :param streamer: Streamer username
    :return: JSON response with the list of messages
    """
    limit = int(request.args.get("limit", 10))

    end_timestamp = int(request.args.get("end_timestamp", datetime.now().timestamp()))
    end_timestamp = datetime.fromtimestamp(end_timestamp)

    start_timestamp = int(request.args.get("start_timestamp", (datetime.now() - timedelta(days=1)).timestamp()))
    start_timestamp = datetime.fromtimestamp(start_timestamp)

    streamer = find_streamer(streamer)
    if not streamer:
        return {"ok": False, "error": "Streamer does not exist!"}

    filtered_messages = [msg for msg in streamer.messages if start_timestamp <= msg.timestamp <= end_timestamp]
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


@bp.post("/stream/<streamer>/chat/send")
def msg_send(streamer):
    """
    Send a message to a streamer's chat.
    This endpoint allows a user to send a message to a streamer's chat.
    It checks if the streamer exists and if the user is authorized.
    If the user is not authorized, it returns an error message.
    If the streamer does not exist, it returns an error message.
    :param streamer: Streamer username
    :return: JSON response with the message status
    """
    data = request.data
    data = json.loads(data)
    user = get_current_user(request.headers)
    if not user:
        return {"ok": False, "error": "User not authorized!"}

    timestamp = request.args.get("timestamp", datetime.now().timestamp())
    timestamp = datetime.fromtimestamp(timestamp)
    if "message" not in data:
        return {"ok": False, "error": "Content field is required!"}

    streamer = find_streamer(streamer)
    if not streamer:
        return {"ok": False, "error": "Streamer does not exist!"}

    try:
        msg = Message(user=user, content=data["message"], timestamp=timestamp)
        msg.validate()
        streamer.messages.append(msg)
        streamer.save()
    except ValidationError as e:
        return {"ok": False, "error": "Message sent error!", "exception": str(e)}
    return {"ok": True, "msg": "Message sent!", "timestamp": timestamp}


def find_streamer(streamer):
    """
    Find a streamer by username.
    This function retrieves a streamer from the database using the provided username.
    It checks if the streamer exists and returns the streamer object.
    :param streamer: Streamer username
    :return: Streamer object or None
    """
    streamer = User.objects(username=streamer).first()
    streamer = StreamingProfile.objects(user=streamer).first()
    return streamer
