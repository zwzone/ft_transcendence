from    Match   import  PENDING, DRAW, WIN

class Player():
    def __init__( self ):
        __board   = [ [ [ 0 for _ in range( 3 ) ] for _ in range( 3 ) ] for _ in range( 9 ) ] #sub_board
        __bot_path    = "" #bot_path
        __mode        = "" #mode ( manual, bot, ai )

    def __str__( self ):
        return  "sub_board   : " +  __sub_board + "\n"
              + "board       : " +  __board     + "\n"
              + "bot_path    : " +  __bot_path  + "\n"
              + "mode        : " +  __mode


    def __move_sub_board( move ):
        

    def __move_board( move ):
        pass

    def __play( move ):
        __move_sub_board( move )
        __move_board    ( move )

    def __win( ):
        

    def simulate( move ):
        __play( move )
        
        return  __win()

