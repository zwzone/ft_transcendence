from    .Board  import  Board

class Player():
    def __init__( self, id ):
        self.__username = ""
        self.__id       = id
        self.__choice   = "" # X or O

        self.__board    = Board()
    
    def simulate( self, move ):
        return  self.__board.simulate( move )

    
        
    