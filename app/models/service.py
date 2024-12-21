from mongoengine import Document, StringField, FloatField, IntField, ReferenceField

from app.models.account import User


class FrontendChatService(Document):
    name = StringField(required=True, unique=True)
    description = StringField(required=True)
    author = ReferenceField(document_type=User)

    initializer_code = StringField(required=True)
    converter_code = StringField(required=True)
