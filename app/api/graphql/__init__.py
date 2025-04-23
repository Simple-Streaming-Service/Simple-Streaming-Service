from graphene import ObjectType, Mutation, String, Field, Schema

from app.api.graphql.models import UserData, BotData, StreamingProfileData
from app.models.account import User


class Query(ObjectType):
    user = Field(UserData, description="Query User",
                 username=String(description="User", required=True))


    def resolve_user(root, info, username):
        return User.nodes.first_or_none(username=username)

class Subscription(ObjectType):
    stream_data = Field(StreamingProfileData, description="Stream Data",
                 streamer=String(description="Streamer", required=True))

    async def subscribe_stream_data(root, info, streamer):
        pass


schema = Schema(
    query=Query,
    subscription=Subscription,
)