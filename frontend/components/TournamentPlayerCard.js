export default class TournamentPlayerCard extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("tournament-player-card");
    const component = template.content.cloneNode(true);
    this.appendChild(component);

    this.classList.add(
      "d-flex",
      "flex-column",
      "justify-content-center",
      "align-items-center",
      "p-1",
    );
  }
}

customElements.define("tournament-player-card", TournamentPlayerCard);
