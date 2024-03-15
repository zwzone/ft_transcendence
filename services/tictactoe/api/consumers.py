from    channels.generic.websocket  import  AsyncWebsocketConsumer
from    .src.Match                  import  Match
from    asgiref.sync                import sync_to_async
from    channels.db                 import database_sync_to_async
from    .models                     import Match as M_Match
from    .models                     import Player as M_Player
from    .models                     import PlayerMatch as M_PlayerMatch
import                                     random
import                                     json
import                                     asyncio

Matches         = {}
Matches_db      = {}

waiting         = -1
waiting_room    = 0
mmatch          = None
players         = {}


@database_sync_to_async
def create_match_db():
    print(" ach kadir a si", flush=True)
    m = M_Match.objects.create( game='TC', state=M_Match.State.UNPLAYED.value )
    return m

@database_sync_to_async
def get_player( player_id ):
    player = M_Player.objects.get( id=player_id )
    return player

@database_sync_to_async
def delete_match( match_id ):
    match = M_Match.objects.get(id=match_id)
    match.delete()

@database_sync_to_async
def db_save(match):
    obj = match.obj
    keys = match.get_keys()

    if len(keys) != 2 or obj.state == obj.State.PLAYED.value:
        return
    
    obj.state = obj.State.PLAYED.value
    

    for key in keys:
        match.players[ key ].player_match_obj = M_PlayerMatch.objects.create( match_id=match.obj, player_id=match.players[ key ].obj )
        match.players[ key ].player_match_obj.save()

    if match.winner is not None:
        match.players[ match.winner ].obj.wins += 1
        match.players[ match.winner ].player_match_obj.score = 1
        match.players[ match.winner ].player_match_obj.won = True

        match.players[ match.winner ^ match.xor_players ].obj.losses += 1
        match.players[ match.winner ^ match.xor_players ].player_match_obj.score = 0
        match.players[ match.winner ^ match.xor_players ].player_match_obj.won = False
    else:
        for player in match.players:
            match.players[ player ].player_match_obj.score = 0
            match.players[ player ].player_match_obj.won = False

    for key in keys:
        match.players[ key ].player_match_obj.save()
        match.players[ key ].obj.save()
    
    # match.obj.save()
    match.obj.save()


class   TicTacToeGameConsumer( AsyncWebsocketConsumer ):

#-------------------------------------Receive------------------------------------#

    async def   connect( self ):
        
        self.__id               = self.scope["payload"]["id"]
        self.__room_id          = ""

        global waiting, waiting_room, mmatch, Matches, players
        print( players , flush=True)

        await self.accept()


        print(players, flush=True)
        if  self.__id in players:
            await self.send( json.dumps({
                "type"  : "already",
                "id"    : self.__id,
            }))
            await self.close(4001)
            
            return

        players[ self.__id ] = self.channel_name

        if waiting == -1:
            print("wayli", flush=True)
            waiting            = self.__id
            players[self.__id] = self.channel_name
            mmatch_obj         = await create_match_db()
            mmatch             = Match( self.__room_id, mmatch_obj )
            self.__room_id     = str(mmatch_obj.id)
            
            
            mmatch.add_player( self.__id )

            await self.channel_layer.group_add(
                self.__room_id,
                self.channel_name 
            )

            mmatch.players[ self.__id ].obj = await get_player( self.__id )
            
            return
        
        if waiting == self.__id:
            waiting = -1
            mmatch  = None
            self.close(4001)
            if self.__id in players:
                players.pop( self.__id )
            return

        players[self.__id] = self.channel_name

        mmatch.add_player( self.__id )

        mmatch.players[ self.__id ].obj = await get_player( self.__id )

        self.__room_id              = str(mmatch.obj.id)
        Matches[ self.__room_id ]   = mmatch
        mmatch                      = None
        waiting                     = -1

        await self.channel_layer.group_add(
            self.__room_id,
            self.channel_name 
        )

        await self.channel_layer.group_send(
              self.__room_id, {
                  "type"      : "start",
              }
        )
        

