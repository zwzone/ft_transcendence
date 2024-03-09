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
        fetching(
          `https://${window.ft_transcendence_host}/authentication/2FA/verify/`,
          "POST",
          JSON.stringify({ code: input.value }),
          { "Content-Type": "application/json" },
        ).then((res) => {
          if (res.statusCode === 200) {
            input.value = "";
            if (res.redirected)
              window.location.href = `https://${window.ft_transcendence_host}/home/`;
            else {
              const popup_twofa = document.querySelector(".popup-twofa");
              const popup_twofa_qrcode = document.querySelector(".popup-twofa-qrcode");
              if (popup_twofa) {
                popup_twofa.removeChild(popup_twofa.lastChild);
                popup_twofa_qrcode.innerHTML = "";
                popup_twofa.style.display = "none";
              }
              alert(res.message);
            }
          } else {
            alert(res.message);
          }
        });
      } else {
        alert("Please enter a 6-digit code.");
      }
    });
  }
}

customElements.define("twofa-input", TwofaInput);
