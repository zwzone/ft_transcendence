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
    const search_btn = this.querySelector(".search-btn");
    const friend_cards = this.querySelector(".friend-cards");

    this.showCards("friends");

    friend_cards.classList.add("d-flex", "flex-wrap", "gap-1");
    friends_btn.addEventListener("click", () => {
      friends_btn.classList.add("active");
      requests_btn.classList.remove("active");
      invites_btn.classList.remove("active");
      search_btn.classList.remove("active");
      this.showCards("friends");
    });
    requests_btn.addEventListener("click", () => {
      friends_btn.classList.remove("active");
      requests_btn.classList.add("active");
      invites_btn.classList.remove("active");
      search_btn.classList.remove("active");
      this.showCards("requests");
    });
    invites_btn.addEventListener("click", () => {
      friends_btn.classList.remove("active");
      requests_btn.classList.remove("active");
      invites_btn.classList.add("active");
      search_btn.classList.remove("active");
      this.showCards("invites");
    });
    search_btn.addEventListener("click", () => {
      friends_btn.classList.remove("active");
      requests_btn.classList.remove("active");
      invites_btn.classList.remove("active");
      search_btn.classList.add("active");
      this.showCards("search");
    });
  }

  showCards(friend_card_type) {
    const friend_cards = this.querySelector(".friend-cards");
    friend_cards.innerHTML = "";

    if (friend_card_type === "search") {
      friend_cards.appendChild(document.createElement("search-list"));
      return;
    }

    fetching(
      `https://${window.ft_transcendence_host}/player/friendship/?target=${friend_card_type}`,
    ).then((req) => {
      const arr = req.friendships;
      for (let i = 0; i < arr.length; i++) {
        const friend_card_elem = document.createElement("friend-card");
        friend_card_elem.setAttribute("friend-card-type", friend_card_type);
        friend_card_elem.setAttribute("player-id", arr[i].id);
        friend_card_elem.setAttribute("first-name", arr[i].first_name);
        friend_card_elem.setAttribute("last-name", arr[i].last_name);
        friend_card_elem.setAttribute("username", arr[i].username);
        friend_card_elem.setAttribute("avatar", arr[i].avatar);
        friend_card_elem.setAttribute("status", arr[i].status);
        friend_cards.appendChild(friend_card_elem);
      }
    });
  }
}

customElements.define("friends-list", FriendsList);
