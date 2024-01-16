export default class FriendCard extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("friend-card");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
  }
}

customElements.define("friend-card", FriendCard);