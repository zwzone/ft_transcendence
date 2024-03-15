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
    const popup_input_alias_name = this.querySelector(".alias-name .popup-input");
    const popup_input_tournament_name = this.querySelector(".tournament-name .popup-input");
    const popup_tournament_name = this.querySelector(".popup-tournament-name");
    const popup_btn = this.querySelector(".popup-btn");

    const popup_type = this.attributes["popup-type"].value;
    const tournament_name = this.attributes["tournament-name"].value;
    const tournament_id = this.attributes["tournament-id"].value;

    close_button.addEventListener("click", (event) => {
      this.parentElement.removeChild(this);
    });

    if (popup_type === "CREATE") {
      popup_header.textContent = "Create Tournament";
      popup_tournament_name.style.display = "none";
      popup_btn.textContent = "Create";
      popup_btn.addEventListener("click", (event) => {
        fetching(
          `https://${window.ft_transcendence_host}/tournament/`,
          "POST",
          JSON.stringify({
            action: "create",
            alias_name: popup_input_alias_name.value,
            tournament_name: popup_input_tournament_name.value,
            tournament_id: tournament_id,
          }),
          {
            "Content-Type": "application/json",
          },
        ).then((data) => {
          console.log("status code", data.statusCode);
          if (data.statusCode === 200) window.location.reload();
          else alert(data.message);
        });
      });
    } else if (popup_type === "JOIN") {
      popup_header.textContent = "Join Tournament";
      popup_input_tournament_name.style.display = "none";
      popup_tournament_name.textContent = tournament_name;
      popup_btn.textContent = "Join";
      popup_btn.addEventListener("click", (event) => {
        fetching(
          `https://${window.ft_transcendence_host}/tournament/`,
          "POST",
          JSON.stringify({
            action: "join",
            alias_name: popup_input_alias_name.value,
            tournament_id: tournament_id,
          }),
          {
            "Content-Type": "application/json",
          },
        ).then((data) => {
          console.log("status code", data.statusCode);
          if (data.statusCode === 200) window.location.reload();
          else alert(data.message);
        });
      });
    }
  }
}

customElements.define("tournament-popup", TournamentPopup);
