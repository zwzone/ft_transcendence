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


    async def disconnect( self, close_code ):


    async def receive( self, data ):
        
        data        = json.loads( data )
        data_type   = data.get("type")


        match data_type:

            case SIMULATE:
                simulate( data )

            case EXIT:
                exit_game( data )


        # Check EndGame

    async def simulate_game( self, data ):
        mode = data.get( "mode" )

        match mode:
            case 'ai':
                # Check Ai bot
                # Send the new result to player
                

            case 'bot':
                # Check bot
                # Send the new result to players ( Player didn't provide a valid move )

            case 'manual':
                # Check data.move

            case 'match-exit':
                # send the new result to players ( Player abort the match ... )

    async def exit_game( self, data ):
        #Abort the game
        #Lose the game
        #Redirect to the intro page
        pass

    async def end_game():
        pass
        
            


            



