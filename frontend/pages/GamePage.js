export default class GamePage extends HTMLElement {
  constructor() {
    super();
  }
  connectedCallback() {
    const template = document.getElementById("game-template");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
  }
}

customElements.define("game-page", GamePage);
