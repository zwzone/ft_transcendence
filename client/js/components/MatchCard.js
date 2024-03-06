export default class MatchCard extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("match-card");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add(
      "d-flex",
      "flex-wrap",
      "justify-content-around",
      "align-items-center",
      "p-1",
      "gap-1",
      "rounded-5",
    );

    const match = JSON.parse(this.getAttribute("match"));
    for (const player of match.players) {
      const player_card_elem = document.createElement("player-card");
      player_card_elem.setAttribute("avatar", player.avatar);
      player_card_elem.setAttribute("username", player.username);
      player_card_elem.setAttribute("score", player.score);
      this.appendChild(player_card_elem);
    }
  }
}

customElements.define("match-card", MatchCard);
