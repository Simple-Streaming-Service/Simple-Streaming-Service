import hashlib
import random

from flask import request, json, session

from app.api import bp
from app.models.account import User, Bot
from app.services.user import get_current_user


@bp.post("/bot/auth")
def bot_auth():
    """
    Bot authentication endpoint. It checks if the bot exists in the database and sets the session user to the bot's username.
    It returns a JSON response indicating the success or failure of the authentication process.
    :return: JSON response indicating the success or failure of the authentication process.
    """

    bot = Bot.objects(token=request.headers.get("X-Api-Key", None)).first()
    if not bot:
        return {"ok": False, "error": "Bot not exists!"}

    session['user'] = bot.user.username
    return {"ok": True, "msg": "User log in successfully!"}


@bp.post("/bot/exit")
def bot_logout():
    """
    Bot logout endpoint. It checks if the bot exists in the database and if the current user is the same as the bot's user.
    If so, it clears the session user and returns a JSON response indicating the success of the logout process.
    If the bot does not exist or the current user is not the same as the bot's user, it returns a JSON response indicating an error.
    :return: JSON response indicating the success or failure of the logout process.
    """
    bot = Bot.objects(token=request.headers.get("X-Api-Key", None)).first()
    if not bot:
        return {"ok": False, "error": "Bot not exists!"}
    if get_current_user() != bot.user:
        return {"ok": False, "error": "Wrong bot credentials!"}
    session['user'] = None
    return {"ok": True, "msg": "Bot log out successfully!"}


@bp.post("/bot/create")
def bot_create():
    """
    Bot creation endpoint. It checks if the user is authorized and if the bot user exists in the database.
    If so, it checks if the bot user password is valid. If all checks pass, it generates a unique token for the bot and saves it to the database.
    It returns a JSON response indicating the success or failure of the bot creation process.
    :return: JSON response indicating the success or failure of the bot creation process.
    """
    data = json.loads(request.data)
    user = get_current_user()
    if not user:
        return {"ok": False, "error": "User not authorized!"}

    bot_user = User.objects(username=data["bot_username"]).first()
    if not bot_user:
        return {"ok": False, "error": "Bot user not exists!"}
    try:
        if bot_user.password != hashlib.sha512(data["bot_password"].encode()).hexdigest():
            return {"ok": False, "error": "Bot user password invalid!"}

        while True:
            token = random.randbytes(32).hex()
            if Bot.objects(token=token).count() == 0:
                break
        bot = Bot(
            user=bot_user,
            creator=user,
            token=token
        )
        bot.validate()
        bot.save()
    except Exception as e:
        return {"ok": False, "error": "Bot creation error!", "exception": str(e)}

    return {"ok": True, "msg": "Bot created successfully!"}


@bp.delete("/bot/remove")
def bot_remove():
    """
    Bot removal endpoint. It checks if the user is authorized and if the bot user exists in the database.
    If so, it checks if the bot user password is valid. If all checks pass, it deletes the bot from the database.
    It returns a JSON response indicating the success or failure of the bot removal process.
    :return: JSON response indicating the success or failure of the bot removal process.
    """

    data = json.loads(request.data)
    user = get_current_user()
    if not user:
        return {"ok": False, "error": "User not authorized!"}

    bot_user = User.objects(username=data["bot_username"]).first()
    if not bot_user:
        return {"ok": False, "error": "Bot user not exists!"}
    try:
        if bot_user.password != hashlib.sha512(data["bot_password"].encode()).hexdigest():
            return {"ok": False, "error": "Bot user password invalid!"}
        Bot.objects(user=bot_user, creator=user).delete()
    except Exception as e:
        return {"ok": False, "error": "Bot removing error!", "exception": str(e)}

    return {"ok": True, "msg": "Bot removed successfully!"}


@bp.post("/bot/token")
def bot_get_token():
    """
    Bot token retrieval endpoint. It checks if the user is authorized and if the bot user exists in the database.
    If so, it checks if the bot user password is valid. If all checks pass, it retrieves the bot token from the database.
    It returns a JSON response indicating the success or failure of the bot token retrieval process.
    :return: JSON response indicating the success or failure of the bot token retrieval process.
    """
    data = json.loads(request.data)
    user = get_current_user()
    if not user:
        return {"ok": False, "error": "User not authorized!"}

    bot_user = User.objects(username=data["bot_username"]).first()
    if not bot_user:
        return {"ok": False, "error": "Bot user not exists!"}

    if bot_user.password != hashlib.sha512(data["bot_password"].encode()).hexdigest():
        return {"ok": False, "error": "Bot user password invalid!"}

    bot = Bot.objects(user=bot_user, creator=user).first()
    if not bot:
        return {"ok": False, "error": "Bot not exists!"}
    return {"ok": True, "token": bot.token}


@bp.patch("/bot/token/regenerate")
def bot_regenerate_token():
    """
    Bot token regeneration endpoint. It checks if the user is authorized and if the bot user exists in the database.
    If so, it checks if the bot user password is valid. If all checks pass, it generates a new unique token for the bot and saves it to the database.
    It returns a JSON response indicating the success or failure of the bot token regeneration process.
    :return: JSON response indicating the success or failure of the bot token regeneration process.
    """
    data = json.loads(request.data)
    user = get_current_user()
    if not user:
        return {"ok": False, "error": "User not authorized!"}

    bot_user = User.objects(username=data["bot_username"]).first()
    if not bot_user:
        return {"ok": False, "error": "Bot user not exists!"}

    if bot_user.password != hashlib.sha512(data["bot_password"].encode()).hexdigest():
        return {"ok": False, "error": "Bot user password invalid!"}

    bot = Bot.objects(user=bot_user, creator=user).first()
    if not bot:
        return {"ok": False, "error": "Bot not exists!"}

    try:
        while True:
            token = random.randbytes(32).hex()
            if Bot.objects(token=token).count() == 0:
                break

        bot.token = token
        bot.validate()
        bot.save()
    except Exception as e:
        return {"ok": False, "error": "Bot token regeneration error!", "exception": str(e)}
    return {"ok": True, "msg": "Bot token regenerated successfully!"}
