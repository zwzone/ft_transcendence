import fetching from "../utilities/fetching.js";

export default class ProfilePage extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("profile-template");
    const component = template.content.cloneNode(true);
    this.appendChild(component);

    this.classList.add("my-page");

    fetching("https://localhost/player/avatar/").then((res) => {
      console.log("CURRENT", res);
      console.log(this.querySelector(".player-data .avatar"));
      this.querySelector(".player-data .avatar").setAttribute(
        "src",
        res.avatar,
      );
    });
    fetching("https://localhost/player/first_name/").then((res) => {
      this.querySelector(".player-data .first-name").innerText = res.first_name;
    });
    fetching("https://localhost/player/last_name/").then((res) => {
      this.querySelector(".player-data .last-name").innerText = res.last_name;
    });
  }
}

customElements.define("profile-page", ProfilePage);
