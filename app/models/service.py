from neomodel import StructuredNode, StringProperty, FloatProperty, IntegerProperty, RelationshipFrom

from app.models.account import User


class FrontendChatService(StructuredNode):
    name = StringProperty(required=True, unique=True)
    description = StringProperty(required=True)
    author = RelationshipFrom(User, "Author")

    initializer_code = StringProperty(required=True)
    converter_code = StringProperty(required=True)
