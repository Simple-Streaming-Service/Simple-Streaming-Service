from neomodel import StructuredNode, StringProperty, EmailProperty, BooleanProperty, RelationshipFrom, \
    RelationshipTo


class User(StructuredNode):
    username = StringProperty(required=True, unique=True)
    password = StringProperty(required=True)
    email = EmailProperty(required=True, unique=True)
    subscriptions = RelationshipTo("app.models.account.StreamingProfile", "SUBSCRIBED")

    profile = RelationshipTo("app.models.account.StreamingProfile", "LINKED")
    bot = RelationshipFrom("app.models.account.Bot", "LINKED")

    bots = RelationshipTo("app.models.account.Bot", "AUTHOR")

class StreamingProfile(StructuredNode):
    user = RelationshipFrom("app.models.account.User", "LINKED")
    token = StringProperty(required=True, unique=True)
    withCredentials = BooleanProperty(default=False)

    # Settings
    stream_name = StringProperty(required=True)
    services = RelationshipFrom("app.models.service.FrontendChatService", "USED")

    # Data
    subscribers = RelationshipFrom("app.models.account.User", "SUBSCRIBED")
    # viewers = RelationshipFrom("app.models.account.User", "VIEWER")
    messages = RelationshipFrom("app.models.messaging.Message", "MESSAGE")


class Bot(StructuredNode):
    token = StringProperty(required=True, unique=True)
    user = RelationshipTo("app.models.account.User", "LINKED")
    author = RelationshipFrom("app.models.account.User", "AUTHOR")


