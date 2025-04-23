import base64
import hashlib
import random

from flask import request, json, session

from app import csrf
from app.api import bp
from app.models.account import User, StreamingProfile, Bot
from app.models.service import FrontendChatService
from app.services.user import get_current_user


@bp.post("/user/auth")
def auth():
    csrf.protect()

    data = json.loads(request.data)
    user = User.nodes.first_or_none(username=data["username"])
    if not user:
        user = User.nodes.first_or_none(email=data["username"])
    if not user: return {"ok": False, "error": "User not exists!"}

    if user.password != hashlib.sha512(data["password"].encode()).hexdigest():
        return {"ok": False, "error": "Invalid password!"}
    session['user'] = user.username
    return {"ok": True, "msg": "User log in successfully!"}

@bp.post("/user/exit")
def logout():
    csrf.protect()
    session['user'] = None
    return {"ok": True, "msg": "User log out successfully!"}



@bp.post("/user/create")
def create_user():
    csrf.protect()

    data = json.loads(request.data)
    try:
        user = User(
            username=data["username"],
            email=data["email"],
            password=hashlib.sha512(data["password"].encode()).hexdigest())
        user.save()
    except Exception as e:
        return {"ok": False, "error": "Registration error!", "exception": str(e)}
    return {"ok": True, "msg": "User created successfully!"}

@bp.patch("/user/password/update")
def update_user_password():
    data = json.loads(request.data)
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}
    try:
        if user.password != hashlib.sha512(data["old_password"].encode()).hexdigest():
            return {"ok": False, "error": "Invalid old password!"}
        user.password = hashlib.sha512(data["new_password"].encode()).hexdigest()
        user.save()
    except Exception as e:
        return {"ok": False, "error": "User password changing error!", "exception": str(e)}
    return {"ok": True, "msg": "User password changed successfully!"}

@bp.patch("/user/username/update")
def update_user_username():
    data = json.loads(request.data)
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}
    try:
        user.username = data["username"]
        user.save()
    except Exception as e:
        return {"ok": False, "error": "Username changing error!", "exception": str(e)}
    session['user'] = user.username
    return {"ok": True, "msg": "Username changed successfully!"}

@bp.patch("/user/email/update")
def update_user_email():
    data = json.loads(request.data)
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}
    try:
        user.email = data["email"]
        user.save()
    except Exception as e:
        return {"ok": False, "error": "Email changing error!", "exception": str(e)}
    return {"ok": True, "msg": "Email changed successfully!"}


@bp.post("/user/profile/create")
def create_profile():
    data = json.loads(request.data)
    try:
        user = get_current_user(request.headers)
        if not user: return {"ok": False, "error": "User not authorized!"}
        if "stream_name" not in data:
            return {"ok": False, "error": "Stream without name!"}

        while True:
            token = random.randbytes(10).hex()
            if len(StreamingProfile.nodes.filter(token=token)) == 0:
                break

        streamer = StreamingProfile(
            stream_name=data["stream_name"],
            token=token,
        )
        streamer.save()
        streamer.user.connect(user)
    except Exception as e:
        return {"ok": False, "error": "Streamer profile error!", "exception": str(e)}
    return {"ok": True, "msg": "Streamer profile created successfully!"}

@bp.get("/user/profile/token")
def get_token():
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}
    profile = user.profile.single()
    if not profile: return {"ok": False, "error": "User not a streamer!"}
    return {"ok": True, "token": f"{base64.urlsafe_b64encode(user.username.encode()).decode().replace('=', '~')}?token={profile.token}"}

@bp.post("/user/profile/token/regenerate")
def regenerate_token():
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}
    profile = user.profile.single()
    if not profile: return {"ok": False, "error": "User not a streamer!"}

    while True:
        token = random.randbytes(10).hex()
        if len(StreamingProfile.nodes.filter(token=token)) == 0:
            break

    profile.token = token
    profile.save()
    return {"ok": True, "msg": "Token regenerated successfully!"}

