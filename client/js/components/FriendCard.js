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

    const player_id = this.attributes["player-id"].value;
    const username = this.attributes["username"].value;
    const first_name = this.attributes["first-name"].value;
    const last_name = this.attributes["last-name"].value;
    const avatar = this.attributes["avatar"].value;
    const status = this.attributes["status"].value;

    this.querySelector("h6").textContent = username;
    this.querySelector("img").src = avatar;
    this.querySelector(".status").style.backgroundColor = status === "ON" ? "green" : "red";

    this.addEventListener("click", () => {
      const friend_card_popup = document.createElement("friend-card-popup");
      friend_card_popup.setAttribute("friend-card-type", this.attributes["friend-card-type"].value);
      friend_card_popup.setAttribute("player-id", this.attributes["player-id"].value);
      friend_card_popup.setAttribute("username", username);
      friend_card_popup.setAttribute("first-name", first_name);
      friend_card_popup.setAttribute("last-name", last_name);
      friend_card_popup.setAttribute("avatar", avatar);

      this.parentNode.appendChild(friend_card_popup);
    });
  }
}

customElements.define("friend-card", FriendCard);
