import hashlib
from datetime import timedelta

from flask.json.tag import TaggedJSONSerializer

from app import load_neo4j
from config import Config
from strawberry.asgi import GraphQL
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

config = Config()
def _lazy_sha1(string: bytes = b""):
    return hashlib.sha1(string)
serializer = URLSafeTimedSerializer(
    secret_key=config.SECRET_KEY,
    salt="cookie-session",
    serializer = TaggedJSONSerializer(),
    signer_kwargs={
        "key_derivation": "hmac",
        "digest_method": staticmethod(_lazy_sha1)
    },
)

def decode_session(cookies) -> dict | None:
    try:
        raw = cookies.get("session")
        if raw is None: return None
        data = serializer.loads(raw, max_age=int(timedelta(days=31).total_seconds()))
        print(f"Decoded Session: {data}", flush=True)
        return data
    except BadSignature | SignatureExpired:
        print(f"Decoding Failed!", flush=True)
        return None

load_neo4j(config.NEO4J_URI)

from app.graphql import schema
app = GraphQL(
    schema=schema,
    graphiql=True
)


