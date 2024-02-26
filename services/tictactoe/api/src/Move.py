class Move( ):
    def __init__( self, type_player_        = -1,
                        row_                = -1,
                        column_             = -1,
                        sub_board_row_      = -1,
                        sub_board_column_   = -1 ):

        self.__row              = row_
        self.__column           = column_
        self.__sub_board_row    = sub_board_row_
        self.__sub_board_column = sub_board_column_
        self.__type_player      = type_player_
  

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
        return  self.__sub_board
    @sub_board_row.setter
    def sub_board_row( self, sub_board_row_ ):
        self.__sub_board_row = sub_board_row_

    @property
    def sub_board_column( self ):
        return  self.__sub_board
    @sub_board_column_.setter
    def sub_board_column( self, sub_board_column_ ):
        self.__sub_board_column = sub_board_column_