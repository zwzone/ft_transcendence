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

    fetching(`https://${window.ft_transcendence_host}/player/`).then((res) => {
      avatar.src = res.player.avatar;
      this.querySelector(".input-username").placeholder = res.player.username;
      this.querySelector(".input-first-name").placeholder =
        res.player.first_name;
      this.querySelector(".input-last-name").placeholder = res.player.last_name;
    });

    input_avatar.onchange = function () {
      const avatarImage = input_avatar.files[0];
      console.log("input_avatar :", avatarImage);
      avatar.src = URL.createObjectURL(avatarImage);
      const formData = new FormData();
      formData.append("avatar", avatarImage);
      fetching(`https://${window.ft_transcendence_host}/player/avatar/`, "POST", formData);
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
    console.log({ [field]: input.value });
    fetching(
      `https://${window.ft_transcendence_host}/player/`,
      "POST",
      JSON.stringify({
        player: {
          [field]: input.value,
        },
      }),
      {
        "Content-Type": "application/json",
      },
    );
  }
}

customElements.define("setting-page", SettingPage);
