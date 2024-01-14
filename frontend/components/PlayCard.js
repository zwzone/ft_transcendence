export default class PlayCard extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("play-card");
    const component = template.content.cloneNode(true);
    console.log(component.children);
    this.appendChild(component);
    const color = this.getAttribute("color");
    const game = this.getAttribute("headText");
    this.classList.add(`text-bg-${color}`);
    this.querySelectorAll(".btn").forEach((btn) => {
      btn.classList.add(`btn-outline-${color}`);
    });
    this.querySelector("h1").textContent = game;
  }
}

customElements.define("play-card", PlayCard);
