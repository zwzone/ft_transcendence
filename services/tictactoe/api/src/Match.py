from    Player  import   Player
from    Move    import   Move

PENDING     = 0
DRAW        = 1
WIN         = 2

class Match():

    def __init__( self ):
        self.__id        = ""
        self.__player_x  = Player() #player_x
        self.__player_o  = Player() #player_o
        self.__moves     = [ ] #moves

    def __str__( self ):
        return  "id         : " + self.__id          + "\n"  \
              + "player_x   : " + self.__player_x    + "\n"  \
              + "player_o   : " + self.__player_o    + "\n"  \
              + "moves      : " + self.__moves

    def simulate( self, move_s, type_player ):
        move    = Move( type_player,
                        int( move_s[2] ),
                        int( move_s[3] ),
                        int( move_s[0] ),
                        int( move_s[1] ) )

        match move.type_player:
            case "x":
                return self.__player_x.simulate( move )
            case "o":
                return self.__player_o.simulate( move )