
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="GIẢI CỨU THẾ GIỚI",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    header, footer, #MainMenu {
        visibility: hidden;
    }
    iframe {
        border: none;
    }
</style>
""", unsafe_allow_html=True)

game = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden}
body{
 background:#163b27;color:white;
 font-family:Arial,sans-serif;
}
#game{position:relative;width:100%;height:100vh;overflow:hidden}
canvas{width:100%;height:100%;display:block;outline:none}
.panel{
 position:absolute;inset:0;display:flex;align-items:center;
 justify-content:center;background:#102b20bb;padding:15px;
}
.card{
 background:#153e2bee;border:2px solid #a4dc76;
 border-radius:22px;padding:25px;text-align:center;
 width:min(420px,95%);box-shadow:0 0 35px #7cff8b55;
}
h1{color:#c9ff94;font-size:clamp(25px,5vw,42px);margin:8px 0}
p{line-height:1.5}
button,input,select{
 font-size:16px;border-radius:12px;padding:11px;
 border:2px solid #a9e58a;
}
button{
 background:#d4ffad;color:#174326;font-weight:bold;
 cursor:pointer;
}
button:hover{background:#fff2a3}
input,select{width:100%;margin:7px 0;background:#f5ffe9;color:#183d27}
.choices{display:flex;gap:10px;margin:12px 0}
.choices button{flex:1}
#hud{
 position:absolute;top:10px;left:10px;right:10px;
 display:flex;justify-content:space-between;align-items:flex-start;
 gap:8px;pointer-events:none;flex-wrap:wrap;
}
.info{
 background:#103b2ddd;border:1px solid #b9ef8d;
 padding:9px 12px;border-radius:12px;font-weight:bold;
 text-shadow:0 1px 2px #000;
}
#message{
 position:absolute;top:75px;left:50%;transform:translateX(-50%);
 background:#163b2be8;padding:9px 14px;border-radius:12px;
 text-align:center;max-width:90%;font-weight:bold;
}
#controls{
 position:absolute;bottom:16px;left:16px;
 display:grid;grid-template-columns:54px 54px 54px;
 grid-template-rows:54px 54px;gap:5px;
}
.arrow{
 width:54px;height:54px;padding:0;font-size:26px;
 background:#e3ffcacc;border:2px solid white;
 touch-action:none;user-select:none;
}
#up{grid-column:2;grid-row:1}
#left{grid-column:1;grid-row:2}
#down{grid-column:2;grid-row:2}
#right{grid-column:3;grid-row:2}
#action{
 position:absolute;bottom:25px;right:18px;
 max-width:150px;
}
#win .card{background:#174c31f5}
#win h1{font-size:clamp(27px,5vw,45px)}
@media(max-width:500px){
 #controls{transform:scale(.85);transform-origin:bottom left}
 #action{bottom:25px;right:8px;font-size:13px}
 .info{font-size:13px;padding:7px}
}
</style>
</head>
<body>
<div id="game">
<canvas id="world" tabindex="0"></canvas>

<div id="hud" style="display:none">
 <div class="info" id="gems">💎 Ngọc: 0/5</div>
 <div class="info" id="playerName">Nhà thám hiểm</div>
</div>
<div id="message" style="display:none"></div>

<div id="controls" style="display:none">
 <button class="arrow" id="up">⬆️</button>
 <button class="arrow" id="left">⬅️</button>
 <button class="arrow" id="down">⬇️</button>
 <button class="arrow" id="right">➡️</button>
</div>
<button id="action" style="display:none">🌟 Tương tác</button>

<div class="panel" id="start">
 <div class="card">
  <div style="font-size:45px">🌲💎🌳</div>
  <h1>GIẢI CỨU<br>THẾ GIỚI</h1>
  <p>Khu rừng đang mất đi phép thuật!<br>
  Hãy tìm 5 viên ngọc và cứu Cây Cổ Thụ.</p>
  <input id="name" maxlength="18" placeholder="Tên nhân vật của em">
  <p>Chọn nhân vật:</p>
  <div class="choices">
   <button id="girl">🧚 Nữ tiên rừng</button>
   <button id="boy">🧑‍🌾 Nam phiêu lưu</button>
  </div>
  <p id="chosen">Đang chọn: Nữ tiên rừng</p>
  <button id="startBtn" style="width:100%">🌟 BẮT ĐẦU PHIÊU LƯU</button>
 </div>
</div>

<div class="panel" id="win" style="display:none">
 <div class="card">
  <div style="font-size:70px">🌳✨🌍</div>
  <h1>BẠN ĐÃ GIẢI CỨU THẾ GIỚI THÀNH CÔNG!</h1>
  <p id="winner"></p>
  <p>Ánh sáng đã trở lại khu rừng. Mọi sinh vật đều được bình yên!</p>
  <button onclick="location.reload()">🔄 Chơi lại</button>
 </div>
</div>
</div>

<script>
const canvas=document.getElementById('world');
const ctx=canvas.getContext('2d');
const W=2200,H=1600;
let cw=innerWidth,ch=innerHeight,dpr=1;
function resize(){
 dpr=Math.min(devicePixelRatio||1,2);
 cw=innerWidth;ch=innerHeight;
 canvas.width=cw*dpr;canvas.height=ch*dpr;
 ctx.setTransform(dpr,0,0,dpr,0,0);
}
addEventListener('resize',resize);resize();

let started=false,gender='girl',name='Nhà thám hiểm';
let player={x:1100,y:850,speed:3.3};
let gems=[],got=new Set(),rabbitHelped=false,won=false;
let keys={},lastMessage='',messageUntil=0,light=0;
const tree={x:1780,y:260};
const rabbit={x:380,y:1170};
const gemSpots=[
 {x:380,y:350},{x:760,y:650},{x:1450,y:600},
 {x:550,y:1000},{x:1550,y:1190}
];
const trees=[];
let seed=7291;
function rand(){
 seed=(seed*16807)%2147483647;
 return (seed-1)/2147483646;
}
for(let i=0;i<180;i++){
 trees.push({x:rand()*W,y:rand()*H,r:22+rand()*25});
}
function say(s,ms=2500){
 lastMessage=s;messageUntil=performance.now()+ms;
 document.getElementById('message').textContent=s;
}
function distance(a,b){return Math.hypot(a.x-b.x,a.y-b.y)}
function startGame(){
 name=document.getElementById('name').value.trim()||'Nhà thám hiểm';
 started=true;
 document.getElementById('start').style.display='none';
 document.getElementById('hud').style.display='flex';
 document.getElementById('controls').style.display='grid';
 document.getElementById('action').style.display='block';
 document.getElementById('playerName').textContent=
 (gender==='girl'?'🧚 ':'🧑‍🌾 ')+name;
 say('🌲 Khám phá khu rừng và tìm 5 viên ngọc quý!');
 canvas.focus();
}
document.getElementById('girl').onclick=()=>{
 gender='girl';document.getElementById('chosen').textContent='Đang chọn: Nữ tiên rừng';
};
document.getElementById('boy').onclick=()=>{
 gender='boy';document.getElementById('chosen').textContent='Đang chọn: Nam phiêu lưu';
};
document.getElementById('startBtn').onclick=startGame;

addEventListener('keydown',e=>{
 const k=e.key.toLowerCase();
 if(['arrowup','arrowdown','arrowleft','arrowright','w','a','s','d',' '].includes(k)){
  e.preventDefault();keys[k]=true;
 }
});
addEventListener('keyup',e=>{keys[e.key.toLowerCase()]=false});
addEventListener('blur',()=>{keys={}});

function bindButton(id,key){
 const b=document.getElementById(id);
 b.addEventListener('pointerdown',e=>{
  e.preventDefault();keys[key]=true;b.setPointerCapture(e.pointerId);
 });
 const release=e=>{keys[key]=false};
 b.addEventListener('pointerup',release);
 b.addEventListener('pointercancel',release);
 b.addEventListener('lostpointercapture',release);
}
bindButton('up','arrowup');bindButton('down','arrowdown');
bindButton('left','arrowleft');bindButton('right','arrowright');

function drawTree(x,y,r,ancient=false){
 ctx.save();ctx.translate(x,y);
 if(ancient){
  ctx.shadowColor='#a9ff55';ctx.shadowBlur=25+Math.sin(light)*12;
 }
 ctx.fillStyle='#62452c';
 ctx.fillRect(-r*.16,-r*.05,r*.32,r*.75);
 ctx.fillStyle=ancient?'#32894a':'#216b3c';
 for(let i=0;i<5;i++){
  ctx.beginPath();
  ctx.arc(Math.sin(i*2)*r*.32,-r*.25-i*r*.13,r*(.52-i*.035),0,Math.PI*2);
  ctx.fill();
 }
 if(ancient){
  ctx.fillStyle='#caff70';
  ctx.beginPath();ctx.arc(0,-r*.3,r*.18,0,Math.PI*2);ctx.fill();
 }
 ctx.restore();
}
function drawCrystal(x,y){
 ctx.save();ctx.translate(x,y);
 ctx.shadowColor='#83ffff';ctx.shadowBlur=15;
 ctx.fillStyle='#a2ffff';
 ctx.beginPath();ctx.moveTo(0,-16);ctx.lineTo(11,-3);
 ctx.lineTo(7,12);ctx.lineTo(-7,12);ctx.lineTo(-11,-3);
 ctx.closePath();ctx.fill();
 ctx.fillStyle='#e9ffff';
 ctx.beginPath();ctx.moveTo(0,-12);ctx.lineTo(3,0);ctx.lineTo(0,7);ctx.lineTo(-3,0);ctx.fill();
 ctx.restore();
}
function drawHero(x,y){
 ctx.save();ctx.translate(x,y);
 // shadow
 ctx.fillStyle='#14351c88';
 ctx.beginPath();ctx.ellipse(0,11,15,7,0,0,Math.PI*2);ctx.fill();
 // boots
 ctx.fillStyle='#69412b';
 ctx.fillRect(-10,3,7,9);ctx.fillRect(4,3,7,9);
 if(gender==='girl'){
  // green dress and cream cape
  ctx.fillStyle='#e8d6a4';
  ctx.beginPath();ctx.moveTo(-10,-8);ctx.lineTo(-17,5);ctx.lineTo(-10,7);ctx.lineTo(0,-4);ctx.fill();
  ctx.fillStyle='#3c9c53';
  ctx.beginPath();ctx.moveTo(-8,-7);ctx.lineTo(8,-7);ctx.lineTo(13,5);ctx.lineTo(-13,5);ctx.closePath();ctx.fill();
  // hair
  ctx.fillStyle='#70452e';
  ctx.beginPath();ctx.ellipse(0,-15,10,11,0,0,Math.PI*2);ctx.fill();
  // face
  ctx.fillStyle='#f4c99d';
  ctx.beginPath();ctx.arc(0,-15,7,0,Math.PI*2);ctx.fill();
  // longer hair
  ctx.fillStyle='#70452e';
  ctx.fillRect(-9,-18,4,19);ctx.fillRect(5,-18,4,19);
  // leaf clip
  ctx.fillStyle='#b5f06b';
  ctx.beginPath();ctx.ellipse(5,-23,5,2,-.6,0,Math.PI*2);ctx.fill();
 }else{
  ctx.fillStyle='#3b8050';
  ctx.fillRect(-10,-8,20,14);
  ctx.fillStyle='#e3c18b';
  ctx.fillRect(-7,-5,14,9);
  ctx.fillStyle='#70452e';
  ctx.beginPath();ctx.arc(0,-15,10,Math.PI,Math.PI*2);ctx.fill();
  ctx.fillStyle='#f4c99d';
  ctx.beginPath();ctx.arc(0,-14,7,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#70452e';
  ctx.fillRect(-8,-20,16,5);
 }
 // backpack
 ctx.fillStyle='#8a6339';ctx.fillRect(-13,-8,5,10);
 ctx.restore();
}
function drawRabbit(x,y){
 ctx.fillStyle='#f3eee2';
 ctx.beginPath();ctx.ellipse(x,y,14,11,0,0,Math.PI*2);ctx.fill();
 ctx.beginPath();ctx.ellipse(x-6,y-16,4,11,-.2,0,Math.PI*2);ctx.fill();
 ctx.beginPath();ctx.ellipse(x+4,y-17,4,11,.2,0,Math.PI*2);ctx.fill();
 ctx.fillStyle='#f4a1b5';
 ctx.beginPath();ctx.arc(x+5,y-3,2.5,0,Math.PI*2);ctx.fill();
}
function drawWorld(){
 ctx.fillStyle='#367c43';ctx.fillRect(0,0,W,H);
 // grass texture
 for(let i=0;i<520;i++){
  let x=(i*137+31)%W,y=(i*251+73)%H;
  ctx.strokeStyle=i%2?'#4a914c':'#2d713a';
  ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+3,y-5);ctx.stroke();
 }
 // winding path
 ctx.lineCap='round';ctx.lineJoin='round';
 ctx.strokeStyle='#b6a16a';ctx.lineWidth=115;
 ctx.beginPath();ctx.moveTo(100,800);ctx.bezierCurveTo(400,700,450,400,850,460);
 ctx.bezierCurveTo(1200,520,1100,1100,1500,1030);
 ctx.bezierCurveTo(1800,980,1750,500,tree.x,tree.y+90);ctx.stroke();
 ctx.strokeStyle='#d0bc82';ctx.lineWidth=90;
 ctx.beginPath();ctx.moveTo(100,800);ctx.bezierCurveTo(400,700,450,400,850,460);
 ctx.bezierCurveTo(1200,520,1100,1100,1500,1030);
 ctx.bezierCurveTo(1800,980,1750,500,tree.x,tree.y+90);ctx.stroke();

 for(const t of trees)drawTree(t.x,t.y,t.r);
 // magical ancient tree
 drawTree(tree.x,tree.y,82,true);
 if(got.size===5){
  ctx.save();
  ctx.globalAlpha=.3+.25*Math.sin(light);
  ctx.strokeStyle='#e8ff9b';ctx.lineWidth=8;
  ctx.beginPath();ctx.arc(tree.x,tree.y,110+Math.sin(light)*10,0,Math.PI*2);ctx.stroke();
  ctx.restore();
 }
 for(let i=0;i<gemSpots.length;i++){
  if(!got.has(i))drawCrystal(gemSpots[i].x,gemSpots[i].y);
 }
 drawRabbit(rabbit.x,rabbit.y);
 drawHero(player.x,player.y);

 if(got.size===5){
  const a=Math.atan2(tree.y-player.y,tree.x-player.x);
  const ax=player.x+Math.cos(a)*48,ay=player.y+Math.sin(a)*48;
  ctx.save();ctx.translate(ax,ay);ctx.rotate(a);
  ctx.shadowColor='#ffff80';ctx.shadowBlur=20;
  ctx.fillStyle='#fff68a';
  ctx.beginPath();ctx.moveTo(22,0);ctx.lineTo(-10,-11);ctx.lineTo(-5,0);ctx.lineTo(-10,11);ctx.closePath();ctx.fill();
  ctx.restore();
 }
}
function update(){
 if(!started||won)return;
 let dx=0,dy=0;
 if(keys.arrowleft||keys.a)dx--;
 if(keys.arrowright||keys.d)dx++;
 if(keys.arrowup||keys.w)dy--;
 if(keys.arrowdown||keys.s)dy++;
 if(dx||dy){
  const len=Math.hypot(dx,dy);
  player.x+=dx/len*player.speed;
  player.y+=dy/len*player.speed;
 }
 player.x=Math.max(25,Math.min(W-25,player.x));
 player.y=Math.max(25,Math.min(H-25,player.y));

 for(let i=0;i<gemSpots.length;i++){
  if(!got.has(i)&&distance(player,gemSpots[i])<32){
   got.add(i);
   document.getElementById('gems').textContent=`💎 Ngọc: ${got.size}/5`;
   say('✨ Em đã thu thập được một viên ngọc!');
   if(got.size===5)say('🌟 Đã đủ 5 viên! Hãy đi theo mũi tên đến Cây Cổ Thụ!',5000);
  }
 }
 if(!rabbitHelped&&distance(player,rabbit)<42){
  say('🐰 Bấm “Tương tác” để giúp chú thỏ nhé!',1500);
 }
 if(got.size===5&&distance(player,tree)<65&&!won){
  say('✨ Đã đến Cây Cổ Thụ! Bấm “Tương tác” để đặt ngọc!',1800);
 }
 light+=.06;
}
document.getElementById('action').onclick=()=>{
 if(!started||won)return;
 if(distance(player,rabbit)<45&&!rabbitHelped){
  rabbitHelped=true;
  say('🐰 Chú thỏ cảm ơn em! Chúc em cứu thế giới thành công!');
 }else if(got.size===5&&distance(player,tree)<75){
  won=true;
  document.getElementById('win').style.display='flex';
  document.getElementById('winner').textContent=
    name+' đã thu thập đủ ngọc và đánh thức Cây Cổ Thụ!';
  say('🌟 Phép thuật đã trở lại!');
 }else if(got.size<5){
  say('💎 Hãy tìm đủ 5 viên ngọc trước nhé!');
 }else{
  say('➡️ Hãy đi theo mũi tên phát sáng đến Cây Cổ Thụ!');
 }
};
function frame(){
 update();
 ctx.clearRect(0,0,cw,ch);
 if(started){
  const scale=Math.min(cw/950,ch/650,1.35);
  const viewW=cw/scale,viewH=ch/scale;
  const camX=Math.max(0,Math.min(W-viewW,player.x-viewW/2));
  const camY=Math.max(0,Math.min(H-viewH,player.y-viewH/2));
  ctx.save();ctx.scale(scale,scale);ctx.translate(-camX,-camY);
  drawWorld();ctx.restore();
  const msg=document.getElementById('message');
  msg.style.display=performance.now()<messageUntil?'block':'none';
 }
 requestAnimationFrame(frame);
}
frame();
</script>
</body>
</html>
"""

components.html(game, height=750, scrolling=False)
