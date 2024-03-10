export default class Stars extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("stars-overlay");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
  }
}

customElements.define("stars-overlay", Stars);
