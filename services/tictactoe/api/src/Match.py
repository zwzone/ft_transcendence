from    Player  import   Player
from    Move    import   Move

PENDING     = 0
DRAW        = 1
WIN         = 2

class Match():

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
        move    = [ int( move_s[0] ),
                    int( move_s[1] ),
                    int( move_s[2] ), ]

        match player_type:
            case "x":
                match __player_x.simulate( move ):
                    case PENDING:
                        #Pending

                    case WIN:
                        #WIN
                    
                    case DRAW:
                        #Annonce the Draw

                    
Software Enginner | Competitive Programmer | Fullstack | C/C++ Proficient