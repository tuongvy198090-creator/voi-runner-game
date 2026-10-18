
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Giải cứu thế giới",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

game_code = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    overflow: hidden;
    font-family: Arial, sans-serif;
    background: #102b20;
}

canvas {
    display: block;
    width: 100%;
    height: 100vh;
    touch-action: none;
}

#menu, #win {
    position: fixed;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    background: linear-gradient(#102d20e8, #07180df0);
    color: white;
    z-index: 5;
    padding: 20px;
}

#menu h1 {
    font-size: clamp(30px, 6vw, 56px);
    color: #b9ff87;
    text-shadow: 0 0 20px #48d65d;
    margin-bottom: 5px;
}

#menu p { font-size: 17px; }

input, select, button {
    font-size: 17px;
    padding: 12px 16px;
    border-radius: 12px;
    border: 0;
    margin: 7px;
}

button {
    background: #8ee45f;
    color: #15391a;
    font-weight: bold;
    cursor: pointer;
}

button:hover { background: #c2ff91; }

#hud {
    position: fixed;
    top: 12px;
    left: 12px;
    color: white;
    z-index: 2;
    font-weight: bold;
    background: #102b20d9;
    padding: 12px 15px;
    border-radius: 14px;
    line-height: 1.7;
}

#help {
    position: fixed;
    top: 12px;
    right: 12px;
    color: white;
    background: #102b20d9;
    border-radius: 12px;
    padding: 10px;
    z-index: 2;
    font-size: 13px;
    max-width: 200px;
}

#joystick {
    position: fixed;
    bottom: 24px;
    left: 24px;
    width: 130px;
    height: 130px;
    border: 3px solid #ffffffaa;
    background: #ffffff25;
    border-radius: 50%;
    z-index: 3;
    touch-action: none;
}

#knob {
    position: absolute;
    left: 36px;
    top: 36px;
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: #e6ffca;
    border: 3px solid #579d46;
    box-shadow: 0 0 15px #baff83;
    pointer-events: none;
}

#win { display: none; }

#win h1 {
    color: #baff83;
    font-size: clamp(27px, 5vw, 45px);
}

.small { font-size: 13px; opacity: .85; }

@media (max-width: 600px) {
    #joystick { width: 115px; height: 115px; }
    #knob { left: 29px; top: 29px; }
    #help { max-width: 145px; font-size: 11px; }
}
</style>
</head>

<body>
<canvas id="game"></canvas>

<div id="menu">
    <h1>🌍 GIẢI CỨU THẾ GIỚI 🌳</h1>
    <p>Khu rừng đang cần sự giúp đỡ của bạn!</p>
    <input id="playerName" placeholder="Nhập tên của bạn" maxlength="18">
    <select id="gender">
        <option value="boy">Nhân vật nam</option>
        <option value="girl">Nhân vật nữ</option>
    </select>
    <button id="startBtn">▶ BẮT ĐẦU</button>
    <p class="small">Thu thập 5 viên đá quý để hồi sinh cây cổ thụ.</p>
</div>

<div id="hud" style="display:none">
    🌟 Người chơi: <span id="nameLabel"></span><br>
    💎 Đá quý: <span id="gemsLabel">0</span>/5<br>
    🌳 Nhiệm vụ: Tìm cây cổ thụ
</div>

<div id="help" style="display:none">
    <b>CÁCH DI CHUYỂN</b><br>
    Máy tính: WASD hoặc phím mũi tên<br>
    Kéo nút tròn để di chuyển
</div>

<div id="joystick" style="display:none">
    <div id="knob"></div>
</div>

<div id="win">
    <h1>🌎 BẠN ĐÃ GIẢI CỨU THẾ GIỚI THÀNH CÔNG! 🌳</h1>
    <p id="winText"></p>
    <p>Khu rừng đã xanh tươi trở lại nhờ bạn!</p>
    <button id="againBtn">🔄 CHƠI LẠI</button>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let W = 0, H = 0;

function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
}
window.addEventListener("resize", resize);
resize();

