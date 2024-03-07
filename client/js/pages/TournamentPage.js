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
    const tournament_players = tournament_current.querySelector("tournament-players");
    const tournament_players_list = tournament_players.querySelector(".tournament-players-list");
    const tournament_players_start = tournament_players.querySelector(".start");
    const tournament_players_leave = tournament_players.querySelector(".leave");
    const tournament_matches = tournament_current.querySelector("tournament-matches");
    const create_btn = tournament_actions.querySelector(".tournament-create button");
    const tournament_list = this.querySelector(".tournament-list");

    fetching(`https://${window.ft_transcendence_host}/tournament/`).then((data) => {
      if (!data.current_tournament || data.current_tournament.status === "FN") {
        tournament_actions.classList.remove("d-none");
        tournament_actions.classList.add("d-flex");
        if (data.tournaments) {
          for (const tournament of data.tournaments) {
            const tournament_card = document.createElement("tournament-card");
            tournament_card.setAttribute("tournament-name", tournament.name);
            tournament_card.setAttribute("size", tournament.players_count);
            tournament_list.append(tournament_card);
            tournament_card.addEventListener("click", () => {
              const tournament_popup = document.createElement("tournament-popup");
              tournament_popup.setAttribute("popup-type", "JOIN");
              tournament_popup.setAttribute("tournament-id", tournament.id);
              tournament_popup.setAttribute("tournament-name", tournament.name);
              this.appendChild(tournament_popup);
            });
          }
        } else {
          tournament_list.textContent = "No tournaments available";
        }
        create_btn.addEventListener("click", () => {
          const tournament_popup = document.createElement("tournament-popup");
          tournament_popup.setAttribute("popup-type", "CREATE");
          tournament_popup.setAttribute("tournament-id", null);
          tournament_popup.setAttribute("tournament-name", null);
          this.appendChild(tournament_popup);
        });
      }
      if (data.current_tournament) {
        tournament_current.classList.remove("d-none");
        tournament_current.classList.add("d-flex");
        if (data.current_tournament.status === "PN") {
          tournament_players.classList.remove("d-none");
          tournament_players.classList.add("d-flex");
          for (const player of data.players) {
            const player_elem = document.createElement("tournament-player-card");
            player_elem.setAttribute("tournament-name", player.tournament_name);
            player_elem.setAttribute("avatar", player.avatar);
            player_elem.setAttribute("status", "PN");
            tournament_players_list.append(player_elem);
          }
          if (data.current_tournament.creator === true) {
            tournament_players_start.classList.remove("d-none");
            tournament_players_start.classList.add("d-block");
          }
          tournament_players_start.addEventListener("click", () => {
            fetching(
              `https://${window.ft_transcendence_host}/tournament/`,
              "POST",
              JSON.stringify({ action: "start", tournament_id: data.current_tournament.id }),
              { "Content-Type": "application/json" },
            ).then((data) => {
              if (data.status === 400) {
                alert(data.message);
              }
            });
          });
          tournament_players_leave.addEventListener("click", () => {
            fetching(
              `https://${window.ft_transcendence_host}/tournament/`,
              "POST",
              JSON.stringify({ action: "leave", tournament_id: data.current_tournament.id }),
              { "Content-Type": "application/json" },
            ).then((data) => {
              window.location.reload();
            });
          });
        } else {
          tournament_matches.classList.remove("d-none");
          tournament_matches.classList.add("d-flex");
          const match_elems = this.querySelectorAll("tournament-match-card");
          for (let i = 0; i < 7; ++i) {
            const match = data.current_tournament.matches[i];
            const match_elem = match_elems[i];
            if (match) {
              match_elem.setAttribute("match-id", match.id);
              if (match.current) {
                match_elem.querySelector("button").classList.remove("d-none");
              }
              for (let j = 0; j < 2; ++j) {
                const player = match.players[j];
                const player_elem = match_elem.querySelector(`.player${j + 1}`);
                player_elem.querySelector("h6").textContent = player.player.tournament_name;
                player_elem.querySelector("img").src = player.player.avatar;
                if (match.state === "PLY")
                  player_elem.querySelector("h3").textContent = player.score;
              }
            }
          }
        }
      }
    });
  }
}

customElements.define("tournament-page", TournamentPage);
