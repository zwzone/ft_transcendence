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
      "justify-content-center",
      "align-items-center",
      "gap-3",
      "py-2",
      "px-3",
      "rounded-5",
    );
  }
}

customElements.define("match-card", MatchCard);