let running = false;
let won = false;
let playerName = "";
let gender = "boy";
let px = 0;
let pz = 0;
let gems = 0;
let collected = new Set();
let keys = {};
let joyX = 0;
let joyY = 0;
let treeGreen = false;
let lastTime = 0;

// Vị trí 5 viên đá quý dọc theo đường đi
const gemPositions = [
    {x: -1.5, z: 12},
    {x:  1.5, z: 23},
    {x: -1.4, z: 34},
    {x:  1.5, z: 46},
    {x:  0.0, z: 58}
];

function rand(seed) {
    const x = Math.sin(seed * 127.1 + 311.7) * 43758.5453;
    return x - Math.floor(x);
}

// Đường cong cố định trong thế giới
function roadCurve(t) {
    return Math.sin(t * 2.5) * 0.95
         + Math.sin(t * 5.2) * 0.25;
}

// Tọa độ đường trên màn hình.
// Phần gần chân trời hẹp, phần gần người chơi rộng hơn.
function roadPoint(t) {
    const depth = Math.max(0, Math.min(1, t));
    return {
        x: W * 0.5 + roadCurve(depth) * W * 0.095,
        y: H * 0.43 + depth * depth * H * 0.63,
        half: W * (0.009 + depth * 0.105)
    };
}

function startGame() {
    playerName =
        document.getElementById("playerName").value.trim()
        || "Nhà thám hiểm";

    gender = document.getElementById("gender").value;
    px = 0;
    pz = 0;
    gems = 0;
    collected.clear();
    won = false;
    treeGreen = false;
    running = true;

    document.getElementById("menu").style.display = "none";
    document.getElementById("win").style.display = "none";
    document.getElementById("hud").style.display = "block";
    document.getElementById("help").style.display = "block";
    document.getElementById("joystick").style.display = "block";

    document.getElementById("nameLabel").textContent = playerName;
    updateHud();
}

document.getElementById("startBtn").addEventListener("click", startGame);

document.getElementById("againBtn").addEventListener("click", () => {
    running = false;
    document.getElementById("menu").style.display = "flex";
    document.getElementById("win").style.display = "none";
    document.getElementById("hud").style.display = "none";
    document.getElementById("help").style.display = "none";
    document.getElementById("joystick").style.display = "none";
});

function updateHud() {
    document.getElementById("gemsLabel").textContent = gems;
}

window.addEventListener("keydown", e => {
    const k = e.key.toLowerCase();

    if ([
        "arrowup", "arrowdown", "arrowleft", "arrowright", " "
    ].includes(k)) {
        e.preventDefault();
    }

    keys[k] = true;
});

window.addEventListener("keyup", e => {
    keys[e.key.toLowerCase()] = false;
});

window.addEventListener("blur", () => {
    keys = {};
});

// Joystick tròn
const joystick = document.getElementById("joystick");
const knob = document.getElementById("knob");
let joyActive = false;

function moveJoy(e) {
    const r = joystick.getBoundingClientRect();
    const cx = r.left + r.width / 2;
    const cy = r.top + r.height / 2;

    let dx = e.clientX - cx;
    let dy = e.clientY - cy;
    const max = r.width * 0.32;
    const len = Math.hypot(dx, dy);

    if (len > max) {
        dx = dx / len * max;
        dy = dy / len * max;
    }

    joyX = dx / max;
    joyY = dy / max;

    knob.style.left = (r.width / 2 - 26 + dx) + "px";
    knob.style.top = (r.height / 2 - 26 + dy) + "px";
}

joystick.addEventListener("pointerdown", e => {
    joyActive = true;
    joystick.setPointerCapture(e.pointerId);
    moveJoy(e);
});

joystick.addEventListener("pointermove", e => {
    if (joyActive) moveJoy(e);
});

function releaseJoy() {
    joyActive = false;
    joyX = 0;
    joyY = 0;

    const r = joystick.getBoundingClientRect();
    knob.style.left = (r.width / 2 - 26) + "px";
    knob.style.top = (r.height / 2 - 26) + "px";
}

joystick.addEventListener("pointerup", releaseJoy);
joystick.addEventListener("pointercancel", releaseJoy);

