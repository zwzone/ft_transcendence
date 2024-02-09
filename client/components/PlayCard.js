export default class PlayCard extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("play-card");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add(
      "d-flex",
      "justify-content-center",
      "align-items-center",
      "flex-column",
      "rounded-5",
      "p-3",
    );

    const text = this.getAttribute("headText");
    const head = this.querySelector("h1");
    head.textContent = text;
  }
}

customElements.define("play-card", PlayCard);
