from flask import render_template

from app.main import bp
from app.services.user import get_current_user


@bp.get("/user")
def user_profile():
    user = get_current_user()
    if not user: return {"ok": False, "error": "User not authorized!"}
    profile = user.profile.single()
    return render_template(
        "profile.html",
        user=user,
        profile=profile)

@bp.get("/auth")
def auth():
    return render_template("auth.html", redirect_uri='main.user_profile')

@bp.get("/register")
def register():
    return render_template("register.html", redirect_uri='main.auth')
