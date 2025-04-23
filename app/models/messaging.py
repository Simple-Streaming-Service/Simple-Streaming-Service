import datetime

from neomodel import RelationshipFrom, DateTimeProperty, StringProperty, StructuredNode


class Message(StructuredNode):
    author = RelationshipFrom("app.models.account.User", "AUTHOR")
    timestamp = DateTimeProperty(default=datetime.datetime.now)
    content = StringProperty(required=True)