@bp.patch("/user/profile/name/update")
def update_profile_stream_name():
    data = json.loads(request.data)
    try:
        user = get_current_user(request.headers)
        if not user: return {"ok": False, "error": "User not authorized!"}
        if "stream_name" not in data:
            return {"ok": False, "error": "Stream without name!"}
        streamer = user.profile.single()
        streamer.stream_name = data["stream_name"]
        streamer.save()
    except Exception as e:
        return {"ok": False, "error": "Stream name change error!", "exception": str(e)}
    return {"ok": True, "msg": "Stream name changed successfully!"}

@bp.get("/user/profile/services")
def profile_services_list():
    data = json.loads(request.data)
    try:
        user = get_current_user(request.headers)
        if not user: return {"ok": False, "error": "User not authorized!"}
        if "stream_name" not in data:
            return {"ok": False, "error": "Stream without name!"}
        profile = user.profile.single()
        if not profile: return {"ok": False, "error": "Streamer does not exist!"}
        return {"ok": True, "services": [service.name for service in profile.services]}
    except Exception as e:
        return {"ok": False, "error": "Stream service adding error!", "exception": str(e)}

@bp.patch("/user/profile/services/add")
def add_profile_services():
    data = json.loads(request.data)
    try:
        user = get_current_user(request.headers)
        if not user: return {"ok": False, "error": "User not authorized!"}
        if "stream_name" not in data:
            return {"ok": False, "error": "Stream without name!"}
        service = FrontendChatService.nodes.first_or_none(name=data["service_name"])
        if not service: return {"ok": False, "error": "Service does not exist!"}
        profile = user.profile.single()
        if not profile: return {"ok": False, "error": "Streamer does not exist!"}
        profile.services.append(service)
        profile.save()
    except Exception as e:
        return {"ok": False, "error": "Stream service adding error!", "exception": str(e)}
    return {"ok": True, "msg": "Stream service added successfully!"}

@bp.patch("/user/profile/services/remove")
def remove_profile_services():
    data = json.loads(request.data)
    try:
        user = get_current_user(request.headers)
        if not user: return {"ok": False, "error": "User not authorized!"}
        if "stream_name" not in data:
            return {"ok": False, "error": "Stream without name!"}
        service = FrontendChatService.nodes.first_or_none(name=data["service_name"])
        if not service: return {"ok": False, "error": "Service does not exist!"}
        profile = user.profile.single()
        if not profile: return {"ok": False, "error": "Streamer does not exist!"}
        profile.services.remove(service)
        profile.save()
    except Exception as e:
        return {"ok": False, "error": "Stream service removing error!", "exception": str(e)}
    return {"ok": True, "msg": "Stream service removed successfully!"}


@bp.get("/user/subscriptions")
def sub_count():
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}

    return {
        "ok": True,
        "subscriptions": [subscription.user.username for subscription in user.subscribers]
    }

@bp.get("/user/bots")
def user_bots_list():
    user = get_current_user(request.headers)
    if not user: return {"ok": False, "error": "User not authorized!"}

    bots = Bot.nodes.filter(creator__username=user.username)
    return {
        "ok": True,
        "bots": [bot.user.username for bot in bots]
    }



@bp.post("/mediamtx/auth")
def streamer_auth():
#     print(request.data, flush=True)
    data = json.loads(request.data)

    if data["action"] == 'read':
        return {"ok": True, "msg": "Reading permission granted!"}

    user = User.nodes.first_or_none(username=base64.urlsafe_b64decode(data["path"].replace('~', '=').encode()).decode())
    if not user: return {"ok": False, "error": "User not found!"}, 400

    profile = user.profile.single()
    if not profile: return {"ok": False, "error": "Streamer not found!"}, 400

    if f"token={profile.token}" not in data["query"]:
        return {"ok": False, "error": "Invalid token!"}, 400

    if data["action"] not in ['publish', 'playback']:
        return {"ok": False, "error": "Permission denied!"}, 403

    if profile.withCredentials:
        user = User.nodes.first_or_none(username=data["user"])
        if not user:
            user = User.nodes.first_or_none(email=data["user"])
        if not user: return {"ok": False, "error": "Wrong streamer credentials!"}, 401
        if user.password != hashlib.sha512(data["password"].encode()).hexdigest():
            return {"ok": False, "error": "Wrong streamer password!"}, 401
    return {"ok": True, "msg": "Streaming auth successful!"}