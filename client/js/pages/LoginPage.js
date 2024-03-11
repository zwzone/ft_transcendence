export default class LoginPage extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("login-template");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add("my-page");
  }
}

customElements.define("login-page", LoginPage);
