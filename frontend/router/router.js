const routes = {
  "/": "home-page",
  "/game": "game-page",
  "/home": "home-page",
  "/login": "login-page",
  "/profile": "profile-page",
  "/setting": "setting-page",
  "/tournament": "tournament-page",
};

const router = {
  init: () => {
    window.addEventListener("popstate", (event) => {
      router.go(event.state.route);
    });
    // check if the player is logged in
    const xfetch = new XMLHttpRequest();
    xfetch.open("GET", "http://localhost:8000/auth/islogged");
    xfetch.withCredentials = true;
    xfetch.responseType = "json";
    xfetch.send();
    if (xfetch.statusCode == 401 || xfetch.statusCode == 403) {
      location.pathname = "/login";
    } else if (xfetch.statusCode == 200) {
      if (location.pathname == "/login") location.pathname = "/home";
    }
    router.go(location.pathname, "replace");
  },

  go: (route, state = "") => {
    if (state == "add") history.pushState({ route }, "", route);
    if (state == "replace") history.replaceState({ route }, "", route);
    let pageElement;
    if (Object.hasOwn(routes, route)) {
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
