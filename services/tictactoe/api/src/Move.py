class Move( ):
    def __init__( self, row_        = -1,
                        column_     = -1,
                        sub_board_  = -1,
                        type_       = -1 ):
        self.__row          = row_
        self.__column       = column_
        self.__sub_board    = sub_board_
        self.__type         = type_
  
    @property
    def row( self ):
        return  self.__row
    @row.setter
    def row( self, row_ ):
        self.__row = row_
    
    @property
    def column( self ):
        return  self.__column
    @column.setter
    def set_column( self, column_ ):
        __column = column_

    @property
    def sub_board( self ):
        return  __sub_board
    @sub_board.setter
    def set_row( self, row ):
        __sub_board = sub_board
