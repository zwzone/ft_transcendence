import Router from "../router/router.js";

export default class Navbar extends HTMLElement {
  constructor() {
    super();
  }
  connectedCallback() {
    const template = document.getElementById("my-navbar");
    const component = template.content.cloneNode(true);
    this.appendChild(component);

    this.classList.add(
      "d-flex",
      "justify-content-between",
      "align-items-center",
      "w-100",
      "px-5",
      "py-2",
    );

    const handleLink = (event) => {
      event.preventDefault();
      const url = event.target.getAttribute("href");
      Router.go(url, "add");
    };

    const logo = this.querySelector(".logo");
    const links = this.querySelectorAll(".link.btn");
    const hamburger = this.querySelector(".hamburger");

    logo.addEventListener("click", handleLink);
    links.forEach((link) => {
      link.addEventListener("click", handleLink);
    });

    hamburger.addEventListener("click", (event) => {
      this.classList.toggle("active");
    });
  }
}

customElements.define("my-navbar", Navbar);
