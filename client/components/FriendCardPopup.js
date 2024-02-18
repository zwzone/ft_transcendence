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
    }

    popup_header.textContent = this.attributes["friend-card-type"].value.toUpperCase().slice(0, -1);

    close_button.addEventListener("click", (event) => {
      this.parentElement.removeChild(this);
    });

    green_button.addEventListener("click", (event) => {
      if (this.attributes["friend-card-type"].value === "invites") {
        fetching(
          `https://${window.ft_transcendence_host}/player/friendship/accept/?target=${this.attributes["username"].value}`,
          "POST",
          {
            id: this.attributes["id"].value,
          },
        ).then((req) => {
          console.log(req);
        });
      }
    });

    green_button.addEventListener("click", (event) => {
      if (this.attributes["friend-card-type"].value === "invites") {
        fetching(
          `https://${window.ft_transcendence_host}/player/friendship/accept/?target=${this.attributes["username"].value}`,
          "DELETE",
          {
            id: this.attributes["id"].value,
          },
        ).then((req) => {
          console.log(req);
        });
      }
    });
  }
}

customElements.define("friend-card-popup", FriendCardPopup);
