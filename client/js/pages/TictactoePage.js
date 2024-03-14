import router from "../utilities/router.js";
import TicTacToe from "../utilities/tictactoe.js"

export default class Tictactoe extends HTMLElement {
    constructor() {
      super();
    }
  
    connectedCallback() {
      const template = document.getElementById("tictactoe-template");
      const component = template.content.cloneNode(true);
      this.appendChild(component);
      this.querySelector("button.exit").addEventListener("click", (event) => {
        router.go("/home/", "", "add");
      })
      TicTacToe();
    }
  }
  
  customElements.define("tictactoe-page", Tictactoe);
  