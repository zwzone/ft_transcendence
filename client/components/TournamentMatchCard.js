export default class TournamentMatchCard extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("tournament-match-card");
    const component = template.content.cloneNode(true);
    this.appendChild(component);

    this.classList.add(
      "d-flex",
      "justify-content-center",
      "align-items-center",
      "flex-wrap",
      "rounded-4",
      "p-2",
    );
  }
}

customElements.define("tournament-match-card", TournamentMatchCard);
