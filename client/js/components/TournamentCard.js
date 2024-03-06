export default class TournamentCard extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("tournament-card");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add(
      "d-flex",
      "flex-column",
      "justify-content-center",
      "align-items-center",
      "flex-wrap",
      "rounded-4",
      "p-2",
    );

    const tournament_name_elem = this.querySelector(".tournament-name");
    const size_elem = this.querySelector(".size");

    const tournament_name = this.attributes["tournament-name"].value;
    const size = this.attributes["size"].value;

    tournament_name_elem.textContent = tournament_name;
    size_elem.textContent = `${size} / 8`;
  }
}

customElements.define("tournament-card", TournamentCard);
