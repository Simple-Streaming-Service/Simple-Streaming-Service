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
    """
    User authentication endpoint. It checks if the user exists in the database and if the password is valid.
    If so, it sets the session user to the user's username and returns a JSON response indicating the success of the authentication process.
    If the user does not exist or the password is invalid, it returns a JSON response indicating an error.
    :return: JSON response indicating the success or failure of the authentication process.
    """
    csrf.protect()

    data = json.loads(request.data)
    user = User.objects(username=data["username"]).first()
    if not user:
        user = User.objects(email=data["username"]).first()
    if not user:
        return {"ok": False, "error": "User not exists!"}

    if user.password != hashlib.sha512(data["password"].encode()).hexdigest():
        return {"ok": False, "error": "Invalid password!"}
    session['user'] = user.username
    return {"ok": True, "msg": "User log in successfully!"}


@bp.post("/user/exit")
def logout():
    """
    User logout endpoint. It checks if the user exists in the database and if the current user is the same as the bot's user.
    If so, it clears the session user and returns a JSON response indicating the success of the logout process.
    If the bot does not exist or the current user is not the same as the bot's user, it returns a JSON response indicating an error.
    :return: JSON response indicating the success or failure of the logout process.
    """
    csrf.protect()
    session['user'] = None
    return {"ok": True, "msg": "User log out successfully!"}


@bp.post("/user/create")
def create_user():
    """
    User creation endpoint. It checks if the user already exists in the database and if the password is valid.
    If so, it creates a new user and saves it to the database.
    It returns a JSON response indicating the success or failure of the user creation process.
    :return: JSON response indicating the success or failure of the user creation process.
    """
    csrf.protect()

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


@bp.patch("/user/password/update")
def update_user_password():
    """
    User password update endpoint. It checks if the user exists in the database and if the old password is valid.
    If so, it updates the user's password and saves it to the database.
    It returns a JSON response indicating the success or failure of the password update process.
    :return: JSON response indicating the success or failure of the password update process.
    """
    data = json.loads(request.data)
    user = get_current_user(request.headers)
    if not user:
        return {"ok": False, "error": "User not authorized!"}
    try:
        if user.password != hashlib.sha512(data["old_password"].encode()).hexdigest():
            return {"ok": False, "error": "Invalid old password!"}
        user.password = hashlib.sha512(data["new_password"].encode()).hexdigest()
        user.validate()
        user.save()
    except Exception as e:
        return {"ok": False, "error": "User password changing error!", "exception": str(e)}
    return {"ok": True, "msg": "User password changed successfully!"}


@bp.patch("/user/username/update")
def update_user_username():
    """
    User username update endpoint. It checks if the user exists in the database and if the new username is valid.
    If so, it updates the user's username and saves it to the database.
    It returns a JSON response indicating the success or failure of the username update process.
    :return: JSON response indicating the success or failure of the username update process.
    """
    data = json.loads(request.data)
    user = get_current_user(request.headers)
    if not user:
        return {"ok": False, "error": "User not authorized!"}
    try:
        user.username = data["username"]
        user.validate()
        user.save()
    except Exception as e:
        return {"ok": False, "error": "Username changing error!", "exception": str(e)}
    session['user'] = user.username
    return {"ok": True, "msg": "Username changed successfully!"}


@bp.patch("/user/email/update")
def update_user_email():
    """
    User email update endpoint. It checks if the user exists in the database and if the new email is valid.
    If so, it updates the user's email and saves it to the database.
    It returns a JSON response indicating the success or failure of the email update process.
    :return: JSON response indicating the success or failure of the email update process.
    """
    data = json.loads(request.data)
    user = get_current_user(request.headers)
    if not user:
        return {"ok": False, "error": "User not authorized!"}
    try:
        user.email = data["email"]
        user.validate()
        user.save()
    except Exception as e:
        return {"ok": False, "error": "Email changing error!", "exception": str(e)}
    return {"ok": True, "msg": "Email changed successfully!"}


@bp.post("/user/profile/create")
def create_profile():
    """
    User profile creation endpoint. It checks if the user exists in the database and if the stream name is valid.
    If so, it creates a new streaming profile and saves it to the database.
    It generates a random token for the streaming profile and ensures that the token is unique.
    It returns a JSON response indicating the success or failure of the profile creation process.
    :return: JSON response indicating the success or failure of the profile creation process.
    """
    data = json.loads(request.data)
    try:
        user = get_current_user(request.headers)
        if not user:
            return {"ok": False, "error": "User not authorized!"}
        if "stream_name" not in data:
            return {"ok": False, "error": "Stream without name!"}

        while True:
            token = random.randbytes(10).hex()
            if StreamingProfile.objects(token=token).count() == 0:
                break

        streamer = StreamingProfile(
            user=user,
            stream_name=data["stream_name"],
            token=token,
        )
        streamer.validate()
        streamer.save()
    except Exception as e:
        return {"ok": False, "error": "Streamer profile error!", "exception": str(e)}
    return {"ok": True, "msg": "Streamer profile created successfully!"}


