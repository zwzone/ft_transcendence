import fetching from "../utilities/fetching.js";

const routes = {
  "/game/": "game-page",
  "/home/": "home-page",
  "/login/": "login-page",
  "/profile/": "profile-page",
  "/setting/": "setting-page",
  "/tournament/": "tournament-page",
};

const router = {
  init: () => {
    window.addEventListener("popstate", (event) => {
      router.go(event.state.route, "navigation");
    });
    // check if the player is logged in
    let pathname = window.location.pathname;
    if (pathname == "/") pathname = "/home/";
    fetching("https://localhost/authentication/isloggedin/").then((res) => {
      if (res.statusCode == 200) {
        if (pathname == "/login/") pathname = "/home/";
      } else {
        if (
          pathname == "/game/" ||
          pathname == "/home/" ||
          pathname == "/profile/" ||
          pathname == "/setting/" ||
          pathname == "/tournament/"
        )
          pathname = "/login/";
      }
      router.go(pathname, "replace");
    });
  },

  go: (route, state) => {
    if (state == "add" && window.location.pathname != route)
      history.pushState({ route }, "", route);
    if (state == "replace") history.replaceState({ route }, "", route);
    let pageElement;
    if (routes.hasOwnProperty(route)) {
      pageElement = document.createElement(routes[route]);
    } else {
      pageElement = document.createElement("notfound-page");
    }
    const rootEl = document.querySelector("div#root");
    rootEl.innerHTML = "";
    rootEl.appendChild(pageElement);
    window.scrollX = 0;
    window.scrollY = 0;
  },
};

export default router;
