import                                      json
import                                      subprocess
from    channels.generic.websocket  import  AsyncWebsocketConsumer
# from    .src.Player                  import  PlayerC
# from    .src.Move                    import  Move
from    .src.Match                   import MatchC

SIMULATE    = "simulate"
EXIT        = "exit"

Matches     = { "test":MatchC() }
num         = 0
moves       = []

red_proc    = None
blue_proc   = None

class TicTacToeConsumer( AsyncWebsocketConsumer ):

    async def connect( self ):
        self.__proc = None
        # print("Connected", flush=True)
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
        # print("end", flush=True)

        if num % 2 == 0: #Red O 
            red_proc = subprocess.Popen( "/home/ychaaibi/Desktop/ft_transcendence/services/tictactoe/api/bin/red",
                                            subprocess.stdin.PIPE,
                                            subprocess.stdout.PIPE,
                                            subprocess.stderr.PIPE,
                                            text=True )
        else: #Blue X
            pass

        num += 1

    async def disconnect( self, close_code ):
        print("disconnected", flush=True)
        await self.channel_layer.group_discard(
            "test",
            self.channel_name
        )

    async def welcome( self, data ):
        #Updata data["index"] = Program
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

        moves.append( data["index"] )


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
            'next-turn': "red" if data["color"] == "blue" else "blue",
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
        
            


            



