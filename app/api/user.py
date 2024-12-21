import hashlib

from flask import request, json, session

from app.api import bp
from app.models.account import User, StreamingProfile
from app.models.service import FrontendChatService
from app.services.user import get_current_user


@bp.post("/user/create")
def create_user():
    data = json.loads(request.data)
    try:
        user = User(
            username=data["username"],
            email=data["email"],
            password=hashlib.sha512(data["password"].encode()).hexdigest())
        user.validate()
        user.save()
    except Exception as e:
        return {"ok": False, "error": "Registration error!", "exception": str(e)}
    return {"ok": True, "msg": "User created successfully!"}

@bp.patch("/user/update/password")
def update_user_password():
    data = json.loads(request.data)
    user = get_current_user()
    if not user: return {"ok": False, "error": "User not authorized!"}
    try:
        if user.password != hashlib.sha512(data["old_password"].encode()).hexdigest():
            return {"ok": False, "error": "Invalid old password!"}
        user.password = hashlib.sha512(data["password"].encode()).hexdigest()
        user.validate()
        user.save()
    except Exception as e:
        return {"ok": False, "error": "User password changing error!", "exception": str(e)}
    return {"ok": True, "msg": "User password changed successfully!"}

@bp.patch("/user/update/username")
def update_user_username():
    data = json.loads(request.data)
    user = get_current_user()
    if not user: return {"ok": False, "error": "User not authorized!"}
    try:
        user.username = data["username"]
        user.validate()
        user.save()
    except Exception as e:
        return {"ok": False, "error": "Username changing error!", "exception": str(e)}
    return {"ok": True, "msg": "Username changed successfully!"}

@bp.patch("/user/update/email")
def update_user_email():
    data = json.loads(request.data)
    user = get_current_user()
    if not user: return {"ok": False, "error": "User not authorized!"}
    try:
        user.email = data["email"]
        user.validate()
        user.save()
    except Exception as e:
        return {"ok": False, "error": "Email changing error!", "exception": str(e)}
    return {"ok": True, "msg": "Email changed successfully!"}


@bp.post("/user/create/profile")
def create_profile():
    data = json.loads(request.data)
    try:
        user = get_current_user()
        if not user: return {"ok": False, "error": "User not authorized!"}
        if "stream_name" not in data:
            return {"ok": False, "error": "Stream without name!"}
        streamer = StreamingProfile(
            user=user,
            stream_name=data["stream_name"])
        streamer.validate()
        streamer.save()
    except Exception as e:
        return {"ok": False, "error": "Streamer profile error!", "exception": str(e)}
    return {"ok": True, "msg": "Streamer profile created successfully!"}

@bp.patch("/user/update/profile/name")
def update_profile_stream_name():
    data = json.loads(request.data)
    try:
        user = get_current_user()
        if not user: return {"ok": False, "error": "User not authorized!"}
        if "stream_name" not in data:
            return {"ok": False, "error": "Stream without name!"}
        StreamingProfile.objects(user=user).update(stream_name=data["stream_name"])
    except Exception as e:
        return {"ok": False, "error": "Stream name change error!", "exception": str(e)}
    return {"ok": True, "msg": "Stream name changed successfully!"}



@bp.get("/user/profile/services")
def profile_services_list():
    data = json.loads(request.data)
    try:
        user = get_current_user()
        if not user: return {"ok": False, "error": "User not authorized!"}
        if "stream_name" not in data:
            return {"ok": False, "error": "Stream without name!"}
        profile = StreamingProfile.objects(user=user).first()
        if not profile: return {"ok": False, "error": "Streamer does not exist!"}
        return {"ok": True, "services": [service.name for service in profile.services]}
    except Exception as e:
        return {"ok": False, "error": "Stream service adding error!", "exception": str(e)}

@bp.patch("/user/profile/services/add")
def add_profile_services():
    data = json.loads(request.data)
    try:
        user = get_current_user()
        if not user: return {"ok": False, "error": "User not authorized!"}
        if "stream_name" not in data:
            return {"ok": False, "error": "Stream without name!"}
        service = FrontendChatService.objects(name=data["service_name"]).first()
        if not service: return {"ok": False, "error": "Service does not exist!"}
        profile = StreamingProfile.objects(user=user).first()
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
        user = get_current_user()
        if not user: return {"ok": False, "error": "User not authorized!"}
        if "stream_name" not in data:
            return {"ok": False, "error": "Stream without name!"}
        service = FrontendChatService.objects(name=data["service_name"]).first()
        if not service: return {"ok": False, "error": "Service does not exist!"}
        profile = StreamingProfile.objects(user=user).first()
        if not profile: return {"ok": False, "error": "Streamer does not exist!"}
        profile.services.remove(service)
        profile.save()
    except Exception as e:
        return {"ok": False, "error": "Stream service removing error!", "exception": str(e)}
    return {"ok": True, "msg": "Stream service removed successfully!"}


@bp.get("/user/subscriptions")
def sub_count():
    user = get_current_user()
    return {
        "ok": True,
        "subscriptions": [ subscription.user.username for subscription in user.subscriptions ]
    }

@bp.post("/user/auth")
def auth():
    data = json.loads(request.data)
    user = User.objects(username=data["user"]).first()
    if not user:
        user = User.objects(email=data["user"]).first()
    if not user: return {"ok": False, "error": "User not exists!"}

    if user.password != hashlib.sha512(data["password"].encode()).hexdigest():
        return {"ok": False, "error": "Invalid password!"}
    session['user_id'] = user.id