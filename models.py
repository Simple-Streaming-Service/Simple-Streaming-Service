from flask_mongoengine import MongoEngine
db = MongoEngine()

class User(db.Document):
    username = db.StringField(required=True)
    password = db.StringField(required=True)
    email = db.StringField(required=True)

class Message(db.Document):
    user = db.ReferenceField(document_type=User)
    content = db.StringField(required=True)

class StreamingProfile(db.Document):
    user = db.ReferenceField(document_type=User)
    streaming_token = db.StringField(required=True)
    stream_name = db.StringField(required=True)
    messages = db.ListField(field=db.ReferenceField(document_type=Message))
