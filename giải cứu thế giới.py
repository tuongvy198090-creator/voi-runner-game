
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
<html>
<head>
<meta charset="UTF-8">
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
    background: linear-gradient(#102d20dd, #07180ddd);
    color: white;
    z-index: 5;
    padding: 20px;
}
#menu h1 {
    font-size: clamp(30px, 6vw, 58px);
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
    background: #102b20c9;
    padding: 12px 15px;
    border-radius: 14px;
    line-height: 1.7;
}
#help {
    position: fixed;
    top: 12px;
    right: 12px;
    color: white;
    background: #102b20c9;
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
#win h1 { color: #baff83; font-size: clamp(27px, 5vw, 48px); }
.small { font-size: 13px; opacity: .85; }
@media (max-width: 600px) {
    #joystick { width: 115px; height: 115px; }
    #knob { left: 31px; top: 31px; }
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
    Điện thoại: kéo nút tròn bên trái
</div>
<div id="joystick" style="display:none"><div id="knob"></div></div>

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
let px = 0, pz = 0;
let gems = 0;
let collected = new Set();
let keys = {};
let joyX = 0, joyY = 0;
let treeGreen = false;
let lastTime = 0;

const gemPositions = [
    {x:-2.2,z:13}, {x:2.0,z:24}, {x:-1.5,z:36},
    {x:2.4,z:49}, {x:0,z:62}
];

function rand(seed) {
    let x = Math.sin(seed * 127.1 + 311.7) * 43758.5453;
    return x - Math.floor(x);
}

function startGame() {
    playerName = document.getElementById("playerName").value.trim() || "Nhà thám hiểm";
    gender = document.getElementById("gender").value;
    px = 0; pz = 0; gems = 0; collected.clear();
    won = false; treeGreen = false; running = true;
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
    document.getElementById("menu").style.display = "flex";
    document.getElementById("win").style.display = "none";
    document.getElementById("hud").style.display = "none";
    document.getElementById("help").style.display = "none";
    document.getElementById("joystick").style.display = "none";
    running = false;
});

function updateHud() {
    document.getElementById("gemsLabel").textContent = gems;
}

window.addEventListener("keydown", e => {
    const k = e.key.toLowerCase();
    if (["arrowup","arrowdown","arrowleft","arrowright"," "].includes(k)) e.preventDefault();
    keys[k] = true;
});
window.addEventListener("keyup", e => keys[e.key.toLowerCase()] = false);
window.addEventListener("blur", () => keys = {});

const joystick = document.getElementById("joystick");
const knob = document.getElementById("knob");
let joyActive = false;
function moveJoy(e) {
    const r = joystick.getBoundingClientRect();
    const cx = r.left + r.width/2, cy = r.top + r.height/2;
    let dx = e.clientX - cx, dy = e.clientY - cy;
    const max = r.width * .32;
    const len = Math.hypot(dx,dy);
    if (len > max) { dx = dx/len*max; dy = dy/len*max; }
    joyX = dx/max; joyY = dy/max;
    knob.style.left = (r.width/2 - 26 + dx) + "px";
    knob.style.top = (r.height/2 - 26 + dy) + "px";
}
joystick.addEventListener("pointerdown", e => {
    joyActive = true;
    joystick.setPointerCapture(e.pointerId);
    moveJoy(e);
});
joystick.addEventListener("pointermove", e => { if(joyActive) moveJoy(e); });
function releaseJoy() {
    joyActive = false; joyX = 0; joyY = 0;
    const r = joystick.getBoundingClientRect();
    knob.style.left = (r.width/2 - 26) + "px";
    knob.style.top = (r.height/2 - 26) + "px";
}
joystick.addEventListener("pointerup", releaseJoy);
joystick.addEventListener("pointercancel", releaseJoy);

function roundedRect(x,y,w,h,r,color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.roundRect(x,y,w,h,r);
    ctx.fill();
}

