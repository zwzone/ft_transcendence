export default class SettingPage extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("setting-template");
    const component = template.content.cloneNode(true);
    this.appendChild(component);

    this.classList.add("my-page");
  }
}

customElements.define("setting-page", SettingPage);
