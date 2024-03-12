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
        self.__players          = {} # { id1:player[0], id2:player[2] }
        self.__turn             = 0 # id
        self.__status_end       = "" #WIN DRAW
        self.__board            = StateBoard()

    @property
    def id( self ):
        return self.__id

    def add_player( self, id ):
        self.__players[ id ] = Player( id )
        self.__board.add_player( id )

    def remove_player( self, id ):
        self.__players.pop( id )

    def simulate( self, move_s, player_id ):
        move        = Move( int( move_s[2] ),
                            int( move_s[3] ),
                            int( move_s[0] ),
                            int( move_s[1] ) )
        
        response    = {}
        
        if self.__board.valid_move():
            response[ "type" ]  = "INVALID"
            return response
        
        response            = self.__players[ player_id ].simulate( move )

        if response[ "status" ] != "PLAYING":
            return response

        game_end_check = self.__board.game_end_check()

        if game_end_check[ "status" ] == "PLAYING":
            return response
        
        response[ "status" ] = game_end_check[ "status" ]

        if response[ "status" ] == "DRAW":
            return response
        
        response[ "winner" ] = game_end_check[ "winner" ]
        
        
                        
