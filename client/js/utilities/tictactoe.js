let __render  = {
    render_board    : function() {

        function convert(digit)
        {
            return ( String.fromCharCode( '0'.charCodeAt(0) + digit ) );
        }
    
        let board = document.getElementById( "board" );
        
        for ( let board_x=0; board_x<3; board_x++ )
        {
            for ( let board_y=0; board_y<3; board_y++ )
            {
                let sub_board       = document.createElement( 'div' );
                
                sub_board.className = 'sub-board';
                sub_board.id        = [ convert(board_x), convert(board_y) ].join('')
    
                for ( let sub_board_x=0; sub_board_x<3; sub_board_x++ )
                {
                    for ( let sub_board_y=0; sub_board_y<3; sub_board_y++ )
                    {
                        
                        let spot = document.createElement( 'div' );
                        
                        spot.className  = 'spot';
                        spot.id         = [ convert(board_x), convert(board_y),
                                            convert(sub_board_x), convert(sub_board_y)].join('');
    
                        sub_board.appendChild( spot ); 
                            
                    }
                    board.appendChild( sub_board );
                }
            }
        }
    },

    render_result   : function() {
        let board   = document.getElementById( "board" );
        let result  = document.getElementById( "result" );
        let status  = document.getElementById( "status" );

        board.classList.add( "anime_desapeir" );
        status.classList.add( "anime_desapeir" );
        result.classList.add( "anime_appeir" );
    }
}

//------------------------------------------------ Move -----------------------------------------------//
class Move
{
    #__move_id;
    #__player_id; // "op", "me"
    
    constructor( move_id, player_id ) {
        
        this.#__move_id    = move_id;
        this.#__player_id  = player_id;

    }

