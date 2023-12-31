export default class TournamentPage extends HTMLElement {
  constructor() {
    super();
  }
  connectedCallback() {
    const template = document.getElementById("tournament-template");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
  }
}

customElements.define("tournament-page", TournamentPage);
