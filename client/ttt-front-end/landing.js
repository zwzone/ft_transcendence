// Controls events actions namespace

let __controls_events = {
    __match         : function()
    {
        console.log( "Match have been clicked !!");
    },

    __ai            : function()
    {
        console.log( "AI have been clicked !!");
    },

    __create_room   : function()
    {
        console.log( "Creat Room have been clicked !!");
    },

    __enter_room    : function()
    {
        console.log( "Enter Room have been clicked !!");
    },

    __exit          : function()
    {
        console.log( "Exit have been clicked !!");
    },

    __lunch         : function()
    {        
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

let __mode_events = {
    __bot           : function()
    {
        console.log( "Bot button was clicked" );
    },

    __manual        : function()
    {
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
        {
            __modes_challenge[i].addEventListener(
                "click", this.__manual
            )
        }
    }
}

let __play_events = {
    __watch         : function()
    {
        console.log( "Watch event was clicked" );
    },

    __play          : function()
    {
        console.log( "Play event was clicked" );
    },

    __lunch         : function()
    {
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
    __controls_events.__lunch();
    __mode_events.__lunch();
    __play_events.__lunch();
};

function    tic_tac_toe()
{
    // Lunch controls events
    lunch_events();

};

// Tic Tac Toe
tic_tac_toe();