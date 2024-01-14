import Router from "../router/router.js";

export default class Navbar extends HTMLElement {
  constructor() {
    super();
  }
  connectedCallback() {
    const template = document.getElementById("my-navbar");
    const component = template.content.cloneNode(true);
    this.appendChild(component);

    const handleLink = (event) => {
      event.preventDefault();
      const url = event.target.getAttribute("href");
      Router.go(url, "add");
    };

    const logo = this.querySelector(".logo");
    logo.addEventListener("click", handleLink);

    const links = this.querySelectorAll(".link.btn");
    links.forEach((link) => {
      link.addEventListener("click", handleLink);
    });
  }
}

customElements.define("my-navbar", Navbar);
