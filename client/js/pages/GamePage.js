import router from "../utilities/router.js";
import { runPongTwoGame, wsTwo } from "../utilities/pongTwo.js";
import { runPongFourGame, wsFour } from "../utilities/pongFour.js";
import { runPongCoopGame } from "../utilities/pongCoop.js";

export default class GamePage extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("game-template");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add("my-page");

    const game_header = this.querySelector(".game-header");
    const game_type = this.querySelector(".game-mode");
    const game_exit = this.querySelector(".game-exit");

    const game_header_query = new URLSearchParams(window.location.search).get("game");
    const game_type_query = new URLSearchParams(window.location.search).get("mode");
    const game_match_query = new URLSearchParams(window.location.search).get("match");

    let match_id = null;
    if (game_header_query === "PG") game_header.textContent = "PING PONG";
    else if (game_header_query === "TTT") game_header.textContent = "TIC TAC TOE";
    if (game_type_query === "two") game_type.textContent = "Two Players";
    else if (game_type_query === "four") game_type.textContent = "Four Players";
    else if (game_type_query === "ai") game_type.textContent = "AI";
    else if (game_type_query === "coop") game_type.textContent = "Co-op";
    if (game_match_query) match_id = Number(game_match_query);
    game_exit.addEventListener("click", () => {
      if (wsTwo) wsTwo.close(1000);
      if (wsFour) wsFour.close(1000);
      router.go("/home/", "", "add");
    });

    const canvas = document.getElementById("canvas-pong");
    const ctx = canvas.getContext("2d");

    if (game_header.textContent === "PING PONG") {
      if (game_type_query === "two") runPongTwoGame(canvas, ctx, match_id);
      else if (game_type_query === "four") runPongFourGame(canvas, ctx);
      else if (game_type_query === "coop") runPongCoopGame(canvas, ctx);
    } else if (game_header.textContent === "TIC TAC TOE") {
      runTicTacToeGame(canvas, ctx);
    }
  }
}

customElements.define("game-page", GamePage);
