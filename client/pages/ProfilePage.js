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

    fetching(`https://${window.ft_transcendence_host}/player/`).then((res) => {
      this.querySelector(".player-data .avatar").setAttribute("src", res.player.avatar);
      this.querySelector(".player-data .username").innerText = res.player.username;
      this.querySelector(".player-data .first-name").innerText = res.player.first_name;
      this.querySelector(".player-data .last-name").innerText = res.player.last_name;
    });
  }
}

customElements.define("profile-page", ProfilePage);
