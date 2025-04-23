import base64
import datetime

from graphene import ObjectType, String, Int, DateTime, Field, List, Enum

from app.services.user import get_current_user


class Order(Enum):
    ASCENDING = 1
    DESCENDING = -1

class MessageData(ObjectType):
    author = String(description="Message Author")
    timestamp = DateTime(description="Message Timestamp")
    content = String(description="Message Content")

    def resolve_author(parent, info):
        return parent.author.single().username

class StreamData(ObjectType):
    stream_name = String(description="Stream Name")
    viewers = Int(description="Stream Viewer Count")

class StreamingProfileData(ObjectType):
    token = String(description="Streamer Token")
    subscribers = Int(description="Streamer Subscriber Count")

    messages = List(MessageData, description="Streamer Messages",
                    start_timestamp=DateTime(description="Messages Start Timestamp"),
                    end_timestamp=DateTime(description="Messages End Timestamp"),
                    limit=Int(description="Messages Limit"),
                    order=Order(description="Messages Order", required=True))
    stream = Field(StreamData, description="Stream Data")

    def resolve_token(parent, info):
        user = parent.user.single()
        if user != get_current_user(): return None
        head = base64.urlsafe_b64encode(user.username.encode()).decode().replace('=', '~')
        return f"{head}?token={parent.token}"

    def resolve_subscribers(parent, info):
        return len(parent.subscribers.all())

    def resolve_messages(parent, info, **args):
        print(args, flush=True)
        messages = [
            msg for msg in parent.messages.all()
            if ("start_timestamp" not in args or args["start_timestamp"] <= msg.timestamp)
            and ("end_timestamp" not in args or msg.timestamp <= args["end_timestamp"])
        ]
        messages = sorted(messages, key=lambda x: x.timestamp, reverse=args["order"]==-1)
        if "limit" in args:
            messages = messages[:args["limit"]]
        return messages

    def resolve_stream(parent, info):
        return dict(
            stream_name = parent.stream_name,
            viewers = 0 # TODO: Viewer counting
        )

class BotData(ObjectType):
    token = String(description="Streamer Email")
    author = String( description="Bot Author")


    def resolve_author(parent, info):
        return parent.author.single().username

class UserData(ObjectType):
    username = String(description="User Username")
    email = String(description="User Email")
    password = String(description="User Password")
    subscriptions = List(String, description="List of Subscriptions")
    profile = Field(StreamingProfileData, description="Streaming Profile Data")
    bot = Field(BotData, description="Bot Data")

    def resolve_subscriptions(parent, info):
        return [
            streamer.user.single().username
            for streamer in parent.subscriptions.all()
        ]

    def resolve_profile(parent, info):
        return parent.profile.single()

    def resolve_bot(parent, info):
        return parent.bot.single()