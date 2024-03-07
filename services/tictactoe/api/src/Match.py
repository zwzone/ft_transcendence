import                      asyncio
from    .Player  import     Player
from    .Move    import     MoveC

PENDING     = 0
DRAW        = 1
WIN         = 3
class Match():
    def __init__( self ):
        self.__id               = 0
        self.__room_name        = "" #using player
        self.__state            = "PENDING" # "CONTINUE", #WIN #LOSE #DRAW
        self.__winner           = 0 #id_winner
        self.__players          = {} # { id1:player[0], id2:player[2] }
        self.__bot_players      = {}
        self.__manual_players   = {}
        self.__moves            = [ ] #moves
        self.__turn             = 0 # id

    def __str__( self ):
        return  "id         : " + str(self.__id)          + "\n"  \
              + "moves      : " + str(self.__moves)
            #   + "player_x   : " + self.__player_x    + "\n"  \ 
            #   + "player_o   : " + self.__player_o    + "\n"  \

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

    async def simulate( self, move_s, mode, player_id ):
        move    = MoveC( int( move_s[2] ),
                         int( move_s[3] ),
                         int( move_s[0] ),
                         int( move_s[1] ) )
        
        
                        
