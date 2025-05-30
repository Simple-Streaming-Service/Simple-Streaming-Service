import asyncio
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
    FrontendChatServiceData,
    get_messages
)
from app.models.account import User, StreamingProfile
from app.models.messaging import Message
from app.models.service import FrontendChatService
from app.services.user import get_current_user, find_streamer
from graphql_asgi import decode_session

query_pattern = re.compile(
    r":(?P<type>\w+) (?P<query>.*?) ?(?=:)",
    re.RegexFlag.S | re.RegexFlag.IGNORECASE
)

import asyncio

class Waiter:
    def __init__(self):
        self._event = asyncio.Event()
        self._result = None
        self._waiting = 0

    async def wait(self):
        self._waiting += 1
        await self._event.wait()
        self._waiting -= 1
        if self._waiting == 0:
            self._event.clear()
        return self._result

    def drop_wait(self):
        self._waiting -= 1
        if self._waiting == 0:
            self._event.clear()
    def trigger(self, result):
        self._result = result
        self._event.set()

chat_updates = {str:Waiter}

@strawberry.type
class Response:
    ok: bool
    error: Optional[str] = None
    msg: Optional[str] = None
    timestamp: Optional[datetime] = None

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
class Mutation:
    @strawberry.mutation(description="Sends a message to chat")
    def send_message(self, info, streamer: str, message: str, timestamp: Optional[datetime] = None) -> Response:
        request = info.context["request"]
        user = get_current_user(request.headers, decode_session(request.cookies))
        if not user:
            return Response(ok=False, error="User not authorized!")

        if timestamp is None: timestamp = datetime.now()
        if message is None:
            return Response(ok=False, error="Content field is required!")

        streamer = find_streamer(streamer)
        if not streamer:
            return Response(ok=False, error="Streamer does not exist!")

        if user in streamer.banned:
            return Response(ok=False, error="User banned!")

        msg = Message(content=message, timestamp=timestamp)
        msg.save()
        msg.author.connect(user)
        streamer.messages.connect(msg)
        if streamer.element_id in chat_updates:
            chat_updates[streamer.element_id].trigger(streamer.messages.all())
        return Response(ok=True, msg="Message sent!", timestamp=timestamp)
    @strawberry.mutation(description="Removes a message from chat")
    def remove_message(self, info, message_id: str) -> Response:
        request = info.context["request"]
        user = get_current_user(request.headers, decode_session(request.cookies))
        if not user:
            return Response(ok=False, error="User not authorized!")
        message = Message.nodes.first_or_none(id=message_id)
        author = message.author.single()
        streamer = message.streamer.single()
        if user != author and user != streamer and user not in streamer.moderators:
            return Response(ok=False, error="User is neither the author of the message nor the moderator of the streamer!")

        message.delete()
        message.save()
        if streamer.element_id in chat_updates:
            chat_updates[streamer.element_id].trigger(streamer.messages.all())
        pass

@strawberry.type
class Subscription:
    @strawberry.subscription(description="Get messages of streamer by username")
    async def onChatChange(
        self,
        info,
        streamer: str,
        start_timestamp: Optional[datetime] = None,
        end_timestamp: Optional[datetime] = None,
        limit: Optional[int] = None,
        order: Order = Order.DESCENDING,
    ) -> AsyncGenerator[List[MessageData], None]:
        streamer = User.nodes.first_or_none(username=streamer).profile.single()
        streamer.viewer_count += 1
        streamer.save()
        if streamer.element_id not in chat_updates:
            chat_updates[streamer.element_id] = Waiter()
        yield get_messages(streamer, start_timestamp, end_timestamp, limit, order)
        try:
            while True:
                yield await chat_updates[streamer.element_id].wait()
        finally:
            streamer.viewer_count -= 1
            streamer.save()
            chat_updates[streamer.element_id].drop_wait()
            if streamer.viewer_count == 0:
                chat_updates.pop(streamer.element_id, None)



schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription
)
