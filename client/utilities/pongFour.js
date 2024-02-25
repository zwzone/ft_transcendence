import {Ball, Paddle, keys} from "./pongTwo.js";

let ws;

export default function runPongFourGame(canvas, ctx) {
  canvas.width = 1300;
  canvas.height = 1300;
  ws = new WebSocket(`wss://${window.ft_transcendence_host}/ws/matchmaking/4/`);
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
  ws.onmessage = function (e) {
    clearInterval(intervalId);
    if (e.data === "error") {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillText("ALREADY IN GAME", canvas.width / 2, canvas.height / 2);
      ws.close();
      return;
    }
    ws = new WebSocket(`wss://${window.ft_transcendence_host}/ws/pong/${e.data}/4/`);
    ws.onmessage = function (e) {
      let tmp = JSON.parse(e.data);
      ball.positionX = tmp["ball"].positionX;
      ball.positionY = tmp["ball"].positionY;
      paddle1.positionY = tmp["padd_left"]["info"].positionY;
      paddle2.positionY = tmp["padd_right"]["info"].positionY;
      paddle3.positionX = tmp["padd_up"]["info"].positionX;
      paddle4.positionX = tmp["padd_down"]["info"].positionX;
      paddle1.score = tmp["padd_left"]["info"]["score"];
      paddle2.score = tmp["padd_right"]["info"]["score"];
      paddle3.score = tmp["padd_up"]["info"]["score"];
      paddle4.score = tmp["padd_down"]["info"]["score"];
      gameLoop(canvas, ctx, ball, paddle1, paddle2, paddle3, paddle4);
    };
  }
  keys[65] = 'a';
  keys[68] = 'd';
  keys[37] = 'left';
  keys[39] = 'right';
  window.addEventListener("keydown", function (e) {
    if (e.keyCode in keys) ws.send(keys[e.keyCode]);
  });
  window.addEventListener("keydown", function(e) {
    if(["Space","ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].indexOf(e.code) > -1) {
        e.preventDefault();
    }
  });
}

function gameLoop(canvas, ctx, ball, paddle1, paddle2, paddle3, paddle4) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ball.render(ctx);
    paddle1.render(ctx);
    paddle2.render(ctx);
    paddle3.render(ctx);
    paddle4.render(ctx);
}
