import fetching from "./fetching.js";
import { wsTwo } from "./pongTwo.js";
import { wsFour } from "./pongFour.js";

const routes = {
  "/game/": "game-page",
  "/tictactoe/": "tictactoe-page",
  "/home/": "home-page",
  "/login/": "login-page",
  "/twofa/": "twofa-page",
  "/profile/": "profile-page",
  "/setting/": "setting-page",
  "/tournaments/": "tournament-page",
};

const router = {
  init: () => {
    window.addEventListener("popstate", (event) => {
      if (wsTwo) wsTwo.close(1000);
      if (wsFour) wsFour.close(1000);
      router.go(event.state.route, event.state.query, "navigation");
    });
    // check if the player is logged in
    let pathname = window.location.pathname;
    pathname = pathname.split("/");
    pathname = pathname.filter((str) => str != "");
    pathname = "/" + pathname.join("/") + "/";
    if (pathname === "/" || pathname === "//") pathname = "/home/";
    const ws = new WebSocket(`wss://${window.ft_transcendence_host}/authentication/ws/login/`);
    ws.onmessage = (event) => {
      const message = event.data;
      if (message === "Valid") {
        if (pathname == "/login/" || pathname == "/twofa/") pathname = "/home/";
      } else if (message === "Twofa") {
        if (
          pathname == "/game/" ||
          pathname == "/tictactoe/" ||
          pathname == "/home/" ||
          pathname == "/login/" ||
          pathname == "/profile/" ||
          pathname == "/setting/" ||
          pathname == "/tournaments/"
        )
          pathname = "/twofa/";
      } else if (message === "Invalid") {
        if (
          pathname == "/game/" ||
          pathname == "/tictactoe/" ||
          pathname == "/home/" ||
          pathname == "/twofa/" ||
          pathname == "/profile/" ||
          pathname == "/setting/" ||
          pathname == "/tournaments/"
        )
          pathname = "/login/";
      }
      router.go(pathname, window.location.search, "replace");
    };
  },

  go: (route, query, state) => {
    if (state == "add" && window.location.pathname != route)
      history.pushState({ route, query }, "", route + query);
    else if (state == "replace") history.replaceState({ route, query }, "", route + query);
    let pageElement;
    if (routes.hasOwnProperty(route)) {
      pageElement = document.createElement(routes[route]);
    } else {
      pageElement = document.createElement("notfound-page");
    }
    const rootEl = document.querySelector("div#root");
    rootEl.innerHTML = "";
    rootEl.appendChild(document.createElement("stars-overlay"));
    rootEl.appendChild(pageElement);
    window.scrollX = 0;
    window.scrollY = 0;
  },
};

export default router;
