
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="GIẢI CỨU THẾ GIỚI",
    page_icon="🌳",
    layout="wide"
)

game = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    background: #102719;
    font-family: Arial, sans-serif;
    color: white;
}
#game {
    position: relative;
    width: 100%;
    max-width: 1200px;
    margin: auto;
    overflow: hidden;
}
canvas {
    width: 100%;
    display: block;
    background: #203e27;
}
.panel {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #06170dcc;
    padding: 12px;
    z-index: 5;
}
.card {
    width: min(480px, 96%);
    padding: 22px;
    text-align: center;
    background: linear-gradient(145deg,#355d36,#10291c);
    border: 3px solid #b7dc85;
    border-radius: 20px;
    box-shadow: 0 8px 30px #0008;
}
h1 {
    color: #e2ffad;
    font-size: clamp(23px,4vw,34px);
    margin: 8px 0;
}
p { line-height: 1.5; }
input, select, button {
    width: 100%;
    font-size: 16px;
    padding: 12px;
    border-radius: 10px;
    border: none;
    margin-top: 8px;
}
button {
    background: #d4f69a;
    color: #17351d;
    font-weight: bold;
    cursor: pointer;
}
button:hover { background: #f0ffd0; }
#hud {
    position: absolute;
    top: 10px;
    left: 10px;
    right: 10px;
    display: flex;
    justify-content: space-between;
    gap: 8px;
    pointer-events: none;
}
.tag {
    background: #102719e8;
    border: 2px solid #c5e99b;
    border-radius: 12px;
    padding: 10px;
    font-weight: bold;
}
#controls {
    position: absolute;
    bottom: 12px;
    left: 12px;
    display: grid;
    grid-template-columns: 48px 48px 48px;
    grid-template-rows: 44px 44px;
    gap: 4px;
}
#controls button {
    margin: 0;
    padding: 4px;
    font-size: 22px;
    background: #153b2bdc;
    border: 1px solid #e0ffc0;
    color: white;
    touch-action: none;
}
#up { grid-column: 2; grid-row: 1; }
#left { grid-column: 1; grid-row: 2; }
#down { grid-column: 2; grid-row: 2; }
#right { grid-column: 3; grid-row: 2; }
#hint {
    position: absolute;
    right: 12px;
    bottom: 14px;
    background: #102719e8;
    border-radius: 10px;
    padding: 10px;
    font-size: 12px;
    max-width: 48%;
}
</style>
</head>
<body>
<div id="game">
<canvas id="canvas" width="1000" height="650"></canvas>

<div id="hud" style="display:none">
    <div class="tag" id="nameTag">Nhà thám hiểm</div>
    <div class="tag" id="gemTag">💎 Ngọc: 0/5</div>
</div>

<div id="controls" style="display:none">
    <button id="up">▲</button>
    <button id="left">◀</button>
    <button id="down">▼</button>
    <button id="right">▶</button>
</div>
<div id="hint" style="display:none">
    W A S D hoặc phím mũi tên để di chuyển
</div>

<div class="panel" id="start">
    <div class="card">
        <div style="font-size:38px">🌿 🌳 🌲</div>
        <h1>CHÀO MỪNG BẠN ĐẾN VỚI TRÒ CHƠI</h1>
        <h1>GIẢI CỨU THẾ GIỚI</h1>
        <p>Khu rừng đang héo úa! Hãy thu thập 5 viên ngọc để đánh thức Cây Cổ Thụ.</p>
        <input id="playerName" maxlength="18" placeholder="Nhập tên nhân vật">
        <p><b>CHỌN NHÂN VẬT</b></p>
        <select id="gender">
            <option value="girl">Nhân vật nữ</option>
            <option value="boy">Nhân vật nam</option>
        </select>
        <button onclick="startGame()">▶ BẮT ĐẦU</button>
        <p style="font-size:12px">Khám phá khu rừng và giải cứu thế giới!</p>
    </div>
</div>

<div class="panel" id="win" style="display:none">
    <div class="card">
        <div style="font-size:60px">🌳 ✨ 🌎</div>
        <h1>BẠN ĐÃ GIẢI CỨU THẾ GIỚI THÀNH CÔNG!</h1>
        <p>Khu rừng đã hồi sinh nhờ bạn!</p>
        <button onclick="restartGame()">CHƠI LẠI</button>
    </div>
</div>
</div>

