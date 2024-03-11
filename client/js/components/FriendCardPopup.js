import fetching from "../utilities/fetching.js";

export default class FriendCardPopup extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("friend-card-popup");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add(
      "d-flex",
      "flex-column",
      "justify-content-center",
      "align-items-center",
      "gap-2",
    );

    const close_button = this.querySelector(".popup-close");
    const popup_header = this.querySelector(".popup-header");
    const avatar = this.querySelector(".avatar");
    const username = this.querySelector(".username");
    const first_name = this.querySelector(".first-name");
    const last_name = this.querySelector(".last-name");
    const green_button = this.querySelector(".green-button");
    const red_button = this.querySelector(".red-button");

    if (this.attributes["friend-card-type"].value === "friends") {
      green_button.style.display = "none";
      red_button.textContent = "Remove";
    } else if (this.attributes["friend-card-type"].value === "requests") {
      green_button.style.display = "none";
      red_button.textContent = "Cancel";
    } else if (this.attributes["friend-card-type"].value === "invites") {
      green_button.textContent = "Accept";
      red_button.textContent = "Decline";
    } else if (this.attributes["friend-card-type"].value === "search") {
      green_button.textContent = "Send Friend Request";
      red_button.style.display = "none";
    }

    popup_header.textContent = this.attributes["friend-card-type"].value.toUpperCase().slice(0, -1);
    if (this.attributes["friend-card-type"].value === "search") popup_header.textContent += "H";
    avatar.src = this.attributes["avatar"].value;
    username.textContent = this.attributes["username"].value;
    first_name.textContent = this.attributes["first-name"].value;
    last_name.textContent = this.attributes["last-name"].value;

    close_button.addEventListener("click", (event) => {
      this.parentElement.removeChild(this);
    });

    const friendship_ation = (action, player_id) => {
      const json = JSON.stringify({
        target_id: Number(player_id),
      });
      fetching(`https://${window.ft_transcendence_host}/player/friendship/`, action, json, {
        "Content-Type": "application/json",
      }).then((req) => {
        if (req.status === 400 && req.message.startsWith("You")) {
          alert(req.message);
          return;
        }
        const friend_list = document.querySelector(".friend-list");
        const friends_list = friend_list.querySelector("friends-list");
        this.parentElement.removeChild(this);
        friend_list.removeChild(friends_list);
        friend_list.appendChild(document.createElement("friends-list"));
      });
    };

    green_button.addEventListener("click", (event) => {
      friendship_ation("POST", this.attributes["player-id"].value);
    });

    red_button.addEventListener("click", (event) => {
      friendship_ation("DELETE", this.attributes["player-id"].value);
    });
  }
}

customElements.define("friend-card-popup", FriendCardPopup);
