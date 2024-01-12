export function runGame(canvas, ctx) {
  const ball = new Ball([2, 2], [canvas.width / 2, canvas.height / 2], 3);
  gameLoop(canvas, ctx, ball);
}

class Ball {
  constructor(speed, position, length) {
    this.speedX = speed[0];
    this.speedY = speed[1];
    this.positionX = position[0];
    this.positionY = position[1];
    this.length = length;
  }
  render(canvas, ctx) {
    ctx.fillStyle = "gray";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    ctx.arc(this.positionX, this.positionY, this.length, 0, 2 * Math.PI);
    ctx.fillStyle = "green";
    ctx.fill();
  }
  update() {
    this.positionX += this.speedX;
    this.positionY += this.speedY;
  }
}

function ballCollision(canvas, ctx, ball) {
  if (ball.positionX + ball.length >= canvas.width) {
    ball.speedX *= -1;
  }
  if (ball.positionY + ball.length >= canvas.height) {
    ball.speedY *= -1;
  }
  if (ball.positionX - ball.length <= 0) {
    ball.speedX *= -1;
  }
  if (ball.positionY - ball.length <= 0) {
    ball.speedY *= -1;
  }
}

function gameLoop(canvas, ctx, ball) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ballCollision(canvas, ctx, ball);
  ball.update();
  ball.render(canvas, ctx);
  window.requestAnimationFrame(() => gameLoop(canvas, ctx, ball));
}