// Vẽ cảnh nền
function drawBackground() {
    const sky = ctx.createLinearGradient(0, 0, 0, H);
    sky.addColorStop(0, "#6eb9ce");
    sky.addColorStop(0.42, "#d0e9bb");
    sky.addColorStop(0.43, "#456d38");
    sky.addColorStop(1, "#142e1b");

    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, W, H);

    ctx.fillStyle = "#527f49";
    ctx.beginPath();
    ctx.moveTo(0, H * 0.47);

    for (let x = 0; x <= W; x += 40) {
        ctx.lineTo(x, H * 0.42 + Math.sin(x * 0.008) * H * 0.035);
    }

    ctx.lineTo(W, H);
    ctx.lineTo(0, H);
    ctx.fill();
}

// Vẽ con đường nhỏ, ngoằn ngoèo
function drawRoad() {
    ctx.fillStyle = "#8a7548";
    ctx.beginPath();

    for (let i = 0; i <= 80; i++) {
        const p = roadPoint(i / 80);

        if (i === 0) ctx.moveTo(p.x - p.half, p.y);
        else ctx.lineTo(p.x - p.half, p.y);
    }

    for (let i = 80; i >= 0; i--) {
        const p = roadPoint(i / 80);
        ctx.lineTo(p.x + p.half, p.y);
    }

    ctx.closePath();
    ctx.fill();

    ctx.strokeStyle = "#b99b64";
    ctx.lineWidth = 3;

    for (const side of [-1, 1]) {
        ctx.beginPath();

        for (let i = 0; i <= 80; i++) {
            const p = roadPoint(i / 80);
            const x = p.x + side * p.half;

            if (i === 0) ctx.moveTo(x, p.y);
            else ctx.lineTo(x, p.y);
        }

        ctx.stroke();
    }

    // Vạch giữa đường
    ctx.strokeStyle = "#e8d5a0";
    ctx.lineWidth = 2;
    ctx.setLineDash([10, 14]);
    ctx.lineDashOffset = -pz * 15;
    ctx.beginPath();

    for (let i = 0; i <= 80; i++) {
        const p = roadPoint(i / 80);

        if (i === 0) ctx.moveTo(p.x, p.y);
        else ctx.lineTo(p.x, p.y);
    }

    ctx.stroke();
    ctx.setLineDash([]);
}

// Rừng cây dày hai bên đường
function drawForest() {
    for (let i = 0; i < 55; i++) {
        let z = ((i * 4.1 - pz * 0.8) % 100 + 100) % 100;
        const depth = 1 - z / 100;
        const y = H * 0.43 + depth * depth * H * 0.63;

        const spread = W * (0.12 + depth * 0.47);

        for (const side of [-1, 1]) {
            const variation = (rand(i * 3 + side + 50) - 0.5) * W * 0.09;
            const x = W * 0.5 + side * spread + variation;
            const size = 12 + depth * 100;

            // Thân cây đặt trên mặt đất
            ctx.fillStyle = "#543b25";
            ctx.fillRect(
                x - size * 0.11,
                y - size * 0.56,
                size * 0.22,
                size * 0.56
            );

            // Tán cây
            ctx.fillStyle = [
                "#174e2c", "#226438", "#2d7136", "#386f30"
            ][i % 4];

            ctx.beginPath();
            ctx.arc(x, y - size * 0.65, size * 0.40, 0, Math.PI * 2);
            ctx.arc(x - size * 0.23, y - size * 0.53, size * 0.29, 0, Math.PI * 2);
            ctx.arc(x + size * 0.23, y - size * 0.53, size * 0.29, 0, Math.PI * 2);
            ctx.fill();
        }
    }
}

