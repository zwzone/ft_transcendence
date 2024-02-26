import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

#Macro-Begin
SIMULATE    = "simulate"
EXIT        = "exit"
#Macro-End

#Data-Begin
game        = Game()


class Player():
    def __init__( self ):
        __sub_board   = [] #sub_board
        __board       = [] #board

        __bot_path    = "" #bot_path
        __mode        = "" #mode ( manual, bot, ai )

    def __str__( self ):
        return  "sub_board   : " +  __sub_board + "\n"
              + "board       : " +  __board     + "\n"
              + "bot_path    : " +  __bot_path  + "\n"
              + "mode        : " +  __mode


    def __move_sub_board( move ):
        pass

    def __move_board( move ):
        pass

    def __play( move ):
        pass

    def __win( ):
        pass

    def simulate( move_s ):
        move = [ int( _move_s[0] ), int( _move_s[1] ) ]

        __play( move )

        match 


class Game():

    def __init__( self ):
        __id        = ""
        __player_x  = Player() #player_x
        __player_o  = Player() #player_o
        __moves     = [ ] #moves

    def __str__( self ):
        return  "id         : " + __id          + "\n"
              + "player_x   : " + __player_x    + "\n"
              + "player_o   : " + __player_o    + "\n"
              + "moves      : " + __moves


    def simulate( move_s, player_type ):
        match player_type:
            case "x":




class TicTacToeConsumer( AsyncJsonWebsocketConsumer ):

    async def connect( self ):


    async def disconnect( self, close_code ):


    async def receive( self, data ):
        
        data        = json.loads( data )
        data_type   = data.get("type")


        match data_type:

            case "simulate":
                simulate( data )

            case "exit":
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
        
            


            



