export default class Card extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("my-card");
    const component = template.content.cloneNode(true);
    console.log(component.children);
    this.appendChild(component);
    this.style.width = "fit-content";
    this.style.paddingInline = "0";
    const color = this.getAttribute("color");
    this.classList.add("card", `text-bg-${color}`);
    this.querySelector(".btn").classList.add(`btn-${color}`);
    this.querySelector("h1").textContent = this.getAttribute("headText");
  }
}

customElements.define("my-card", Card);
