from app import load_neo4j
from config import Config
from strawberry.asgi import GraphQL
from app.graphql import schema

load_neo4j(Config().NEO4J_URI)
app = GraphQL(
    schema=schema,
    graphiql=True
)


