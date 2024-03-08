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
            "type"      : "move",
            "status"    : data["status"],
            "move"      : data["move"],
            "player"    : data["player"],
            "sub-win"   : data["sub-win"] if data["status"] == "SUB-WIN" else ""
        }))

    async def   disconnect( self, code ):
        mmatch.remove_player( self.__id )

        await self.close()
        
        await self.channel_layer.group_discard(
            self.__room_name,
            self.channel_name
        )


    async def receive( self, text_data=None ):

        text_data = json.loads(text_data)

        response = await self.__simulate( text_data["move"], int(text_data["player"]) )

        
        await self.channel_layer.group_send(
            self.__room_name,
            {
                "type"      : "play_move",
                "status"    : response["status"],
                "sub-win"   : response["sub-win"] if "sub-win" in response else "",
                "move"      : text_data["move"],
                "player"    : text_data["player"],
            }
        )


    async def __simulate( self, move, player_id ):
        response = mmatch.simulate( move, player_id )
        print("socket ", response, flush=True)

        return response