<script>
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const W = canvas.width, H = canvas.height;
const WORLD = 3200;
let playerName = "Nhà thám hiểm";
let gender = "girl";
let running = false, won = false;
let collected = 0, victoryStarted = false;
let player = {x:1600, y:1600, speed:5};
const ancient = {x:2600, y:850};
let trees = [], gems = [];
const keys = {};

function rand(n) {
    let v = Math.sin(n * 127.1 + 311.7) * 43758.5453;
    return v - Math.floor(v);
}

function makeWorld() {
    trees = [];
    gems = [];
    for (let i=0; i<1250; i++) {
        let x = rand(i+10)*WORLD;
        let y = rand(i+1800)*WORLD;
        if (Math.hypot(x-1600,y-1600)<100) continue;
        if (Math.hypot(x-ancient.x,y-ancient.y)<220) continue;
        trees.push({x,y,size:1+rand(i+4000)*1.4});
    }
    const spots = [
        [1200,1300], [1900,1100], [1000,2100],
        [2300,1700], [2800,1200]
    ];
    spots.forEach((p,i)=>gems.push({
        x:p[0], y:p[1], got:false,
        color:["#76f5ff","#e6a8ff","#fff19b","#a5c8ff","#b2ff9b"][i]
    }));
}

function project(x,y) {
    let dx=x-player.x, dy=y-player.y;
    let depth=dy+420;
    if(depth<35) return null;
    let scale=430/depth;
    return {
        x:W/2+dx*scale,
        y:H*0.52-(420-depth)*0.52,
        scale:scale
    };
}

function drawBackground() {
    let sky=ctx.createLinearGradient(0,0,0,H);
    sky.addColorStop(0,"#173c31");
    sky.addColorStop(0.5,"#315b38");
    sky.addColorStop(1,"#182d1d");
    ctx.fillStyle=sky;
    ctx.fillRect(0,0,W,H);

    ctx.fillStyle="#314b2c";
    ctx.beginPath();
    ctx.moveTo(0,H*0.43);
    ctx.lineTo(W,H*0.39);
    ctx.lineTo(W,H);
    ctx.lineTo(0,H);
    ctx.fill();

    // Thảm cỏ và lối đi
    ctx.fillStyle="#554c32";
    ctx.beginPath();
    ctx.moveTo(W*0.43,H);
    ctx.lineTo(W*0.49,H*0.43);
    ctx.lineTo(W*0.53,H*0.43);
    ctx.lineTo(W*0.68,H);
    ctx.fill();

    // Tán lá lớn phủ phần trên màn hình
    for(let i=0;i<18;i++){
        let x=i*65-25;
        let r=65+rand(i+80)*45;
        ctx.fillStyle=["#163b24","#204a29","#285532"][i%3];
        ctx.beginPath();
        ctx.arc(x,25+rand(i+30)*65,r,0,Math.PI*2);
        ctx.fill();
    }

    // Những thân cây khổng lồ sát camera
    for(let i=0;i<11;i++){
        let x=i*105-50;
        let width=45+rand(i+100)*45;
        ctx.fillStyle="#342d20";
        ctx.fillRect(x,0,width,H);
        ctx.fillStyle="#51432c";
        ctx.fillRect(x+width*0.25,0,width*0.18,H);
        ctx.fillStyle="#1b3824";
        ctx.fillRect(x+width*0.85,0,width*0.18,H);
        // Cành cây lớn
        ctx.strokeStyle="#342d20";
        ctx.lineWidth=width*0.3;
        ctx.beginPath();
        ctx.moveTo(x+width/2,H*0.25);
        ctx.lineTo(x+width/2+65,H*0.12);
        ctx.stroke();
    }

    // Tạo khoảng nhìn ở giữa cho người chơi
    ctx.fillStyle="#314b2c";
    ctx.fillRect(W*0.28,H*0.42,W*0.44,H*0.58);
    ctx.fillStyle="#554c32";
    ctx.beginPath();
    ctx.moveTo(W*0.43,H);
    ctx.lineTo(W*0.49,H*0.42);
    ctx.lineTo(W*0.53,H*0.42);
    ctx.lineTo(W*0.68,H);
    ctx.fill();
}

