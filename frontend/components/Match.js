export default class Match extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("match-card");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
  }
}

customElements.define("match-card", Match);
