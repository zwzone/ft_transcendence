import fetching from "../utilities/fetching.js";

export default class TwofaInput extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const template = document.getElementById("twofa-input");
    const component = template.content.cloneNode(true);
    this.appendChild(component);
    this.classList.add(
      "d-flex",
      "flex-column",
      "align-items-center",
      "justify-content-center",
      "gap-2",
    );

    const input = this.querySelector("input");
    const button = this.querySelector("button");

    button.addEventListener("click", (event) => {
      const code = this.querySelector("input").value;
      if (code.length === 6) {
        const query = new URLSearchParams(window.location.search);
        fetching(
          `https://${window.ft_transcendence_host}/authentication/2FA/verify/`,
          "POST",
          JSON.stringify({ id: query.get("id"), code: input.value }),
          { "Content-Type": "application/json" },
        ).then((res) => {
          if (res.statusCode === 200) {
            if (res.redirected)
              window.location.href = `https://${window.ft_transcendence_host}/home/`;
            else {
              const popup_twofa = document.querySelector(".popup-twofa");
              if (popup_twofa) {
                popup_twofa.removeChild(popup_twofa.lastChild);
                popup_twofa.style.display = "none";
              }
            }
          }
        });
      }
    });
  }
}

customElements.define("twofa-input", TwofaInput);
