import router from "../utilities/router.js";

export default class PlayCard extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("play-card");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add(
      "d-flex",
      "justify-content-center",
      "align-items-center",
      "flex-column",
      "rounded-5",
      "pb-3",
    );

    const play_two_elem = this.querySelector(".play-two");
    const play_four_elem = this.querySelector(".play-four");
    const play_ai_elem = this.querySelector(".play-ai");
    const play_coop_elem = this.querySelector(".play-coop");
    const head = this.querySelector("h1");
    const game = this.getAttribute("game");
    const wallpaper = this.getAttribute("wallpaper");

    this.querySelector("img").src = wallpaper;
    if (game === "PG") {
      head.textContent = "PING PONG";
      play_ai_elem.style.display = "none";
    } else if (game === "TTT") {
      head.textContent = "TIC TAC TOE";
      play_four_elem.style.display = "none";
    }
    play_two_elem.addEventListener("click", () => {
      router.go("/game/", `?game=${game}&mode=two`, "add");
    });
    play_four_elem.addEventListener("click", () => {
      router.go("/game/", `?game=${game}&mode=four`, "add");
    });
    play_ai_elem.addEventListener("click", () => {
      router.go("/game/", `?game=${game}&mode=ai`, "add");
    });
    play_coop_elem.addEventListener("click", () => {
      router.go("/game/", `?game=${game}&mode=coop`, "add");
    });
  }
}

customElements.define("play-card", PlayCard);
