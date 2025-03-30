from neomodel import StructuredNode, StringProperty, EmailProperty, BooleanProperty, RelationshipTo, RelationshipFrom


class User(StructuredNode):
    username = StringProperty(required=True, unique=True)
    password = StringProperty(required=True)
    email = EmailProperty(required=True, unique=True)

from app.models.messaging import Message
from app.models.service import FrontendChatService

class StreamingProfile(StructuredNode):
    user = RelationshipFrom(User, "User")
    token = StringProperty(required=True, unique=True)
    withCredentials = BooleanProperty(default=False)

    # Settings
    stream_name = StringProperty(required=True)
    services = RelationshipFrom(FrontendChatService, "Service")

    # Data
    subscriptions = RelationshipTo(User, "Subscriber")
    # viewers = RelationshipTo(User, "Viewer")
    messages = RelationshipTo(Message, "Message")


class Bot(StructuredNode):
    user = RelationshipTo(User, "User")
    token = StringProperty(required=True, unique=True)

    creator = RelationshipFrom(User, "Creator")


