from    channels.generic.websocket  import  AsyncWebsocketConsumer
class TicTacToeConsumer( AsyncWebsocketConsumer ):

    async def connect( self ):
        self.__proc = None
        # print("Connected", flush=True)
        await self.channel_layer.group_add(
            "test",
            self.channel_name

        )
        await self.accept()


    async def disconnect( self, close_code ):
        print("disconnected", flush=True)
        await self.channel_layer.group_discard(
            "test",
            self.channel_name
        )

    async def receive( self, text_data=None ):
        pass