#-------------------------------------Disconnect------------------------------------#

    async def   disconnect( self, code=None ):
        global waiting, waiting_room, mmatch, Matches, players

        if self.__id in players and players[self.__id] == self.channel_name:
            players.pop( self.__id )
        
    
        if code == 4001 or code == 1006:
            await self.close()
            
            return

        if self.__room_id not in Matches:
            waiting = -1
            await self.close()
            
            if self.__id in players:
                players.pop( self.__id )

            await delete_match( mmatch.obj.id )
            mmatch = None
            
            return
        
        await self.channel_layer.group_discard(
            self.__room_id,
            self.channel_name
        )

        await self.close()

        Matches[ self.__room_id ].winner = self.__id ^ Matches[ self.__room_id ].xor_players
        await db_save(Matches[ self.__room_id ])

        await self.channel_layer.group_send(
            self.__room_id, {
                "type"  : "abort",
                "state" : "ABORT",
            }
        )
        
        #save db
        #remove from Matches

#-------------------------------------Receive------------------------------------#


    async def receive( self, text_data=None ):

        text_data = json.loads(text_data)

        if int(text_data["player"]) != Matches[self.__room_id].turn:
            await self.channel_layer.group_send(
                self.__room_id, {
                    "type"      : "not-turn",
                }
            )
            return
        
        Matches[self.__room_id].turn = Matches[self.__room_id].turn ^ Matches[ self.__room_id ].xor_players
        response = await self.__simulate( text_data["move"], int(text_data["player"]) )

        await self.channel_layer.group_send(
            self.__room_id,
            {
                "type"      : "move",

                "status"    : response["status"] if "status" in response else "",
                "sub-win"   : response["sub-win"] if "sub-win" in response else "",
                "winner"    : response["winner"] if "winner" in response else "",
                "move"      : text_data["move"] if "move" in text_data else "",
                "player"    : text_data["player"] if "player" in text_data else "",
            }
        )

    #  ----------------------------------------------------------Events Send----------------------------------------------------------------------- #

    async def start( self, data ):
        keys = Matches[ self.__room_id ].get_keys()
        Matches[ self.__room_id ].turn = keys[0]

        print( Matches[self.__room_id].turn, flush=True)

        await self.send( json.dumps( {
            "type"              : "start",

            "status"            : "PLAYING",
            "player-me"         : self.__id,
            "player-op"         : self.__id ^ Matches[ self.__room_id ].xor_players,
            "choice-me"         : "x" if self.__id == keys[0] else "o",
            "choice-op"         : "o" if self.__id == keys[0] else "x",
            "turn"              : Matches[ self.__room_id ].turn,
            "player-me-avatar"  : Matches[ self.__room_id ].players[ self.__id ].obj.avatar,
            "player-op-avatar"  : Matches[ self.__room_id ].players[ self.__id ^ Matches[ self.__room_id ].xor_players ].obj.avatar,
            "player-me-name"    : Matches[ self.__room_id ].players[ self.__id ].obj.username,
            "player-op-name"    : Matches[ self.__room_id ].players[ self.__id ^ Matches[ self.__room_id ].xor_players ].obj.username,

        }))
        
        # create table on db

    async def move( self, data ):
        if data["status"] == "WIN":
            Matches[ self.__room_id ].winner = int( data["winner"] )
            await db_save( Matches[ self.__room_id ] )


        elif data["status"] == "DRAW":
            Matches[ self.__room_id ].winner = None
            await db_save( Matches[ self.__room_id ] )


        await self.send( json.dumps( {
            "type"      : "move",

            "status"    : data["status"] if "status" in data else "",
            "move"      : data["move"] if "move" in data else "",
            "player"    : data["player"] if "player" in data else "",
            "sub-win"   : data["sub-win"] if "sub-win" in data else "",
            "winner"    : data["winner"] if "winner" in data else "",
        }))

    async def abort( self, data ):
        await self.send( json.dumps( {
            "type"      : "abort",

            "status"    : "ABORT",
            "winner"    : self.__id,
        }))

    async def not_turn( self, data ):
        await self.send( json.dumps( {
            "type"      : "not-turn",
        }))

        # Write win on db

    # async def save_db( self, match_id, status, winner ):
    #     matc

    #  --------------------------------------------------------------Game-------------------------------------------------------------------------- #
        
    async def __simulate( self, move, player_id ):
        global Matches
        response = Matches[self.__room_id].simulate( move, player_id )

        return response
