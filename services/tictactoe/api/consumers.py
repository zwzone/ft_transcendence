from    channels.generic.websocket  import  AsyncWebsocketConsumer
from    .src.Match                  import  MatchC, Matches
            
class TicTacToeConsumer( AsyncWebsocketConsumer ):

    async def connect( self ):
        pass 

    async def disconnect( self, close_code ):
        pass

    async def receive( self, text_data=None ):
        pass

            


            





            



