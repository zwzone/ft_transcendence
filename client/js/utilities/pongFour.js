import { Ball, Paddle, keys } from "./pongTwo.js";

export let wsFour;
let FourPressKey = true;

function setImage(pong_players_elem, avatar, username) {
  let player_elem = document.createElement("div");
  player_elem.style.display = "flex";
  player_elem.style.flexDirection = "column";
  player_elem.style.justifyContent = "center";
  player_elem.style.alignItems = "center";
  player_elem.innerHTML = `
    <img src="${avatar}" alt="avatar" referrerpolicy="no-referrer">
    <h1>${username}</h1>
  `;
  player_elem.querySelector("img").style.width = "100px";
  player_elem.querySelector("img").style.borderRadius = "50%";
  pong_players_elem.append(player_elem);
}

function setPlayerData(data) {
  const avatar_left = data["padd_left"]["avatar"];
  const avatar_right = data["padd_right"]["avatar"];
  const avatar_up = data["padd_up"]["avatar"];
  const avatar_down = data["padd_down"]["avatar"];
  const username_left = data["padd_left"]["username"];
  const username_right = data["padd_right"]["username"];
  const username_up = data["padd_up"]["username"];
  const username_down = data["padd_down"]["username"];
  const pong_players_elem = document.querySelector(".pong-players");
  setImage(pong_players_elem, avatar_left, username_left);
  setImage(pong_players_elem, avatar_right, username_right);
  setImage(pong_players_elem, avatar_up, username_up);
  setImage(pong_players_elem, avatar_down, username_down);
}

export function runPongFourGame(canvas, ctx) {
  canvas.width = 1300;
  canvas.height = 1300;
  wsFour = new WebSocket(`wss://${window.ft_transcendence_host}/ws/matchmaking/4/`);
  const ball = new Ball([canvas.width / 2, canvas.height / 2], 20);
  const paddle1 = new Paddle([60, canvas.height / 2 - 100], [40, 200]);
  const paddle2 = new Paddle([canvas.width - 100, canvas.height / 2 - 100], [40, 200]);
  const paddle3 = new Paddle([canvas.width / 2 - 100, 60], [200, 40]);
  const paddle4 = new Paddle([canvas.width / 2 - 100, canvas.height - 100], [200, 40]);
  ctx.fillStyle = "white";
  ctx.font = "50px monospace";
  ctx.textAlign = "center";
  let i = 0;
  const intervalId = setInterval(() => {
    i++;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillText(
      "MATCHING" + ".".repeat(i) + " ".repeat(3 - i),
      canvas.width / 2 + i,
      canvas.height / 2,
    );
    if (i === 3) i = 0;
  }, 500);
  wsFour.onmessage = function (e) {
    clearInterval(intervalId);
    if (e.data === "ALREADY IN GAME") {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillText(e.data, canvas.width / 2, canvas.height / 2);
      wsFour.close();
      return;
    }
    let alreadyInGame = false;
    wsFour = new WebSocket(`wss://${window.ft_transcendence_host}/ws/pong/${e.data}/4/`);
    let pos;
    wsFour.onmessage = function (e) {
      let tmp = JSON.parse(e.data);
      if (!alreadyInGame) {
        if (typeof tmp === "number") {
          pos = tmp;
          return;
        }
        setPlayerData(tmp);
        alreadyInGame = true;
      }
      if (typeof tmp === "string") {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "white";
        ctx.fillText(tmp, canvas.width / 2, canvas.height / 2);
        wsFour.close();
        return;
      }
      ball.positionX = tmp["ball"].positionX;
      ball.positionY = tmp["ball"].positionY;
      paddle1.positionY = tmp["padd_left"]["info"].positionY;
      paddle1.eliminated = tmp["padd_left"]["info"]["eliminated"];
      paddle2.positionY = tmp["padd_right"]["info"].positionY;
      paddle2.eliminated = tmp["padd_right"]["info"]["eliminated"];
      paddle3.positionX = tmp["padd_up"]["info"].positionX;
      paddle3.eliminated = tmp["padd_up"]["info"]["eliminated"];
      paddle4.positionX = tmp["padd_down"]["info"].positionX;
      paddle4.eliminated = tmp["padd_down"]["info"]["eliminated"];
      paddle1.score = tmp["padd_left"]["info"]["score"];
      paddle2.score = tmp["padd_right"]["info"]["score"];
      paddle3.score = tmp["padd_up"]["info"]["score"];
      paddle4.score = tmp["padd_down"]["info"]["score"];
      gameLoop(canvas, ctx, ball, paddle1, paddle2, paddle3, paddle4, pos);
    };
  };
  keys[65] = "a";
  keys[68] = "d";
  keys[37] = "left";
  keys[39] = "right";
  if (FourPressKey)
    window.addEventListener("keydown", function (e) {
      if (e.keyCode in keys && wsFour.readyState !== WebSocket.CLOSED) wsFour.send(keys[e.keyCode]);
    });
  FourPressKey = false;
}

function gameLoop(canvas, ctx, ball, paddle1, paddle2, paddle3, paddle4, pos) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ball.render(ctx);
  if (paddle1.eliminated === false) {
    if (pos === 1) paddle1.render(ctx, "#f8ec90");
    else paddle1.render(ctx);
  }
  if (paddle2.eliminated === false) {
    if (pos === 2) paddle2.render(ctx, "#f8ec90");
    else paddle2.render(ctx);
  }
  if (paddle3.eliminated === false) {
    if (pos === 3) paddle3.render(ctx, "#f8ec90");
    else paddle3.render(ctx);
  }
  if (paddle4.eliminated === false) {
    if (pos === 4) paddle4.render(ctx, "#f8ec90");
    else paddle4.render(ctx);
  }
}