    get player() {
        return ( this.#__player_id );
    }

    get move() {
        return ( this.#__move_id );
    }
}

//----------------------------------------------- Player ----------------------------------------------//
class Player
{
    #__id;
    #__choice;

    constructor( id, choice ) {

        this.#__id       = id;
        this.#__choice   = choice;
    }

    get id()
    {
        return ( this.#__id );
    }

    get choice()
    {
        return ( this.#__choice );
    }
}

//----------------------------------------------- Macth -----------------------------------------------//
class Match
{
    #__id;
    #__player;
    #__players;
    #__moves = []; // [Move(), Move()]]
    #__turn_move; // "me", "op"
    #__state; // PENDING, END
    #__win; // id

    constructor ( id, player, player_me, player_op ) {

        this.#__id              = id;
        this.#__player          = player;
        this.#__players         = new Map([
                                    [ player_me.id, player_me ],
                                    [ player_op.id, player_op ]
                                ]);
        this.#__turn_move       = 1;

        // console.log( player_me.id );
        // console.log( this.#__players.get(player_me.id ) );
    }

    get player( )
    {
        return ( this.#__player );
    }

    choice( player )
    {
        // console.log( this.#__players.get( player ) );
        return this.#__players.get( player ).choice;
    }

    id( player_id )
    {
        return this.#__players.get( player_id ).id;
    }

    turn( )
    {
        // console.log( this.)
        return ( this.#__turn_move == this.#__player );
    }

    switch_turn( )
    {
        const keys = this.#__players.keys();

        this.#__turn_move = keys.next().value ^ keys.next().value ^ this.#__turn_move;
        console.log("-----------------");
        console.log(this.#__turn_move);
        console.log("-----------------");
    }

    simulate_match( move )
    {
        let spot        = document.getElementById( move.move );

        spot.classList.add( __game.choice( move.player ) );
        spot.innerHTML  = "<span>" + __game.choice( move.player ).toUpperCase() + "</span>"
        spot.removeEventListener( "click", __move_events.__move );

        __game.switch_turn();
    }

    simulate_status( data )
    {
        console.log( data );
        let status = data["status"];
        
        console.log( status );
        if ( status == "PLAYING" )
            return ( status );
     
        if ( data[ "sub-win" ] != "" )
        {
            let sub_board   = document.getElementById( data[ "sub-win" ] );

            switch ( __game.choice( data[ "player" ] ) )
            {
                case "x":
                    sub_board.className = "sub-board filled";
                    sub_board.innerHTML = "<div class=\"spot-fill-x\"><span>X</span></div>";
                    break ;
                case "o":
                    sub_board.className = "sub-board filled";
                    sub_board.innerHTML = "<div class=\"spot-fill-o\"><span>O</span></div>";
                    break ;
            }
        }
        
        switch ( status )
        {
            case "WIN":
                setTimeout(() => {
                    __render.render_result()
                }, 500);
                break ;

            case "DRAW":
                setTimeout(() => {
                    __render.render_result()
                }, 500);
                break ;
        }
        
        return ( status );
    }
}

//----------------------------------------------- Game ------------------------------------------------//

class Game
{
    #__socket;
    #__room;

    constructor( ) {

    }

    init_game( data )
    {
        lunch_events();

        this.#__room    = new Match( data["match-id"],
                                     data["player-me"],
                                     new Player( data["player-me"], data["choice-me"] ),
                                     new Player( data["player-op"], data["choice-op"] ) );
    }

    end_game( )
    {
        __move_events.__stop();
    }

    get player()
    {
        return ( this.#__room.player );
    }

    id( player )
    {
        return ( this.#__room.id( player ) );
    }

    choice( player )
    {
        return ( this.#__room.choice( player ) );
    }

    turn( )
    {
        return ( this.#__room.turn() );
    }

    switch_turn()
    {
        this.#__room.switch_turn();
    }

    simulate_match( move )
    {
        this.#__room.simulate_match( move );
    }

    simulate_status( data )
    {
        return ( this.#__room.simulate_status( data ) );
    }

    destructor() {
        this.__socket.close();
    }
}

/////////////////////////////////////////////////////////////////////////////////

let __game      = new Game( "test-room" );

let __socket    = undefined;

/////////////////////////////////////////////////////////////////////////////////

let __move_events = {
    __move          : function(e) {
        console.log( __game.player );
        if ( !__game.turn( __game ) )
        {
            console.log("should wait for your turn");
            return ;
        }

        __socket.send( JSON.stringify( {
                "move": e.target.getAttribute( "id" ),
                "player": __game.player,
        }));
    },

    __lunch         : function() {
        let __move_spots = document.getElementsByClassName("spot");

        for ( let i=0; i<__move_spots.length; i++ )
            __move_spots[i].addEventListener(
                "click", this.__move
            );
    },

    __stop          : function() 
    {        let __move_spots = document.getElementsByClassName("spot");

        for ( let i=0; i<__move_spots.length; i++ )
        {
            __move_spots[i].removeEventListener(
                "click", this.__move
            );
            __move_spots[i].style.cursor = "none";
        }
    }
}

function    lunch_events()
{
    __move_events.__lunch();

};

function    render_board()
{
    function convert(digit)
    {
        return ( String.fromCharCode( '0'.charCodeAt(0) + digit ) );
    }

    let board = document.getElementById( "board" );
    
    for ( let board_x=0; board_x<3; board_x++ )
    {
        for ( let board_y=0; board_y<3; board_y++ )
        {
            let sub_board       = document.createElement( 'div' );
            
            sub_board.className = 'sub-board';
            sub_board.id        = [ convert(board_x), convert(board_y) ].join('')

            for ( let sub_board_x=0; sub_board_x<3; sub_board_x++ )
            {
                for ( let sub_board_y=0; sub_board_y<3; sub_board_y++ )
                {
                    
                    let spot = document.createElement( 'div' );
                    
                    spot.className  = 'spot';
                    spot.id         = [ convert(board_x), convert(board_y),
                                        convert(sub_board_x), convert(sub_board_y)].join('');

                    sub_board.appendChild( spot ); 
                        
                }
                board.appendChild( sub_board );
            }
        }
    }
}

export default function    TicTacToe()
{
    render_board();

    __socket            = new WebSocket( "wss://localhost/ws/tictactoe/" );
    
    __socket.onopen     = (event)=> {
        console.log("hello");
    }
            
    __socket.onmessage  = (event)=> {
        let data = JSON.parse(event.data);
        
        console.log( data );
        
        switch ( data["type"] )
        {
            case "start":
                __game.init_game( data );
                return ;
            case "abort":
                alert("Game was aborted");
                __socket.close();
                __game.end_game();
                return ;
            case "already":
                alert("Game is already");
                __socket.close(3001);
                __game.end_game();
                return ;
        }
    
        __game.simulate_match ( new Move( data["move"], data["player"] ) );
        
        // console.log( __game.simulate_status( data ) );
        switch ( __game.simulate_status( data ) )
        {
            case "PLAYING":
                return ;
            case "SUB-WIN":
                return ;

        }
        __socket.close();
        __game.end_game();
    }

};