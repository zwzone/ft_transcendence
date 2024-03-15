# from    .Match   import  PENDING, DRAW, WIN
from    .Move   import  Move

class StateBoard():
    def __init__( self ):
        self.__players           = []
        self.__all_board         = [ [ [ [ False for _ in range( 3 ) ]
                                            for _ in range( 3 ) ]
                                            for _ in range( 3 ) ]
                                            for _ in range( 3 ) ]
        
        self.__sub_board         = [ [ False for _ in range( 3 ) ]
                                             for _ in range( 3 ) ]
        
    def add_player( self, player_id ):
        self.__players.append( player_id )

    def valid_move( self, move ):
        return not self.__all_board[move.sub_board_row]     \
                                   [move.sub_board_column]  \
                                   [move.row]               \
                                   [move.column]            \

    def game_end_check( self ):
        check   = {}
        count   = { self.__players[0]:0, self.__players[1]:0 }

        for s_i in range(3):
            for s_j in range(3):
                if self.__sub_board[s_i][s_j]:
                    count[self.__sub_board[s_i][s_j]] += 1
                    continue

                for m_i in range(3):
                    for m_j in range(3):
                        if not self.__all_board[s_i][s_j][m_i][m_j]:
                            check[ "status" ] = "PLAYING"
                            return check
                        
        if count[ self.__players[0] ] == count[ self.__players[1] ]:
            check[ "status" ] = "DRAW"
        elif count[ self.__players[0] ] < count[ self.__players[1] ]:
            check[ "winner" ] = self.__players[1]
            check[ "status" ] = "WIN"
        else:
            check[ "winner" ] = self.__players[0]
            check[ "status" ] = "WIN"
        
        return check
        
    def do_move_sub( self, move, player_id ):
        self.__all_board[move.sub_board_row][move.sub_board_column][move.row][move.column] = player_id
    
    def do_move( self, move, player_id ):
        self.__sub_board[move.sub_board_row][move.sub_board_column] = player_id
    

class Board():
    

    def __init__( self ):

        self.response            = {}

        self.__sub_board_stats   = [ [ {    "row"       : [ 0 for _ in range( 3 ) ],
                                            "column"    : [ 0 for _ in range( 3 ) ],
                                            "diagonal"  : [ 0 for _ in range( 6 ) ],
                                            "stat"      : "Pending" }
                                            for _ in range( 3 ) ]
                                            for _ in range( 3 ) ]

        self.__board_stats       = {    "row"       : [0 for _ in range( 3 ) ],
                                        "column"    : [0 for _ in range( 3 ) ],
                                        "diagonal"  : [0 for _ in range( 6 ) ]  }
        

    def __increment_row( self, move ):
        self.__sub_board_stats[ move.sub_board_row ]         \
                              [ move.sub_board_column ]      \
                              [ "row" ]                      \
                              [ move.row ] += 1

    def __increment_column( self, move ):
        self.__sub_board_stats[ move.sub_board_row ]         \
                              [ move.sub_board_column ]      \
                              [ "column" ]                   \
                              [ move.column ] += 1

    def __increment_lb_rt_diagonal( self, move ): #Increment Left-Buttom Right-Top Diagonal
        self.__sub_board_stats[ move.sub_board_row ]         \
                              [ move.sub_board_column ]      \
                              [ "diagonal" ]                 \
                              [ move.column + move.row ] += 1 * ( move.column + move.row == 2 )

        # Left-Buttom Right-Top Diagona only if [ move.column + move.row == 2 ]
        #  00  01 (02) 
        #  10 (11) 12
        # (20) 21  22

        # "20" = 2 + 0 = 2 | "11" = 1 + 1 = 2 | "02" = 0 + 2 = 2

    def __increment_lt_rb_diagonal( self, move ): #Increment Left-Top Right-Buttom Diagonal
        self.__sub_board_stats[ move.sub_board_row ]  \
                         [ move.sub_board_column ]    \
                         [ "diagonal" ]                 \
                         [ abs( move.column -  move.row ) ] += 1 * ( move.column == move.row )

        # Left-Buttom Right-Top Diagona only if [ move.__column + move.__row == 2 ]
        # (00) 01  02 
        #  10 (11) 12
        #  20  21 (22)

        # "00" => (0 == 0 ) | "11" => ( 1 == 1 ) | "22" => ( 2 == 2 )

    def __move_sub_board( self, move ):
        self.__increment_row           ( move )
        self.__increment_column        ( move )
        self.__increment_lb_rt_diagonal( move )
        self.__increment_lt_rb_diagonal( move )


    def __check_row( self, move ):
        return  self.__sub_board_stats[ move.sub_board_row ]      \
                                      [ move.sub_board_column ]   \
                                      [ "row" ]                     \
                                      [ move.row ] == 3

    def __check_column( self, move ):
        return  self.__sub_board_stats[ move.sub_board_row ]       \
                                      [ move.sub_board_column ]    \
                                      [ "column" ]                   \
                                      [ move.column ] == 3

    def __check_lb_rt_diagonal( self, move ): #Check Left-Buttom Right-Top Diagonal
        return  self.__sub_board_stats[ move.sub_board_row ]      \
                                      [ move.sub_board_column ]   \
                                      [ "diagonal" ]                \
                                      [ 2 ] == 3

    def __check_lt_rb_diagonal( self, move ): #Check Left-Top Right-Buttom Diagonal
        return  self.__sub_board_stats[ move.sub_board_row ]      \
                                      [ move.sub_board_column ]   \
                                      [ "diagonal" ]                \
                                      [ 0 ] == 3

    def __move_board( self, move ):
        if  self.__check_row           ( move ) or  \
            self.__check_column        ( move ) or  \
            self.__check_lb_rt_diagonal( move ) or  \
            self.__check_lt_rb_diagonal( move ):
            self.__board_stats[   "row"   ] \
                         [ move.sub_board_row ] += 1
            self.__board_stats[  "column" ] \
                         [ move.sub_board_column ] += 1
            self.__board_stats[ "diagonal" ] \
                         [ move.sub_board_column + move.sub_board_row ] += 1 * ( move.sub_board_column +  move.sub_board_row == 2 )
            self.__board_stats[ "diagonal" ]  \
                              [ abs( move.sub_board_column - move.sub_board_row ) ] += 1 * ( move.sub_board_column == move.sub_board_row )
            self.response[ "status" ]   = "SUB-WIN"
            self.response[ "sub-win" ]  = f"{move.sub_board_row}{move.sub_board_column}"
                        
    def __stat( self, move ):
        if  self.__board_stats[   "row"   ]                 \
                              [ move.sub_board_row ] == 3   \
                or  \
                self.__board_stats[  "column" ]                     \
                                  [ move.sub_board_column ] == 3    \
                or  \
                self.__board_stats[ "diagonal" ]    \
                                  [ 0 ] == 3        \
                or  \
                self.__board_stats[ "diagonal" ]  \
                                  [ 2 ] == 3:
            self.response["status"] = "WIN"

        


            
    def __play( self, move ):
        self.__move_sub_board( move )
        self.__move_board    ( move )
        self.__stat( move )

        if "status" not in self.response:
            self.response["status"] = "PLAYING"


    def simulate( self, move ):
        self.response = {}
        self.__play( move )
        return self.response

# 0000 0001 0002     0100 0101 0102     0200 0201 0202
# 0010 0011 0012     0110 0111 0112     0210 0211 0212
# 0020 0021 0022     0120 0121 0122     0220 0221 0222