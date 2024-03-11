from    channels.generic.websocket  import  AsyncWebsocketConsumer
import                                      json
from    .src.Match                  import  Match
import                                      random

Matches = {}

mmatch = Match()

class   TicTacToeGameConsumer( AsyncWebsocketConsumer ):
    async def   connect( self ):

        self.__room_id          = self.scope["url_route"]["kwargs"]["room_id"]
        self.__id               = self.scope["url_route"]["kwargs"]["player_id"]

        await self.accept()

        if mmatch == "PLAYING":
            await self.send( json.dumps({
                "type"          :"invalid",
            }))
            self.close()
            return

        await self.channel_layer.group_add(
            self.__room_id,
            self.channel_name 
        )

        mmatch.add_player( self.__id )
        # match mmatch.status():
        if mmatch.status() == "PLAYING":
            await self.channel_layer.group_send(
                  self.__room_id, {
                      "type"      : "start",
                  }
            )

    async def   disconnect( self, code ):
        mmatch.remove_player( self.__id )

        await self.close()
        
        await self.channel_layer.group_discard(
            self.__room_id,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.__room_id, {
                "type"  : "abort",

                "state" : "ABORT",
            }
        )

    async def receive( self, text_data=None ):

        text_data = json.loads(text_data)

        print( text_data, flush=True)
        response = await self.__simulate( text_data["move"], int(text_data["player"]) )

        await self.channel_layer.group_send(
            self.__room_id,
            {
                "type"      : "move",

                "status"    : response["status"],
                "sub-win"   : response["sub-win"] if "sub-win" in response else "",
                "move"      : text_data["move"],
                "player"    : text_data["player"],
            }
        )

    #  ----------------------------------------------------------Events Send----------------------------------------------------------------------- #

    async def start( self, data ):
    # print("id ", self.__id, flush=True)
        await self.send( json.dumps( {
            "type"      : "start",

            "status"    : "PLAYING",
            "player-me" : self.__id,
            "choice-me" : "x" if self.__id == 1 else "o",
            "player-op" : 2 if self.__id == 1 else 1,
            "choice-op" : "o" if self.__id == 1 else "x",
            "turn"      : random.randint(0, 2),
        }))
        
        # create table on db

    async def move( self, data ):
        await self.send( json.dumps( {
            "type"      : "move",

            "status"    : data["status"],
            "move"      : data["move"],
            "player"    : data["player"],
            "sub-win"   : data["sub-win"] if "sub-win" in data else ""
        }))

    async def abort( self, data ):
        await self.send( json.dumps( {
            "type"      : "abort",

            "status"    : "ABORT",
        }))

        # Write win on db

    #  --------------------------------------------------------------Game-------------------------------------------------------------------------- #
        
    async def __simulate( self, move, player_id ):
        response = mmatch.simulate( move, player_id )

        return response
