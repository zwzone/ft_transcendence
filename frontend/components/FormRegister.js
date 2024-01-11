export default class FormRegister extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("form-register");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
  }
}

customElements.define("form-register", FormRegister);
