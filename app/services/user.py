from app.models.account import User


def get_current_user(args):
    if "user" not in args: return None
    return User.objects(username=args["user"]).first()

def get_user(args):
    if "user" not in args: return None
    return User.objects(username=args["user"]).first()