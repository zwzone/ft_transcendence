export default class Footer extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("my-footer");
    const component = template.content.cloneNode(true);
    this.appendChild(component);

    this.style.fontFamily = "Koulen";
  }
}

customElements.define("my-footer", Footer);