// Vẽ đá quý
function drawGems() {
    for (let i = 0; i < gemPositions.length; i++) {
        if (collected.has(i)) continue;

        const g = gemPositions[i];
        const dz = g.z - pz;

        if (dz < 1 || dz > 65) continue;

        const depth = 1 - dz / 65;
        const t = Math.max(0, Math.min(1, depth));
        const p = roadPoint(t);

        const x = p.x + (g.x - px) * W * (0.10 + depth * 0.12);
        const y = p.y - 7 - depth * 15;
        const r = 5 + depth * 16;

        ctx.save();
        ctx.translate(x, y);
        ctx.shadowBlur = 15;
        ctx.shadowColor = "#7ffaff";
        ctx.fillStyle = [
            "#56f5ff", "#ff6ee7", "#fff36b", "#a7a0ff", "#65ff9a"
        ][i];

        ctx.beginPath();
        ctx.moveTo(0, -r);
        ctx.lineTo(r * 0.7, -r * 0.2);
        ctx.lineTo(r * 0.5, r * 0.8);
        ctx.lineTo(0, r);
        ctx.lineTo(-r * 0.5, r * 0.8);
        ctx.lineTo(-r * 0.7, -r * 0.2);
        ctx.closePath();
        ctx.fill();
        ctx.restore();
    }
}

// Cây cổ thụ: tọa độ ngang và dọc cố định trong thế giới.
// Cây không bị kéo ngang theo nhân vật.
function drawAncientTree() {
    const treeZ = 76;
    const dz = treeZ - pz;

    if (dz < -3 || dz > 100) return;

    const depth = Math.max(0.08, 1 - dz / 100);
    const t = 0.76;
    const roadAtTree = roadPoint(t);

    // Cây luôn ở cùng vị trí tương đối với con đường.
    const x = roadAtTree.x;
    const y = roadAtTree.y;
    const size = 25 + depth * 165;

    // Thân cây
    ctx.fillStyle = "#47331f";
    ctx.fillRect(
        x - size * 0.10,
        y - size * 0.63,
        size * 0.20,
        size * 0.63
    );

    // Cành
    ctx.strokeStyle = "#47331f";
    ctx.lineWidth = Math.max(3, size * 0.09);
    ctx.beginPath();
    ctx.moveTo(x, y - size * 0.38);
    ctx.lineTo(x - size * 0.26, y - size * 0.59);
    ctx.moveTo(x, y - size * 0.44);
    ctx.lineTo(x + size * 0.25, y - size * 0.62);
    ctx.stroke();

    // Tán cây khô hoặc xanh sau khi hoàn thành nhiệm vụ
    ctx.fillStyle = treeGreen ? "#38dc58" : "#625d43";
    ctx.beginPath();
    ctx.arc(x, y - size * 0.70, size * 0.30, 0, Math.PI * 2);
    ctx.arc(x - size * 0.22, y - size * 0.60, size * 0.23, 0, Math.PI * 2);
    ctx.arc(x + size * 0.22, y - size * 0.60, size * 0.23, 0, Math.PI * 2);
    ctx.fill();

    if (treeGreen) {
        // Luồng sáng bay lên trời
        ctx.save();
        ctx.globalAlpha = 0.72;

        const beam = ctx.createLinearGradient(x, 0, x, y);
        beam.addColorStop(0, "#eaff9a00");
        beam.addColorStop(0.5, "#d7ff8b99");
        beam.addColorStop(1, "#eaff9a00");

        ctx.fillStyle = beam;
        ctx.beginPath();
        ctx.moveTo(x - size * 0.12, y - size * 0.85);
        ctx.lineTo(x + size * 0.12, y - size * 0.85);
        ctx.lineTo(x + size * 0.55, 0);
        ctx.lineTo(x - size * 0.55, 0);
        ctx.closePath();
        ctx.fill();
        ctx.restore();
    }

    if (dz < 25 && dz > 0) {
        ctx.fillStyle = "white";
        ctx.font = "bold 16px Arial";
        ctx.textAlign = "center";
        ctx.fillText(
            gems === 5 ? "CÂY CỔ THỤ" : "Hãy tìm đủ 5 viên đá!",
            x,
            y - size * 1.05
        );
    }
}

