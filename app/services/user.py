from wsgiref.headers import Headers

from flask import session
from requests import Request

from app.main import bp
from app.models.account import User, Bot


def is_authenticated():
    return get_current_user() is not None

def get_current_user(args : Headers=None):
    user = session.get('user', None)
    if user is None:
        if args is None: return None
        token = args.get("Api-Key", None)
        if token is None: return None
        bot = Bot.objects(token=token).first()
        if not bot: return None
        return bot.user

    return User.objects(username=user).first()

def get_user(args):
    if "user" not in args:
        return None
    return User.objects(username=args["user"]).first()

@bp.context_processor
def utility_processor():
    return dict(
        is_authenticated=is_authenticated,
        get_current_user=get_current_user
    )