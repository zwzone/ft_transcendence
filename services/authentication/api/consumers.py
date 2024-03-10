from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Player

playersOpenTabs = {}

@database_sync_to_async
def set_player_status(playerId, playerStatus):
    Player.objects.filter(id=playerId).update(status=playerStatus)


class LoginConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        if self.scope['status'] == 'Valid':
            self.id = self.scope['payload']['id']
            if self.id not in playersOpenTabs:
                await set_player_status(self.id, Player.Status.ONLINE.value)
                playersOpenTabs[self.id] = 1
            else:
                playersOpenTabs[self.id] += 1
        await self.send(self.scope['status'])

    async def disconnect(self, close_code):
        if playersOpenTabs[self.id] == 1:
            await set_player_status(self.id, Player.Status.OFFLINE.value)
            del playersOpenTabs[self.id]
        else:
            playersOpenTabs[self.id] -= 1

    async def receive(self, text_data):
        pass