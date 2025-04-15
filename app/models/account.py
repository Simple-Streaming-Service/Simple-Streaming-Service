from mongoengine import Document, StringField, EmailField, ReferenceField, ListField, EmbeddedDocumentField, \
    BooleanField


class StreamingProfile(Document):
    pass


class User(Document):
    """
    User model representing a user in the system.
    This model contains fields for username, password, email, and subscriptions.
    The username and email fields are required and must be unique.
    The subscriptions field is a list of references to StreamingProfile documents.
    """
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    email = EmailField(required=True, unique=True)
    subscriptions = ListField(default=[], field=ReferenceField(required=True, document_type=StreamingProfile))


from app.models.messaging import Message
from app.models.service import FrontendChatService


class StreamingProfile(Document):
    """
    StreamingProfile model representing a streaming profile in the system.
    This model contains fields for user reference, token, stream name, services,
    subscribers, viewers, and messages.
    The user field is a reference to the User document and is required and unique.
    The token field is a unique string used for authentication.
    The stream_name field is a required string representing the name of the stream.
    The services field is a list of references to FrontendChatService documents.
    The subscribers and viewers fields are lists of references to User documents.
    The messages field is a list of embedded documents representing messages.
    """
    user = ReferenceField(document_type=User, unique=True, required=True)
    token = StringField(required=True, unique=True)
    withCredentials = BooleanField(required=True, default=False)

    # Settings
    stream_name = StringField(required=True)
    services = ListField(default=[], field=ReferenceField(required=True, document_type=FrontendChatService))

    # Data
    subscribers = ListField(default=[], field=ReferenceField(required=True, document_type=User))
    viewers = ListField(default=[], field=ReferenceField(required=True, document_type=User))
    messages = ListField(default=[], field=EmbeddedDocumentField(required=True, document_type=Message))


class Bot(Document):
    """
    Bot model representing a bot in the system.
    This model contains fields for user reference, token, and creator.
    The user field is a reference to the User document and is required and unique.
    The token field is a unique string used for authentication.
    The creator field is a reference to the User document representing the creator of the bot.
    """
    user = ReferenceField(document_type=User, unique=True, required=True)
    token = StringField(required=True, unique=True)

    creator = ReferenceField(document_type=User, required=True)
