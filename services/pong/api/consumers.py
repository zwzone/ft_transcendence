from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import random, json

rooms = {}
padd_left = {
    'speed': 30,
    'positionX': 0,
    'positionY': 0,
    'sizeX': 40,
    'sizeY': 200,
}
padd_right = {
    'speed': 30,
    'positionX': 0,
    'positionY': 0,
    'sizeX': 40,
    'sizeY': 200,
}
padd_up = {
    'speed': 30,
    'positionX': 0,
    'positionY': 0,
    'sizeX': 200,
    'sizeY': 40,
}
padd_down = {
    'speed': 30,
    'positionX': 0,
    'positionY': 0,
    'sizeX': 200,
    'sizeY': 40,
}


def ball_direction():
    rand = random.randint(0, 2)
    if rand == 0:
        return 0
    elif rand == 1:
        return 10
    return -10


class Pong(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        room_id = self.scope['url_route']['kwargs']['room_id']
        self.capacity = self.scope['url_route']['kwargs']['capacity']
        await self.channel_layer.group_add(
            room_id,
            self.channel_name
        )
        if room_id not in rooms:
            rooms[room_id] = {
                'padd_left': {
                    'player': self.channel_name,
                    'info': padd_left.copy()
                },
            }
        else:
            if rooms[room_id].get('padd_right') is None and self.capacity >= 2:
                rooms[room_id]['padd_right'] = {
                    'player': self.channel_name,
                    'info': padd_right.copy()
                }
            elif rooms[room_id].get('padd_up') is None and self.capacity > 2:
                rooms[room_id]['padd_up'] = {
                    'player': self.channel_name,
                    'info': padd_up.copy()
                }
            elif rooms[room_id].get('padd_down') is None and self.capacity > 2:
                rooms[room_id]['padd_down'] = {
                    'player': self.channel_name,
                    'info': padd_down.copy()
                }
            if len(rooms[room_id]) == self.capacity:
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
        if (room_id in rooms
                and ((self.channel_name in rooms[room_id]['padd_left']['player'])
                     or (self.channel_name in rooms[room_id]['padd_right']['player'])
                     or (self.channel_name in rooms[room_id]['padd_up']['player'])
                     or (self.channel_name in rooms[room_id]['padd_down']['player']))):
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
        elif self.capacity == 4:
            if text_data == 'left' or text_data == 'a':
                if self.channel_name in rooms[room_id]['padd_up']['player']:
                    rooms[room_id]['padd_up']['info']['positionX'] -= rooms[room_id]['padd_up']['info']['speed']
                elif self.channel_name in rooms[room_id]['padd_down']['player']:
                    rooms[room_id]['padd_down']['info']['positionX'] -= rooms[room_id]['padd_down']['info']['speed']
            elif text_data == 'right' or text_data == 'd':
                if self.channel_name in rooms[room_id]['padd_up']['player']:
                    rooms[room_id]['padd_up']['info']['positionX'] += rooms[room_id]['padd_up']['info']['speed']
                elif self.channel_name in rooms[room_id]['padd_down']['player']:
                    rooms[room_id]['padd_down']['info']['positionX'] += rooms[room_id]['padd_down']['info']['speed']
        self.paddleCollision(room_id)

    async def start_game(self, room_id):
        self.init_game(room_id)
        rooms[room_id]['ball']['positionX'] += rooms[room_id]['ball']['speedX']
        rooms[room_id]['ball']['positionY'] += rooms[room_id]['ball']['speedY']
        print(self.channel_layer.groups.get(room_id, {}).items(), flush=True)
        await self.channel_layer.group_send(
            room_id,
            {
                'type': 'pong.message',
                'message': 'ball',
            }
        )
        if room_id in rooms:
            await asyncio.create_task(self.game_loop(room_id))

    def init_game(self, room_id):
        rooms[room_id]['padd_left']['info']['score'] = 0
        rooms[room_id]['padd_right']['info']['score'] = 0
        if self.capacity == 4:
            rooms[room_id]['canvas_width'] = 1300
            rooms[room_id]['canvas_height'] = 1300
            rooms[room_id]['padd_up']['info']['score'] = 0
            rooms[room_id]['padd_up']['info']['positionX'] = rooms[room_id]['canvas_width'] / 2 - 100
            rooms[room_id]['padd_up']['info']['positionY'] = 100
            rooms[room_id]['padd_down']['info']['score'] = 0
            rooms[room_id]['padd_down']['info']['positionX'] = rooms[room_id]['canvas_width'] / 2 - 100
            rooms[room_id]['padd_down']['info']['positionY'] = rooms[room_id]['canvas_height'] - 100
        else:
            rooms[room_id]['canvas_width'] = 1920
            rooms[room_id]['canvas_height'] = 1080
        rooms[room_id]['padd_left']['info']['positionX'] = 60
        rooms[room_id]['padd_left']['info']['positionY'] = rooms[room_id]['canvas_height'] / 2 - 100
        rooms[room_id]['padd_right']['info']['positionX'] = rooms[room_id]['canvas_width'] - 100
        rooms[room_id]['padd_right']['info']['positionY'] = rooms[room_id]['canvas_height'] / 2 - 100
        rooms[room_id]['ball'] = {
            'speedX': ball_direction(),
            'speedY': ball_direction(),
            'positionX': rooms[room_id]['canvas_width'] / 2,
            'positionY': rooms[room_id]['canvas_height'] / 2,
            'size': 20,
        }

    def reset_game(self, room_id):
        if rooms[room_id]['ball']['speedX'] > 0:
            rooms[room_id]['padd_right']['info']['score'] += 1
            rooms[room_id]['ball']['speedX'] = 10
        else:
            rooms[room_id]['padd_left']['info']['score'] += 1
            rooms[room_id]['ball']['speedX'] = -10
        rooms[room_id]['ball']['positionX'] = rooms[room_id]['canvas_width'] / 2
        rooms[room_id]['ball']['positionY'] = rooms[room_id]['canvas_height'] / 2
        rooms[room_id]['ball']['speedY'] = ball_direction()
        rooms[room_id]['padd_left']['info']['positionY'] = rooms[room_id]['canvas_height'] / 2 - 100
        rooms[room_id]['padd_right']['info']['positionY'] = rooms[room_id]['canvas_height'] / 2 - 100
        if self.capacity == 4:
            rooms[room_id]['padd_up']['info']['positionX'] = rooms[room_id]['canvas_width'] / 2 - 100
            rooms[room_id]['padd_down']['info']['positionX'] = rooms[room_id]['canvas_width'] / 2 - 100

    def BallCollision(self, room_id):
        if ((rooms[room_id]['ball']['positionX'] +
             rooms[room_id]['ball']['size'] >= rooms[room_id]['canvas_width']) or
                (rooms[room_id]['ball']['positionX'] -
                 rooms[room_id]['ball']['size'] <= 0)):
            self.reset_game(room_id)
        if ((rooms[room_id]['ball']['positionY'] +
            rooms[room_id]['ball']['size'] >= rooms[room_id]['canvas_height'])
                or (rooms[room_id]['ball']['positionY'] - rooms[room_id]['ball']['size'] <= 0)):
            if self.capacity == 4:
                self.reset_game(room_id)
            else:
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
        tmp = size_x
        size_x = size_y
        size_y = tmp
        if side == 'upX':
            return rooms[room_id]['padd_up']['info']['positionX'] + size_x / 2
        elif side == 'upY':
            return rooms[room_id]['padd_up']['info']['positionY'] + size_y / 2
        elif side == 'downX':
            return rooms[room_id]['padd_down']['info']['positionX'] + size_x / 2
        elif side == 'downY':
            return rooms[room_id]['padd_down']['info']['positionY'] + size_y / 2

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
        if self.capacity == 4:
            tmp = sizeX
            sizeX = sizeY
            sizeY = tmp
            upX_center = self.get_padd_center(room_id, 'upX')
            upY_center = self.get_padd_center(room_id, 'upY')
            downX_center = self.get_padd_center(room_id, 'downX')
            downY_center = self.get_padd_center(room_id, 'downY')
            up_dx = abs(rooms[room_id]['ball']['positionX'] - upX_center)
            up_dy = abs(rooms[room_id]['ball']['positionY'] - upY_center)
            down_dx = abs(rooms[room_id]['ball']['positionX'] - downX_center)
            down_dy = abs(rooms[room_id]['ball']['positionY'] - downY_center)
            if up_dx <= rooms[room_id]['ball']['size'] + sizeX / 2 and \
                    up_dy <= rooms[room_id]['ball']['size'] + sizeY / 2:
                if (rooms[room_id]['ball']['positionY'] >=
                    upY_center and rooms[room_id]['ball']['speedY'] > 0) or (
                        rooms[room_id]['ball']['positionY'] <=
                        upY_center and rooms[room_id]['ball']['speedY'] < 0):
                    return
                rooms[room_id]['ball']['speedY'] *= -1
            elif down_dx <= rooms[room_id]['ball']['size'] + sizeX / 2 and \
                    down_dy <= rooms[room_id]['ball']['size'] + sizeY / 2:
                if (rooms[room_id]['ball']['positionY'] >=
                    downY_center and rooms[room_id]['ball']['speedY'] > 0) or (
                        rooms[room_id]['ball']['positionY'] <=
                        downY_center and rooms[room_id]['ball']['speedY'] < 0):
                    return
                rooms[room_id]['ball']['speedY'] *= -1

    def paddleCollision(self, room_id):
        size = rooms[room_id]['padd_right']['info']['sizeY']
        pos_right = rooms[room_id]['padd_right']['info']['positionY']
        pos_left = rooms[room_id]['padd_left']['info']['positionY']
        if pos_right + size >= rooms[room_id]['canvas_height']:
            rooms[room_id]['padd_right']['info']['positionY'] \
                = rooms[room_id]['canvas_height'] - size
        elif pos_right <= 0:
            rooms[room_id]['padd_right']['info']['positionY'] = 0
        if pos_left + size >= rooms[room_id]['canvas_height']:
            rooms[room_id]['padd_left']['info']['positionY'] \
                = rooms[room_id]['canvas_height'] - size
        elif pos_left <= 0:
            rooms[room_id]['padd_left']['info']['positionY'] = 0
        if self.capacity == 4:
            size = rooms[room_id]['padd_up']['info']['sizeX']
            pos_up = rooms[room_id]['padd_up']['info']['positionX']
            pos_down = rooms[room_id]['padd_down']['info']['positionX']
            if pos_up + size >= rooms[room_id]['canvas_width']:
                rooms[room_id]['padd_up']['info']['positionX'] \
                    = rooms[room_id]['canvas_width'] - size
            elif pos_up <= 0:
                rooms[room_id]['padd_up']['info']['positionX'] = 0
            if pos_down + size >= rooms[room_id]['canvas_width']:
                rooms[room_id]['padd_down']['info']['positionX'] \
                    = rooms[room_id]['canvas_width'] - size
            elif pos_down <= 0:
                rooms[room_id]['padd_down']['info']['positionX'] = 0

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
            if rooms[room_id]['ball']['speedX'] > 0:
                rooms[room_id]['ball']['speedX'] += 0.01
            else:
                rooms[room_id]['ball']['speedX'] -= 0.01
            if rooms[room_id]['ball']['speedY'] > 0:
                rooms[room_id]['ball']['speedY'] += 0.01
            else:
                rooms[room_id]['ball']['speedY'] -= 0.01
            await asyncio.sleep(0.015)
        print(rooms)
