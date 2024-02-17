export default class TwofaPage extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("twofa-template");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add("my-page");
  }
}

customElements.define("twofa-page", TwofaPage);
