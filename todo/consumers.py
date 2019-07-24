from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Todo


class TodoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.group_name = 'todos'
        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytesdata=None):
        pk = text_data
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'post_action_receive',
                'message': {
                    "id": pk,
                }
            }
        )

    async def post_action_receive(self, event):
        message = event['message']
        pk = message['id']
        todo = await database_sync_to_async(Todo.objects.get)(pk=pk)
        await self.send(text_data=todo.content)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)