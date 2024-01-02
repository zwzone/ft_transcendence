export default class HomePage extends HTMLElement {
  constructor() {
    super();
  }
  connectedCallback() {
    const template = document.getElementById("home-template");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
  }
}

customElements.define("home-page", HomePage);
