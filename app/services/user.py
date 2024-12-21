from flask import session

from app.models.account import User


def is_authenticated():
    return 'user_id' in session

def get_current_user():
    user_id = session.get('user_id', None)
    if user_id is None:
        return None
    return User.objects(id=user_id).first()

def get_user(args):
    if "user" not in args:
        return None
    return User.objects(username=args["user"]).first()