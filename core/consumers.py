from channels.generic.websocket import AsyncJsonWebsocketConsumer
from redis_collections import Deque
from django.conf import settings



class ChatConsumer(AsyncJsonWebsocketConsumer):
    group_name = "broadcast"
    users = set()
    messages = Deque([], settings.CHAT_QUEUE_LEN)

    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            await self.accept()
            await self.join_room()


    async def receive_json(self, content):
        if content.get("type", None) == "ADD_MESSAGE":
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat.message",
                    "username": self.scope["user"].username,
                    "message": content.get("message", None),
                }
            )


    async def disconnect(self, code):
        self.users.remove(self.scope["user"])

        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "broadcast.presence",
                "users": [{'name': u.username, 'id': u.id} for u in self.users],
            }
        )


    async def join_room(self):
        """
        Called by receive_json when someone sent a join command.
        """
        self.users.add(self.scope["user"])

        # Add them to the group so they get room messages
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "broadcast.presence",
                "users": [{'name': u.username, 'id': u.id} for u in self.users],
            }
        )

        await self.send_json({"messages": list(self.messages), "type": "ADD_MESSAGES"})


    # These helper methods are named by the types we send - so broadcast.presence becomes broadcast_presence
    async def broadcast_presence(self, event):
        """
        Called when someone has joined or left our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "type": "USERS_LIST",
                "users": event["users"],
            },
        )


    # These helper methods are named by the types we send - so chat.message becomes chat_message
    async def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Save message and send down to the client
        message = {
            "author": event["username"],
            "message": event["message"],
        }

        self.messages.append(message)

        message["type"] = "ADD_MESSAGE"
        await self.send_json(message)