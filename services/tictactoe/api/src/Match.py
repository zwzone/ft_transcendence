import                      asyncio
from    .Player  import     PlayerC
from    .Move    import     MoveC

PENDING     = 0
DRAW        = 1
WIN         = 3

Matches     = { "PENDING":{}, "MATCHING":{}, "PLAYING":{} }
Users       = { "PENDING"}

class MatchC():
    def __init__( self,  ):
        self.__id        = "" #generate using database
        self.__room_name = "" #using player
        self.__state     = "PENDING"  
        self.__moves     = [ ] #moves

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
        Matches[ self.__state ].pop( self.__id )
        #end

    async def wait_player( self ):
        await asyncio.sleep( 15 )

        # Can have mutexes
        # Abort the player and the other one win
        # end

    def simulate( self, move_s, type_player ):
        move    = MoveC( type_player,
                        int( move_s[2] ),
                        int( move_s[3] ),
                        int( move_s[0] ),
                        int( move_s[1] ) )

        match move.type_player:
            case "x":
                return self.__player_x.simulate( move )
            case "o":
                return self.__player_o.simulate( move )