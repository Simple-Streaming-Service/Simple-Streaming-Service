from wsgiref.headers import Headers

from flask import session

from app.main import bp
from app.models.account import User, Bot


def is_authenticated():
    """
    Check if the user is authenticated.
    This function checks if the user is authenticated by checking the session.
    If the user is authenticated, it returns True.
    If the user is not authenticated, it returns False.
    :return:
    """
    return get_current_user() is not None


def get_current_user(args: Headers = None):
    """
    Get the current user.
    This function retrieves the current user from the session.
    If the user is not in the session, it checks if the user is a bot.
    If the user is a bot, it retrieves the bot's user from the database.
    If the user is not a bot, it returns None.
    If the user is in the session, it retrieves the user from the database.
    :param args: Headers
    :return: User object or None
    """
    user = session.get('user', None)
    if user is None:
        if args is None:
            return None
        token = args.get("X-Api-Key", None)
        if token is None:
            return None
        bot = Bot.objects(token=token).first()
        if not bot:
            return None
        return bot.user

    return User.objects(username=user).first()


def get_user(args):
    """
    Get a user by username.
    This function retrieves a user from the database by username.
    If the user does not exist, it returns None.
    If the user exists, it returns the user object.
    :param args: Headers
    :return: User object or None
    """
    if "user" not in args:
        return None
    return User.objects(username=args["user"]).first()


@bp.context_processor
def utility_processor():
    """
    Utility processor for Flask.
    This function registers the utility functions as context processors.
    This allows the functions to be used in templates.
    :return: Dictionary of utility functions
    """
    return dict(
        is_authenticated=is_authenticated,
        get_current_user=get_current_user,
        get_user=get_user
    )
