import TicTacToe from "../utilities/tictactoe.js"

export default class Tictactoe extends HTMLElement {
    constructor() {
      super();
    }
  
    connectedCallback() {
      const template = document.getElementById("tictactoe-template");
      const component = template.content.cloneNode(true);
      this.appendChild(component);
      TicTacToe();
    }
  }
  
  customElements.define("tictactoe-page", Tictactoe);
  