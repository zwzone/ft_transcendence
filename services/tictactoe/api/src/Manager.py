from    Match   import  MatchC

class MatchManager:
    def __init__( self ):
        self.__matches  = { "PENDING"   : {},
                            "PLAYING"   : {} }
        self.__players  = {} # id : Player()

    def get_match( self, match_status, room_name ):
        return  self.__matches[ match_status ][ room_name ]                     \
                    if room_name in self.__matches[ match_status ] [room_name]  \
                    else None
    
    def add_match( self, type, room_name ):
        match type:
            case "PENDING":
                #Create in database -> match_id
                match_id = 0

                self.__pending_matches[ room_name ]  = MatchC( match_id, type )
                
            case "PLAYING":
                #Create in database -> match_id
                match_id = 0

                self.__pending_matches[ room_name ]  = MatchC( match_id, type )
                
    def add_user( self, id, player ):
        if id in self.__players:
            return
        self.__players[ id ] = player

    def get_user( self, id ):
        return self.__players[ id ] if id in self.__players else None
    
