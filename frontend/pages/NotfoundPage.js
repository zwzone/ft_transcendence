export default class NotfoundPage extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("notfound-template");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
  }
}

customElements.define("notfound-page", NotfoundPage);