// Draws a third-person forest scene. Forward progress changes only when moving.
function draw() {
    const sky = ctx.createLinearGradient(0,0,0,H);
    sky.addColorStop(0, "#6eb9ce");
    sky.addColorStop(.42, "#d0e9bb");
    sky.addColorStop(.43, "#456d38");
    sky.addColorStop(1, "#142e1b");
    ctx.fillStyle = sky;
    ctx.fillRect(0,0,W,H);

    // Distant hills
    ctx.fillStyle = "#527f49";
    ctx.beginPath();
    ctx.moveTo(0,H*.47);
    for(let x=0;x<=W;x+=40)
        ctx.lineTo(x,H*.42 + Math.sin(x*.008)*H*.035);
    ctx.lineTo(W,H); ctx.lineTo(0,H); ctx.fill();

    // Perspective path
    const horizon = H*.43;
    ctx.fillStyle = "#8a7548";
    ctx.beginPath();
    ctx.moveTo(W*.47,horizon);
    ctx.lineTo(W*.53,horizon);
    ctx.lineTo(W*.91,H);
    ctx.lineTo(W*.09,H);
    ctx.closePath(); ctx.fill();

    // Path edge
    ctx.strokeStyle = "#c0a36a";
    ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.moveTo(W*.47,horizon); ctx.lineTo(W*.09,H);
    ctx.moveTo(W*.53,horizon); ctx.lineTo(W*.91,H);
    ctx.stroke();

    // Dashed path markers scroll as player moves
    ctx.strokeStyle = "#e8d5a0";
    ctx.lineWidth = 3;
    ctx.setLineDash([14,16]);
    ctx.lineDashOffset = -pz*15;
    ctx.beginPath();
    ctx.moveTo(W*.5,horizon);
    ctx.lineTo(W*.5,H);
    ctx.stroke();
    ctx.setLineDash([]);

    // Trees are planted along both sides of the path.
    // Their base stays on the ground; only perspective changes with distance.
    for(let i=0;i<44;i++) {
        let z = ((i*4.3 - pz*.8) % 100 + 100) % 100;
        let depth = 1 - z/100;
        let y = horizon + depth*depth*(H*.63);
        let spread = W*(.07 + depth*.47);
        for(let side of [-1,1]) {
            let variation = (rand(i*3+side+50)-.5)*W*.10;
            let x = W*.5 + side*spread + variation;
            let size = 12 + depth*100;
            // Trunk
            ctx.fillStyle = "#543b25";
            ctx.fillRect(x-size*.11, y-size*.6, size*.22, size*.6);
            // Foliage
            ctx.fillStyle = ["#174e2c","#226438","#2d7136","#386f30"][i%4];
            ctx.beginPath();
            ctx.arc(x, y-size*.68, size*.42, 0, Math.PI*2);
            ctx.arc(x-size*.24, y-size*.53, size*.30, 0, Math.PI*2);
            ctx.arc(x+size*.24, y-size*.53, size*.30, 0, Math.PI*2);
            ctx.fill();
        }
    }

    // Gem sprites on the path, getting larger as they approach.
    for(let i=0;i<gemPositions.length;i++) {
        if(collected.has(i)) continue;
        const g = gemPositions[i];
        const dz = g.z - pz;
        if(dz < 1 || dz > 65) continue;
        const depth = 1 - dz/65;
        const y = horizon + depth*depth*(H*.60);
        const curve = Math.sin(g.z*.15)*W*.035;
        const x = W*.5 + (g.x-px)*W*(.12 + depth*.35) + curve;
        const r = 5 + depth*18;
        ctx.save();
        ctx.translate(x,y-r);
        ctx.shadowBlur = 16; ctx.shadowColor = "#7ffaff";
        ctx.fillStyle = ["#56f5ff","#ff6ee7","#fff36b","#a7a0ff","#65ff9a"][i];
        ctx.beginPath();
        ctx.moveTo(0,-r); ctx.lineTo(r*.7,-r*.2);
        ctx.lineTo(r*.5,r*.8); ctx.lineTo(0,r);
        ctx.lineTo(-r*.5,r*.8); ctx.lineTo(-r*.7,-r*.2);
        ctx.closePath(); ctx.fill();
        ctx.restore();
    }

    // Ancient tree appears at the end of the trail.
    const treeZ = 76;
    const dz = treeZ-pz;
    if(dz > -3 && dz < 100) {
        const depth = Math.max(.08,1-dz/100);
        const x = W*.5 - px*W*.14;
        const y = horizon + depth*depth*(H*.57);
        const size = 30 + depth*190;
        ctx.fillStyle = "#47331f";
        ctx.fillRect(x-size*.11,y-size*.65,size*.22,size*.65);
        ctx.fillStyle = treeGreen ? "#4df06a" : "#5b5a43";
        ctx.beginPath();
        ctx.arc(x,y-size*.75,size*.32,0,Math.PI*2);
        ctx.arc(x-size*.22,y-size*.62,size*.25,0,Math.PI*2);
        ctx.arc(x+size*.22,y-size*.62,size*.25,0,Math.PI*2);
        ctx.fill();
        if(treeGreen) {
            ctx.save();
            ctx.globalAlpha = .8;
            const beam = ctx.createLinearGradient(x,0,x,H*.8);
            beam.addColorStop(0,"#eaff9a00");
            beam.addColorStop(.5,"#d7ff8b88");
            beam.addColorStop(1,"#eaff9a00");
            ctx.fillStyle = beam;
            ctx.beginPath();
            ctx.moveTo(x-size*.16,y-size*.9);
            ctx.lineTo(x+size*.16,y-size*.9);
            ctx.lineTo(x+size*.7,0);
            ctx.lineTo(x-size*.7,0);
            ctx.closePath(); ctx.fill();
            ctx.restore();
        }
        if(dz < 24 && dz > 0) {
            ctx.fillStyle = "white";
            ctx.font = "bold 16px Arial";
            ctx.textAlign = "center";
            ctx.fillText(gems===5 ? "CÂY CỔ THỤ" : "Hãy tìm đủ 5 viên đá!", x, y-size*.98);
        }
    }

    // Main character, always anchored near the bottom center.
    const cx = W*.5, footY = H*.83;
    // Shadow
    ctx.fillStyle = "#07160b88";
    ctx.beginPath(); ctx.ellipse(cx,footY+4,25,9,0,0,Math.PI*2); ctx.fill();

    // Legs
    const stride = running && !won ? Math.sin(performance.now()*.018)*7 : 0;
    ctx.strokeStyle = "#202a35"; ctx.lineWidth = 12; ctx.lineCap = "round";
    ctx.beginPath();
    ctx.moveTo(cx-8,footY-29); ctx.lineTo(cx-10-stride,footY-4);
    ctx.moveTo(cx+8,footY-29); ctx.lineTo(cx+10+stride,footY-4);
    ctx.stroke();

    // Body
    ctx.fillStyle = gender==="girl" ? "#e95b9d" : "#3585e8";
    ctx.beginPath();
    ctx.roundRect(cx-19,footY-70,38,43,10); ctx.fill();

    // Arms
    ctx.strokeStyle = gender==="girl" ? "#e95b9d" : "#3585e8";
    ctx.lineWidth = 10;
    ctx.beginPath();
    ctx.moveTo(cx-17,footY-62); ctx.lineTo(cx-28,footY-39);
    ctx.moveTo(cx+17,footY-62); ctx.lineTo(cx+28,footY-39);
    ctx.stroke();

    // Head, viewed from behind
    ctx.fillStyle = "#e9b98c";
    ctx.beginPath(); ctx.arc(cx,footY-82,16,0,Math.PI*2); ctx.fill();
    ctx.fillStyle = "#392719";
    ctx.beginPath();
    ctx.arc(cx,footY-87,17,Math.PI,Math.PI*2);
    ctx.lineTo(cx+16,footY-79); ctx.lineTo(cx-16,footY-79);
    ctx.fill();
    if(gender==="girl") {
        ctx.fillStyle="#392719";
        ctx.beginPath(); ctx.arc(cx-15,footY-78,6,0,Math.PI*2); ctx.fill();
        ctx.beginPath(); ctx.arc(cx+15,footY-78,6,0,Math.PI*2); ctx.fill();
    }
}

