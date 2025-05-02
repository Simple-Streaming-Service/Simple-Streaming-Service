from app import load_neo4j
from config import Config
from strawberry.asgi import GraphQL
from app.api.graphql import schema

load_neo4j(Config())
app = GraphQL(
    schema=schema,
    graphiql=True
)


