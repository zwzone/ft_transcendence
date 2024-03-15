import                      asyncio
from    .Player  import     Player
from    .Move    import     Move
from .Board   import     StateBoard

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from    api.models  import Match as M_Match

PENDING     = 0
DRAW        = 1
WIN         = 3

class Match():
    def __init__( self, id, obj ):
        self.xor_players      = 0
        self.__id               = 0
        self.__room_name        = "" #using player
        self.players            = {} # { id1:player[0], id2:player[2] }
        self.__turn             = 0 # id
        self.__status           = "" #WIN DRAW
        self.__board            = StateBoard()
        self.obj                = obj
        self.winner             = None

    @property
    def id( self ):
        return self.__id

    def get_keys( self ):
        keys = []

        for key in self.players.keys():
            keys.append( key )
        return keys

    def add_player( self, id ):
        self.players[ id ] = Player( id )
    
        self.__board.add_player( id )
        self.xor_players ^= id
        return True

    def remove_player( self, id ):
        print("removing ", id, flush=True)
        self.players.pop( id )
        self.xor_players ^= id
        return True

    def simulate( self, move_s, player_id ):
        move        = Move( int( move_s[2] ),
                            int( move_s[3] ),
                            int( move_s[0] ),
                            int( move_s[1] ) )
        
        response    = {}
        

        if not self.__board.valid_move( move ):
            response[ "type" ]  = "invalid"
            return response
        
        response    = self.players[ player_id ].simulate( move )

        self.__board.do_move_sub( move, player_id )

        if "sub-win" in response:
            self.__board.do_move( move, player_id )

        if response[ "status" ] == "WIN":
            response[ "winner" ] = player_id
            return response
        
        if  response[ "status" ] != "PLAYING" \
         and response[ "status"] != "SUB-WIN":
            return response

        game_end_check = self.__board.game_end_check()

        if game_end_check[ "status" ] == "PLAYING":
            return response
        
        response[ "status" ] = game_end_check[ "status" ]

        if response[ "status" ] == "DRAW":
            return response
        
        response[ "winner" ] = game_end_check[ "winner" ]
        
        return response
    
        
                        
