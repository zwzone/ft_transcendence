from    channels.generic.websocket  import  AsyncWebsocketConsumer
from    .src.Match                  import  MatchC
from    .src.Manager           import  Manager

__manager   = Manager()

class   TicTacToeGameConsumer( AsyncWebsocketConsumer ):
    async def   connect( self ):
        self.__room_name        = "test"
        self.__user             = __manager.get_user( id )

        await self.accept()

        await self.channel_layer.group_add(
            self.__room_name,
            self.channel_name
        )
        
        self.__match = __manager.get_match( self.__room_name )

        if  not __manager.is_match( self.__room_name ):
            # room_name doesn't exist room doesn't exist
            pass


        self.__match.connect_player( self.__user )

        match self.__match.status:
            case "PENDING":
                match self.__match.connections:
                    case 2:
                        self.__match.status = "PLAYING"
                        #Be careful with this if you update the status may go to other case
                        self.__match.abort_cancel()
    
            case "PLAYING":
                self.__match.forfeit_cancel( self.__user.id )

    async def   disconnect( self, code ):
        self.channel_layer.group_discard(
            self.__room_name,
            self.channel_name
        )
        match self.__match.status:
            case "PLAYING":
                self.__match.forfeit_lunch()

    async def receive( self, text_data ):
        move_mode   = text_data["mode"]
        move_value  = text_data["move"]

        await self.__simulate( move_mode, move_value )



    async def __simulate( self, move_mode, move_value ):
        

                

class   TicTacToeLandingConsumer( AsyncWebsocketConsumer ):
    async def   connect( self ):
        # check if the user already connected
    
        # close the old connection

        # connect the new connection which is this

        # fitch player matches
            # pending
            # playing

        # fitch friends
            # send them
        pass

    async def   disconnect(self, code):
        # discard the channel...
        pass

    async def   receive(self, text_data ):
        # match
            # try to match with another one waiting

        # challenge friend
            # add a match pending for both of them in db
            # send new-challenge ( match_id ) send to all connect channels that are for the user
        pass