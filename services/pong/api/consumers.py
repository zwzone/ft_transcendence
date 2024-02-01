from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio

import json

rooms = {}
canvas_width = 1920
canvas_height = 1080
padd_left = {
    'speed': 15,
    'positionX': 60,
    'positionY': canvas_height / 2 - 100,
    'sizeX': 40,
    'sizeY': 200
}
padd_right = {
    'speed': 15,
    'positionX': canvas_width - 100,
    'positionY': canvas_height / 2 - 100,
    'sizeX': 40,
    'sizeY': 200
}


class Pong(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        room_id = self.scope['url_route']['kwargs']['room_id']
        capacity = self.scope['url_route']['kwargs']['capacity']
        await self.channel_layer.group_add(
            room_id,
            self.channel_name
        )
        if room_id not in rooms:
            rooms[room_id] = {
                'padd_left': {
                    'player': self.channel_name,
                    'info': padd_left
                },
            }
        else:
            rooms[room_id]['padd_right'] = {
                'player': self.channel_name,
                'info': padd_right
            }
            if len(rooms[room_id]) == capacity:
                await self.start_game(room_id)

    async def pong_message(self, event):
        if (event['message'] == 'ball'
                and self.scope['url_route']['kwargs']['room_id'] in rooms):
            await self.send(text_data=json.dumps(
                rooms[self.scope['url_route']['kwargs']['room_id']]
            ))

    async def disconnect(self, close_code):
        room_id = self.scope['url_route']['kwargs']['room_id']
        await self.channel_layer.group_discard(
            room_id,
            self.channel_name
        )
        if room_id in rooms and self.channel_name in rooms[room_id]:
            del rooms[room_id]

    async def receive(self, text_data=None, bytes_data=None):
        room_id = self.scope['url_route']['kwargs']['room_id']
        if text_data == 'up' or text_data == 'w':
            if self.channel_name in rooms[room_id]['padd_left']['player']:
                rooms[room_id]['padd_left']['info']['positionY'] -= rooms[room_id]['padd_left']['info']['speed']
            elif self.channel_name in rooms[room_id]['padd_right']['player']:
                rooms[room_id]['padd_right']['info']['positionY'] -= rooms[room_id]['padd_right']['info']['speed']
        elif text_data == 'down' or text_data == 's':
            if self.channel_name in rooms[room_id]['padd_left']['player']:
                rooms[room_id]['padd_left']['info']['positionY'] += rooms[room_id]['padd_left']['info']['speed']
            elif self.channel_name in rooms[room_id]['padd_right']['player']:
                rooms[room_id]['padd_right']['info']['positionY'] += rooms[room_id]['padd_right']['info']['speed']

    async def start_game(self, room_id):
        self.init_game(room_id)
        rooms[room_id]['ball']['positionX'] += rooms[room_id]['ball']['speedX']
        rooms[room_id]['ball']['positionY'] += rooms[room_id]['ball']['speedY']
        await self.channel_layer.group_send(
            room_id,
            {
                'type': 'pong_message',
                'message': 'ball',
            }
        )
        if room_id in rooms:
            asyncio.create_task(self.game_loop(room_id))

    def init_game(self, room_id):
        rooms[room_id]['ball'] = {
            'speedX': 10,
            'speedY': 10,
            'positionX': 10,
            'positionY': 10,
            'size': 20
        }
        # rooms[room_id]['padd_left'] = {
        #     'speed': 15,
        #     'positionX': 60,
        #     'positionY': canvas_height / 2 - 100,
        #     'sizeX': 40,
        #     'sizeY': 200
        # }
        # rooms[room_id]['padd_right'] = {
        #     'speed': 15,
        #     'positionX': canvas_width - 100,
        #     'positionY': canvas_height / 2 - 100,
        #     'sizeX': 40,
        #     'sizeY': 200
        # }

    def BallCollision(self, room_id):
        if (rooms[room_id]['ball']['positionX'] +
                rooms[room_id]['ball']['size'] >= canvas_width):
            rooms[room_id]['ball']['speedX'] *= -1
        if (rooms[room_id]['ball']['positionX'] -
                rooms[room_id]['ball']['size'] <= 0):
            rooms[room_id]['ball']['speedX'] *= -1
        if (rooms[room_id]['ball']['positionY'] +
                rooms[room_id]['ball']['size'] >= canvas_height):
            rooms[room_id]['ball']['speedY'] *= -1
        if (rooms[room_id]['ball']['positionY'] -
                rooms[room_id]['ball']['size'] <= 0):
            rooms[room_id]['ball']['speedY'] *= -1

    def get_padd_center(self, room_id, side):
        size_x = rooms[room_id]['padd_left']['info']['sizeX']
        size_y = rooms[room_id]['padd_left']['info']['sizeY']
        if side == 'leftX':
            return rooms[room_id]['padd_left']['info']['positionX'] + size_x / 2
        elif side == 'leftY':
            return rooms[room_id]['padd_left']['info']['positionY'] + size_y / 2
        elif side == 'rightX':
            return rooms[room_id]['padd_right']['info']['positionX'] + size_x / 2
        elif side == 'rightY':
            return rooms[room_id]['padd_right']['info']['positionY'] + size_y / 2

    def BallPaddleCollision(self, room_id):
        sizeY = rooms[room_id]['padd_left']['info']['sizeY']
        sizeX = rooms[room_id]['padd_left']['info']['sizeX']
        leftX_center = self.get_padd_center(room_id, 'leftX')
        leftY_center = self.get_padd_center(room_id, 'leftY')
        rightX_center = self.get_padd_center(room_id, 'rightX')
        rightY_center = self.get_padd_center(room_id, 'rightY')
        left_dx = abs(rooms[room_id]['ball']['positionX'] - leftX_center)
        left_dy = abs(rooms[room_id]['ball']['positionY'] - leftY_center)
        right_dx = abs(rooms[room_id]['ball']['positionX'] - rightX_center)
        right_dy = abs(rooms[room_id]['ball']['positionY'] - rightY_center)
        if (left_dx <= rooms[room_id]['ball']['size'] + sizeX / 2 and
                left_dy <= rooms[room_id]['ball']['size'] + sizeY / 2):
            if (rooms[room_id]['ball']['positionX'] >=
                    leftX_center and rooms[room_id]['ball']['speedX'] > 0) or (
                        rooms[room_id]['ball']['positionX'] <=
                        leftX_center and rooms[room_id]['ball']['speedX'] < 0):
                return
            rooms[room_id]['ball']['speedX'] *= -1
        elif (right_dx <= rooms[room_id]['ball']['size'] + sizeX / 2 and
                right_dy <= rooms[room_id]['ball']['size'] + sizeY / 2):
            if (rooms[room_id]['ball']['positionX'] >=
                    rightX_center and rooms[room_id]['ball']['speedX'] > 0) or (
                        rooms[room_id]['ball']['positionX'] <=
                        rightX_center and rooms[room_id]['ball']['speedX'] < 0):
                return
            rooms[room_id]['ball']['speedX'] *= -1

    def paddleCollision(self, room_id):
        size = rooms[room_id]['padd_right']['info']['sizeY']
        pos_right = rooms[room_id]['padd_right']['info']['positionY']
        pos_left = rooms[room_id]['padd_left']['info']['positionY']
        if pos_right + size >= canvas_height:
            rooms[room_id]['padd_right']['info']['positionY']\
                = canvas_height - size
        elif pos_right <= 0:
            rooms[room_id]['padd_right']['info']['positionY'] = 0
        if pos_left + size >= canvas_height:
            rooms[room_id]['padd_left']['info']['positionY']\
                = canvas_height - size
        elif pos_left <= 0:
            rooms[room_id]['padd_left']['info']['positionY'] = 0

    async def game_loop(self, room_id):
        while True:
            if room_id not in rooms:
                print('Game over for: ', room_id)
                break
            rooms[room_id]['ball']['positionX'] += rooms[room_id]['ball']['speedX']
            rooms[room_id]['ball']['positionY'] += rooms[room_id]['ball']['speedY']
            self.BallCollision(room_id)
            self.paddleCollision(room_id)
            self.BallPaddleCollision(room_id)
            await self.channel_layer.group_send(
                room_id,
                {
                    'type': 'pong_message',
                    'message': 'ball',
                }
            )
            await asyncio.sleep(0.015)
        print(rooms)