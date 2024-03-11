import router from "../utilities/router.js";

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
      "gap-3",
      "p-1",
    );

    const btn = this.querySelector("button");
    btn.addEventListener("click", () => {
      router.go("/game/", `?game=PG&mode=two&match=${this.getAttribute("match-id")}`, "add");
    });
  }
}

customElements.define("tournament-match-card", TournamentMatchCard);
