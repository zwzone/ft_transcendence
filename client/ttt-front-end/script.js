// Controls events actions namespace

let __controls_events = {
    __matches       : function()
    {
        console.log( "Matches have been clicked !!");
    },

    __random        : function()
    {
        console.log( "Random have been clicked !!");
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
    }
};

function    lunch_events()
{
    let __events = [
        __controls_events.__matches,
        __controls_events.__random,
        __controls_events.__ai,
        __controls_events.__create_room,
        __controls_events.__enter_room,
        __controls_events.__exit,
    ]

    let __controls = document.getElementsByClassName("control");

    for ( let i=0; i<__controls.length; i++ )
    {
        __controls[i].addEventListener(
            "click",
            __events[ parseInt( __controls[i].getAttribute("index") ) ] );
    }
};

function    tic_tac_toe()
{
    // Lunch controls events
    lunch_events();

};

// Tic Tac Toe
tic_tac_toe();