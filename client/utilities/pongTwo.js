let ws;
let alreadyInGame = false;

function setPlayerData(data) {
  const avatar_left = data["padd_left"]["avatar"];
  const avatar_right = data["padd_right"]["avatar"];
  const username_left = data["padd_left"]["username"];
  const username_right = data["padd_right"]["username"];
  const pong_players_elem = document.querySelector(".pong-players");
  let player_elem;
  player_elem = document.createElement("div");
  player_elem.style.display = "flex";
  player_elem.style.flexDirection = "column";
  player_elem.style.justifyContent = "center";
  player_elem.style.alignItems = "center";
  player_elem.innerHTML = `
    <img src="${avatar_left}" alt="avatar">
    <h1>${username_left}</h1>
  `;
  player_elem.querySelector("img").style.width = "100px";
  player_elem.querySelector("img").style.borderRadius = "50%";
  pong_players_elem.append(player_elem);
  player_elem = document.createElement("div");
  player_elem.style.display = "flex";
  player_elem.style.flexDirection = "column";
  player_elem.style.justifyContent = "center";
  player_elem.style.alignItems = "center";
  player_elem.innerHTML = `
    <img src="${avatar_right}" alt="avatar">
    <h1>${username_right}</h1>
  `;
  player_elem.querySelector("img").style.width = "100px";
  player_elem.querySelector("img").style.borderRadius = "50%";
  pong_players_elem.appendChild(player_elem);
}

export default function runPongTwoGame(canvas, ctx, match_id) {
  ws = new WebSocket(
    `wss://${window.ft_transcendence_host}/ws/matchmaking/2/${!match_id ? "" : match_id + "/"}`,
  );
  canvas.width = 1920;
  canvas.height = 1080;
  const ball = new Ball([canvas.width / 2, canvas.height / 2], 20);
  const paddle1 = new Paddle([60, canvas.height / 2 - 100], [40, 200]);
  const paddle2 = new Paddle([canvas.width - 100, canvas.height / 2 - 100], [40, 200]);
  ctx.fillStyle = "white";
  ctx.font = "100px monospace";
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
  ws.onmessage = function (e) {
    clearInterval(intervalId);
    if (e.data === "error") {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = "white";
      ctx.font = "100px monospace";
      ctx.textAlign = "center";
      ctx.fillText("ALREADY IN GAME", canvas.width / 2, canvas.height / 2);
      ws.close();
      return;
    }
    ws = new WebSocket(`wss://${window.ft_transcendence_host}/ws/pong/${e.data}/2/${!match_id ? "" : match_id + "/"}`);
    ws.onmessage = function (e) {
      let tmp = JSON.parse(e.data);
      if (!alreadyInGame) {
        setPlayerData(tmp);
        alreadyInGame = true;
      }
      if (typeof tmp === "string") {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillText(tmp, canvas.width / 2, canvas.height / 2);
        ws.close();
        return;
      }
      ball.positionX = tmp["ball"].positionX;
      ball.positionY = tmp["ball"].positionY;
      paddle1.positionY = tmp["padd_left"]["info"].positionY;
      paddle2.positionY = tmp["padd_right"]["info"].positionY;
      paddle1.score = tmp["padd_left"]["info"]["score"];
      paddle2.score = tmp["padd_right"]["info"]["score"];
      gameLoop(canvas, ctx, ball, paddle1, paddle2);
    };
  };
  window.addEventListener("keydown", function (e) {
    if (e.keyCode in keys && ws.readyState != WebSocket.CLOSED) ws.send(keys[e.keyCode]);
  });
  window.addEventListener("keydown", function (e) {
    if (["Space", "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].indexOf(e.code) > -1) {
      e.preventDefault();
    }
  });
}

export const keys = {
  38: "up",
  40: "down",
  87: "w",
  83: "s",
};


export  class Paddle {
  constructor(position, size) {
    this.positionX = position[0];
    this.positionY = position[1];
    this.sizeX = size[0];
    this.sizeY = size[1];
    this.score = 0;
  }

  render(ctx) {
    ctx.fillStyle = "whitesmoke";
    ctx.beginPath();
    ctx.roundRect(this.positionX, this.positionY, this.sizeX, this.sizeY, 20);
    ctx.stroke();
    ctx.fill();
  }
}

export class Ball {
  constructor(position, size) {
    this.positionX = position[0];
    this.positionY = position[1];
    this.size = size;
  }

  render(ctx) {
    ctx.beginPath();
    ctx.arc(this.positionX, this.positionY, this.size, 0, 2 * Math.PI);
    ctx.fillStyle = "white";
    ctx.fill();
  }
}

function RenderScore(ctx, canvas, right, left) {
  ctx.fillStyle = "white";
  ctx.font = "bold 60px Arial";
  ctx.fillText(left, canvas.width / 2 - 100, 120);
  ctx.fillText(right, canvas.width / 2 + 100, 120);
}

function gameLoop(canvas, ctx, ball, paddle1, paddle2) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ball.render(ctx);
  paddle1.render(ctx);
  paddle2.render(ctx);
  RenderScore(ctx, canvas, paddle2.score, paddle1.score);
}