// Nhân vật nhìn từ phía sau
function drawPlayer() {
    const cx = W * 0.5;
    const footY = H * 0.83;

    ctx.fillStyle = "#07160b88";
    ctx.beginPath();
    ctx.ellipse(cx, footY + 4, 25, 9, 0, 0, Math.PI * 2);
    ctx.fill();

    const moving = running && !won &&
        (Math.abs(joyX) > 0.1 || Math.abs(joyY) > 0.1 ||
         keys["w"] || keys["a"] || keys["s"] || keys["d"] ||
         keys["arrowup"] || keys["arrowdown"] ||
         keys["arrowleft"] || keys["arrowright"]);

    const stride = moving ? Math.sin(performance.now() * 0.018) * 7 : 0;

    ctx.strokeStyle = "#202a35";
    ctx.lineWidth = 12;
    ctx.lineCap = "round";
    ctx.beginPath();
    ctx.moveTo(cx - 8, footY - 29);
    ctx.lineTo(cx - 10 - stride, footY - 4);
    ctx.moveTo(cx + 8, footY - 29);
    ctx.lineTo(cx + 10 + stride, footY - 4);
    ctx.stroke();

    ctx.fillStyle = gender === "girl" ? "#e95b9d" : "#3585e8";
    ctx.beginPath();
    ctx.roundRect(cx - 19, footY - 70, 38, 43, 10);
    ctx.fill();

    ctx.strokeStyle = gender === "girl" ? "#e95b9d" : "#3585e8";
    ctx.lineWidth = 10;
    ctx.beginPath();
    ctx.moveTo(cx - 17, footY - 62);
    ctx.lineTo(cx - 28, footY - 39);
    ctx.moveTo(cx + 17, footY - 62);
    ctx.lineTo(cx + 28, footY - 39);
    ctx.stroke();

    ctx.fillStyle = "#e9b98c";
    ctx.beginPath();
    ctx.arc(cx, footY - 82, 16, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = "#392719";
    ctx.beginPath();
    ctx.arc(cx, footY - 87, 17, Math.PI, Math.PI * 2);
    ctx.lineTo(cx + 16, footY - 79);
    ctx.lineTo(cx - 16, footY - 79);
    ctx.fill();

    if (gender === "girl") {
        ctx.fillStyle = "#392719";
        ctx.beginPath();
        ctx.arc(cx - 15, footY - 78, 6, 0, Math.PI * 2);
        ctx.arc(cx + 15, footY - 78, 6, 0, Math.PI * 2);
        ctx.fill();
    }
}

function update(dt) {
    if (!running || won) return;

    let dx = 0;
    let dz = 0;

    if (keys["arrowleft"] || keys["a"]) dx -= 1;
    if (keys["arrowright"] || keys["d"]) dx += 1;
    if (keys["arrowup"] || keys["w"]) dz += 1;
    if (keys["arrowdown"] || keys["s"]) dz -= 1;

    dx += joyX;
    dz += -joyY;

    const len = Math.hypot(dx, dz);
    if (len > 1) {
        dx /= len;
        dz /= len;
    }

    const speed = dt * 0.012;

    px = Math.max(-3.5, Math.min(3.5, px + dx * speed * 2.5));
    pz = Math.max(0, Math.min(80, pz + dz * speed * 4));

    for (let i = 0; i < gemPositions.length; i++) {
        if (collected.has(i)) continue;

        const g = gemPositions[i];

        if (Math.abs(g.z - pz) < 1.8 &&
            Math.abs(g.x - px) < 1.8) {
            collected.add(i);
            gems++;
            updateHud();
        }
    }

    if (pz >= 75 && gems === 5) {
        won = true;
        treeGreen = true;

        document.getElementById("winText").textContent =
            "Chúc mừng " + playerName +
            "! Bạn đã thu thập đủ 5 viên đá quý.";

        document.getElementById("win").style.display = "flex";
    }
}

function draw() {
    drawBackground();
    drawRoad();
    drawForest();
    drawGems();
    drawAncientTree();
    drawPlayer();
}

function frame(t) {
    const dt = Math.min(40, t - (lastTime || t));
    lastTime = t;

    update(dt);
    draw();

    requestAnimationFrame(frame);
}

requestAnimationFrame(frame);
</script>
</body>
</html>
"""

components.html(game_code, height=800, scrolling=False)
