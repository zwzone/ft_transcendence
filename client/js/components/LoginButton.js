export default class LoginButton extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("login-button");
    const component = template.content.cloneNode(true);
    this.appendChild(component);

    const link = this.getAttribute("link");
    const color = this.getAttribute("color");
    const text = this.getAttribute("text");

    const button = this.querySelector("a");
    button.setAttribute("href", link);
    button.style.backgroundColor = `var(--bs-${color})`;
    button.textContent = text;
    button.classList.add(`border-${color}-subtle`);
    if (color === "success") {
      button.classList.add("intra");
    } else if (color === "primary") {
      button.classList.add("google");
    }
  }
}

customElements.define("login-button", LoginButton);
