import pytest
from django.contrib.auth import get_user_model
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async

from .consumers import ChatConsumer



@database_sync_to_async
def create_user(name, email, password):
    return get_user_model().objects.create_user(name, email, password)


@pytest.mark.asyncio
async def websocket_consumer_check():
    """
    Tests that ChatConsumer is implemented correctly.
    """
    user1 = await create_user('user_1', 'user_1@test.test', '123')
    user2 = await create_user('user_2', 'user_2@test.test', '123')

    communicator1 = WebsocketCommunicator(ChatConsumer, "/ws/chat/")
    communicator1.scope['user'] = user1
    communicator1.scope['session'] = {}

    connected, _ = await communicator1.connect()
    # test user_1 connected
    assert connected
    response = await communicator1.receive_json_from()
    # test users list updated
    assert response ==  {'type': 'USERS_LIST', 'users': [{'id': 1, 'name': 'user_1'}]}

    communicator2 = WebsocketCommunicator(ChatConsumer, "/ws/chat/")
    communicator2.scope['user'] = user2
    communicator2.scope['session'] = {}

    connected, _ = await communicator2.connect()
    # test user_2 connected
    assert connected
    response = await communicator2.receive_json_from()
    # test users list updated
    assert response ==  {'type': 'USERS_LIST', 'users': [{'id': 1, 'name': 'user_1'}, {'id': 2, 'name': 'user_2'}]}

    # sending message from user_1 to group
    await communicator1.send_json_to({"type": "ADD_MESSAGE", "message": "hello", "author": "user_1"})

    response = await communicator2.receive_json_from()
    # test user_2 get message
    assert response == {'type': 'ADD_MESSAGE', 'author': 'user_1', 'message': 'hello'}

    await communicator1.disconnect()
    response = await communicator2.receive_json_from()
    # test users list updated after user_1 disconnected
    assert response ==  {'type': 'USERS_LIST', 'users': [{'id': 2, 'name': 'user_2'}]}
    await communicator2.disconnect()
