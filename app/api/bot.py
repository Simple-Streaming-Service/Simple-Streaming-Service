import hashlib
import random
from datetime import datetime

from flask import request, json, session

from app.api import bp, user
from app.models.account import User, Bot
from app.services.user import get_current_user


@bp.post("/bot/auth")
def bot_auth():
    bot = Bot.nodes.first_or_none(token=request.headers.get("X-Api-Key", None))
    if not bot: return {"ok": False, "error": "Bot not exists!"}
    bot_user = bot.user.single()
    if bot_user.revoked_at is not None:
        return {"ok": False, "error": "User banned!"}
    session['user'] = bot_user.username
    bot_user.last_login = datetime.now()
    bot_user.save()
    return {"ok": True, "msg": "Bot log in successfully!"}

@bp.post("/bot/exit")
def bot_logout():
    bot = Bot.nodes.first_or_none(token=request.headers.get("X-Api-Key", None))
    if not bot: return {"ok": False, "error": "Bot not exists!"}
    if get_current_user() != bot.user:
        return {"ok": False, "error": "Wrong bot credentials!"}
    session['user'] = None
    return {"ok": True, "msg": "Bot log out successfully!"}

@bp.post("/bot/create")
def bot_create():
    data = json.loads(request.data)
    user = get_current_user()
    if not user: return {"ok": False, "error": "User not authorized!"}

    bot_user = User.nodes.first_or_none(username=data["bot_username"])
    if not bot_user: return {"ok": False, "error": "Bot user not exists!"}
    try:
        if bot_user.password != hashlib.sha512(data["bot_password"].encode()).hexdigest():
            return {"ok": False, "error": "Bot user password invalid!"}

        while True:
            token = random.randbytes(32).hex()
            if len(Bot.nodes.filter(token=token)) == 0:
                break
        bot = Bot(token=token)
        bot.save()
        bot.user.connect(bot_user)
        bot.author.connect(user)
    except Exception as e:
        return {"ok": False, "error": "Bot creation error!", "exception": str(e)}

    return {"ok": True, "msg": "Bot created successfully!"}


@bp.delete("/bot/remove")
def bot_remove():
    data = json.loads(request.data)
    user = get_current_user()
    if not user: return {"ok": False, "error": "User not authorized!"}

    bot_user = User.nodes.first_or_none(username=data["bot_username"])
    if not bot_user: return {"ok": False, "error": "Bot user not exists!"}
    try:
        if bot_user.password != hashlib.sha512(data["bot_password"].encode()).hexdigest():
            return {"ok": False, "error": "Bot user password invalid!"}

        bot = bot_user.bot.single()
        if not bot: return {"ok": False, "error": "Bot not exists!"}

        if bot.author.single() != user:
            return {"ok": False, "error": "User not author of this bot!"}
        bot.delete()
    except Exception as e:
        return {"ok": False, "error": "Bot removing error!", "exception": str(e)}

    return {"ok": True, "msg": "Bot removed successfully!"}


@bp.post("/bot/token")
def bot_get_token():
    data = json.loads(request.data)
    user = get_current_user()
    if not user: return {"ok": False, "error": "User not authorized!"}

    bot_user = User.nodes.first_or_none(username=data["bot_username"])
    if not bot_user: return {"ok": False, "error": "Bot user not exists!"}

    if bot_user.password != hashlib.sha512(data["bot_password"].encode()).hexdigest():
        return {"ok": False, "error": "Bot user password invalid!"}

    bot = bot_user.bot.single()
    if not bot: return {"ok": False, "error": "Bot not exists!"}

    if bot.author.single() != user:
        return {"ok": False, "error": "User not author of this bot!"}

    return {"ok": True, "token": bot.token}

@bp.patch("/bot/token/regenerate")
def bot_regenerate_token():
    data = json.loads(request.data)
    user = get_current_user()
    if not user: return {"ok": False, "error": "User not authorized!"}

    bot_user = User.nodes.first_or_none(username=data["bot_username"])
    if not bot_user: return {"ok": False, "error": "Bot user not exists!"}

    if bot_user.password != hashlib.sha512(data["bot_password"].encode()).hexdigest():
        return {"ok": False, "error": "Bot user password invalid!"}

    bot = bot_user.bot.single()
    if not bot: return {"ok": False, "error": "Bot not exists!"}

    if bot.author.single() != user:
        return {"ok": False, "error": "User not author of this bot!"}

    try:
        while True:
            token = random.randbytes(32).hex()
            if len(Bot.nodes.filter(token=token)) == 0:
                break

        bot.token = token
        bot.save()
    except Exception as e:
        return {"ok": False, "error": "Bot token regeneration error!", "exception": str(e)}
    return {"ok": True, "msg": "Bot token regenerated successfully!"}