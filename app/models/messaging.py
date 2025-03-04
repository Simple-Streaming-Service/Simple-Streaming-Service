import datetime

from neomodel import RelationshipFrom, DateTimeProperty, StringProperty, StructuredNode

from app.models.account import User


class Message(StructuredNode):
    user = RelationshipFrom(User, "Author")
    timestamp = DateTimeProperty(default=datetime.datetime.now)
    content = StringProperty(required=True)