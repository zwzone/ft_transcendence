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

    const avatar = this.querySelector(".setting-avatar .avatar");
    const input_avatar = this.querySelector("#input-avatar");
    const input_username = this.querySelector(".input-username");
    const button_username = this.querySelector(".button-username");
    const input_first_name = this.querySelector(".input-first-name");
    const button_first_name = this.querySelector(".button-first-name");
    const input_last_name = this.querySelector(".input-last-name");
    const button_last_name = this.querySelector(".button-last-name");

    fetching("https://localhost/player/avatar/").then((res) => {
      avatar.src = res.avatar;
    });
    fetching("https://localhost/player/username/").then((res) => {
      this.querySelector(".input-username").placeholder = res.username;
    });
    fetching("https://localhost/player/first_name/").then((res) => {
      this.querySelector(".input-first-name").placeholder = res.first_name;
    });
    fetching("https://localhost/player/last_name/").then((res) => {
      this.querySelector(".input-last-name").placeholder = res.last_name;
    });

    input_avatar.onchange = function () {
      console.log("input_avatar :", input_avatar.files[0]);
      avatar.src = URL.createObjectURL(input_avatar.files[0]);
      fetching("https://localhost/player/avatar/", "POST", {
        avatar: input_avatar.files[0],
      });
    };
    button_username.onclick = (event) => {
      this.input_change(input_username, "username");
    };
    button_first_name.onclick = (event) => {
      this.input_change(input_first_name, "first_name");
    };
    button_last_name.onclick = (event) => {
      this.input_change(input_last_name, "last_name");
    };
  }

  input_change(input, field) {
    console.log("hello");
    fetching(`https://localhost/player/${field}/`, "POST", {
      [field]: input.value,
    });
  }
}

customElements.define("setting-page", SettingPage);
