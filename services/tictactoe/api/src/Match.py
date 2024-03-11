import                      asyncio
from    .Player  import     Player
from    .Move    import     Move
from    .Board   import     StateBoard

PENDING     = 0
DRAW        = 1
WIN         = 3

class Match():
    def __init__( self, id ):
        self.__id               = 0
        self.__room_name        = "" #using player
        self.__state            = "PENDING" # "CONTINUE", #WIN, #LOSE, #DRAW, #PAUSE
        self.__players          = {} # { id1:player[0], id2:player[2] }
        self.__owners           = []
        self.__moves            = [ ] #moves
        self.__turn             = 0 # id

        self.__board            = StateBoard()

    @property
    def id( self ):
        return self.__id

    def add_player( self, id ):
        self.__players[ id ] = Player( id )

    def remove_player( self, id ):
        self.__players.pop( id )

    def status( self ):
        if len( self.__players ) == 2:
            return "PLAYING"
        else:
            return "PENDING"

    def simulate( self, move_s, player_id ):
        move    = Move( int( move_s[2] ),
                        int( move_s[3] ),
                        int( move_s[0] ),
                        int( move_s[1] ) )

        response = self.__players[ player_id ].simulate( move )

        return response
        
        
                        
