import fetching from "../utilities/fetching.js";

export default class FriendsList extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("friends-list");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add("d-flex", "justify-content-center", "flex-column", "gap-2");

    const nav = this.querySelector("nav");
    const friends_btn = nav.querySelector(".friends-btn");
    const requests_btn = nav.querySelector(".requests-btn");
    const invites_btn = nav.querySelector(".invites-btn");
    const friend_cards = this.querySelector(".friend-cards");
    const friend_card_popup = this.querySelector("friend-card-popup");

    this.showCards("friends");

    friend_cards.classList.add("d-flex", "flex-wrap", "gap-1");
    friends_btn.addEventListener("click", () => {
      this.showCards("friends");
    });
    requests_btn.addEventListener("click", () => {
      this.showCards("requests");
    });
    invites_btn.addEventListener("click", () => {
      this.showCards("invites");
    });
  }

  showCards(friend_card_type) {
    const friend_cards = this.querySelector(".friend-cards");

    fetching(
      `https://${window.ft_transcendence_host}/player/friendship/?target=${friend_card_type}`,
    ).then((req) => {
      const arr = req.friendships;
      console.log("FRIENDS:", arr);
      friend_cards.innerHTML = "";
      for (let i = 0; i < arr.length; i++) {
        const friend_card_elem = document.createElement("friend-card");
        friend_card_elem.setAttribute("friend-card-type", friend_card_type);
        friend_card_elem.setAttribute("id", arr[i].id);
        friend_card_elem.setAttribute("avatar", arr[i].avatar);
        friend_card_elem.setAttribute("username", arr[i].username);
        friend_cards.appendChild(friend_card_elem);
      }
    });
  }
}

customElements.define("friends-list", FriendsList);
