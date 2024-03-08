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

class Move
{
    #__move;
    #__player; // "op", "me"
    
    constructor( move, player ) {
        
        this.#__move    = move;
        this.#__player  = player;

    }

    get player() {
        return ( this.#__player );
    }

    get move() {
        return ( this.#__move );
    }
}

class Match
{
    #__id;
    #__player_me; // Me [ User ]
    #__player_op; // Opponent
    #__moves = []; // [Move(), Move()]]
    #__current_move; // [1,2,3,4,..., n ]
    #__turn_move; // "me", "op"
    #__state; // PENDING, END
    #__win; // "op", "me"

    constructor ( id, player_me, player_op ) {

        this.#__id              = id;
        this.#__player_me       = player_me;
        this.#__player_op       = player_op;
        this.#__current_move    = "CONTINUE";

    }

    add_move( move ) {
        this.#__moves.add( move );
    }

    next_move( ) {
        if ( this.#__current_move + 1 < this.#__current_move - 1 )
            this.#__current_move++;
    }

    prev_move( ) {
        if ( this.#__current_move - 1 >= 0 )
            this.#__current_move--;
    }

    choice( player )
    {
        switch( player )
        {
            case this.#__player_me.id:
                return this.#__player_me.choice;

            case this.#__player_op.id:
                return this.#__player_op.choice;
        }
    }


    id( player )
    {
        switch( player )
        {
            case "ME":
                return this.#__player_me.id;

            case "OP":
                return this.#__player_op.id;
        }
    }

    turn( player_id )
    {
        if ( this.#__turn_move == player_id )
            return ( true );
        return ( false );
    }

    simulate( move )
    {
        if ( this.#__turn_move == move.player() )
        {
            getElementById( data["move"] ).appendChild( choice( move.player() ) );
        }
        else
            console.log("should wait for your turn");
    }
    // Maybe later
    // navigate_move( ) {

    // }
}

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
                                     new Player( data["player-me"], data["choice-me"] ),
                                     new Player( data["player-op"], data["choice-op"] ) );
    }

    id( player )
    {
        return ( this.#__room.id( player ) );
    }

    choice( player )
    {
        return ( this.#__room.choice( player ) );
    }

    destructor() {
        this.__socket.close();
    }
}

/////////////////////////////////////////////////////////////////////////////////

let __game      = new Game( "test-room" );


let __socket    = new WebSocket( "ws://localhost:8000/tictactoe/ws/" );

/////////////////////////////////////////////////////////////////////////////////

let __move_events = {
    __move          : function(e) {
        // e.target.style.display = "none";
        __socket.send( JSON.stringify( {"move": e.target.getAttribute( "id" ), "player": __game.id( "ME" ) } ) );
        // console.log(e.target.getAttribute( "id" ) );
    },

    __lunch         : function() {
        let __move_spots = document.getElementsByClassName("spot");

        for ( let i=0; i<__move_spots.length; i++ )
            __move_spots[i].addEventListener(
                "click", this.__move
            );
    }
}

// Controls events actions namespace

let __controls_events = {
    __match         : function() {
        console.log( "Match have been clicked !!");
    },

    __ai            : function() {
        console.log( "AI have been clicked !!");
    },

    __create_room   : function() {
        console.log( "Create Room have been clicked !!");
    },

    __enter_room    : function() {
        console.log( "Enter Room have been clicked !!");
    },

    __exit          : function() {
        console.log( "Exit have been clicked !!");
    },

    __lunch         : function() {        
        document.getElementById("match").addEventListener(
            "click", this.__match
        )

        document.getElementById("ai").addEventListener(
            "click", this.__ai
        )

        document.getElementById("create-room").addEventListener(
            "click", this.__create_room
        )

        document.getElementById("enter-room").addEventListener(
            "click", this.__enter_room
        )

        document.getElementById("exit").addEventListener(
            "click", this.__exit
        )
    }
};

let __mode_events  = {
    __bot           : function() {
        console.log( "Bot button was clicked" );
    },

    __manual        : function() {
        console.log( "Manual was clicked" );
    },

    __lunch         : function()
    {
        let __modes_challenge;

        __modes_challenge = document.getElementsByClassName("mode-challenge bot");

        for ( let i=0; i<__modes_challenge.length; i++ )
            __modes_challenge[i].addEventListener(
                "click", this.__bot
        )

        __modes_challenge = document.getElementsByClassName( "mode-challenge manual" );

        for ( let i=0; i<__modes_challenge.length; i++ )
            __modes_challenge[i].addEventListener(
                "click", this.__manual
            )
    }
}

let __play_events = {
    __watch         : function() {
        console.log( "Watch event was clicked" );
    },

    __play          : function() {
        console.log( "Play event was clicked" );
    },

    __lunch         : function() {
        let __modes_play;

        __modes_play = document.getElementsByClassName("__play");

        for ( let i=0; i<__modes_play.length; i++ )
            __modes_play[i].addEventListener(
                "click", this.__play
            )

        __modes_play = document.getElementsByClassName( "__watch" );

        for ( let i=0; i<__modes_play.length; i++ )
        {
            __modes_play[i].addEventListener(
                "click", this.__watch
            )
        }
    }
}

function    lunch_events()
{
    // __controls_events.__lunch();
    // __mode_events.__lunch();
    // __play_events.__lunch();
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

__socket.onopen = (event)=> {
    console.log("hello");
}

__socket.onmessage = (event)=> {
    let data = JSON.parse(event.data);


    if ( data["type"] == "start-game" )
    {
        __game.init_game( data );
        return ;
    }

    console.log( data );

    let move    = new Move( data["move"], data["player"] );
    let spot    = document.getElementById( data["move"] );
    let status  = data["status"]

    spot.classList.add( __game.choice( data["player"] ) );
    
    spot.innerHTML = __game.choice( data["player"] ).toUpperCase();

    spot.removeEventListener( "click", __move_events.__move );

    if ( status == "SUB-WIN" )
    {
        console.log( data["sub-win"] );

        let sub_board   = document.getElementById( data[ "sub-win" ] );

        switch ( __game.choice( data[ "player" ] ) )
        {
            case "x":
                sub_board.className = "sub-board filled";
                sub_board.innerHTML = "<div class=\"spot-fill-x\">X</div>";
                break ;
            case "o":
                sub_board.className = "sub-board filled";
                sub_board.innerHTML = "<div class=\"spot-fill-o\">O</div>";
                break ;
        }
    }

    asyncio.sl
    if ( __game.choice( data["player"] ) == 'x')
    {

    }
    // spot.removeEventListener( "click", __move_events.__move );
}


function    TicTacToe()
{
    render_board();
    // lunch_events();
    // Lunch controls events
};

// Tic Tac Toe
TicTacToe();