import                                      json
from    channels.generic.websocket  import  AsyncWebsocketConsumer
# from    .src.Player                  import  PlayerC
# from    .src.Move                    import  Move
from    .src.Match                   import  MatchC

SIMULATE    = "simulate"
EXIT        = "exit"

Matches     = { "test":MatchC() }
num         = 0

class TicTacToeConsumer( AsyncWebsocketConsumer ):

    async def connect( self ):
        print("Connected", flush=True)
        await self.channel_layer.group_add(
            "test",
            self.channel_name

        )
        await self.accept()

        global num
        print( num, "red" if ( num % 2 == 0 ) else "blue", flush=True)
        await self.send(
            text_data=json.dumps({
                "type":"welcome",
                "color":"red" if ( num % 2 == 0 ) else "blue",
            })
        )
        num += 1

    async def disconnect( self, close_code ):
        print("disconnected", flush=True)
        await self.channel_layer.group_discard(
            "test",
            self.channel_name
        )

    async def welcome( self, data ):
        await self.send(
            text_data=json.dumps({
                "type":data["type"],
                "color":data["color"],
            })
        )

    async def simulate_game( self, data ):
        print("simu\n", flush=True)
        print(str(Matches["test"]), flush=True)

        # await self.close()
        # _mode       = ""
        # _type       = data.get("type")
        # _message    = data.get("message")


        # match _mode:
        #     case 'ai':
        #         # Check Ai bot
        #         # Send the new result to player
        #         pass

        #     case 'bot':
        #         # Check bot
        #         # Send the new result to players ( Player didn't provide a valid move )
        #         pass

        #     case 'manual':
        #         # Check data.move
        #         pass

        #     case 'match-exit':
        #         # send the new result to players ( Player abort the match ... )
        #         pass
        
        #     case 'test':

        # global Matches
        if data["color"] == "red":
            
            match Matches["test"].simulate( data["index"], "x" ):
                case "WIN":
                    print("Nod dga3d", flush=True)
                    status = "WIN"
                case "PENDING":
                    print("Ba9i", flush=True)
                    status = "PENDING"

        else:
            match Matches["test"].simulate( data["index"], "o" ):
                case "WIN":
                    print("Nod dga3d", flush=True)
                    Matches["test"] = MatchC()

                    status = "WIN"
                case "PENDING":
                    print("Ba9i", flush=True)
                    status = "PENDING"


        print(status, flush=True)
        await self.channel_layer.group_send("test", {
                'type': 'send_message',
                'index': data["index"],
                'color': data["color"],
                'status': status,
        })
    
    async def send_message( self, data ):
        # exit(0)
        await self.send(text_data=json.dumps({
            "index": data["index"],
            "color": data["color"],
            "status": data["status"],
        }))

    async def receive( self, text_data=None ):
        # exit(0)
        print("received\n", flush=True)
        data        = json.loads( text_data )
        print(data, flush=True)
        # data_type   = data.get("type")

        # match data_type:

        #     case "SIMULATE_GAME":
        #         self.__simulate_game( data )

        #     case "EXIT_GAME":
        #         self.__exit_game( data )
            
        #     case "test":
                
        # await self.channel_layer.group_send("test", {
        #         'type': 'send_message',
        #         'message': text_data,
        # })

        await self.simulate_game( data )


        # Check EndGame




    async def __exit_game( self, data ):
        #Abort the game
        #Lose the game
        #Redirect to the intro page
        pass

    async def __end_game():
        pass
        
            


            



