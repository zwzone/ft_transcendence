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
      "flex-column",
      "justify-content-center",
      "align-items-center",
      "rounded-4",
      "p-2",
    );

    const btn = this.querySelector("button");
    btn.addEventListener("click", () => {
      window.location.href = `/game?game=PG&mode=two&match=${this.getAttribute("match-id")}`;
    });
  }
}

customElements.define("tournament-match-card", TournamentMatchCard);
