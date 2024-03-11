export default class Footer extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("my-footer");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add(
      "d-flex",
      "justify-content-center",
      "align-items-center",
    );
    this.style.fontFamily = "Koulen";
  }
}

customElements.define("my-footer", Footer);
