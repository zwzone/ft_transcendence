// Router
import router from "./router/router.js";

// Components
import Navbar from "./components/Navbar.js";
import Footer from "./components/Footer.js";
import PlayCard from "./components/PlayCard.js";
import FriendsList from "./components/FriendsList.js";
import SearchList from "./components/SearchList.js";
import FriendCard from "./components/FriendCard.js";
import FriendCardPopup from "./components/FriendCardPopup.js";
import PlayerCard from "./components/PlayerCard.js";
import MatchCard from "./components/MatchCard.js";
import MatchHistory from "./components/MatchHistory.js";
import LoginButton from "./components/LoginButton.js";
import TwofaInput from "./components/TwofaInput.js";
import TournamentCard from "./components/TournamentCard.js";
import TournamentPlayers from "./components/TournamentPlayers.js";
import TournamentPopup from "./components/TournamentPopup.js";
import TournamentMatches from "./components/TournamentMatches.js";
import TournamentMatchCard from "./components/TournamentMatchCard.js";
import TournamentPlayerCard from "./components/TournamentPlayerCard.js";

// Pages
import GamePage from "./pages/GamePage.js";
import HomePage from "./pages/HomePage.js";
import LoginPage from "./pages/LoginPage.js";
import TwofaPage from "./pages/TwofaPage.js";
import ProfilePage from "./pages/ProfilePage.js";
import SettingPage from "./pages/SettingPage.js";
import TournamentPage from "./pages/TournamentPage.js";
import NotfoundPage from "./pages/NotfoundPage.js";

window.ft_transcendence_host = "localhost";

window.addEventListener("DOMContentLoaded", () => {
  router.init();
});
