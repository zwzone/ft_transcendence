from channels.generic.websocket import AsyncWebsocketConsumer


class LoginConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print('connected', flush=True)

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass