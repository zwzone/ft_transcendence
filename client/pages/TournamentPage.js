export default class TournamentPage extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("tournament-template");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add("my-page");
  }
}

customElements.define("tournament-page", TournamentPage);
