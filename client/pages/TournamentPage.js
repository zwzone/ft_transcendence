import fetching from "../utilities/fetching.js";

export default class TournamentPage extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("tournament-template");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add("my-page");

    const tournament_actions = this.querySelector(".tournament-actions");
    const tournament_current = this.querySelector(".tournament-current");
    const create_btn = tournament_actions.querySelector(".tournament-create");
    const join_btn = tournament_actions.querySelector(".tournament-join");
    const tournament_list = this.querySelector(".tournament-list");

    fetching(`https://${window.ft_transcendence_host}/tournaments/`).then((data) => {
      // if (data.tournaments) {
      tournament_actions.classList.remove("d-none");
      tournament_actions.classList.add("d-flex");
      create_btn.addEventListener("click", () => {
        const tournament_popup = document.createElement("tournament-popup");
        tournament_popup.setAttribute("popup-type", "CREATE");
        this.appendChild(tournament_popup);
      });
      for (const tournament of data.tournaments) {
      }
      join_btn.addEventListener("click", () => {
        const tournament_popup = document.createElement("tournament-popup");
        tournament_popup.setAttribute("popup-type", "JOIN");
        this.appendChild(tournament_popup);
      });
      // }
      /*       if (data.current_tournament) {
        tournament_current.classList.remove("d-none");
        tournament_current.classList.add("d-flex");
        tournaments = data.tournaments;
      } */
    });
  }
}

customElements.define("tournament-page", TournamentPage);
