import datetime

from neomodel import RelationshipFrom, DateTimeProperty, StringProperty, StructuredNode


class Message(StructuredNode):
    user = RelationshipFrom("app.models.account.User", "AUTHOR")
    timestamp = DateTimeProperty(default=datetime.datetime.now)
    content = StringProperty(required=True)