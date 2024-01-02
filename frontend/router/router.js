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
      if (event.state) router.go(event.state.route);
    });
    router.go(location.pathname, "replace");
  },

  go: (route, state = "") => {
    console.log(`Going to ${route}`);
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
