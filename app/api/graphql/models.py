from graphene import ObjectType, String, Int, DateTime, Field, List


class User(ObjectType):
    username = String(description="User Username", required=True)
    email = String(description="User Email", required=True)
    password = String(description="User Password", required=True)
    subscriptions = List(String, description="List of Subscriptions", required=True)

    def resolve_subscriptions(parent, info):
        return []

class Message(ObjectType):
    user = Field(User, description="Message Author", required=True)
    timestamp = DateTime(description="Message Timestamp", required=True)
    content = String(description="Message Content", default="", required=True)

class StreamingProfile(ObjectType):
    user = Field(User, description="Streamer Data", required=True)
    token = String(description="Streamer Token", required=True)
    stream_name = String(description="Stream Name", required=True)

    subscriptions = Int(description="Streamer Subscriber Count", required=True)
    messages = List(Message, description="Streamer Messages", required=True)

class Bot(ObjectType):
    user = Field(User, description="Bot User Data", required=True)
    token = String(description="Streamer Email", required=True)
    creator = Field(User, description="Bot Creator", required=True)