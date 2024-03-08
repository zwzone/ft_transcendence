from    channels.generic.websocket  import  AsyncWebsocketConsumer
import                                      json
from    .src.Match                  import  Match
# from    .src.Manager                import  Manager

# __manager   = Manager()

mmatch = Match()
num = 0
# btws = 0

class   TicTacToeGameConsumer( AsyncWebsocketConsumer ):
    async def   connect( self ):
        global num
        self.__id               = num
        # btws = btws ^ num
        num += 1 # resolve from the middleware
        # self.__id_opponent      = 2
        self.__room_name        = "test"
        # self.__player           = __manager.get_player( id )

        await self.accept()

        await self.channel_layer.group_add(
            self.__room_name,
            self.channel_name 
        )

        mmatch.add_player( self.__id )

        match mmatch.status():
            case "PLAYING":
                print( "what", flush=True)
                await self.channel_layer.group_send(
                    self.__room_name,
                    {
                        "type"      : "start_game",
                    } )
        
        
    async def start_game( self, data ):
        await self.send( json.dumps( {  "type"      : "start-game",
                                        "player-me" : self.__id,
                                        "choice-me" : "x" if self.__id == 0 else "o",
                                        "player-op" : 1 if self.__id == 0 else 0,
                                        "choice-op" : "o" if self.__id == 0 else "x",
        }))
        # await self.__preface_game()

    async def play_move( self, data ):
        await self.send( json.dumps( {
            "type"  : "move",
            "status": data["status"],
            "move"  : data["move"],
            "player": data["player"],
        }))

    async def   disconnect( self, code ):
        await self.channel_layer.group_discard(
            self.__room_name,
            self.channel_name
        )

        mmatch.remove_player( self.__id )
        # match self.__match.status:
        #     case "PLAYING":
        #         if  self.__id in self.__manual_players:
        #             self.__match.forfeit_lunch()

    async def receive( self, text_data ):
        if  mmatch.status() != "CONTINUE":
            # Wait game start
            pass

        print("move", flush=True)
        # await self.channel_layer.group_send(
        #     self.__room_name,
        #     {
        #         "type  "    : "play_move",
        #         "status"    : "CONTINUE",
        #         "move"      : text_data["move"],
        #         "player"    : text_data["player"],
        #     }
        # )

        
        # print("send", flush=True)
    #     move  = text_data["move"]

    #     await self.__simulate( move )

    # #######################################################################

    # async def __preface_game( self ):
    #     self.__match = __manager.get_match( self.__room_name )

    #     if  not __manager.is_match( self.__room_name ):
    #         # room_name doesn't exist room doesn't exist
    #         self.close()
    #         # Handle by onerror
    #         pass 

    #     if  self.__preface_player() == "WATCH-MODE":
    #         return

    #     match self.__match.status:
    #         case "PENDING":
    #             if  self.__match.connections == self.__manual_players:
    #                 #Be careful with this if you update the status may go to other case
    #                 self.__match.status = "PLAYING"
    #                 self.__match.abort_cancel()
    
    #         case "PLAYING":
    #             self.__match.forfeit_cancel( self.__user.id )

    # async def __preface_player( self ):
    #     if  not self.__match.is_player( self.__id ):
    #         return "WATCH-MODE"

    #     self.__match.connect_player( self.__player )
    #     return "PLAY-MODE"
    
    # async def __valid_player( self ):
    #     if  self.__match.turn != self.__id:
    #         return False
    #     return True

    # async def __simulate( self, move ):
    #     if  not self.__valid_player():
    #         #Wait the other opponenets
    #         return
        
    #     moves = []
    #     moves.append( { self.__id : self.__match.simulate( move, "MANUAL", id ) } )

    #     if  not move.valid:
    #         # serve not valid move
    #         return
    #     else:
    #         # update new time
    #         pass
    
    #     if  move.status != "CONTINUE":
    #         # serve moves
    #         # write to db
    #         # cut connection : handle by error
    #         return

    #     if  len( self.__match.__bot_players ):
    #         move = await self.__match.simulate( "bot", self.__id_opponent ) # oppenent id

    #         if  move.status != "CONTINUE":
    #             moves.append( { self.__id_opponent : self.__match.simulate( move, "bot", id ) } )
    #             # serve moves
    #             # write to db
    #             # cut connection : handle by error
    #             return
    #     else:
    #         self.__match.turn = self.__id_opponent
