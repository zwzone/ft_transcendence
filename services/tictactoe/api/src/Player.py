# from    .Match   import  PENDING, DRAW, WIN

class PlayerC():
    def __init__( self, bot_path ):
        self.__board             = [ [ [ [ 0 for _ in range( 3 ) ]
                                             for _ in range( 3 ) ]
                                             for _ in range( 3 ) ]
                                             for _ in range( 3 ) ]

        self.__sub_board_stats   = [ [ {    "row"       : [ 0 for _ in range( 3 ) ],
                                            "column"    : [ 0 for _ in range( 3 ) ],
                                            "diagonal"  : [ 0 for _ in range( 6 ) ],
                                            "stat"      : "Pending" }
                                            for _ in range( 3 ) ]
                                            for _ in range( 3 ) ]

        self.__board_stats       = {    "row"       : [0 for _ in range( 3 ) ],
                                        "column"    : [0 for _ in range( 3 ) ],
                                        "diagonal"  : [0 for _ in range( 6 ) ]  }

        self.__bot_path          = bot_path #bot_path
        self.__mode              = "" #mode ( manual, bot, ai )

    def __str__( self ):
        return    "board       : " +  self.__board      + "\n" \
                + "bot_path    : " +  self.__bot_path   + "\n" \
                + "mode        : " +  self.__mode

    def __increment_row( self, move ):
        self.__sub_board_stats[ move.sub_board_row ]       \
                              [ move.sub_board_column ]    \
                              [ "row" ]                      \
                              [ move.row ] += 1

    def __increment_column( self, move ):
        self.__sub_board_stats[ move.sub_board_row ]       \
                              [ move.sub_board_column ]    \
                              [ "column" ]                   \
                              [ move.column ] += 1

    def __increment_lb_rt_diagonal( self, move ): #Increment Left-Buttom Right-Top Diagonal
        self.__sub_board_stats[ move.sub_board_row ]       \
                              [ move.sub_board_column ]    \
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
            print("one win", flush=True)
            self.__board_stats[   "row"   ] \
                         [ move.sub_board_row ] += 1
            self.__board_stats[  "column" ] \
                         [ move.sub_board_column ] += 1
            self.__board_stats[ "diagonal" ] \
                         [ move.sub_board_column + move.sub_board_row ] += 1 * ( move.sub_board_column +  move.sub_board_row == 2 )
            self.__board_stats[ "diagonal" ]  \
                              [ abs( move.sub_board_column - move.sub_board_row ) ] += 1 * ( move.sub_board_column == move.sub_board_row )
            self.__sub_board_stats[ move.sub_board_row ]      \
                                  [ move.sub_board_column ]   \
                                  [ "stats" ] = move.type_player # Update Sub-Board stat to move.player_type ( X, O ) [ WIN ]
                        
    def __play( self, move ):
        print(str(move))
        print(self.__board_stats)
        self.__move_sub_board( move )
        self.__move_board    ( move )
    def __stat( self, move ):
        if  self.__board_stats[   "row"   ]             \
                         [ move.sub_board_row ] == 3  \
            or  \
            self.__board_stats[  "column" ]                 \
                         [ move.sub_board_column ] == 3   \
            or  \
            self.__board_stats[ "diagonal" ]     \
                         [ 0 ] == 3             \
            or  \
            self.__board_stats[ "diagonal" ]  \
                         [ 2 ] == 3:
            print("WIN ALL", flush=True)
            return  "WIN"
        #Check Draw
        #else Then
        return "PENDING"

    def simulate( self, move ):
        print("Enter here", flush=True)
        self.__play( move )
        # pass
        return self.__stat( move )


# 0000 0001 0002     0100 0101 0102     0200 0201 0202
# 0010 0011 0012     0110 0111 0112     0210 0211 0212
# 0020 0021 0022     0120 0121 0122     0220 0221 0222