import fetching from "../utilities/fetching.js";

export default class MatchHistory extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("match-history");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add(
      "d-flex",
      "flex-column",
      "justify-content-center",
      "gap-3",
      "py-2",
      "px-3",
      "rounded-5",
    );

    fetching(`https://${window.ft_transcendence_host}/player/matches/`).then((data) => {
      const matches = data.matches;
      if (matches.length === 0) {
        this.textContent = "No matches found";
      }
      for (const match of matches) {
        const match_card_elem = document.createElement("match-card");
        match_card_elem.setAttribute("match", JSON.stringify(match));
        this.appendChild(match_card_elem);
      }
    });
  }
}

customElements.define("match-history", MatchHistory);
