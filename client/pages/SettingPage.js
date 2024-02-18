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
    const checkbox_twofa = this.querySelector(".setting-twofa input[type=checkbox]");
    const popup_twofa = this.querySelector(".popup-twofa");
    const popup_twofa_qrcode = this.querySelector(".popup-twofa-qrcode");
    const popup_twofa_close = this.querySelector(".popup-twofa-close");

    fetching(`https://${window.ft_transcendence_host}/player/`).then((res) => {
      avatar.src = res.player.avatar;
      input_username.placeholder = res.player.username;
      input_first_name.placeholder = res.player.first_name;
      input_last_name.placeholder = res.player.last_name;
      checkbox_twofa.checked = res.player.two_factor;
    });

    input_avatar.onchange = function () {
      const avatarImage = input_avatar.files[0];
      avatar.src = URL.createObjectURL(avatarImage);
      const formData = new FormData();
      formData.append("avatar", avatarImage);
      fetching(`https://${window.ft_transcendence_host}/player/avatar/`, "POST", formData);
    };
    button_username.onclick = (event) => {
      player_post_changes("username", input_username.value);
    };
    button_first_name.onclick = (event) => {
      player_post_changes("first_name", input_first_name.value);
    };
    button_last_name.onclick = (event) => {
      player_post_changes("last_name", input_last_name.value);
    };
    checkbox_twofa.onchange = (event) => {
      if (checkbox_twofa.checked) {
        fetch(`https://localhost/authentication/2FA/qrcode/`)
          .then((res) => res.blob())
          .then((blob) => set_qrcode(blob));
      } else {
        player_post_changes("two_factor", checkbox_twofa.checked);
      }
    };

    popup_twofa_close.onclick = (event) => {
      checkbox_twofa.checked = !checkbox_twofa.checked;
      popup_twofa.removeChild(popup_twofa.lastChild);
      popup_twofa.style.display = "none";
    };

    function player_post_changes(field, value) {
      fetching(
        `https://${window.ft_transcendence_host}/player/`,
        "POST",
        JSON.stringify({ player: { [field]: value } }),
        { "Content-Type": "application/json" },
      ).then((res) => {
        alert(res.message);
      });
    }

    function set_qrcode(blob) {
      const url = URL.createObjectURL(blob);
      const img = new Image();
      img.src = url;
      img.onload = () => {
        popup_twofa.style.display = "flex";
        popup_twofa_qrcode.appendChild(img);
      };
    }
  }
}

customElements.define("setting-page", SettingPage);
