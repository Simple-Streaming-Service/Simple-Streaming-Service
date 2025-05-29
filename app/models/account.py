from neomodel import StructuredNode, StringProperty, EmailProperty, BooleanProperty, RelationshipFrom, \
    RelationshipTo, IntegerProperty, DateTimeProperty


class User(StructuredNode):
    username = StringProperty(required=True, unique=True)
    password = StringProperty(required=True)
    email = EmailProperty(required=True, unique=True)

    created_at = DateTimeProperty(default_now=True)
    last_login = DateTimeProperty(default_now=True)
    revoked_at = DateTimeProperty(default=None)
    revoked_by = RelationshipFrom("app.models.account.User", "REVOKE")


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
    viewer_count = IntegerProperty(default=0)
    moderators = RelationshipFrom("app.models.account.User", "MODERATING")
    banned = RelationshipFrom("app.models.account.User", "BANNED")
    subscribers = RelationshipFrom("app.models.account.User", "SUBSCRIBED")
    messages = RelationshipFrom("app.models.messaging.Message", "MESSAGE")


class Bot(StructuredNode):
    token = StringProperty(required=True, unique=True)
    user = RelationshipTo("app.models.account.User", "LINKED")
    author = RelationshipFrom("app.models.account.User", "AUTHOR")


