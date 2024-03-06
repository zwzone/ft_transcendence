import fetching from "../utilities/fetching.js";

const routes = {
  "/game/": "game-page",
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
      router.go(event.state.route, "navigation");
    });
    // check if the player is logged in
    let pathname = window.location.pathname;
    pathname = pathname.split("/");
    pathname = pathname.filter((str) => str != "");
    pathname = "/" + pathname.join("/") + "/";
    if (pathname === "/" || pathname === "//") pathname = "/home/";
    fetching(`https://${window.ft_transcendence_host}/authentication/isloggedin/`).then((res) => {
      if (res.statusCode == 200) {
        if (pathname == "/login/" || pathname == "/twofa/") pathname = "/home/";
      } else if (res.error.startsWith("2FA")) {
        if (
          pathname == "/game/" ||
          pathname == "/home/" ||
          pathname == "/login/" ||
          pathname == "/profile/" ||
          pathname == "/setting/" ||
          pathname == "/tournaments/"
        )
          pathname = "/twofa/";
      } else {
        if (
          pathname == "/game/" ||
          pathname == "/home/" ||
          pathname == "/twofa/" ||
          pathname == "/profile/" ||
          pathname == "/setting/" ||
          pathname == "/tournaments/"
        )
          pathname = "/login/";
      }
      router.go(pathname, "replace");
    });
  },

  go: (route, state) => {
    if (state == "add" && window.location.pathname != route)
      history.pushState({ route: route + window.location.search }, "", route + window.location.search);
    else if (state == "replace") history.replaceState({ route: route + window.location.search }, "", route + window.location.search);
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
