import datetime

from mongoengine import ReferenceField, DateTimeField, StringField, EmbeddedDocument

from app.models.account import User


class Message(EmbeddedDocument):
    user = ReferenceField(required=True, document_type=User)
    timestamp = DateTimeField(required=True, default=datetime.datetime.now)
    content = StringField(required=True)