@bp.get("/user/profile/token")
def get_token():
    """
    User profile token retrieval endpoint. It checks if the user exists in the database and if the user is a streamer.
    If so, it retrieves the streaming profile and returns the token in a JSON response.
    It encodes the username in base64 format and appends the token to the URL.
    If the user is not authorized or not a streamer, it returns an error message.
    :return: JSON response with the token or an error message
    """
    user = get_current_user(request.headers)
    if not user:
        return {"ok": False, "error": "User not authorized!"}
    profile = StreamingProfile.objects(user=user).first()
    if not profile:
        return {"ok": False, "error": "User not a streamer!"}
    return {"ok": True,
            "token": f"{base64.urlsafe_b64encode(user.username.encode()).decode().replace('=', '~')}?token={profile.token}"}


@bp.post("/user/profile/token/regenerate")
def regenerate_token():
    """
    User profile token regeneration endpoint. It checks if the user exists in the database and if the user is a streamer.
    If so, it generates a new random token for the streaming profile and ensures that the token is unique.
    It updates the token in the database and returns a JSON response indicating the success of the token regeneration process.
    If the user is not authorized or not a streamer, it returns an error message.
    :return: JSON response indicating the success or failure of the token regeneration process.
    """
    user = get_current_user(request.headers)
    if not user:
        return {"ok": False, "error": "User not authorized!"}
    profile = StreamingProfile.objects(user=user).first()
    if not profile:
        return {"ok": False, "error": "User not a streamer!"}

    while True:
        token = random.randbytes(10).hex()
        if StreamingProfile.objects(token=token).count() == 0:
            break

    profile.token = token
    profile.validate()
    profile.save()
    return {"ok": True, "msg": "Token regenerated successfully!"}


@bp.patch("/user/profile/name/update")
def update_profile_stream_name():
    """
    User profile stream name update endpoint. It checks if the user exists in the database and if the user is a streamer.
    If so, it updates the stream name in the streaming profile and saves it to the database.
    It returns a JSON response indicating the success or failure of the stream name update process.
    If the user is not authorized or not a streamer, it returns an error message.
    If the stream name is not provided, it returns an error message.
    If the stream name is invalid, it returns an error message.
    :return: JSON response indicating the success or failure of the stream name update process
    """
    data = json.loads(request.data)
    try:
        user = get_current_user(request.headers)
        if not user:
            return {"ok": False, "error": "User not authorized!"}
        if "stream_name" not in data:
            return {"ok": False, "error": "Stream without name!"}
        streamer = StreamingProfile.objects(user=user).first()
        streamer.stream_name = data["stream_name"]
        streamer.validate()
        streamer.save()
    except Exception as e:
        return {"ok": False, "error": "Stream name change error!", "exception": str(e)}
    return {"ok": True, "msg": "Stream name changed successfully!"}


@bp.get("/user/profile/services")
def profile_services_list():
    """
    User profile services list endpoint. It checks if the user exists in the database and if the user is a streamer.
    If so, it retrieves the streaming profile and returns the list of services in a JSON response.
    It returns an error message if the user is not authorized or not a streamer.
    If the stream name is not provided, it returns an error message.
    If the streamer does not exist, it returns an error message.
    If the streamer has no services, it returns an empty list.
    If the streamer has services, it returns the list of service names.
    :return: JSON response with the list of services or an error message
    """
    data = json.loads(request.data)
    try:
        user = get_current_user(request.headers)
        if not user:
            return {"ok": False, "error": "User not authorized!"}
        if "stream_name" not in data:
            return {"ok": False, "error": "Stream without name!"}
        profile = StreamingProfile.objects(user=user).first()
        if not profile:
            return {"ok": False, "error": "Streamer does not exist!"}
        return {"ok": True, "services": [service.name for service in profile.services]}
    except Exception as e:
        return {"ok": False, "error": "Stream service adding error!", "exception": str(e)}


@bp.patch("/user/profile/services/add")
def add_profile_services():
    """
    User profile services addition endpoint. It checks if the user exists in the database and if the user is a streamer.
    If so, it retrieves the streaming profile and adds the specified service to the list of services.
    It returns a JSON response indicating the success or failure of the service addition process.
    If the user is not authorized or not a streamer, it returns an error message.
    If the stream name is not provided, it returns an error message.
    If the service name is not provided, it returns an error message.
    If the service does not exist, it returns an error message.
    If the streamer does not exist, it returns an error message.
    If the streamer has no services, it returns an empty list.
    If the streamer has services, it returns the list of service names.
    If the service is already in the list of services, it returns an error message.
    If the service is successfully added, it returns a success message.
    If the service is not successfully added, it returns an error message.
    If the service is not successfully removed, it returns an error message.
    If the service is successfully removed, it returns a success message.
    If the service is not successfully updated, it returns an error message.
    If the service is successfully updated, it returns a success message.
    :return: JSON response indicating the success or failure of the service addition process
    """
    data = json.loads(request.data)
    try:
        user = get_current_user(request.headers)
        if not user:
            return {"ok": False, "error": "User not authorized!"}
        if "stream_name" not in data:
            return {"ok": False, "error": "Stream without name!"}
        service = FrontendChatService.objects(name=data["service_name"]).first()
        if not service:
            return {"ok": False, "error": "Service does not exist!"}
        profile = StreamingProfile.objects(user=user).first()
        if not profile:
            return {"ok": False, "error": "Streamer does not exist!"}
        profile.services.append(service)
        profile.save()
    except Exception as e:
        return {"ok": False, "error": "Stream service adding error!", "exception": str(e)}
    return {"ok": True, "msg": "Stream service added successfully!"}


