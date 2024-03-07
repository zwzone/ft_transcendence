class Player
{
    #__id;
    #__choice;

    constructor( id, choice ) {

        this.#__id       = id;
        this.#__choice   = choice;

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
    #__moves; // [Move(), Move()]]
    #__current_move; // [1,2,3,4,..., n ]
    #__turn_move; // "me", "op"
    #__state; // PENDING, END
    #__win; // "op", "me"

    constructor ( id, player_me, player_op ) {

        this.#__id          = id;
        this.#__player_me   = player_me;
        this.#__player_op   = player_op;

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

    // Maybe later
    // navigate_move( ) {

    // }
}

class Game
{
    constructor() {
        
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
        console.log( "Creat Room have been clicked !!");
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

let __move_events = {
    __move          : function(e) {
        console.log(e);
        e.target.classList.add("o");
        e.target.innerHTML = "O";
        // e.target.style.display = "none";
    },

    __lunch         : function() {
        let __move_spots = document.getElementsByClassName("spot");

        console.log( __move_spots );
        for ( let i=0; i<__move_spots.length; i++ )
            __move_spots[i].addEventListener(
                "click", this.__move
            );
    }
}

function    lunch_events()
{
    // __controls_events.__lunch();
    // __mode_events.__lunch();
    // __play_events.__lunch();
    __move_events.__lunch();

};

function    TicTacToe()
{
    // Lunch controls events
    lunch_events();
};

// Tic Tac Toe
TicTacToe();

let ws = new WebSocket( "ws://localhost:8000/ws/match/" );