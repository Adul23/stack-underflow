# Python imports
import uuid

# Channels imports
from channels.generic.websocket import AsyncJsonWebsocketConsumer

# Project imports
from apps.chat.rate_limit import is_rate_limited


class AdminChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.user_group = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.user_group, self.channel_name)
        await self.accept()
        await self.send_json({"type": "welcome"})

    async def disconnect(self, close_code):
        pass

    async def receive_json(self, content):
        user_id = self.user.id if self.user.is_authenticated else self.channel_name
        if await is_rate_limited(user_id):
            await self.send_json(
                {"type": "error", "message": "Rate limit exceeded. Please wait before sending more messages."}
            )
            return

        if content["type"] == "invite":
            chat_id = str(uuid.uuid4())
            for member in content["members"]:
                await self.channel_layer.group_send(f"user_{member}", {"type": "chat.invite", "id": chat_id})
        elif content["type"] == "notify":
            await self.channel_layer.group_send(
                content["id"],
                {
                    "type": "chat.notify",
                    "kind": content["kind"],
                    "message": content["message"],
                    "sender": self.channel_name,
                },
            )
        elif content["type"] == "disconnect":
            await self.channel_layer.group_send(content["id"], {"type": "chat.disconnect", "id": content["id"]})

    async def chat_invite(self, event):
        await self.channel_layer.group_add(event["id"], self.channel_name)
        await self.send_json(event)

    async def chat_disconnect(self, event):
        await self.channel_layer.group_discard(event["id"], self.channel_name)

    async def chat_notify(self, event):
        if event["sender"] != self.channel_name:
            await self.send_json(event)


class PublicChatConsumer(AsyncJsonWebsocketConsumer):
    ROOM_GROUP = "public_chat"

    async def connect(self):
        self.user = self.scope["user"]
        await self.channel_layer.group_add(self.ROOM_GROUP, self.channel_name)
        await self.accept()
        await self.send_json({"type": "welcome"})

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.ROOM_GROUP, self.channel_name)

    async def receive_json(self, content):
        user_id = self.user.id if self.user.is_authenticated else self.channel_name
        if await is_rate_limited(user_id):
            await self.send_json(
                {"type": "error", "message": "Rate limit exceeded. Please wait before sending more messages."}
            )
            return

        if content["type"] == "message":
            await self.channel_layer.group_send(
                self.ROOM_GROUP,
                {
                    "type": "chat.message",
                    "message": content["message"],
                    "sender": self.channel_name,
                    "username": self.user.email if self.user.is_authenticated else "anonymous",
                },
            )

    async def chat_message(self, event):
        if event["sender"] != self.channel_name:
            await self.send_json(
                {
                    "type": "message",
                    "message": event["message"],
                    "username": event["username"],
                }
            )
