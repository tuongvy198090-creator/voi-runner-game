
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
<style>
*{box-sizing:border-box}
body{
  margin:0;background:#102b20;color:white;
  font-family:Arial,sans-serif;overflow:hidden
}
#game{
  position:relative;width:100%;max-width:1100px;
  margin:auto
}
canvas{
  display:block;width:100%;height:auto;
  border-radius:12px;background:#254d32
}
.panel{
  position:absolute;inset:0;display:flex;
  justify-content:center;align-items:center;
  background:rgba(5,24,17,.83);z-index:5;
  padding:15px
}
.card{
  width:min(420px,95%);padding:25px;
  background:linear-gradient(145deg,#214f37,#102d23);
  border:2px solid #a6dc80;border-radius:20px;
  text-align:center;box-shadow:0 0 30px #7bd66b55
}
h1{color:#d9ff9d;font-size:clamp(24px,4vw,36px);margin:0 0 10px}
p{line-height:1.5}
input,select,button{
  font-size:16px;border-radius:10px;
  padding:12px;border:0
}
input,select{width:100%;margin:7px 0;background:#fff;color:#183425}
button{
  cursor:pointer;font-weight:bold;
  background:#b9ef78;color:#173820;margin:5px
}
button:hover{background:#e0ffae}
#hud{
  position:absolute;top:10px;left:10px;right:10px;
  display:flex;justify-content:space-between;gap:8px;
  pointer-events:none;flex-wrap:wrap
}
.tag{
  background:#102b20dd;border:1px solid #b9ef78;
  border-radius:10px;padding:8px 12px;font-size:14px
}
#controls{
  position:absolute;bottom:12px;left:12px;
  display:grid;grid-template-columns:45px 45px 45px;
  grid-template-rows:42px 42px;gap:4px
}
#controls button{
  margin:0;padding:5px;font-size:19px;
  background:#173b2cdd;color:white;
  border:1px solid #b9ef78;touch-action:none
}
#up{grid-column:2;grid-row:1}
#left{grid-column:1;grid-row:2}
#down{grid-column:2;grid-row:2}
#right{grid-column:3;grid-row:2}
#hint{
  position:absolute;bottom:15px;right:12px;
  max-width:47%;background:#102b20dd;
  border-radius:10px;padding:9px;font-size:12px;
  text-align:right
}
#win h1{font-size:clamp(25px,4vw,38px)}
</style>
</head>
<body>
<div id="game">
<canvas id="canvas" width="1000" height="650"></canvas>

<div id="hud" style="display:none">
  <div class="tag" id="nameTag">Nhà thám hiểm</div>
  <div class="tag" id="gemTag">💎 Ngọc: 0/5</div>
  <div class="tag" id="rabbitTag">🐇 Chú thỏ: chưa giúp</div>
</div>

<div id="controls" style="display:none">
  <button id="up">▲</button>
  <button id="left">◀</button>
  <button id="down">▼</button>
  <button id="right">▶</button>
</div>
<div id="hint" style="display:none">
  Dùng WASD hoặc phím mũi tên để di chuyển
</div>

<div class="panel" id="start">
  <div class="card">
    <h1>🌿 GIẢI CỨU THẾ GIỚI 🌿</h1>
    <p>Khu rừng đang dần héo úa. Hãy tìm những viên ngọc phép thuật, giúp chú thỏ và hồi sinh Cây Cổ Thụ!</p>
    <input id="playerName" maxlength="18" placeholder="Tên nhân vật của em">
    <select id="gender">
      <option value="girl">Nhân vật nữ</option>
      <option value="boy">Nhân vật nam</option>
    </select>
    <button onclick="startGame()" style="width:100%;margin-top:12px">
      BẮT ĐẦU PHIÊU LƯU
    </button>
    <p style="font-size:12px">Thu thập đủ 5 viên ngọc rồi đến gần Cây Cổ Thụ nhé!</p>
  </div>
</div>

<div class="panel" id="win" style="display:none">
  <div class="card">
    <div style="font-size:58px">🌳✨🌎</div>
    <h1>BẠN ĐÃ GIẢI CỨU THẾ GIỚI THÀNH CÔNG!</h1>
    <p>Khu rừng đã hồi sinh nhờ bạn!</p>
    <p>Những mầm xanh lại vươn lên, muôn loài được sống bình yên. Em chính là người hùng của khu rừng!</p>
    <button onclick="restartGame()">CHƠI LẠI</button>
  </div>
