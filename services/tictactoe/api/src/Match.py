from    .Player  import   PlayerC
from    .Move    import   MoveC

PENDING     = 0
DRAW        = 1
WIN         = 3

class MatchC():

    def __init__( self ):
        self.__id        = ""
        self.__player_x  = PlayerC() #player_x
        self.__player_o  = PlayerC() #player_o
        self.__moves     = [ ] #moves

    def __str__( self ):
        return  "id         : " + str(self.__id)          + "\n"  \
              + "moves      : " + str(self.__moves)
            #   + "player_x   : " + self.__player_x    + "\n"  \ 
            #   + "player_o   : " + self.__player_o    + "\n"  \

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