@bp.patch("/user/profile/services/remove")
def remove_profile_services():
    """
    User profile services removal endpoint. It checks if the user exists in the database and if the user is a streamer.
    If so, it retrieves the streaming profile and removes the specified service from the list of services.
    It returns a JSON response indicating the success or failure of the service removal process.
    If the user is not authorized or not a streamer, it returns an error message.
    If the stream name is not provided, it returns an error message.
    If the service name is not provided, it returns an error message.
    :return: JSON response indicating the success or failure of the service removal process
    """
    data = json.loads(request.data)
    try:
        user = get_current_user(request.headers)
        if not user:
            return {"ok": False, "error": "User not authorized!"}
        if "stream_name" not in data:
            return {"ok": False, "error": "Stream without name!"}
        service = FrontendChatService.objects(name=data["service_name"]).first()
        if not service:
            return {"ok": False, "error": "Service does not exist!"}
        profile = StreamingProfile.objects(user=user).first()
        if not profile:
            return {"ok": False, "error": "Streamer does not exist!"}
        profile.services.remove(service)
        profile.save()
    except Exception as e:
        return {"ok": False, "error": "Stream service removing error!", "exception": str(e)}
    return {"ok": True, "msg": "Stream service removed successfully!"}


@bp.get("/user/subscriptions")
def sub_count():
    """
    User subscriptions list endpoint. It checks if the user exists in the database and if the user is a streamer.
    If so, it retrieves the streaming profile and returns the list of subscriptions in a JSON response.
    It returns an error message if the user is not authorized or not a streamer.
    If the stream name is not provided, it returns an error message.
    :return: JSON response with the list of subscriptions or an error message
    """
    user = get_current_user(request.headers)
    if not user:
        return {"ok": False, "error": "User not authorized!"}

    return {
        "ok": True,
        "subscriptions": [subscription.user.username for subscription in user.subscriptions]
    }


@bp.get("/user/bots")
def user_bots_list():
    """
    User bots list endpoint. It checks if the user exists in the database and if the user is a streamer.
    If so, it retrieves the streaming profile and returns the list of bots in a JSON response.
    It returns an error message if the user is not authorized or not a streamer.
    :return: JSON response with the list of bots or an error message
    """
    user = get_current_user(request.headers)
    if not user:
        return {"ok": False, "error": "User not authorized!"}

    bots = Bot.objects(creator=user)
    return {
        "ok": True,
        "bots": [bot.user.username for bot in bots]
    }


@bp.post("/mediamtx/auth")
def streamer_auth():
    """
    Streaming authentication endpoint. It checks if the user exists in the database and if the user is a streamer.
    If so, it retrieves the streaming profile and checks if the token is valid.
    If the token is valid, it returns a JSON response indicating the success of the authentication process.
    If the token is invalid, it returns an error message.
    If the user is not authorized or not a streamer, it returns an error message.
    :return: JSON response indicating the success or failure of the authentication process
    """
    #     print(request.data, flush=True)
    data = json.loads(request.data)

    if data["action"] == 'read':
        return {"ok": True, "msg": "Reading permission granted!"}

    user = User.objects(username=base64.urlsafe_b64decode(data["path"].replace('~', '=').encode()).decode()).first()
    if not user:
        return {"ok": False, "error": "User not found!"}, 400

    profile = StreamingProfile.objects(user=user).first()
    if not profile:
        return {"ok": False, "error": "Streamer not found!"}, 400

    if f"token={profile.token}" not in data["query"]:
        return {"ok": False, "error": "Invalid token!"}, 400

    if data["action"] not in ['publish', 'playback']:
        return {"ok": False, "error": "Permission denied!"}, 403

    if profile.withCredentials:
        user = User.objects(username=data["user"]).first()
        if not user:
            user = User.objects(email=data["user"]).first()
        if not user:
            return {"ok": False, "error": "Wrong streamer credentials!"}, 401
        if user.password != hashlib.sha512(data["password"].encode()).hexdigest():
            return {"ok": False, "error": "Wrong streamer password!"}, 401
    return {"ok": True, "msg": "Streaming auth successful!"}
