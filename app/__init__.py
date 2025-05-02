from flask import Flask
from flask_wtf import CSRFProtect
from neomodel import db


from config import Config

csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    load_neo4j(app.config['NEO4J_URI'])
    csrf.init_app(app)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    csrf.exempt(api_bp)

    return app

def load_neo4j(uri):
    db.set_connection(url=uri)
