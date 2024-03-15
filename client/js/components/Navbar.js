import router from "../utilities/router.js";

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
      router.go(url, "", "add");
    };

    const logo = this.querySelector(".logo");
    const colorizer = this.querySelector(".colorizer.btn");
    const links = this.querySelectorAll(".link.btn");
    const hamburger = this.querySelector(".hamburger");

    logo.addEventListener("click", handleLink);

    colorizer.addEventListener("click", (event) => {
      const color_primary = localStorage.getItem("colorizer");
      if (color_primary === "blue") {
        localStorage.setItem("colorizer", "yellow");
        document.documentElement.style.setProperty("--color-primary", "#f8ec9030");
        document.documentElement.style.setProperty("--color-primary-solid", "#2e2c1d");
        document.documentElement.style.setProperty("--color-primary-light", "#f8ec90");
      } else {
        localStorage.setItem("colorizer", "blue");
        document.documentElement.style.setProperty("--color-primary", "#2cacff30");
        document.documentElement.style.setProperty("--color-primary-solid", "#0f3c5a");
        document.documentElement.style.setProperty("--color-primary-light", "#2cacff");
      }
    });

    links.forEach((link) => {
      link.addEventListener("click", handleLink);
    });

    hamburger.addEventListener("click", (event) => {
      this.classList.toggle("active");
    });
  }
}

customElements.define("my-navbar", Navbar);
