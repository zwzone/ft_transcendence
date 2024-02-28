import                                      json
from    channels.generic.websocket  import  AsyncJsonWebsocketConsumer
from    src.Player                  import  Player
from    src.Move                    import  Move
from    src.Match                   import  Match

SIMULATE    = "simulate"
EXIT        = "exit"

Matches     = {}

class TicTacToeConsumer( AsyncJsonWebsocketConsumer ):

    async def connect( self ):
        await self.channel_layer.group_add(
            "test",
            self.channel_name
        )
        await self.accept()
        print("Connected")

    async def disconnect( self, close_code ):
        await self.channel_layer.group_discard(
            "test",
            self.channel_name
        )
        print("disconnected")

    async def receive( self, data ):
        
        data        = json.loads( data )
        data_type   = data.get("type")


        match data_type:

            case "SIMULATE_GAME":
                self.__simulate_game( data )

            case "EXIT_GAME":
                self.__exit_game( data )


        # Check EndGame

    async def __simulate_game( self, data ):
        mode = data.get( "mode" )

        match mode:
            case 'ai':
                # Check Ai bot
                # Send the new result to player
                pass

            case 'bot':
                # Check bot
                # Send the new result to players ( Player didn't provide a valid move )
                pass

            case 'manual':
                # Check data.move
                pass

            case 'match-exit':
                # send the new result to players ( Player abort the match ... )
                pass

    async def __exit_game( self, data ):
        #Abort the game
        #Lose the game
        #Redirect to the intro page
        pass

    async def __end_game():
        pass
        
            


            



