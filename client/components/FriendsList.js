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

    friend_cards.classList.add("d-flex", "flex-wrap", "gap-1");
    friends_btn.addEventListener("click", () => {
      this.showFriends();
    });
    requests_btn.addEventListener("click", () => {
      this.showRequests();
    });
    invites_btn.addEventListener("click", () => {
      this.showInvites();
    });
  }

  showFriends() {
    const friend_cards = this.querySelector(".friend-cards");

    friend_cards.innerHTML = "";
    for (let i = 0; i < 17; i++) friend_cards.appendChild(document.createElement("friend-card"));
  }

  showRequests() {
    const friend_cards = this.querySelector(".friend-cards");

    friend_cards.innerHTML = "";
    for (let i = 0; i < 2; i++) friend_cards.appendChild(document.createElement("friend-card"));
  }

  showInvites() {
    const friend_cards = this.querySelector(".friend-cards");

    friend_cards.innerHTML = "";
    for (let i = 0; i < 4; i++) friend_cards.appendChild(document.createElement("friend-card"));
  }
}

customElements.define("friends-list", FriendsList);
