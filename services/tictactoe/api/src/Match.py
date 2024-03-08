import                      asyncio
from    .Player  import     Player
from    .Move    import     Move

PENDING     = 0
DRAW        = 1
WIN         = 3
class Match():
    def __init__( self ):
        self.__id               = 0
        self.__room_name        = "" #using player
        self.__state            = "PENDING" # "CONTINUE", #WIN, #LOSE, #DRAW, #PAUSE
        self.__winner           = 0 #id_winner
        self.__players          = {} # { id1:player[0], id2:player[2] }
        self.__owners           = {}
        self.__bot_players      = {}
        self.__manual_players   = {}
        self.__moves            = [ ] #moves
        self.__turn             = 0 # id

    def add_player( self, id ):
        self.__players[ id ] = 1

    def remove_player( self, id ):
        self.__players.pop( id )

    def status( self ):
        print( "players ", self.__players )
        if len( self.__players ) == 2:
            return "PLAYING"
        else:
            return "PENDING"

    async def wait_match( self ):
        await asyncio.sleep( 120 )
        #incst
        #incst
        #incst
        #incst
        #incst
        #incst
        # Can have mutexes
        # Matches[ self.__state ].pop( self.__id )
        #end

    async def wait_player( self ):
        await asyncio.sleep( 15 )

        # Can have mutexes
        # Abort the player and the other one win
        # end

    def simulate( self, move_s, mode, player_id ):
        move    = Move( int( move_s[2] ),
                        int( move_s[3] ),
                        int( move_s[0] ),
                        int( move_s[1] ) )
        
        self.__players[ player_id ].simulate( move )
        
        
                        
