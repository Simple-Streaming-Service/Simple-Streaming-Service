from flask import session

from app.main import bp
from app.models.account import User


def is_authenticated():
    return get_current_user() is not None

def get_current_user():
    user = session.get('user', None)
    if user is None: return None
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