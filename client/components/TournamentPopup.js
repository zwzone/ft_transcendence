import fetching from "../utilities/fetching.js";

export default class TournamentPopup extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("tournament-popup");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add(
      "d-flex",
      "flex-column",
      "justify-content-center",
      "align-items-center",
      "gap-2",
    );

    const close_button = this.querySelector(".popup-close");
    const popup_header = this.querySelector(".popup-header");
    const popup_input = this.querySelector(".popup-input");
    const popup_name = this.querySelector(".popup-name");
    const popup_btn = this.querySelector(".popup-btn");

    const popup_type = this.attributes["popup-type"].value;

    if (popup_type === "CREATE") {
      popup_header.textContent = "Create Tournament";
      popup_name.style.display = "none";
      popup_btn.textContent = "Create";
    } else if (popup_type === "JOIN") {
      popup_header.textContent = "Join Tournament";
      popup_input.style.display = "none";
      popup_name.textContent = "Tournament ID";
      popup_btn.textContent = "Join";
    }

    close_button.addEventListener("click", (event) => {
      this.parentElement.removeChild(this);
    });
  }
}

customElements.define("tournament-popup", TournamentPopup);
