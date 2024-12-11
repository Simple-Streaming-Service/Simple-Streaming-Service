import hashlib

from flask import request, json, current_app
from mongoengine import ValidationError

from app.api import bp
from app.models.account import User, StreamingProfile
from app.services.user import get_current_user


@bp.post("/create/user")
def create_user():
    data = json.loads(request.data)
    try:
        user = User(
            username=data["username"],
            email=data["email"],
            password=hashlib.sha512(data["password"].encode()).hexdigest())
        user.validate()
        user.save()
    except ValidationError as e:
        return {"ok": False, "error": "Registration error!", "exception": str(e)}
    return {"ok": True, "msg": "User created successfully!"}

@bp.patch("/update/user/password")
def update_user_password():
    data = json.loads(request.data)
    user = get_current_user(data)
    if not user: return {"ok": False, "error": "User does not exist!"}
    try:
        if user.password != hashlib.sha512(data["old_password"].encode()).hexdigest():
            return {"ok": False, "error": "Invalid old password!"}
        user.password = hashlib.sha512(data["password"].encode()).hexdigest()
        user.validate()
        user.save()
    except ValidationError as e:
        return {"ok": False, "error": "User password changing error!", "exception": str(e)}
    return {"ok": True, "msg": "User password changed successfully!"}

@bp.patch("/update/user/username")
def update_user_username():
    data = json.loads(request.data)
    user = get_current_user(data)
    if not user: return {"ok": False, "error": "User does not exist!"}
    try:
        user.username = data["username"]
        user.validate()
        user.save()
    except ValidationError as e:
        return {"ok": False, "error": "Username changing error!", "exception": str(e)}
    return {"ok": True, "msg": "Username changed successfully!"}

@bp.patch("/update/user/email")
def update_user_email():
    data = json.loads(request.data)
    user = get_current_user(data)
    if not user: return {"ok": False, "error": "User does not exist!"}
    try:
        user.email = data["email"]
        user.validate()
        user.save()
    except ValidationError as e:
        return {"ok": False, "error": "Email changing error!", "exception": str(e)}
    return {"ok": True, "msg": "Email changed successfully!"}


@bp.post("/create/profile")
def create_profile():
    data = json.loads(request.data)
    try:
        user = get_current_user(data)
        if not user: return {"ok": False, "error": "User does not exist!"}
        if "stream_name" not in data:
            return {"ok": False, "error": "Stream without name!"}
        streamer = StreamingProfile(
            user=user,
            stream_name=data["stream_name"])
        streamer.validate()
        streamer.save()
    except ValidationError as e:
        return {"ok": False, "error": "Streamer profile error!", "exception": str(e)}
    return {"ok": True, "msg": "Streamer profile created successfully!"}

@bp.post("/update/profile/name")
def update_profile__stream_name():
    data = json.loads(request.data)
    try:
        user = get_current_user(data)
        if not user: return {"ok": False, "error": "User does not exist!"}
        if "stream_name" not in data:
            return {"ok": False, "error": "Stream without name!"}
        StreamingProfile.objects(user=user).update(name=data["stream_name"])
    except ValidationError as e:
        return {"ok": False, "error": "Stream name change error!", "exception": str(e)}
    return {"ok": True, "msg": "Stream name changed successfully!"}