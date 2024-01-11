export default class FormLogin extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("form-login");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
  }
}

customElements.define("form-login", FormLogin);
