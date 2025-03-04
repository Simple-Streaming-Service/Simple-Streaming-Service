from flask import Flask
from flask_graphql import GraphQLView
from flask_wtf import CSRFProtect
from mongoengine import connect

from api.graphql import schema
from config import Config

csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # Initialize Flask extensions here
    load_mongo(app)
    csrf.init_app(app)
    app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
    ))
    app.add_url_rule('/graphql/batch', view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        batch=True
    ))

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    csrf.exempt(api_bp)

    return app

def load_mongo(app):
    client = connect(host=app.config['MONGO_URI'], timeoutms=1000)
    try:
        app.logger.info("Connected to MongoDB: {0}", client.admin.command('ping'))
    except Exception as e:
        app.logger.info("Connection to MongoDB failed: {0}", e)
