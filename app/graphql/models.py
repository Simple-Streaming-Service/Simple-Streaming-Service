import base64
import re
from enum import Enum

import strawberry
from datetime import datetime
from typing import Optional, List
from strawberry.types import Info

from app.models.account import StreamingProfile
from app.services.user import get_current_user
from graphql_asgi import decode_session

query_pattern = re.compile(
    r":(?P<type>\w+) (?P<query>.*?) ?(?=:)",
    re.RegexFlag.S | re.RegexFlag.IGNORECASE
)


@strawberry.type(description="Service Metadata for Chat Frontend")
class FrontendChatServiceData:
    name: str
    description: str
    author: str
    initializer_code: str
    formatting_code: str
    style: str


@strawberry.enum(description="Ordering options")
class Order(Enum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


@strawberry.type(description="Message Structure")
class MessageData:
    id: str
    author: str
    timestamp: datetime
    content: str

    @strawberry.field
    def id(self, info: Info) -> str:
        return self.element_id

    @strawberry.field
    def author(self, info: Info) -> Optional[str]:
        return self.author.single().username

@strawberry.type(description="Stream Metadata")
class StreamData:
    stream_name: str
    viewer_count: int

    @strawberry.field
    def services(
        self,
        info: Info,
        query: Optional[str] = None
    ) -> List[FrontendChatServiceData]:
        if query:
            parsed = ":any " + query + ":"
            parsed = query_pattern.finditer(parsed)
            query_dict = {
                match.group("type"): match.group("query") for match in parsed
            }
            query_any = query_dict.get("any", "")
            result = []

            result += self.services.filter(
                name__contains=query_any,
                description__contains=query_any,
                author__username__contains=query_any,
            ).all()

            if "name" in query_dict:
                result += self.services.filter(
                    name__contains=query_dict["name"],
                    description__contains=query_any,
                    author__username__contains=query_any,
                ).all()
            if "description" in query_dict:
                result += self.services.filter(
                    name__contains=query_any,
                    description__contains=query_dict["description"],
                    author__username__contains=query_any,
                ).all()
            if "author" in query_dict:
                result += self.services.filter(
                    name__contains=query_any,
                    description__contains=query_any,
                    author__username__contains=query_dict["author"],
                ).all()

            return list(set(result))
        else:
            return self.services.all()


@strawberry.type(description="Streamer Profile Data")
class StreamingProfileData:
    token: Optional[str]
    subscribers: int

    @strawberry.field
    def messages(
        self,
        info: Info,
        start_timestamp: Optional[datetime] = None,
        end_timestamp: Optional[datetime] = None,
        limit: Optional[int] = None,
        order: Order = Order.DESCENDING,
    ) -> List[MessageData]:
        return get_messages(self, start_timestamp, end_timestamp, limit, order)

    @strawberry.field
    def stream(self, info: Info) -> Optional[StreamData]:
        return self

    @strawberry.field
    def token(self, info: Info) -> Optional[str]:
        user = self.user.single()
        request = info.context["request"]
        if user != get_current_user(request.headers, decode_session(request.cookies)):
            return None
        head = base64.urlsafe_b64encode(user.username.encode()).decode().replace('=', '~')
        return f"{head}?token={self.token}"

    @strawberry.field
    def subscribers(self, info: Info) -> int:
        return len(self.subscribers.all())


@strawberry.type(description="Bot Information")
class BotData:
    token: Optional[str]
    author: str

    @strawberry.field
    def token(self, info: Info) -> Optional[str]:
        request = info.context["request"]
        user = get_current_user(request.headers, decode_session(request.cookies))
        bot_user = self.user.single()
        author = self.author.single()
        if user != bot_user and user != author:
            return None
        return self.token

    @strawberry.field
    def author(self, info: Info) -> Optional[str]:
        return self.author.single().username


@strawberry.type(description="User Data")
class UserData:
    username: str
    email: str
    password: Optional[str]

    @strawberry.field
    def subscriptions(self, info: Info) -> List[str]:
        return [
            streamer.user.single().username
            for streamer in self.subscriptions.all()
        ]

    @strawberry.field
    def profile(self, info: Info) -> StreamingProfileData:
        return self.profile.single()

    @strawberry.field
    def bot(self, info: Info) -> BotData:
        return self.bot.single()

    @strawberry.field
    def password(self, info: Info) -> Optional[str]:
        request = info.context["request"]
        user = get_current_user(request.headers, decode_session(request.cookies))
        if user != self:
            return None
        return self.password


def get_messages(
        streamer: StreamingProfile,
        start_timestamp: Optional[datetime] = None,
        end_timestamp: Optional[datetime] = None,
        limit: Optional[int] = None,
        order: Order = Order.DESCENDING) -> List[MessageData]:
    filtered = [
        msg for msg in streamer.messages.all()
        if (not start_timestamp or start_timestamp <= msg.timestamp) and
           (not end_timestamp or msg.timestamp <= end_timestamp)
    ]
    reverse = order == Order.ASCENDING
    sorted_msgs = sorted(filtered, key=lambda m: m.timestamp, reverse=not reverse)
    return sorted_msgs[:limit] if limit else sorted_msgs