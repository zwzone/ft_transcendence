from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
import uuid

rooms = []


def create_room(channel_name, capacity):
    rooms.append({
        "players": [channel_name],
        'id': str(uuid.uuid4()),
        'capacity': capacity
    })
    return rooms[len(rooms) - 1]


def get_room(channel_name, capacity):
    for room in rooms:
        if (len(room['players']) < capacity and
                room['capacity'] == capacity):
            room['players'].append(channel_name)
            async_to_sync(get_channel_layer().group_add)(room['id'], channel_name)
            if len(room['players']) == capacity:
                async_to_sync(get_channel_layer().group_send)(room['id'], {
                    "type": "chat.message",
                    "text": room['id'],
                })
                rooms.remove(room)
            return
    return create_room(channel_name, capacity)


def find_channels_room(channel_name):
    for room in rooms:
        if channel_name in room['players']:
            room['players'].remove(channel_name)
            return room
    return None


class Matchmaking(WebsocketConsumer):
    def receive(self, text_data):
        print(text_data)

    def chat_message(self, event):
        print(self.scope['client'], "     ", self.scope['user'])
        self.send(text_data=event["text"])

    def connect(self):
        self.accept()
        r = get_room(self.channel_name, self.scope['url_route']['kwargs']['capacity'])
        if not r:
            return
        async_to_sync(self.channel_layer.group_add)(r['id'], self.channel_name)

    def disconnect(self, close_code):
        r = find_channels_room(self.channel_name)
        if r:
            async_to_sync(self.channel_layer.group_discard)(r['id'], self.channel_name)
