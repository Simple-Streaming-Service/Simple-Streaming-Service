from graphene import ObjectType, Mutation, String, Field, Schema

from app.models.account import User as UserModel, StreamingProfile as StreamingProfileModel, Bot as BotModel
from app.api.graphql.models import User, StreamingProfile, Bot

class Query(ObjectType):
    user = Field(User, description="Query User", username=String(description="Query User Username", required=True))
    profile = Field(StreamingProfile, description="Query Profile Data", username=String(description="Query Profile Username", required=True))
    bot = Field(Bot, description="Query Bot", username=String(description="Query Bot Username", required=True))

    def resolve_user(root, info, username):
        return UserModel.nodes.first_or_none(username=username)

    def resolve_profile(root, info, username):
        user = UserModel.nodes.first_or_none(username=username)
        if not user: return None
        return StreamingProfileModel.nodes.first_or_none(user=user)

    def resolve_bot(root, info, username):
        user = UserModel.nodes.first_or_none(username=username)
        if not user: return None
        return BotModel.nodes.first_or_none(user=user)


class UserMutation(Mutation):
    pass



class Subscription(ObjectType):
    pass

schema = Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription
)