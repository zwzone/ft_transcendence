export default class PlayerCard extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("player-card");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add(
      "d-flex",
      "flex-column",
      "justify-content-center",
      "align-items-center",
      "py-2",
      "rounded-5",
    );

    const avatar_elem = this.querySelector(".avatar");
    const username_elem = this.querySelector(".username");
    const score_elem = this.querySelector(".score");

    const avatar = this.getAttribute("avatar");
    const username = this.getAttribute("username");
    const score = this.getAttribute("score");

    avatar_elem.src = avatar;
    username_elem.textContent = username;
    score_elem.textContent = score;
  }
}

customElements.define("player-card", PlayerCard);
