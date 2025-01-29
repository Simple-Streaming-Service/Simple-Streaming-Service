import hashlib
import random

from flask import request, json, session

from app.api import bp
from app.models.account import User, Bot
from app.services.user import get_current_user


@bp.post("/bot/auth")
def bot_auth():
    data = json.loads(request.data)
    bot = Bot.objects(token=data["token"]).first()
    if not bot: return {"ok": False, "error": "Bot not exists!"}

    session['user'] = bot.user.username
    return {"ok": True, "msg": "User log in successfully!"}

@bp.post("/bot/exit")
def bot_logout():
    data = json.loads(request.data)
    bot = Bot.objects(token=data["token"]).first()
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

    bot_user = User.objects(username=data["bot_username"]).first()
    if not bot_user: return {"ok": False, "error": "Bot user not exists!"}
    try:
        if bot_user.password != hashlib.sha512(data["bot_password"].encode()).hexdigest():
            return {"ok": False, "error": "Bot user linking password invalid!"}

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
