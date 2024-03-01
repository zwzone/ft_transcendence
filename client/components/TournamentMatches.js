export default class TournamentMatches extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("tournament-matches");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add("d-none", "justify-content-center", "gap-3");
  }
}

customElements.define("tournament-matches", TournamentMatches);
