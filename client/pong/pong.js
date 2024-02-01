let ws;

export function runGame(canvas, ctx) {
    console.log("waiting...");
    ws = new WebSocket("ws://127.0.0.1:8000/ws/matchemaking/2/");
    canvas.width = 1920;
    canvas.height = 1080;
    const ball = new Ball([10, 10], [canvas.width / 2, canvas.height / 2], 20);
    const paddle1 = new Paddle(15, [60, canvas.height / 2 - 100], [40, 200]);
    const paddle2 = new Paddle(
        15,
        [canvas.width - 100, canvas.height / 2 - 100],
        [40, 200],
    );
    ws.onmessage = function (e) {
        console.log(e.data);
        ws.close();
        ws = new WebSocket(`ws://127.0.0.1:9000/ws/pong/${e.data}/2/`);
        ws.onmessage = function (e) {
            let tmp = JSON.parse(e.data);
            ball.positionX = tmp["ball"].positionX;
            ball.positionY = tmp["ball"].positionY;
            paddle1.positionY = tmp["padd_left"]["info"].positionY;
            paddle2.positionY = tmp["padd_right"]["info"].positionY;
            gameLoop(canvas, ctx, ball, paddle1, paddle2);
        };
    };
}

const KeyPressed = [];
const keys = {
    38: "up",
    40: "down",
    87: "w",
    83: "s",
};
const KeyUP = 38;
const keydown = 40;
const keyW = 87;
const keyS = 83;

let left = 0;
let right = 0;

class Paddle {
    constructor(speed, position, size) {
        this.speedY = speed;
        this.positionX = position[0];
        this.positionY = position[1];
        this.sizeX = size[0];
        this.sizeY = size[1];
    }

    update(right) {
        if (!right) {
            if (KeyPressed[keydown]) {
                this.positionY += this.speedY;
            }
            if (KeyPressed[KeyUP]) {
                this.positionY -= this.speedY;
            }
        } else {
            if (KeyPressed[keyS]) {
                this.positionY += this.speedY;
            }
            if (KeyPressed[keyW]) {
                this.positionY -= this.speedY;
            }
        }
    }

    render(canvas, ctx) {
        canvas;
        ctx.fillStyle = "whitesmoke";
        ctx.fillRect(this.positionX, this.positionY, this.sizeX, this.sizeY);
    }

    Center() {
        return [this.positionX + this.sizeX / 2, this.positionY + this.sizeY / 2];
    }
}

class Ball {
    constructor(speed, position, size) {
        this.speedX = speed[0];
        this.speedY = speed[1];
        this.positionX = position[0];
        this.positionY = position[1];
        this.size = size;
    }

    render(canvas, ctx) {
        ctx.beginPath();
        ctx.arc(this.positionX, this.positionY, this.size, 0, 2 * Math.PI);
        ctx.fillStyle = "white";
        ctx.fill();
    }

    update() {
        this.positionX += this.speedX;
        this.positionY += this.speedY;
    }
}

window.addEventListener("keydown", function (e) {
    KeyPressed[e.keyCode] = true;
    if (e.keyCode in keys) ws.send(keys[e.keyCode]);
});

window.addEventListener("keyup", function (e) {
    KeyPressed[e.keyCode] = false;
});

function BallPaddleCollision(ball, paddle) {
    const dx = Math.abs(ball.positionX - paddle.Center()[0]);
    const dy = Math.abs(ball.positionY - paddle.Center()[1]);
    if (
        dx <= ball.size + paddle.sizeX / 2 &&
        dy <= ball.size + paddle.sizeY / 2
    ) {
        if (
            (ball.speedX > 0 && ball.positionX >= paddle.Center()[0]) ||
            (ball.speedX < 0 && ball.positionX <= paddle.Center()[0])
        ) {
            return;
        }
        ball.speedX *= -1;
    }
}

function paddleCollision(canvas, paddle) {
    if (paddle.positionY + paddle.sizeY >= canvas.height) {
        paddle.positionY = canvas.height - paddle.sizeY;
    }
    if (paddle.positionY <= 0) {
        paddle.positionY = 0;
    }
}

function ballCollision(canvas, ball) {
    if (
        ball.positionX + ball.size >= canvas.width ||
        ball.positionX - ball.size <= 0
    ) {
        reset(ball, canvas);
        return;
    }
    if (ball.positionY + ball.size >= canvas.height) {
        ball.speedY *= -1;
    }
    if (ball.positionY - ball.size <= 0) {
        ball.speedY *= -1;
    }
}

function reset(ball, canvas) {
    ball.positionX = canvas.width / 2;
    ball.positionY = canvas.height / 2;
    if (ball.speedX < 0) {
        left += 1;
    } else {
        right += 1;
    }
    if (Math.floor(Math.random() * 2)) ball.speedX = 10;
    else ball.speedX = -10;
    if (Math.floor(Math.random() * 2)) ball.speedY = 10;
    else ball.speedY = -10;
}

function Score(ctx, canvas, right, left) {
    ctx.fillStyle = "white";
    ctx.font = "bold 60px Arial";
    ctx.fillText(right, canvas.width / 2 - 100, 120);
    ctx.fillText(left, canvas.width / 2 + 100, 120);
}

function gameLoop(canvas, ctx, ball, paddle1, paddle2) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // window.requestAnimationFrame(() =>
    //   gameLoop(canvas, ctx, ball, paddle1, paddle2),
    // );
    // ball.update();
    // paddle1.update(true);
    // paddle2.update(false);
    // ballCollision(canvas, ball);
    // paddleCollision(canvas, paddle1);
    // paddleCollision(canvas, paddle2);
    // BallPaddleCollision(ball, paddle1);
    // BallPaddleCollision(ball, paddle2);
    ball.render(canvas, ctx);
    paddle1.render(canvas, ctx);
    paddle2.render(canvas, ctx);
    // Score(ctx, canvas, right, left);
    // if (ball.speedX > 0) ball.speedX += 0.01;
    // else ball.speedX -= 0.01;
    // if (ball.speedY > 0) ball.speedY += 0.01;
    // else ball.speedY -= 0.01;
}
