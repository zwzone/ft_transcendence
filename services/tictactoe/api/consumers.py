from    channels.generic.websocket  import  AsyncWebsocketConsumer
import                                      json
from    .src.Match                  import  Match
import                                      asyncio
# from    .src.Manager                import  Manager

# __manager   = Manager()

mmatch = Match()
abort_task = None
num = 0
# btws = 0

class   TicTacToeGameConsumer( AsyncWebsocketConsumer ):
    async def   connect( self ):
        global abort_task

        self.__room_id          = self.scope["url_route"]["kwargs"]["room_id"]
        self.__id               = self.scope["url_route"]["kwargs"]["player_id"]

        await self.accept()

        await self.channel_layer.group_add(
            self.__room_id,
            self.channel_name 
        )
 
        mmatch.add_player( self.__id )

        match mmatch.status():
            case "PLAYING":
                # self.wait_match( mmatch )
                # print( self.__abort_task, flush=True)
                abort_task.cancel()
                await self.channel_layer.group_send(
                      self.__room_id, {
                          "type"      : "start_game",
                      }
                )
                return
                
        abort_task = asyncio.create_task( self.wait_match( mmatch ) )
        # print( self.__abort_task, flush=True)


        
        
    async def start_game( self, data ):
        # print("id ", self.__id, flush=True)
        await self.send( json.dumps( {  "type"      : "start-game",
                                        "player-me" : self.__id,
                                        "choice-me" : "x" if self.__id == 1 else "o",
                                        "player-op" : 2 if self.__id == 1 else 1,
                                        "choice-op" : "o" if self.__id == 1 else "x",
        }))
        # await self.__preface_game()

    async def play_move( self, data ):
        await self.send( json.dumps( {
            "type"      : "move",
            "status"    : data["status"],
            "move"      : data["move"],
            "player"    : data["player"],
            "sub-win"   : data["sub-win"] if "sub-win" in data else ""
        }))

    async def   disconnect( self, code ):
        mmatch.remove_player( self.__id )

        await self.close()
        
        await self.channel_layer.group_discard(
            self.__room_id,
            self.channel_name
        )


    async def receive( self, text_data=None ):

        text_data = json.loads(text_data)

        response = await self.__simulate( text_data["move"], int(text_data["player"]) )

        await self.channel_layer.group_send(
            self.__room_id,
            {
                "type"      : "play_move",
                "status"    : response["status"],
                "sub-win"   : response["sub-win"] if "sub-win" in response else "",
                "move"      : text_data["move"],
                "player"    : text_data["player"],
            }
        )

    async def wait_player( self, match ):
        await asyncio.sleep( 120 )

    async def wait_match( self, match ):
        await asyncio.sleep( 10 )

        await self.send( json.dumps( {
            "type"      : "ABORT",
        }))

        print("Match abort", flush=True)

    async def __simulate( self, move, player_id ):
        response = mmatch.simulate( move, player_id )

        return response
