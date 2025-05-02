import re
import strawberry
from typing import Optional, List, AsyncGenerator
from datetime import datetime

from app.graphql.models import (
    UserData,
    BotData,
    StreamingProfileData,
    MessageData,
    Order,
    FrontendChatServiceData
)
from app.models.account import User
from app.models.service import FrontendChatService

query_pattern = re.compile(
    r":(?P<type>\w+) (?P<query>.*?) ?(?=:)",
    re.RegexFlag.S | re.RegexFlag.IGNORECASE
)

@strawberry.type
class Query:
    @strawberry.field(description="Get user data by username")
    def user(self, info, username: str) -> Optional[UserData]:
        return User.nodes.first_or_none(username=username)

    @strawberry.field(description="Frontend Chat Services")
    def services(self, info, query: Optional[str] = None) -> List[FrontendChatServiceData]:
        if query:
            parsed = ":any " + query + ":"
            parsed = query_pattern.finditer(parsed)
            query_dict = {
                match.group("type"): match.group("query") for match in parsed
            }
            query_any = query_dict.get("any", "")
            result = []

            result += FrontendChatService.nodes.filter(
                name__contains=query_any,
                description__contains=query_any,
                author__username__contains=query_any,
            ).all()

            if "name" in query_dict:
                result += FrontendChatService.nodes.filter(
                    name__contains=query_dict["name"],
                    description__contains=query_any,
                    author__username__contains=query_any,
                ).all()
            if "description" in query_dict:
                result += FrontendChatService.nodes.filter(
                    name__contains=query_any,
                    description__contains=query_dict["description"],
                    author__username__contains=query_any,
                ).all()
            if "author" in query_dict:
                result += FrontendChatService.nodes.filter(
                    name__contains=query_any,
                    description__contains=query_any,
                    author__username__contains=query_dict["author"],
                ).all()

            return list(set(result))
        else:
            return FrontendChatService.nodes.all()

@strawberry.type
class Subscription:
    @strawberry.subscription(description="Get messages of streamer by username")
    async def messages(
        self,
        info,
        streamer: str,
        start_timestamp: Optional[datetime] = None,
        end_timestamp: Optional[datetime] = None,
        limit: Optional[int] = None,
        order: Order = Order.DESCENDING,
    ) -> AsyncGenerator[List[MessageData], None]:
        profile = User.nodes.first_or_none(username=streamer).profile.single()
        profile.viewer_count += 1
        try:
            while True:
                pass
            #     data = []
            #     if data[0] != profile:
            #         continue
            #     msgs = [
            #         msg for msg in data[1]
            #         if (not start_timestamp or start_timestamp <= msg.timestamp) and
            #            (not end_timestamp or msg.timestamp <= end_timestamp)
            #     ]
            #     reverse = order == Order.ASCENDING
            #     msgs = sorted(msgs, key=lambda m: m.timestamp, reverse=not reverse)
            #     if limit:
            #         msgs = msgs[:limit]
            #     yield msgs
        finally:
            profile.viewer_count -= 1

schema = strawberry.Schema(query=Query, subscription=Subscription)