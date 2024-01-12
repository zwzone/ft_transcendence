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

    const brand = this.querySelector("a.navbar-brand");
    brand.addEventListener("click", handleLink);

    const links = this.querySelectorAll("a.nav-link");
    links.forEach((link) => {
      link.addEventListener("click", handleLink);
    });
  }
}

customElements.define("my-navbar", Navbar);