function drawTree(t) {
    let q=project(t.x,t.y);
    if(!q || q.scale>4) return;
    let s=Math.min(9,q.scale*170*t.size);
    let x=q.x, y=q.y;
    if(x < -s*2 || x > W+s*2) return;

    // Thân cây cao, to
    ctx.fillStyle="#493522";
    ctx.fillRect(x-s*0.20,y-s*3.5,s*0.4,s*3.8);

    ctx.fillStyle="#715035";
    ctx.fillRect(x-s*0.06,y-s*3.4,s*0.10,s*3.6);

    // Các tầng tán lá lớn
    for(let j=0;j<5;j++){
        let yy=y-s*(3.1-j*0.48);
        let ww=s*(1.8-j*0.12);
        ctx.fillStyle=["#153d23","#1b4b29","#245a30","#2c6535","#34723a"][j];
        ctx.beginPath();
        ctx.moveTo(x,yy-s*1.0);
        ctx.lineTo(x-ww,yy+s*0.5);
        ctx.lineTo(x+ww,yy+s*0.5);
        ctx.closePath();
        ctx.fill();
    }
}

function drawAncientTree() {
    let q=project(ancient.x,ancient.y);
    if(!q) return;
    let s=Math.min(13,q.scale*300);
    let x=q.x,y=q.y;
    if(x < -s*4 || x > W+s*4) return;

    ctx.fillStyle=won?"#745337":"#57402a";
    ctx.fillRect(x-s*0.22,y-s*3.8,s*0.44,s*4);

    ctx.strokeStyle=won?"#735037":"#57402a";
    ctx.lineWidth=s*0.25;
    ctx.beginPath();
    ctx.moveTo(x,y-s*1.2);
    ctx.lineTo(x-s*1.5,y-s*3.5);
    ctx.moveTo(x,y-s*1.8);
    ctx.lineTo(x+s*1.5,y-s*3.7);
    ctx.moveTo(x,y-s*2.5);
    ctx.lineTo(x-s*0.9,y-s*4.5);
    ctx.moveTo(x,y-s*2.4);
    ctx.lineTo(x+s*0.9,y-s*4.5);
    ctx.stroke();

    if(won){
        for(let i=0;i<45;i++){
            let lx=x+(rand(i+300)-0.5)*s*5;
            let ly=y-s*(2.2+rand(i+500)*2.6);
            ctx.fillStyle=["#2d873d","#46a84b","#78c957","#b2e77b"][i%4];
            ctx.beginPath();
            ctx.arc(lx,ly,s*(0.25+rand(i+700)*0.2),0,Math.PI*2);
            ctx.fill();
        }
    } else {
        ctx.strokeStyle="#76543a";
        ctx.lineWidth=s*0.14;
        for(let i=0;i<12;i++){
            ctx.beginPath();
            ctx.moveTo(x,y-s*2.5);
            ctx.lineTo(x+(rand(i+100)-0.5)*s*4,y-s*(3+rand(i+200)*2));
            ctx.stroke();
        }
    }
}

function drawGem(g) {
    if(g.got) return;
    let q=project(g.x,g.y);
    if(!q || q.scale>3) return;
    let s=Math.max(5,q.scale*28);
    ctx.fillStyle=g.color;
    ctx.beginPath();
    ctx.moveTo(q.x,q.y-s);
    ctx.lineTo(q.x+s*0.65,q.y);
    ctx.lineTo(q.x,q.y+s);
    ctx.lineTo(q.x-s*0.65,q.y);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle="#ffffff";
    ctx.lineWidth=2;
    ctx.stroke();
}

function drawDashedPath() {
    if(collected<5) return;
    let q=project(ancient.x,ancient.y);
    if(!q) return;
    ctx.setLineDash([10,12]);
    ctx.strokeStyle="#fff49a";
    ctx.lineWidth=4;
    ctx.beginPath();
    ctx.moveTo(W/2,H-90);
    ctx.lineTo(q.x,q.y);
    ctx.stroke();
    ctx.setLineDash([]);
}

function drawPlayer() {
    let x=W/2,y=H-85;
    // Bóng nhân vật
    ctx.fillStyle="#172219";
    ctx.beginPath();
    ctx.ellipse(x,y+12,28,10,0,0,Math.PI*2);
    ctx.fill();

    // Chân
    ctx.fillStyle="#26364c";
    ctx.fillRect(x-17,y-32,13,35);
    ctx.fillRect(x+4,y-32,13,35);

    // Áo
    ctx.fillStyle=gender==="girl"?"#e98cbd":"#4c9ce8";
    ctx.beginPath();
    ctx.moveTo(x-24,y-72);
    ctx.lineTo(x+24,y-72);
    ctx.lineTo(x+30,y-30);
    ctx.lineTo(x-30,y-30);
    ctx.closePath();
    ctx.fill();

    // Đầu nhìn từ phía sau
    ctx.fillStyle="#edc19b";
    ctx.beginPath();
    ctx.arc(x,y-87,19,0,Math.PI*2);
    ctx.fill();

    // Tóc
    ctx.fillStyle=gender==="girl"?"#38251e":"#29221d";
    ctx.beginPath();
    ctx.arc(x,y-92,20,Math.PI,Math.PI*2);
    ctx.lineTo(x+19,y-75);
    if(gender==="girl") ctx.lineTo(x+24,y-38);
    ctx.lineTo(x-20,y-74);
    ctx.closePath();
    ctx.fill();

    // Ba lô
    ctx.fillStyle="#c9a84e";
    ctx.fillRect(x-22,y-67,9,23);
    ctx.fillRect(x+13,y-67,9,23);
}

