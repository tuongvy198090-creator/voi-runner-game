
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Bò ơi, đứng lại!",
    page_icon="🐮",
    layout="wide"
)

st.title("🐮 BÒ ƠI, ĐỨNG LẠI!")
st.write("Chạy trốn nông dân và né chướng ngại vật nhé!")

game = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: #b8e994;
  text-align: center;
}
canvas {
  width: 100%;
  max-width: 800px;
  display: block;
  margin: auto;
  border: 3px solid #386641;
  border-radius: 12px;
  outline: none;
}
p { margin: 7px; color: #183b20; }
</style>
</head>
<body>
<p><b>← →</b> Đổi làn | <b>SPACE / ↑</b> Nhảy | <b>R</b> Chơi lại</p>
<canvas id="game" width="800" height="500" tabindex="0"></canvas>
<p id="status">Bấm vào màn hình game để bắt đầu!</p>

<script>
const c = document.getElementById("game");
const ctx = c.getContext("2d");
const statusText = document.getElementById("status");

let lane = 1;
let jump = 0;
let jumpSpeed = 0;
let obstacles = [];
let score = 0;
let speed = 3;
let frame = 0;
let over = false;
let started = false;

function reset() {
  lane = 1;
  jump = 0;
  jumpSpeed = 0;
  obstacles = [];
  score = 0;
  speed = 3;
  frame = 0;
  over = false;
  started = true;
  statusText.textContent = "Cố lên! Đừng để nông dân bắt được!";
}

function key(e) {
  if (["ArrowLeft","ArrowRight","ArrowUp"," "].includes(e.key)) {
    e.preventDefault();
  }
  if (!started || over) {
    if (e.key.toLowerCase() === "r" || e.key === " ") reset();
    return;
  }
  if (e.key === "ArrowLeft") lane = Math.max(0, lane - 1);
  if (e.key === "ArrowRight") lane = Math.min(2, lane + 1);
  if ((e.key === "ArrowUp" || e.key === " ") && jump === 0) {
    jumpSpeed = 13;
  }
}
document.addEventListener("keydown", key);
c.addEventListener("click", () => {
  c.focus();
  if (!started || over) reset();
});

function draw() {
  ctx.clearRect(0, 0, 800, 500);

  // Đồng quê
  ctx.fillStyle = "#a8d878";
  ctx.fillRect(0, 0, 800, 500);

  // Con đường ba làn
  ctx.fillStyle = "#c5a16b";
  ctx.beginPath();
  ctx.moveTo(245, 0);
  ctx.lineTo(555, 0);
  ctx.lineTo(760, 500);
  ctx.lineTo(40, 500);
  ctx.closePath();
  ctx.fill();

  // Vạch chia làn
  ctx.strokeStyle = "#fff0c2";
  ctx.lineWidth = 4;
  ctx.setLineDash([20, 20]);
  ctx.beginPath();
  ctx.moveTo(348, 0); ctx.lineTo(280, 500);
  ctx.moveTo(452, 0); ctx.lineTo(520, 500);
  ctx.stroke();
  ctx.setLineDash([]);

  // Cây và bụi cỏ hai bên
  for (let i = 0; i < 7; i++) {
    let y = (i * 85 + frame * speed * 0.8) % 560 - 40;
    ctx.font = "30px Arial";
    ctx.fillText("🌳", 70 + (i%2)*65, y);
    ctx.fillText("🌳", 635 + (i%2)*55, y);
  }

  // Nông dân phía sau
  ctx.font = "48px Arial";
  ctx.fillText("🧑‍🌾", 340, 455);
  ctx.fillText("🧑‍🌾", 415, 455);

  // Tạo vật cản
  if (frame % Math.max(28, 75 - Math.floor(speed*5)) === 0) {
    obstacles.push({
      lane: Math.floor(Math.random()*3),
      y: -30,
      type: Math.random() < 0.5 ? "🪵" : "🌾"
    });
  }

  // Di chuyển và vẽ vật cản
  for (let o of obstacles) {
    o.y += speed;
    let x = 300 + o.lane * 100;
    ctx.font = "40px Arial";
    ctx.fillText(o.type, x, o.y);

    if (o.lane === lane && o.y > 375 && o.y < 440 && jump < 30) {
      over = true;
      statusText.textContent =
        "Ôi! Bò va vào chướng ngại vật! Điểm: " +
        Math.floor(score) + " — Nhấn R để chơi lại.";
    }
  }
  obstacles = obstacles.filter(o => o.y < 540);

  // Nhảy
  if (jumpSpeed !== 0 || jump > 0) {
    jump += jumpSpeed;
    jumpSpeed -= 0.7;
    if (jump < 0) { jump = 0; jumpSpeed = 0; }
  }

  // Con bò
  let cowX = 300 + lane * 100;
  ctx.font = "60px Arial";
  ctx.fillText("🐮", cowX - 20, 410 - jump);

  // Điểm
  if (!over && started) {
    score += 0.12;
    speed = Math.min(8, 3 + score/40);
  }
  ctx.fillStyle = "#183b20";
  ctx.font = "bold 23px Arial";
  ctx.fillText("Điểm: " + Math.floor(score), 20, 35);

  if (!started) {
    ctx.fillStyle = "rgba(255,255,255,0.85)";
    ctx.fillRect(170, 180, 460, 100);
    ctx.fillStyle = "#183b20";
    ctx.font = "bold 27px Arial";
    ctx.fillText("🐮 BÒ ƠI, ĐỨNG LẠI!", 220, 220);
    ctx.font = "18px Arial";
    ctx.fillText("Bấm vào màn hình để bắt đầu", 240, 255);
  }

  if (over) {
    ctx.fillStyle = "rgba(0,0,0,0.55)";
    ctx.fillRect(180, 185, 440, 100);
    ctx.fillStyle = "white";
    ctx.font = "bold 28px Arial";
    ctx.fillText("GAME OVER!", 300, 225);
    ctx.font = "19px Arial";
    ctx.fillText("Nhấn R để chơi lại", 300, 260);
  }

  frame++;
  requestAnimationFrame(draw);
}
draw();
</script>
</body>
</html>
"""

components.html(game, height=560, scrolling=False)
