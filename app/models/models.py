from mongoengine import Document, StringField, EmailField, ReferenceField, ListField

class User(Document):
    username = StringField(required=True)
    password = StringField(required=True)
    email_field = EmailField(required=True)

class Message(Document):
    user = ReferenceField(document_type=User)
    content = StringField(required=True)

class StreamingProfile(Document):
    user = ReferenceField(document_type=User)
    streaming_token = StringField(required=True)
    stream_name = StringField(required=True)
    messages = ListField(field=ReferenceField(document_type=Message))
