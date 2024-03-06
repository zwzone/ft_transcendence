export default class HomePage extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("home-template");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add("my-page");
  }
}

customElements.define("home-page", HomePage);
