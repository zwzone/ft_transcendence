from    Match   import  PENDING, DRAW, WIN

class Player():
    def __init__( self ):
        __board             = [ [ [ [ 0 for _ in range( 3 ) ]
                                    for _ in range( 3 ) ]
                                    for _ in range( 3 ) ]
                                    for _ in range( 3 ) ]

        __sub_board_stats   = [ [ { "row"       : [ 0 for _ in range( 3 ) ],
                                    "column"    : [ 0 for _ in range( 3 ) ],
                                    "diagonal"  : [ 0 for _ in range( 6 ) ],
                                    "stat"      : "Pending" }
                                    for _ in range( 3 ) ]
                                    for _ in range( 3 ) ]

        __board_stats       = { "row"       : [0 for _ in range( 3 ) ],
                                "column"    : [0 for _ in range( 3 ) ],
                                "diagonal"  : [0 for _ in range( 6 ) ] }

        __bot_path          = "" #bot_path
        __mode              = "" #mode ( manual, bot, ai )

    def __str__( self ):
        return  "sub_board   : " +  __sub_board + "\n"
              + "board       : " +  __board     + "\n"
              + "bot_path    : " +  __bot_path  + "\n"
              + "mode        : " +  __mode

    def __move_sub_board( move ):
        __sub_board_stats[ move.__sub_board_row ]
                         [ move.__sub_board_column ]
                         [ "row" ]
                         [ move.__row ] += 1

        __sub_board_stats[ move.__sub_board_row ]
                         [ move.__sub_board_column ]
                         [ "column" ]
                         [ move.__column ] += 1

        __sub_board_stats[ move.__sub_board_row ]
                         [ move.__sub_board_column ]
                         [ "diagonal" ]
                         [ move.__column + move.__row ] += 1

        __sub_board_stats[ move.__sub_board_row ]
                         [ move.__sub_board_column ]
                         [ "diagonal" ]
                         [ abs( move.__column -  move.__row ) ] += 1

    def __move_board( move ):
        if ( __sub_board_stats[ move.__sub_board_row ]
                              [ move.__sub_board_column ]
                              [ "row" ]
                              [ move.__row ] == 3
            or
            __sub_board_stats[ move.__sub_board_row ]
                            [ move.__sub_board_column ]
                            [ "column" ]
                            [ move.__column ] == 3
            or
            __sub_board_stats[ move.__sub_board_row ]
                            [ move.__sub_board_column ]
                            [ "diagonal" ]
                            [ move.__column + move.__row ] == 3
            or
            __sub_board_stats[ move.__sub_board_row ]
                            [ move.__sub_board_column ]
                            [ "diagonal" ]
                            [ abs( move.__column -  move.__row ) ] == 3 )
            __board_stats[   "row"   ][ move.__sub_board_row ]                                  += 1
            __board_stats[  "column" ][ move.__sub_board_column ]                               += 1
            __board_stats[ "digonal" ][ move.__sub_board_column + move.__sub_board_row ]        += 1
            __board_stats[ "digonal" ][ abs( move.__sub_board_column - move.__sub_board_row ) ] += 1
                        
    def __play( move ):
        __move_sub_board( move )
        __move_board    ( move )

    def __stat( ):
        Pending = false

        for r in range ( 3 ):
            for c in range ( 3 ):
                for e in range ( 3 ):
                    if __board_stats[ "row" ][ e ] == 3:
                        return  "WIN"
                    if __board_stats[ "column" ][ e ] == 3:
                        return  "WIN"

                for e in range ( 6 ):
                    if __board_stats[ "diagonal" ][ e ] == 3:
                        return  "WIN"

        return  "PENDING"
        

    def simulate( move ):
        __play( move )
        
        return  __stat()


# 0000 0001 0002     0100 0101 0102     0200 0201 0202
# 0010 0011 0012     0110 0111 0112     0210 0211 0212
# 0020 0021 0022     0120 0121 0122     0220 0221 0222