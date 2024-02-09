import { runGame } from "../pong/pong.js";

export default class GamePage extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("game-template");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add("my-page");

    const canvas = document.getElementById("canvas-pong");
    const ctx = canvas.getContext("2d");
    runGame(canvas, ctx);
  }
}

customElements.define("game-page", GamePage);
