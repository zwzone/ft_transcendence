from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
import uuid

rooms = []


def create_room(player_id, channel_name, capacity, match_id):
    rooms.append({
        "players": [{
            player_id: channel_name,
        }],
        'id': str(uuid.uuid4()),
        'match_id': match_id,
        'capacity': capacity
    })
    return rooms[len(rooms) - 1]


def get_room(player_id, capacity, channel_name, match_id):
    for room in rooms:
        if (len(room['players']) < capacity and
                room['capacity'] == capacity and
                room['match_id'] == match_id):
            room['players'].append({player_id: channel_name})
            async_to_sync(get_channel_layer().group_add)(room['id'], channel_name)
            if len(room['players']) == capacity:
                async_to_sync(get_channel_layer().group_send)(room['id'], {
                    "type": "chat.message",
                    "text": room['id'],
                })
                rooms.remove(room)
            return
    return create_room(player_id, channel_name, capacity, match_id)


def find_channels_room(player_id, channel_name):
    for room in rooms:
        for player in room['players']:
            if player_id in player:
                if player[player_id] == channel_name:
                    room['players'].remove(player)
                return room
    return None


class Matchmaking(WebsocketConsumer):
    def receive(self, text_data):
        print(text_data)

    def chat_message(self, event):
        self.send(text_data=event["text"])

    def connect(self):
        match_id = self.scope['url_route']['kwargs'].get('match_id')
        self.accept()
        if find_channels_room(self.scope['payload']['id'], self.channel_name):
            self.send("error")
            return
        r = get_room(self.scope['payload']['id'], self.scope['url_route']['kwargs']['capacity'], self.channel_name, match_id)
        if not r:
            return
        async_to_sync(self.channel_layer.group_add)(r['id'], self.channel_name)

    def disconnect(self, close_code):
        r = find_channels_room(self.scope['payload']['id'], self.channel_name)
        if r:
            async_to_sync(self.channel_layer.group_discard)(r['id'], self.channel_name)
