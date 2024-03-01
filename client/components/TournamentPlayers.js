export default class TournamentPlayers extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("tournament-players");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add("d-none", "flex-column", "justify-content-center", "p-2");
  }
}

customElements.define("tournament-players", TournamentPlayers);
