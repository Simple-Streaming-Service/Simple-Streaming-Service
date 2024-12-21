from mongoengine import Document, StringField, EmailField, ReferenceField, ListField, EmbeddedDocumentField



class StreamingProfile(Document):
    pass

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    email = EmailField(required=True, unique=True)
    subscriptions = ListField(default=[], field=ReferenceField(required=True, document_type=StreamingProfile))

from app.models.messaging import Message
from app.models.service import FrontendChatService

class StreamingProfile(Document):
    user = ReferenceField(document_type=User, unique=True)

    # Settings
    stream_name = StringField(required=True)
    services = ListField(default=[], field=ReferenceField(required=True, document_type=FrontendChatService))

    # Data
    subscribers = ListField(default=[], field=ReferenceField(required=True, document_type=User))
    viewers = ListField(default=[], field=ReferenceField(required=True, document_type=User))
    messages = ListField(default=[], field=EmbeddedDocumentField(required=True, document_type=Message))


