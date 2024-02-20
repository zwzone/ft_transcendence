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

    const username = this.attributes["username"].value;
    const avatar = this.attributes["avatar"].value;

    this.querySelector("h6").textContent = username;
    this.querySelector("img").src = avatar;

    this.addEventListener("click", () => {
      const friend_card_popup = document.createElement("friend-card-popup");
      friend_card_popup.setAttribute("player-id", this.attributes["player-id"].value);
      friend_card_popup.setAttribute("friend-card-type", this.attributes["friend-card-type"].value);
      this.parentNode.appendChild(friend_card_popup);
    });
  }
}

customElements.define("friend-card", FriendCard);
