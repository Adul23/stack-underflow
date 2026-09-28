import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator

from apps.chat.consumers import AdminChatConsumer, PublicChatConsumer
from apps.users.models import CustomUser


@database_sync_to_async
def create_user(email, password="test123!") -> CustomUser:
    return CustomUser.objects.create_user(
        email=email,
        password=password,
        first_name="Test",
        last_name="User",
    )


@pytest.mark.django_db(transaction=True)
class TestOpenConsumers:

    url = "ws/chat/public/"

    @pytest.mark.asyncio
    async def test_public_connect(self):
        communicator = WebsocketCommunicator(PublicChatConsumer.as_asgi(), self.url)
        communicator.scope["user"] = await create_user("New")

        connected, _ = await communicator.connect()
        assert connected

        response = await communicator.receive_json_from()
        assert response["type"] == "welcome"

        await communicator.disconnect()

    @pytest.mark.asyncio
    async def test_public_message_broadcast(self):
        user_alice = await create_user("alice")
        user_bob = await create_user("bob")

        alice = WebsocketCommunicator(PublicChatConsumer.as_asgi(), self.url)
        alice.scope["user"] = user_alice

        bob = WebsocketCommunicator(PublicChatConsumer.as_asgi(), self.url)
        bob.scope["user"] = user_bob

        await alice.connect()
        await alice.receive_json_from()  # welcome

        await bob.connect()
        await bob.receive_json_from()  # welcome

        # Alice sends a message
        await alice.send_json_to({"type": "message", "message": "hello everyone"})

        # Bob receives it
        response = await bob.receive_json_from()
        assert response["type"] == "message"
        assert response["message"] == "hello everyone"
        assert response["username"] == "alice"

        # Alice does NOT receive her own message
        assert await alice.receive_nothing() is True

        await alice.disconnect()
        await bob.disconnect()


@pytest.mark.django_db(transaction=True)
class TestAdminConsumers:
    url = "ws/chat/admin/"

    @pytest.mark.asyncio
    async def test_admin_connect(self):
        communicator = WebsocketCommunicator(AdminChatConsumer.as_asgi(), self.url)
        communicator.scope["user"] = await create_user("admin1")

        connected, _ = await communicator.connect()
        assert connected

        response = await communicator.receive_json_from()
        assert response["type"] == "welcome"

        await communicator.disconnect()

    @pytest.mark.asyncio
    async def test_admin_invite_creates_group(self):
        user_admin = await create_user("admin1")
        user_member = await create_user("member1")

        admin = WebsocketCommunicator(AdminChatConsumer.as_asgi(), self.url)
        admin.scope["user"] = user_admin

        member = WebsocketCommunicator(AdminChatConsumer.as_asgi(), self.url)
        member.scope["user"] = user_member

        await admin.connect()
        await admin.receive_json_from()  # welcome

        await member.connect()
        await member.receive_json_from()  # welcome

        # Admin invites member by user ID
        await admin.send_json_to(
            {
                "type": "invite",
                "members": [user_member.id],
            }
        )

        # Member receives the invite
        response = await member.receive_json_from()
        assert response["type"] == "chat.invite"
        assert "id" in response  # the generated chat UUID

        await admin.disconnect()
        await member.disconnect()
