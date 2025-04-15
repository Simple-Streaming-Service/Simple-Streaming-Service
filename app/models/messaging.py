import datetime

from mongoengine import ReferenceField, DateTimeField, StringField, EmbeddedDocument

from app.models.account import User


class Message(EmbeddedDocument):
    """
    Message model representing a message in the system.
    This model contains fields for user reference, timestamp, and content.
    The user field is a reference to the User document and is required.
    The timestamp field is a DateTimeField that defaults to the current time.
    The content field is a required string representing the content of the message.
    """
    user = ReferenceField(required=True, document_type=User)
    timestamp = DateTimeField(required=True, default=datetime.datetime.now)
    content = StringField(required=True)
