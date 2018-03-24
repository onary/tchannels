from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    group_name = "broadcast"
    users = set()

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

        print('disconnected: %s' % (self.scope["user"].username, ))

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

        print('connected %s ' % (self.scope["user"].username, ))

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

    async def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        await self.send_json(
            {
                "type": "ADD_MESSAGE",
                "author": event["username"],
                "message": event["message"],
            },
        )