</div>
</div>

<script>
const canvas=document.getElementById('canvas');
const ctx=canvas.getContext('2d');

const W=canvas.width,H=canvas.height;
const worldW=2600,worldH=2100;

let running=false,won=false,light=0,winTimer=0;
let playerName='Nhà thám hiểm',gender='girl';
let keys={};
let camera={x:0,y:0};
let gems=[],trees=[],bushes=[],flowers=[];
let rabbit={x:1200,y:1050,rescued:false};
let collected=0;
let player={x:300,y:300,speed:3.2,dir:0};
let victoryStarted=false;

function rand(seed){
  let x=Math.sin(seed*127.1+311.7)*43758.5453;
  return x-Math.floor(x);
}

function createWorld(){
  trees=[];bushes=[];flowers=[];gems=[];
  for(let i=0;i<530;i++){
    let x=rand(i+2)*worldW;
    let y=rand(i+900)*worldH;
    if(Math.hypot(x-300,y-300)<115)continue;
    if(Math.hypot(x-2200,y-1650)<170)continue;
    trees.push({x,y,s:0.65+rand(i+400)*0.85,
      type:rand(i+600)});
  }
  for(let i=0;i<360;i++){
    bushes.push({
      x:rand(i+1200)*worldW,
      y:rand(i+1600)*worldH,
      s:0.5+rand(i+2000)*0.8
    });
  }
  for(let i=0;i<160;i++){
    flowers.push({
      x:rand(i+2500)*worldW,
      y:rand(i+3500)*worldH,
      c:['#f7e7a0','#f3b6c8','#c5e9ff'][i%3]
    });
  }
  for(let i=0;i<5;i++){
    gems.push({
      x:550+i*360,
      y:500+(i%2)*410,
      got:false,
      hue:i
    });
  }
}

const ancient={x:2200,y:1650};

function startGame(){
  playerName=document.getElementById('playerName').value.trim()||'Nhà thám hiểm';
  gender=document.getElementById('gender').value;
  document.getElementById('start').style.display='none';
  document.getElementById('hud').style.display='flex';
  document.getElementById('controls').style.display='grid';
  document.getElementById('hint').style.display='block';
  document.getElementById('nameTag').textContent='🧭 '+playerName;
  running=true;
  requestAnimationFrame(loop);
}

function restartGame(){
  player={x:300,y:300,speed:3.2,dir:0};
  collected=0;
  rabbit={x:1200,y:1050,rescued:false};
  won=false;victoryStarted=false;winTimer=0;
  createWorld();
  document.getElementById('win').style.display='none';
  document.getElementById('hud').style.display='flex';
  document.getElementById('controls').style.display='grid';
  document.getElementById('hint').style.display='block';
  running=true;
  requestAnimationFrame(loop);
}