function drawBeam() {
    if(!victoryStarted) return;
    let q=project(ancient.x,ancient.y);
    if(!q) return;
    let pulse=0.7+Math.sin(Date.now()/180)*0.2;
    let s=Math.min(13,q.scale*300);
    let x=q.x,y=q.y-s*4;
    let grad=ctx.createLinearGradient(x,y-450,x,y);
    grad.addColorStop(0,"#fffbdc00");
    grad.addColorStop(0.5,"#e6ffb8aa");
    grad.addColorStop(1,"#fff6a8dd");
    ctx.fillStyle=grad;
    ctx.fillRect(x-18*pulse,y-450,36*pulse,450);
  }

function update() {
    if(!running || won) return;
    let dx=0,dy=0;
    if(keys.ArrowUp||keys.w||keys.W) dy-=player.speed;
    if(keys.ArrowDown||keys.s||keys.S) dy+=player.speed;
    if(keys.ArrowLeft||keys.a||keys.A) dx-=player.speed;
    if(keys.ArrowRight||keys.d||keys.D) dx+=player.speed;
    player.x=Math.max(0,Math.min(WORLD,player.x+dx));
    player.y=Math.max(0,Math.min(WORLD,player.y+dy));

    gems.forEach(g=>{
        if(!g.got && Math.hypot(player.x-g.x,player.y-g.y)<65){
            g.got=true;
            collected++;
            document.getElementById("gemTag").textContent="💎 Ngọc: "+collected+"/5";
        }
    });

    if(collected===5 && Math.hypot(player.x-ancient.x,player.y-ancient.y)<120){
        won=true;
        victoryStarted=true;
        setTimeout(()=>{
            document.getElementById("win").style.display="flex";
        },1800);
    }
}

function loop() {
    drawBackground();
    trees.slice().sort((a,b)=>b.y-a.y).forEach(drawTree);
    drawAncientTree();
    gems.forEach(drawGem);
    drawDashedPath();
    drawBeam();
    drawPlayer();
    update();
    requestAnimationFrame(loop);
}

function startGame() {
    playerName=document.getElementById("playerName").value.trim()||"Nhà thám hiểm";
    gender=document.getElementById("gender").value;
    document.getElementById("nameTag").textContent="🧭 "+playerName;
    document.getElementById("start").style.display="none";
    document.getElementById("hud").style.display="flex";
    document.getElementById("controls").style.display="grid";
    document.getElementById("hint").style.display="block";
    running=true;
}

function restartGame() {
    player={x:1600,y:1600,speed:5};
    collected=0;
    won=false;
    victoryStarted=false;
    makeWorld();
    document.getElementById("gemTag").textContent="💎 Ngọc: 0/5";
    document.getElementById("win").style.display="none";
    document.getElementById("start").style.display="flex";
    document.getElementById("hud").style.display="none";
    document.getElementById("controls").style.display="none";
    document.getElementById("hint").style.display="none";
    running=false;
}

window.addEventListener("keydown",e=>{
    keys[e.key]=true;
    if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"," "].includes(e.key)) e.preventDefault();
});
window.addEventListener("keyup",e=>keys[e.key]=false);

["up","down","left","right"].forEach(id=>{
    const el=document.getElementById(id);
    const map={up:"ArrowUp",down:"ArrowDown",left:"ArrowLeft",right:"ArrowRight"};
    el.addEventListener("pointerdown",e=>{e.preventDefault();keys[map[id]]=true;});
    ["pointerup","pointerleave","pointercancel"].forEach(ev=>
        el.addEventListener(ev,()=>keys[map[id]]=false)
    );
});

makeWorld();
loop();
</script>
</body>
</html>
"""

components.html(game, height=690, scrolling=False)
