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
      "px-1",
      "rounded-4",
    );

    const avatar = this.querySelector(".avatar");
    const tournament_name = this.querySelector(".tournament-name");
    const score = this.querySelector(".score");

    const avatar_att = this.getAttribute("avatar");
    const tournament_name_att = this.getAttribute("tournament-name");
    const status = this.getAttribute("status");

    if (avatar_att) avatar.src = avatar_att;
    else avatar.src = "/images/gray.png";

    tournament_name.textContent = tournament_name_att;

    if (status === "PN") {
      score.style.display = "none";
    } else if (status === "PR") {
      score.textContent = this.getAttribute("score");
    }
  }
}

customElements.define("tournament-player-card", TournamentPlayerCard);
