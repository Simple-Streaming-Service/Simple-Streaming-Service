from neomodel import StructuredNode, StringProperty, RelationshipFrom


class FrontendChatService(StructuredNode):
    name = StringProperty(required=True, unique=True)
    description = StringProperty(required=True)
    author = RelationshipFrom("app.models.account.User", "AUTHOR")

    initializer_code = StringProperty(required=True)
    formatting_code = StringProperty(required=True)
    style = StringProperty(required=True)
