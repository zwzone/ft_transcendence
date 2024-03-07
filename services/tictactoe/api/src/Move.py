class MoveC( ):
    def __init__( self,
                        row_                = -1,
                        column_             = -1,
                        sub_board_row_      = -1,
                        sub_board_column_   = -1 ):

        self.__row              = row_
        self.__column           = column_
        self.__sub_board_row    = sub_board_row_
        self.__sub_board_column = sub_board_column_
        self.__debug            = ""
        self.__game_info        = ""
  
    def __str__( self ):
        return  "row    :   "   + str( self.__row )                 + "\n"  + \
                "column :   "   + str( self.__column )              + "\n"  + \
                "_sub_r :   "   + str( self.__sub_board_row )       + "\n"  + \
                "_sub_c :   "   + str( self.__sub_board_column )    + "\n"

    @property
    def type_player( self ):
        return  self.__type_player
    @type_player.setter
    def type_player( self, type_player_ ):
        self.__type_player  = type_player_

    @property
    def row( self ):
        return  self.__row
    @row.setter
    def row( self, row_ ):
        self.__row  = row_
    
    @property
    def column( self ):
        return  self.__column
    @column.setter
    def column( self, column_ ):
        self.__column = column_

    @property
    def sub_board_row( self ):
        return  self.__sub_board_row
    @sub_board_row.setter
    def sub_board_row( self, sub_board_row_ ):
        self.__sub_board_row = sub_board_row_

    @property
    def sub_board_column( self ):
        return  self.__sub_board_column
    @sub_board_column.setter
    def sub_board_column( self, sub_board_column_ ):
        self.__sub_board_column = sub_board_column_