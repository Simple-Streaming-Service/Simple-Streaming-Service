from flask import Blueprint
from flask_graphql import GraphQLView

from app.api.graphql import schema

bp = Blueprint('api', __name__)

bp.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
))
bp.add_url_rule('/graphql/batch', view_func=GraphQLView.as_view(
    'graphql-batch',
    schema=schema,
    batch=True
))

from app.api import user, stream, services, bot