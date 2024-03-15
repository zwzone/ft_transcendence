from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Player

playersOpenTabs = {}

@database_sync_to_async
def set_player_status(player,  playerStatus):
    player.status = playerStatus
    player.save(update_fields=["status"])


class LoginConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.id = None
        if self.scope['status'] == 'Valid':
            self.player = self.scope['player']
            self.id = self.player.id
            if self.id not in playersOpenTabs:
                await set_player_status(self.player, Player.Status.ONLINE.value)
                playersOpenTabs[self.id] = 1
            else:
                playersOpenTabs[self.id] += 1
        await self.send(self.scope['status'])

    async def disconnect(self, close_code):
        if self.id is None:
            return
        if playersOpenTabs[self.id] == 1:
            await set_player_status(self.player, Player.Status.OFFLINE.value)
            del playersOpenTabs[self.id]
        else:
            playersOpenTabs[self.id] -= 1

    async def receive(self, text_data):
        pass
