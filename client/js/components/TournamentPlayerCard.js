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
      "py-2",
      "px-3",
      "rounded-5",
    );

    const avatar = this.querySelector(".avatar");
    const tournament_name = this.querySelector(".tournament-name");
    const score = this.querySelector(".score");
    const status = this.getAttribute("status");

    avatar.src = this.getAttribute("avatar");
    tournament_name.textContent = this.getAttribute("tournament-name");
    if (status === "PN") {
      score.textContent = "-";
    } else if (status === "PR") {
      score.textContent = this.getAttribute("score");
    }
  }
}

customElements.define("tournament-player-card", TournamentPlayerCard);