function update(dt) {
    if(!running || won) return;
    let dx = 0, dz = 0;
    if(keys["arrowleft"] || keys["a"]) dx -= 1;
    if(keys["arrowright"] || keys["d"]) dx += 1;
    if(keys["arrowup"] || keys["w"]) dz += 1;
    if(keys["arrowdown"] || keys["s"]) dz -= 1;
    dx += joyX;
    dz += -joyY;
    const len = Math.hypot(dx,dz);
    if(len > 1) { dx/=len; dz/=len; }
    const speed = dt * 0.012;
    px = Math.max(-3.5, Math.min(3.5, px + dx*speed*2.5));
    pz = Math.max(0, Math.min(80, pz + dz*speed*4));

    for(let i=0;i<gemPositions.length;i++) {
        if(collected.has(i)) continue;
        const g = gemPositions[i];
        if(Math.abs(g.z-pz)<1.6 && Math.abs(g.x-px)<1.6) {
            collected.add(i); gems++; updateHud();
        }
    }
    if(pz >= 75 && gems === 5) {
        won = true; treeGreen = true;
        document.getElementById("winText").textContent =
            "Chúc mừng " + playerName + "! Bạn đã thu thập đủ 5 viên đá quý.";
        document.getElementById("win").style.display = "flex";
    }
}

function frame(t) {
    const dt = Math.min(40, t-(lastTime||t));
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
vvv
