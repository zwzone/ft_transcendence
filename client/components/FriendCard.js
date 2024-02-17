export default class FriendCard extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("friend-card");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add(
      "d-flex",
      "flex-column",
      "justify-content-center",
      "align-items-center",
      "py-2",
      "px-3",
      "rounded-5",
    );
  }
}

customElements.define("friend-card", FriendCard);
