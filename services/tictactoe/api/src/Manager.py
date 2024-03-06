from    Match   import  MatchC

class ManagerC:
    def __init__( self ):
        self.__matching_matches = {} #id    :MatchC()
        self.__pending_matches  = {} #id    :MatchC()
        self.__playing_matches  = {} #id    :MatchC()
        self.__user_connected   = {} #user  :(channel_name, Player())

    def get_match( self, type, match_room ):
        match type:
            case "MATCHING":
                return  self.__matching_matches[ match_room ]         \
                            if match_room in self.__matching_matches  \
                            else None
            case "PENDING":
                return  self.__pending_matches[ match_room ]          \
                            if match_room in self.__matching_matches  \
                            else None
            case "PLAYING":
                return  self.__playing_matches[ match_room ]          \
                            if match_room in self.__matching_matches  \
                            else None

    def is_match( self, type, match_room ):
        return  match_room in self.__matching_matches \
            or  match_room in self.__pending_matches  \
            or  match_room in self.__playing_matches

    def add_match( self, type, match_room ):
        match type:
            case "MATCHING":
                # Create in database -> match_id
                match_id = 0

                self.__matching_matches[ match_room ] = MatchC( match_id, type )

            case "PENDING":
                #Create in database -> match_id

                self.__pending_matches[ match_room ]  = MatchC( match_id, type )
                
            case "PLAYING":
                self.__
            