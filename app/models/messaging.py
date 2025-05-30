from neomodel import RelationshipFrom, DateTimeProperty, StringProperty, StructuredNode, RelationshipTo


class Message(StructuredNode):
    streamer = RelationshipTo("app.models.account.StreamingProfile", "MESSAGE")
    author = RelationshipFrom("app.models.account.User", "AUTHOR")
    timestamp = DateTimeProperty(default_now=True)
    content = StringProperty(required=True)