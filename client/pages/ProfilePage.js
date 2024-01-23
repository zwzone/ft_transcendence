export default class ProfilePage extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("profile-template");
    const component = template.content.cloneNode(true);
    this.appendChild(component);

    this.classList.add("my-page");
  }
}

customElements.define("profile-page", ProfilePage);
