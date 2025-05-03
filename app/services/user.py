from flask import session
from app.models.account import User, Bot, StreamingProfile


def is_authenticated(args=None, content=session) -> bool:
    return get_current_user(args, content) is not None

def get_current_user(args=None, content=session) -> User | None:
    user = None
    if content:
        user = content.get('user', None)
    if user is None:
        if args is None: return None
        token = args.get("X-Api-Key", None)
        if token is None: return None
        bot = Bot.nodes.first_or_none(token=token)
        if not bot: return None
        return bot.user.single()

    return User.nodes.first_or_none(username=user)

def get_user(args) -> User or None:
    if "user" not in args:
        return None
    return User.nodes.first_or_none(username=args["user"])

def find_streamer(streamer) -> StreamingProfile:
    user = User.nodes.first_or_none(username=streamer)
    return user.profile.single()
