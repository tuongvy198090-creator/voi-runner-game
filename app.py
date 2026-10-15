
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Bò ơi, đứng lại!", page_icon="🐮")

st.title("🐮 BÒ ƠI, ĐỨNG LẠI!")
st.write("Giúp bò né đống rơm và chạy trốn những người nông dân!")

game = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
body {
  margin: 0;
  background: #b9df91;
  font-family: Arial;
  text-align: center;
}
canvas {
  width: 100%;
  max-width: 800px;
  display: block;
  margin: auto;
  border: 3px solid #436b32;
  border-radius: 12px;
  outline: none;
}
p { font-size: 15px; }
</style>
</head>
<body>
<p>← → Đổi làn &nbsp; | &nbsp; SPACE / ↑ Nhảy &nbsp; | &nbsp; R Chơi lại</p>
<canvas id="game" width="800" height="520" tabindex="0"></canvas>
<p id="msg">Bấm vào màn hình để bắt đầu!</p>

<script>
const c = document.getElementById("game");
const ctx = c.getContext("2d");
const msg = document.getElementById("msg");

let lane = 1, jump = 0, vy = 0;
let obstacles = [], score = 0, speed = 3, frame = 0;
let started = false, over = false;

function reset() {
  lane = 1; jump = 0; vy = 0;
  obstacles = []; score = 0; speed = 3; frame = 0;
  started = true; over = false;
  msg.textContent = "Chạy đi bò ơi!";
}

function key(e) {
  if (["ArrowLeft","ArrowRight","ArrowUp"," "].includes(e.key))
    e.preventDefault();

  if (!started || over) {
    if (e.key.toLowerCase() === "r" || e.key === " ") reset();
    return;
  }
  if (e.key === "ArrowLeft") lane = Math.max(0, lane - 1);
  if (e.key === "ArrowRight") lane = Math.min(2, lane + 1);
  if ((e.key === "ArrowUp" || e.key === " ") && jump === 0) vy = 13;
}
document.addEventListener("keydown", key);
c.addEventListener("click", () => {
  c.focus();
  if (!started || over) reset();
});

// Tâm của ba làn đường
function laneX(n, y) {
  const bottom = [160, 400, 640][n];
  return 400 + (bottom - 400) * (y / 520);
}

// Vẽ một người nông dân có đầu, thân, tay và chân
function farmer(x, y, s, phase) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(s, s);

  // Chân đang chạy
  const leg = Math.sin(phase) * 9;
  ctx.lineCap = "round";
  ctx.lineWidth = 6;
  ctx.strokeStyle = "#334b35";

  ctx.beginPath();
  ctx.moveTo(-5, -17);
  ctx.lineTo(-7 + leg, -2);
  ctx.moveTo(5, -17);
  ctx.lineTo(7 - leg, -2);
  ctx.stroke();

  // Thân áo
  ctx.fillStyle = "#3979c3";
  ctx.fillRect(-11, -39, 22, 24);

  // Hai tay
  ctx.strokeStyle = "#efbd91";
  ctx.lineWidth = 6;
  ctx.beginPath();
  ctx.moveTo(-10, -34);
  ctx.lineTo(-17 - leg * 0.4, -23);
  ctx.moveTo(10, -34);
  ctx.lineTo(17 + leg * 0.4, -23);
  ctx.stroke();

  // Đầu
  ctx.fillStyle = "#efbd91";
  ctx.beginPath();
  ctx.arc(0, -47, 10, 0, Math.PI * 2);
  ctx.fill();

  // Nón lá
  ctx.fillStyle = "#d8bd68";
  ctx.beginPath();
  ctx.ellipse(0, -56, 17, 5, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#e8d58c";
  ctx.beginPath();
  ctx.arc(0, -58, 8, Math.PI, 0);
  ctx.fill();

  ctx.restore();
}

