from flask import render_template, current_app
from app.posts import bp


# JUST EXAMPLES

@bp.route('/')
def index():
    return render_template('posts/index.html')


@bp.route('/categories/')
def categories():
    return render_template('posts/categories.html')
