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

        let left_result = document.getElementById("left-result");
        let right_result = document.getElementById("right-result");

        let left_result_name = document.getElementById("player-name-left-result");
        let right_result_name = document.getElementById("player-name-right-result");

        let left_result_star = document.getElementById("left-win-star");
        let right_result_star = document.getElementById("right-win-star");

        if ( __game.player_me.choice == 'x')
        {
            left_result.setAttribute( "src", __game.player_me.avatar );
            left_result_name.innerHTML = __game.player_me.username;
            if ( __game.player_me.is_winner )
            {
                left_result_star.style.display = "block";
                left_result_star.parentNode.classList.add("win");
            }

            right_result.setAttribute( "src", __game.player_op.avatar );
            right_result_name.innerHTML = __game.player_op.username;
            if ( __game.player_op.is_winner )
            {
                right_result_star.style.display = "block";
                right_result_star.parentNode.classList.add("win");
            }
        }
        else
        {
            left_result.setAttribute( "src", __game.player_op.avatar );
            left_result_name.innerHTML = __game.player_op.username;
            if ( __game.player_op.is_winner )
            {
                left_result_star.style.display = "block";
                left_result_star.parentNode.classList.add("win");
            }

            right_result.setAttribute( "src", __game.player_me.avatar );
            right_result_name.innerHTML = __game.player_me.username;
            if ( __game.player_me.is_winner )
            {
                right_result_star.style.display = "block";
                right_result_star.parentNode.classList.add("win");
            }
        }
        
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
    avatar;
    username;
    is_winner;

    constructor( id, choice, username, avatar ) {

        this.#__id       = id;
        this.#__choice   = choice;
        this.avatar      = avatar
        this.username    = username;
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
    player_me;
    player_op;
    #__players;
    #__moves = []; // [Move(), Move()]]
    #__turn_move; // "me", "op"
    #__state; // PENDING, END
    #__win; // id

    constructor ( id, player, player_me, player_op, turn ) {

        this.#__id              = id;
        this.#__player          = player;
        this.#__players         = new Map([
                                    [ player_me.id, player_me ],
                                    [ player_op.id, player_op ]
                                ]);
                                
                                this.player_me          = player_me;
                                this.player_op          = player_op;

        this.#__turn_move       = turn;

    }

    get player( )
    {
        return ( this.#__player );
    }

    choice( player )
    {
        return this.#__players.get( player ).choice;
    }

    id( player_id )
    {
        return this.#__players.get( player_id ).id;
    }

    turn( )
    {
        return ( this.#__turn_move == this.#__player );
    }

    switch_turn( )
    {
        const keys = this.#__players.keys();

        this.#__turn_move = keys.next().value ^ keys.next().value ^ this.#__turn_move;
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
        let status = data["status"];
    
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
                if ( this.player_me.id == data["winner"] )
                    this.player_me.is_winner = true;
                else
                    this.player_op.is_winner = true;

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
    player_me;
    player_op;

    constructor( ) {

    }

    init_game( data )
    {
        lunch_events();

        this.#__room    = new Match( data["match-id"],
                                     data["player-me"],
                                     new Player( data["player-me"], data["choice-me"], data["player-me-name"], data["player-me-avatar"] ),
                                     new Player( data["player-op"], data["choice-op"], data["player-op-name"], data["player-op-avatar"] ),
                                     parseInt(data["turn"])) ;

        console.log( parseInt(data["turn"]) )
        this.player_me  = this.#__room.player_me;
        this.player_op  = this.#__room.player_op;

        let left_avatar = document.getElementById( "left" );
        let left_name   = document.getElementById( "player-left-name");

        let right_avatar = document.getElementById( "right" );
        let right_name   = document.getElementById( "player-right-name");

        left_avatar.style.display = "block";
        right_avatar.style.display = "block";

        if ( data["choice-me"] == 'x')
        {
            left_avatar.setAttribute( "src", data["player-me-avatar"] );
            left_name.innerHTML = data["player-me-name"];

            right_avatar.setAttribute( "src", data["player-op-avatar"] );
            right_name.innerHTML = data["player-op-name"];
        }
        else
        {
            left_avatar.setAttribute( "src", data["player-op-avatar"] );
            left_name.innerHTML = data["player-op-name"];


            right_avatar.setAttribute( "src", data["player-me-avatar"] );
            right_name.innerHTML = data["player-me-name"];
        }


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

export let __socket    = undefined;

/////////////////////////////////////////////////////////////////////////////////

let __move_events = {
    __move          : function(e) {

        if ( !__game.turn( __game ) )
        {
            console.log("not your turn");
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

    __socket            = new WebSocket( `wss://${window.ft_transcendence_host}/ws/tictactoe/` );
    
    __socket.onopen     = (event)=> {
    }
            
    __socket.onmessage  = (event)=> {
        let data = JSON.parse(event.data);
        
        switch ( data["type"] )
        {
            case "start":
                __game.init_game( data );
                return ;
            case "abort":
                __socket.close();
                __game.end_game();
                __game.player_me.is_winner = true;
                __render.render_result();
                return ;
            case "already":
                __socket.close(4001);
                __game.end_game();
                setTimeout(() => {
                    alert("Game is already");
                }, 500);
                return ;
            case "not-turn":
                alert("Not your turn");
                return ;
        }
    
        __game.simulate_match ( new Move( data["move"], data["player"] ) );
        
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