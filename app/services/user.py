from wsgiref.headers import Headers

from flask import session

from app.main import bp
from app.models.account import User, Bot


def is_authenticated() -> bool:
    return get_current_user() is not None

def get_current_user(args : Headers=None) -> User or None:
    user = session.get('user', None)
    if user is None:
        if args is None: return None
        token = args.get("X-Api-Key", None)
        if token is None: return None
        bot = Bot.nodes.first_or_none(token=token)
        if not bot: return None
        return bot.user

    return User.nodes.first_or_none(username=user)

def get_user(args) -> User or None:
    if "user" not in args:
        return None
    return User.nodes.first_or_none(username=args["user"])

@bp.context_processor
def utility_processor():
    return dict(
        is_authenticated=is_authenticated,
        get_current_user=get_current_user,
        get_user=get_user
    )