function drawTree(x,y,s,type,old=false){
  ctx.save();ctx.translate(x,y);ctx.scale(s,s);

  // Bóng dưới gốc cây
  ctx.fillStyle='#183b27';
  ctx.beginPath();ctx.ellipse(0,5,34,13,0,0,Math.PI*2);ctx.fill();

  // Thân cây
  ctx.strokeStyle=old?'#655143':'#765039';
  ctx.lineWidth=12;ctx.lineCap='round';
  ctx.beginPath();
  ctx.moveTo(0,5);ctx.lineTo(0,-35);
  ctx.lineTo(-19,-56);ctx.moveTo(0,-35);
  ctx.lineTo(19,-57);ctx.moveTo(0,-23);ctx.lineTo(-5,-73);
  ctx.stroke();

  if(old){
    ctx.strokeStyle='#57483e';ctx.lineWidth=5;
    ctx.beginPath();
    ctx.moveTo(-19,-56);ctx.lineTo(-29,-68);
    ctx.moveTo(19,-57);ctx.lineTo(29,-70);
    ctx.moveTo(-5,-73);ctx.lineTo(-13,-83);
    ctx.stroke();
    // Một vài chiếc lá héo
    ctx.fillStyle='#9b884a';
    for(let i=0;i<5;i++){
      ctx.beginPath();
      ctx.ellipse((i-2)*9,-57-(i%2)*13,5,3,i*.5,0,Math.PI*2);
      ctx.fill();
    }
  }else{
    let pulse=0.5+0.5*Math.sin(light*0.04);
    ctx.shadowColor='#9bff80';
    ctx.shadowBlur=8+pulse*15;
    const leaves=['#3c9c51','#55b95c','#77cf65','#2d8247'];
    for(let i=0;i<11;i++){
      let a=rand(i+20)*Math.PI*2;
      let r=12+rand(i+50)*30;
      ctx.fillStyle=leaves[i%leaves.length];
      ctx.beginPath();
      ctx.ellipse(Math.cos(a)*r,-57+Math.sin(a)*r,
        15,19,a,0,Math.PI*2);
      ctx.fill();
    }
    ctx.shadowBlur=0;
    ctx.fillStyle='#b9fca0';
    ctx.globalAlpha=.55+pulse*.35;
    ctx.beginPath();ctx.arc(0,-59,10+pulse*5,0,Math.PI*2);ctx.fill();
  }
  ctx.restore();
}

