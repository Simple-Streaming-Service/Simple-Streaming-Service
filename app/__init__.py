from time import sleep

from flask import Flask
from mongoengine import connect, get_connection

from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    load_mongo(app)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

def load_mongo(app):
    client = connect(host=app.config['MONGO_URI'], timeoutms=1000)
    try:
        app.logger.info("Connected to MongoDB: {0}", client.admin.command('ping'))
    except Exception as e:
        app.logger.info("Connection to MongoDB failed: {0}", e)