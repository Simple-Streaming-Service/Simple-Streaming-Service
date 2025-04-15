from flask import render_template

from app.main import bp
from app.models.account import StreamingProfile, Bot
from app.services.user import get_current_user


@bp.get("/user")
def user_profile():
    """
    User profile page.
    This endpoint serves the user profile page.
    It retrieves the user's profile and checks if the user is authorized.
    If the user is not authorized, it returns an error message.
    If the user is authorized, it renders the profile page with the user's information.
    :return: HTML page with the user's profile or JSON response with an error message
    """
    user = get_current_user()
    if not user: return {"ok": False, "error": "User not authorized!"}
    profile = StreamingProfile.objects(user=user)
    bots = Bot.objects(creator=user)

    return render_template("profile.html", user=user, profile=profile.first(), is_streamer=profile.count() != 0)


@bp.get("/auth")
def auth():
    """
    Authentication page.
    This endpoint serves the authentication page.
    It checks if the user is already authenticated.
    If the user is authenticated, it redirects to the user profile page.
    If the user is not authenticated, it renders the authentication page.
    :return: HTML page with the authentication form or JSON response with an error message
    """
    return render_template("auth.html", redirect_uri='main.user_profile')


@bp.get("/register")
def register():
    """
    Registration page.
    This endpoint serves the registration page.
    It checks if the user is already authenticated.
    If the user is authenticated, it redirects to the user profile page.
    If the user is not authenticated, it renders the registration page.
    :return: HTML page with the registration form or JSON response with an error message
    """
    return render_template("register.html", redirect_uri='main.auth')