function drawForest(){
  // Mặt đất
  ctx.fillStyle=won?'#4d9b50':'#315d39';
  ctx.fillRect(0,0,worldW,worldH);

  // Mảng cỏ và lối mòn
  for(let i=0;i<240;i++){
    let x=rand(i+500)*worldW,y=rand(i+750)*worldH;
    ctx.fillStyle=i%2?'#396943':'#35633d';
    ctx.beginPath();ctx.ellipse(x,y,20,12,0,0,Math.PI*2);ctx.fill();
  }

  // Con đường quanh co
  ctx.lineCap='round';
  ctx.strokeStyle='#9b8a5d';ctx.lineWidth=105;
  ctx.beginPath();ctx.moveTo(120,320);ctx.bezierCurveTo(600,450,550,850,1000,930);
  ctx.bezierCurveTo(1350,1030,1300,1450,1800,1430);
  ctx.bezierCurveTo(2000,1430,2050,1570,2200,1650);ctx.stroke();
  ctx.strokeStyle='#b7a477';ctx.lineWidth=80;
  ctx.stroke();

  for(const f of flowers){
    ctx.fillStyle=f.c;ctx.beginPath();ctx.arc(f.x,f.y,2.5,0,Math.PI*2);ctx.fill();
  }
  for(const b of bushes){
    ctx.fillStyle='#245b35';
    ctx.beginPath();ctx.arc(b.x,b.y,12*b.s,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#347743';
    ctx.beginPath();ctx.arc(b.x-6*b.s,b.y-4*b.s,8*b.s,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(b.x+7*b.s,b.y-2*b.s,7*b.s,0,Math.PI*2);ctx.fill();
  }
  for(const t of trees){
    drawTree(t.x,t.y,t.s,t.type,false);
  }
  drawTree(ancient.x,ancient.y,2.7,0,!victoryStarted);
}

function drawGem(g){
  if(g.got)return;
  ctx.save();ctx.translate(g.x,g.y);
  ctx.shadowColor='#9bffff';ctx.shadowBlur=20;
  ctx.fillStyle=['#77f7ff','#f2a9ff','#fff48b','#9cc8ff','#a5ffbc'][g.hue];
  ctx.beginPath();
  ctx.moveTo(0,-16);ctx.lineTo(12,-4);
  ctx.lineTo(7,12);ctx.lineTo(-7,12);ctx.lineTo(-12,-4);
  ctx.closePath();ctx.fill();
  ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.stroke();
  ctx.restore();
}

function drawRabbit(){
  ctx.save();ctx.translate(rabbit.x,rabbit.y);
  ctx.fillStyle=rabbit.rescued?'#fff0c4':'#eee4d2';
  ctx.beginPath();ctx.ellipse(0,0,15,11,0,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(10,-12,10,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.ellipse(7,-26,4,12,-.2,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.ellipse(15,-26,4,11,.2,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#d88e9d';ctx.beginPath();ctx.arc(13,-13,2,0,Math.PI*2);ctx.fill();
  ctx.restore();
}

function drawPlayer(){
  ctx.save();ctx.translate(player.x,player.y);

  // Bóng
  ctx.fillStyle='#193b29';
  ctx.beginPath();ctx.ellipse(0,7,17,8,0,0,Math.PI*2);ctx.fill();

  // Chân và giày
  ctx.fillStyle='#62452f';
  ctx.fillRect(-10,-2,7,15);ctx.fillRect(3,-2,7,15);
  ctx.fillStyle='#49372c';
  ctx.fillRect(-12,10,10,5);ctx.fillRect(2,10,10,5);

  // Ba lô
  ctx.fillStyle='#8b603b';ctx.fillRect(-14,-27,28,25);
  ctx.fillStyle='#b4874f';ctx.fillRect(-11,-24,22,17);

  // Áo choàng / trang phục
  if(gender==='girl'){
    ctx.fillStyle='#e7dfc8';
    ctx.beginPath();ctx.moveTo(-12,-36);ctx.lineTo(12,-36);
    ctx.lineTo(18,-8);ctx.lineTo(-18,-8);ctx.closePath();ctx.fill();
    ctx.fillStyle='#39874d';
    ctx.beginPath();ctx.moveTo(-10,-34);ctx.lineTo(10,-34);
    ctx.lineTo(14,-5);ctx.lineTo(-14,-5);ctx.closePath();ctx.fill();
  }else{
    ctx.fillStyle='#397c50';ctx.fillRect(-13,-37,26,31);
    ctx.fillStyle='#c2a16d';ctx.fillRect(-4,-36,8,26);
  }

  // Đầu
  ctx.fillStyle='#e9bd91';
  ctx.beginPath();ctx.arc(0,-45,12,0,Math.PI*2);ctx.fill();

  // Tóc
  ctx.fillStyle='#583a27';
  ctx.beginPath();ctx.arc(0,-49,12,Math.PI,Math.PI*2);ctx.fill();
  ctx.fillRect(-12,-49,5,11);
  ctx.fillRect(7,-49,5,10);
  if(gender==='girl'){
    ctx.beginPath();ctx.ellipse(10,-54,5,3,.5,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#a5d96a';ctx.beginPath();ctx.arc(9,-57,4,0,Math.PI*2);ctx.fill();
  }
  ctx.restore();
}

function drawDirection(){
  if(collected<5||won)return;
  const dx=ancient.x-player.x,dy=ancient.y-player.y;
  const distance=Math.hypot(dx,dy);
  if(distance<75)return;

  // Đường nét đứt phát sáng dẫn đến Cây Cổ Thụ
  ctx.save();
  ctx.strokeStyle='#eaff9a';
  ctx.lineWidth=4;
  ctx.setLineDash([10,12]);
  ctx.lineDashOffset=-light*1.5;
  ctx.shadowColor='#cfff72';
  ctx.shadowBlur=13;
  ctx.beginPath();
  ctx.moveTo(player.x,player.y);
  ctx.lineTo(
    player.x+dx/distance*Math.min(distance,500),
    player.y+dy/distance*Math.min(distance,500)
  );
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.restore();
}

function drawSkyBeam(){
  if(!victoryStarted)return;
  const t=Math.min(winTimer/100,1);
  const alpha=Math.min(t*1.6,1);
  ctx.save();
  ctx.globalAlpha=alpha;
  ctx.translate(ancient.x,ancient.y-150);

  // Luồng sáng hướng lên trời
  const grad=ctx.createLinearGradient(0,0,0,-850);
  grad.addColorStop(0,'rgba(255,255,180,.85)');
  grad.addColorStop(.25,'rgba(197,255,144,.55)');
  grad.addColorStop(1,'rgba(190,255,180,0)');
  ctx.fillStyle=grad;
  ctx.beginPath();
  ctx.moveTo(-45,0);ctx.lineTo(-125,-850);
  ctx.lineTo(125,-850);ctx.lineTo(45,0);
  ctx.closePath();ctx.fill();

  // Tia sáng trung tâm
  ctx.strokeStyle='#ffffd0';ctx.lineWidth=7;
  ctx.shadowColor='#e5ff9b';ctx.shadowBlur=28;
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,-900);ctx.stroke();

  // Các đốm phép thuật bay lên
  for(let i=0;i<35;i++){
    const yy=-((light*4+i*31)%800);
    const xx=Math.sin(light*.04+i*2)*25;
    ctx.fillStyle=i%2?'#fff8a5':'#c9ffb3';
    ctx.beginPath();ctx.arc(xx,yy,2+(i%3),0,Math.PI*2);ctx.fill();
  }
  ctx.restore();
}

function update(){
  if(!running||won)return;
  let dx=0,dy=0;
  if(keys['ArrowUp']||keys['w']||keys['W'])dy--;
  if(keys['ArrowDown']||keys['s']||keys['S'])dy++;
  if(keys['ArrowLeft']||keys['a']||keys['A'])dx--;
  if(keys['ArrowRight']||keys['d']||keys['D'])dx++;
  if(dx&&dy){dx*=.707;dy*=.707}
  player.x=Math.max(25,Math.min(worldW-25,player.x+dx*player.speed));
  player.y=Math.max(25,Math.min(worldH-25,player.y+dy*player.speed));
  if(dx||dy)player.dir=Math.atan2(dy,dx);

  for(const g of gems){
    if(!g.got&&Math.hypot(g.x-player.x,g.y-player.y)<35){
      g.got=true;collected++;
      document.getElementById('gemTag').textContent='💎 Ngọc: '+collected+'/5';
    }
  }

  if(!rabbit.rescued&&Math.hypot(rabbit.x-player.x,rabbit.y-player.y)<48){
    rabbit.rescued=true;
    document.getElementById('rabbitTag').textContent='🐇 Đã giúp chú thỏ!';
  }

  camera.x=Math.max(0,Math.min(worldW-W,player.x-W/2));
  camera.y=Math.max(0,Math.min(worldH-H,player.y-H/2));

  // Khi đủ ngọc và đến gần cây, cây bắt đầu hồi sinh
  if(collected>=5&&!victoryStarted&&
     Math.hypot(ancient.x-player.x,ancient.y-player.y)<100){
    victoryStarted=true;
    winTimer=0;
  }

  if(victoryStarted){
    winTimer++;
    if(winTimer>115){
      won=true;
      document.getElementById('win').style.display='flex';
      document.getElementById('hud').style.display='none';
      document.getElementById('controls').style.display='none';
      document.getElementById('hint').style.display='none';
    }
  }
}

function loop(){
  if(!running)return;
  light++;
  update();

  ctx.clearRect(0,0,W,H);
  ctx.save();
  ctx.translate(-camera.x,-camera.y);

  drawForest();

  for(const g of gems)drawGem(g);
  drawRabbit();
  drawDirection();

  // Nhân vật và cây được vẽ theo tọa độ thế giới
  drawPlayer();
  drawSkyBeam();

  ctx.restore();

  // Nhắc người chơi nếu chưa đủ ngọc
  if(!won&&collected<5&&Math.hypot(ancient.x-player.x,ancient.y-player.y)<350){
    ctx.fillStyle='#fff4b5';
    ctx.font='bold 16px Arial';
    ctx.textAlign='center';
    ctx.fillText('Hãy tìm đủ 5 viên ngọc trước nhé!',W/2, H-25);
  }

  requestAnimationFrame(loop);
}

window.addEventListener('keydown',e=>{
  if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight',' '].includes(e.key))e.preventDefault();
  keys[e.key]=true;
});
window.addEventListener('keyup',e=>{keys[e.key]=false});

function bindButton(id,key){
  const b=document.getElementById(id);
  b.addEventListener('pointerdown',e=>{e.preventDefault();keys[key]=true});
  b.addEventListener('pointerup',()=>keys[key]=false);
  b.addEventListener('pointerleave',()=>keys[key]=false);
  b.addEventListener('pointercancel',()=>keys[key]=false);
}
bindButton('up','ArrowUp');
bindButton('down','ArrowDown');
bindButton('left','ArrowLeft');
bindButton('right','ArrowRight');

createWorld();
drawForest();
drawRabbit();
drawPlayer();
</script>
</body>
</html>
"""

components.html(game, height=690, scrolling=False)