// Vẽ con bò nhìn từ phía sau, có thân và bốn chân
function cow(x, y, s, phase) {
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(s, s);

  const leg = Math.sin(phase) * 10;
  ctx.lineCap = "round";

  // Đuôi
  ctx.strokeStyle = "#292929";
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(0, -46);
  ctx.quadraticCurveTo(22, -43, 15 + Math.sin(phase)*5, -28);
  ctx.stroke();

  // Bốn chân
  ctx.lineWidth = 8;
  ctx.strokeStyle = "#eee8da";
  ctx.beginPath();
  ctx.moveTo(-19, -25);
  ctx.lineTo(-21 + leg, -3);
  ctx.moveTo(-7, -25);
  ctx.lineTo(-7 - leg, -3);
  ctx.moveTo(7, -25);
  ctx.lineTo(7 + leg, -3);
  ctx.moveTo(19, -25);
  ctx.lineTo(21 - leg, -3);
  ctx.stroke();

  // Móng guốc
  ctx.strokeStyle = "#38312b";
  ctx.lineWidth = 7;
  ctx.beginPath();
  for (const xx of [-21 + leg, -7 - leg, 7 + leg, 21 - leg]) {
    ctx.moveTo(xx - 2, -3);
    ctx.lineTo(xx + 2, 0);
  }
  ctx.stroke();

  // Thân bò
  ctx.fillStyle = "#fffdf3";
  ctx.beginPath();
  ctx.ellipse(0, -36, 30, 24, 0, 0, Math.PI * 2);
  ctx.fill();

  // Những đốm đen trên thân
  ctx.fillStyle = "#292929";
  ctx.beginPath();
  ctx.ellipse(-17, -40, 9, 11, -0.4, 0, Math.PI * 2);
  ctx.ellipse(12, -45, 10, 7, 0.5, 0, Math.PI * 2);
  ctx.ellipse(15, -29, 7, 6, 0, 0, Math.PI * 2);
  ctx.fill();

  // Đầu bò và hai tai
  ctx.fillStyle = "#fffdf3";
  ctx.beginPath();
  ctx.ellipse(0, -56, 17, 15, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.beginPath();
  ctx.ellipse(-17, -56, 9, 4, -0.3, 0, Math.PI*2);
  ctx.ellipse(17, -56, 9, 4, 0.3, 0, Math.PI*2);
  ctx.fill();

  // Hai sừng nhỏ
  ctx.fillStyle = "#d7bd81";
  ctx.beginPath();
  ctx.moveTo(-10, -66);
  ctx.lineTo(-13, -76);
  ctx.lineTo(-5, -67);
  ctx.moveTo(10, -66);
  ctx.lineTo(13, -76);
  ctx.lineTo(5, -67);
  ctx.fill();

  // Đường viền và mặt phía sau đầu
  ctx.strokeStyle = "#b3a996";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.ellipse(0, -56, 17, 15, 0, 0, Math.PI*2);
  ctx.stroke();

  ctx.restore();
}


 // Vẽ đống rơm lớn
function hay(x, y, s = 1) {
  ctx.save();
  ctx.translate(x, y);

  // Tăng kích thước đống rơm
  ctx.scale(s * 1.8, s * 1.8);

  // Bóng dưới đống rơm
  ctx.fillStyle = "rgba(60, 40, 15, 0.3)";
  ctx.beginPath();
  ctx.ellipse(0, 2, 35, 10, 0, 0, Math.PI * 2);
  ctx.fill();

  // Thân đống rơm
  ctx.fillStyle = "#d99b26";
  ctx.beginPath();
  ctx.moveTo(-32, 0);
  ctx.lineTo(-30, -22);
  ctx.lineTo(-22, -38);
  ctx.lineTo(-10, -46);
  ctx.lineTo(12, -46);
  ctx.lineTo(27, -34);
  ctx.lineTo(32, -18);
  ctx.lineTo(32, 0);
  ctx.closePath();
  ctx.fill();

  // Phần rơm sáng trên đỉnh
  ctx.fillStyle = "#ffe078";
  ctx.beginPath();
  ctx.ellipse(0, -38, 22, 10, 0, Math.PI, Math.PI * 2);
  ctx.fill();

  // Các sợi rơm
  ctx.strokeStyle = "#b77a1e";
  ctx.lineWidth = 2;
  for (let i = -22; i <= 22; i += 8) {
    ctx.beginPath();
    ctx.moveTo(i, -27);
    ctx.lineTo(i + 3, -5);
    ctx.stroke();
  }

  ctx.restore();
}

function draw() {
  ctx.clearRect(0, 0, 800, 520);

  // Đồng cỏ
  ctx.fillStyle = "#a8d87e";
  ctx.fillRect(0, 0, 800, 520);

  // Đường làng
  ctx.fillStyle = "#c5a16b";
  ctx.beginPath();
  ctx.moveTo(245, 0);
  ctx.lineTo(555, 0);
  ctx.lineTo(800, 520);
  ctx.lineTo(0, 520);
  ctx.closePath();
  ctx.fill();

  // Vạch đường
  ctx.strokeStyle = "#fff0c2";
  ctx.lineWidth = 3;
  ctx.setLineDash([18, 18]);
  ctx.beginPath();
  ctx.moveTo(348, 0); ctx.lineTo(267, 520);
  ctx.moveTo(452, 0); ctx.lineTo(533, 520);
  ctx.stroke();
  ctx.setLineDash([]);

  // Cây hai bên đường
  for (let i = 0; i < 8; i++) {
    const y = (i * 85 + frame * speed * 0.65) % 560 - 20;
    const scale = 0.5 + y / 520 * 0.7;
    ctx.fillStyle = "#76502e";
    ctx.fillRect(90 + (i%2)*65, y, 9*scale, 28*scale);
    ctx.fillStyle = "#3d8b42";
    ctx.beginPath();
    ctx.arc(94 + (i%2)*65, y, 19*scale, 0, Math.PI*2);
    ctx.fill();

    ctx.fillStyle = "#76502e";
    ctx.fillRect(650 + (i%2)*55, y, 9*scale, 28*scale);
    ctx.fillStyle = "#3d8b42";
    ctx.beginPath();
    ctx.arc(654 + (i%2)*55, y, 19*scale, 0, Math.PI*2);
    ctx.fill();
  }

  // Nông dân đuổi theo phía sau bò
  farmer(365, 466, 0.95, frame * 0.22);
  farmer(430, 466, 0.95, frame * 0.22 + 2);

  // Sinh đống rơm
  if (started && !over &&
      frame % Math.max(38, 75 - Math.floor(speed*4)) === 0) {
    obstacles.push({
      lane: Math.floor(Math.random()*3),
      y: -15
    });
  }

  for (const o of obstacles) {
    o.y += speed;
    const x = laneX(o.lane, o.y);
    const s = 0.35 + o.y / 520 * 0.8;
    hay(x, o.y, s);

    // Kiểm tra bò va vào đống rơm
    if (started && !over && o.lane === lane &&
        o.y > 365 && o.y < 425 && jump < 25) {
      over = true;
      msg.textContent =
        "Bò bị vấp đống rơm! Điểm: " +
        Math.floor(score) + " — Nhấn R để chơi lại.";
    }
  }
  obstacles = obstacles.filter(o => o.y < 550);

  // Hoạt ảnh nhảy
  if (vy !== 0 || jump > 0) {
    jump += vy;
    vy -= 0.7;
    if (jump < 0) { jump = 0; vy = 0; }
  }

  // Bò chạy ở phía trước
  cow(laneX(lane, 405), 420 - jump, 1.15, frame * 0.35);

  // Điểm và tốc độ
  if (started && !over) {
    score += 0.12;
    speed = Math.min(7, 3 + score/50);
  }

  ctx.fillStyle = "#183b20";
  ctx.font = "bold 23px Arial";
  ctx.fillText("Điểm: " + Math.floor(score), 20, 35);

  if (!started) {
    ctx.fillStyle = "rgba(255,255,255,0.88)";
    ctx.fillRect(160, 180, 480, 110);
    ctx.fillStyle = "#183b20";
    ctx.font = "bold 28px Arial";
    ctx.fillText("BO OI, DUNG LAI!", 270, 222);
    ctx.font = "19px Arial";
    ctx.fillText("Bấm vào màn hình để bắt đầu", 240, 260);
  }

  if (over) {
    ctx.fillStyle = "rgba(0,0,0,0.6)";
    ctx.fillRect(190, 190, 420, 105);
    ctx.fillStyle = "white";
    ctx.font = "bold 30px Arial";
    ctx.fillText("GAME OVER!", 300, 233);
    ctx.font = "20px Arial";
    ctx.fillText("Nhấn R để chơi lại", 300, 270);
  }

  frame++;
  requestAnimationFrame(draw);
}
draw();
</script>
</body>
</html>
"""

components.html(game, height=610, scrolling=False)
