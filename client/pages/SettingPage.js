import fetching from "../utilities/fetching.js";

export default class SettingPage extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("setting-template");
    const component = template.content.cloneNode(true);
    this.appendChild(component);

    this.classList.add("my-page");

    fetching("https://localhost/player/avatar/").then((res) => {
      this.querySelector(".setting-data .avatar").setAttribute(
        "src",
        res.avatar,
      );
    });
    fetching("https://localhost/player/username/").then((res) => {
      this.querySelector(".setting-data .username").placeholder = res.username;
    });
    fetching("https://localhost/player/first_name/").then((res) => {
      this.querySelector(".setting-data .first_name").placeholder =
        res.first_name;
    });
    fetching("https://localhost/player/last_name/").then((res) => {
      this.querySelector(".setting-data .last_name").placeholder =
        res.last_name;
    });
  }
}

customElements.define("setting-page", SettingPage);
