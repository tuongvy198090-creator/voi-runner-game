
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
body{margin:0;background:#102719;color:white;font-family:Arial}
#game{position:relative;width:100%;max-width:1100px;margin:auto}
canvas{width:100%;height:auto;display:block;border-radius:12px}
.panel{
 position:absolute;inset:0;display:flex;align-items:center;
 justify-content:center;background:#07190fdc;z-index:5;padding:12px
}
.card{
 width:min(460px,96%);padding:24px;text-align:center;
 background:linear-gradient(145deg,#244f32,#10291d);
 border:2px solid #b6df87;border-radius:20px;
 box-shadow:0 0 25px #0008
}
h1{color:#e0ffad;font-size:clamp(25px,4vw,38px)}
p{line-height:1.5}
input,select,button{font-size:16px;padding:12px;border-radius:10px;border:0}
input,select{width:100%;margin:6px 0}
button{cursor:pointer;font-weight:bold;background:#c8f38a;color:#19351f;margin:5px}
button:hover{background:#e4ffc0}
#hud{
 position:absolute;top:10px;left:10px;right:10px;
 display:flex;justify-content:space-between;gap:6px;flex-wrap:wrap;
 pointer-events:none
}
.tag{background:#102719dd;border:1px solid #b6df87;border-radius:10px;padding:8px 11px;font-size:14px}
#controls{
 position:absolute;bottom:12px;left:12px;
 display:grid;grid-template-columns:48px 48px 48px;
 grid-template-rows:44px 44px;gap:4px
}
#controls button{
 margin:0;padding:4px;font-size:21px;color:white;
 background:#183a2cdd;border:1px solid #d5f5a6;
 touch-action:none
}
#up{grid-column:2;grid-row:1}
#left{grid-column:1;grid-row:2}
#down{grid-column:2;grid-row:2}
#right{grid-column:3;grid-row:2}
#hint{
 position:absolute;right:12px;bottom:15px;max-width:48%;
 background:#102719dd;padding:9px;border-radius:10px;
 font-size:12px;text-align:right
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
<div id="hint" style="display:none">WASD hoặc phím mũi tên để di chuyển</div>

<div class="panel" id="start">
 <div class="card">
  <h1>🌿 GIẢI CỨU THẾ GIỚI 🌿</h1>
  <p>Khu rừng đang héo úa. Hãy tìm đủ 5 viên ngọc phép thuật để hồi sinh Cây Cổ Thụ!</p>
  <input id="playerName" maxlength="18" placeholder="Tên nhân vật của em">
  <select id="gender">
   <option value="girl">Nhân vật nữ</option>
   <option value="boy">Nhân vật nam</option>
  </select>
  <button onclick="startGame()" style="width:100%;margin-top:10px">BẮT ĐẦU PHIÊU LƯU</button>
  <p style="font-size:12px">Khám phá khu rừng, thu thập ngọc và tìm Cây Cổ Thụ.</p>
 </div>
</div>

<div class="panel" id="win" style="display:none">
 <div class="card">
  <div style="font-size:65px">🌳✨</div>
  <h1>BẠN ĐÃ GIẢI CỨU THẾ GIỚI THÀNH CÔNG!</h1>
  <p>Khu rừng đã hồi sinh nhờ bạn. Ánh sáng phép thuật đã trở lại!</p>
  <button onclick="restartGame()">CHƠI LẠI</button>
 </div>
</div>
</div>

<script>
const canvas=document.getElementById('canvas');
const ctx=canvas.getContext('2d');
const W=canvas.width,H=canvas.height;
const WORLD=3200;
const keys={};

let running=false,won=false,light=0;
let playerName='Nhà thám hiểm',gender='girl';
let collected=0,victoryStarted=false,winTimer=0;
let player={x:1600,y:1600,angle:0,speed:4};
let trees=[],gems=[];
const ancient={x:2600,y:850};

function rand(n){
 const v=Math.sin(n*127.1+311.7)*43758.5453;
 return v-Math.floor(v);
}

function makeWorld(){
 trees=[];gems=[];
 // Rừng cây mọc dày đặc
 for(let i=0;i<1450;i++){
  let x=rand(i+10)*WORLD;
  let y=rand(i+1800)*WORLD;
  if(Math.hypot(x-1600,y-1600)<100)continue;
  if(Math.hypot(x-ancient.x,y-ancient.y)<115)continue;
  trees.push({
   x,y,
   size:0.8+rand(i+4000)*1.15,
   kind:rand(i+8000)
  });
 }
 // Năm viên ngọc nằm rải rác trong rừng
 const spots=[
  [1200,1300],[1900,1100],[1000,2100],
  [2300,1700],[2800,1200]
 ];
 spots.forEach((p,i)=>gems.push({
  x:p[0],y:p[1],got:false,color:
  ['#76f5ff','#e6a8ff','#fff19b','#a5c8ff','#b2ff9b'][i]
 }));
}

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
 player={x:1600,y:1600,angle:0,speed:4};
 collected=0;victoryStarted=false;winTimer=0;won=false;
 makeWorld();
 document.getElementById('gemTag').textContent='💎 Ngọc: 0/5';
 document.getElementById('win').style.display='none';
 document.getElementById('hud').style.display='flex';
 document.getElementById('controls').style.display='grid';
 document.getElementById('hint').style.display='block';
 running=true;
 requestAnimationFrame(loop);
}

// Đổi tọa độ khu rừng thành góc nhìn từ sau lưng nhân vật
function project(x,y){
 const dx=x-player.x,dy=y-player.y;
 const a=player.angle;
 const forward=dx*Math.cos(a)+dy*Math.sin(a);
 const side=-dx*Math.sin(a)+dy*Math.cos(a);
 if(forward<15)return null;
 const focal=410;
 const scale=focal/(forward+110);
 return {
  x:W/2+side*scale,
  y:285+145*scale,
  scale,depth:forward
 };
}

function drawBackground(){
 const sky=ctx.createLinearGradient(0,0,0,H);
 sky.addColorStop(0,'#8bb9a0');
 sky.addColorStop(.5,'#b6c9a0');
 sky.addColorStop(1,'#537d42');
 ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);

 // Mặt đất rừng
 ctx.fillStyle='#496e39';
 ctx.beginPath();
 ctx.moveTo(0,285);ctx.lineTo(W,285);
 ctx.lineTo(W,H);ctx.lineTo(0,H);ctx.fill();

 // Lối mòn giữa rừng
 ctx.fillStyle='#8a7951';
 ctx.beginPath();
 ctx.moveTo(460,285);ctx.lineTo(540,285);
 ctx.lineTo(870,H);ctx.lineTo(130,H);ctx.closePath();ctx.fill();

 // Ánh sáng tự nhiên trên mặt đất, không phát sáng
 ctx.fillStyle='#66854a';
 ctx.beginPath();
 ctx.moveTo(490,285);ctx.lineTo(510,285);
 ctx.lineTo(650,H);ctx.lineTo(350,H);ctx.closePath();ctx.fill();
}

function drawTree(t){
 const q=project(t.x,t.y);
 if(!q||q.x<-120||q.x>W+120||q.y>H+130)return;
 const s=Math.min(5.5,q.scale*90*t.size);
 const x=q.x,y=q.y;
 if(s<2)return;

 ctx.save();
 // Bóng cây bình thường
 ctx.fillStyle='#29482b88';
 ctx.beginPath();ctx.ellipse(x,y,Math.max(3,s*.48),Math.max(2,s*.12),0,0,Math.PI*2);ctx.fill();

 // Thân cây
 ctx.fillStyle='#60452e';
 ctx.fillRect(x-s*.12,y-s*.8,s*.24,s*.82);

 // Tán cây nhiều tầng
 const old=!victoryStarted;
 const greens=old?
  ['#6b7050','#77734c','#5b6743']:
  ['#347b3d','#3f9147','#4c9e4f'];
 for(let i=0;i<3;i++){
  ctx.fillStyle=greens[i];
  ctx.beginPath();
  ctx.moveTo(x,y-s*(2.25-i*.36));
  ctx.lineTo(x-s*(.68-i*.12),y-s*(.95-i*.18));
  ctx.lineTo(x+s*(.68-i*.12),y-s*(.95-i*.18));
  ctx.closePath();ctx.fill();
 }
 ctx.restore();
}

function drawAncientTree(){
 const q=project(ancient.x,ancient.y);
 if(!q||q.x<-250||q.x>W+250||q.y>H+200)return;
 const s=Math.min(7,q.scale*180);
 const x=q.x,y=q.y;
 const revived=victoryStarted;

 ctx.save();
 // Bóng dưới gốc
 ctx.fillStyle='#243d2488';
 ctx.beginPath();ctx.ellipse(x,y,s*.65,s*.15,0,0,Math.PI*2);ctx.fill();

 // Thân cổ thụ
 ctx.strokeStyle=revived?'#795335':'#594738';
 ctx.lineWidth=Math.max(3,s*.16);
 ctx.lineCap='round';
 ctx.beginPath();
 ctx.moveTo(x,y);ctx.lineTo(x-s*.05,y-s*1.1);
 ctx.lineTo(x-s*.48,y-s*1.65);
 ctx.moveTo(x-s*.04,y-s*1.15);ctx.lineTo(x+s*.43,y-s*1.7);
 ctx.moveTo(x-s*.02,y-s*.85);ctx.lineTo(x-s*.1,y-s*2.05);
 ctx.stroke();

 if(!revived){
  // Cây héo: cành khô, không có hiệu ứng phát sáng
  ctx.strokeStyle='#6d5846';ctx.lineWidth=Math.max(2,s*.07);
  ctx.beginPath();
  ctx.moveTo(x-s*.48,y-s*1.65);ctx.lineTo(x-s*.65,y-s*1.85);
  ctx.moveTo(x+s*.43,y-s*1.7);ctx.lineTo(x+s*.65,y-s*1.93);
  ctx.moveTo(x-s*.1,y-s*2.05);ctx.lineTo(x-s*.23,y-s*2.22);
  ctx.stroke();
  ctx.fillStyle='#8a8050';
  for(let i=0;i<7;i++){
   ctx.beginPath();
   ctx.ellipse(x+(i-3)*s*.13,y-s*(1.7+(i%3)*.12),s*.07,s*.035,i*.3,0,Math.PI*2);
   ctx.fill();
  }
 }else{
  // Tán lá chỉ xuất hiện khi cây hồi sinh
  const colors=['#319449','#4eb85b','#70cd68','#9de77d'];
  for(let i=0;i<24;i++){
   const a=rand(i+91)*Math.PI*2;
   const r=s*(.25+rand(i+33)*.55);
   ctx.fillStyle=colors[i%colors.length];
   ctx.beginPath();
   ctx.ellipse(x+Math.cos(a)*r,y-s*1.8+Math.sin(a)*r*.65,
    s*.16,s*.21,a,0,Math.PI*2);
   ctx.fill();
  }
 }
 ctx.restore();
}

function drawGem(g){
 if(g.got)return;
 const q=project(g.x,g.y);
 if(!q||q.x<-30||q.x>W+30||q.y>H+20)return;
 const s=Math.max(3,Math.min(15,q.scale*19));
 ctx.save();
 ctx.fillStyle=g.color;
 ctx.beginPath();
 ctx.moveTo(q.x,q.y-s);
 ctx.lineTo(q.x+s*.7,q.y);
 ctx.lineTo(q.x,q.y+s);
 ctx.lineTo(q.x-s*.7,q.y);
 ctx.closePath();ctx.fill();
 ctx.strokeStyle='#fff';ctx.lineWidth=1.5;ctx.stroke();
 ctx.restore();
}

function drawPlayer(){
 const x=W/2,y=H-92;
 const s=1.45;
 ctx.save();ctx.translate(x,y);ctx.scale(s,s);

 // Bóng dưới chân
 ctx.fillStyle='#263d2588';
 ctx.beginPath();ctx.ellipse(0,8,24,10,0,0,Math.PI*2);ctx.fill();

 // Chân và giày
 ctx.fillStyle='#4d3929';
 ctx.fillRect(-13,-3,10,26);
 ctx.fillRect(4,-3,10,26);
 ctx.fillStyle='#302b22';
 ctx.fillRect(-15,19,14,7);
 ctx.fillRect(3,19,14,7);

 // Ba lô
 ctx.fillStyle='#795333';
 ctx.fillRect(-20,-48,40,36);
 ctx.fillStyle='#9b7547';
 ctx.fillRect(-16,-44,32,25);
 ctx.fillStyle='#4b3827';
 ctx.fillRect(-4,-44,8,25);

 // Trang phục nhìn từ sau
 if(gender==='girl'){
  ctx.fillStyle='#e8ddc5';
  ctx.beginPath();ctx.moveTo(-17,-53);ctx.lineTo(17,-53);
  ctx.lineTo(24,-13);ctx.lineTo(-24,-13);ctx.closePath();ctx.fill();
  ctx.fillStyle='#3d8550';
  ctx.beginPath();ctx.moveTo(-15,-52);ctx.lineTo(15,-52);
  ctx.lineTo(20,-11);ctx.lineTo(-20,-11);ctx.closePath();ctx.fill();
 }else{
  ctx.fillStyle='#387b4a';
  ctx.fillRect(-18,-55,36,43);
  ctx.fillStyle='#b59a6a';
  ctx.fillRect(-5,-53,10,38);
 }

 // Đầu và tóc, nhìn từ phía sau
 ctx.fillStyle='#e5b78b';
 ctx.beginPath();ctx.arc(0,-64,15,0,Math.PI*2);ctx.fill();
 ctx.fillStyle='#503421';
 ctx.beginPath();ctx.arc(0,-68,16,Math.PI,Math.PI*2);ctx.fill();
 ctx.fillRect(-15,-70,5,17);
 ctx.fillRect(10,-70,5,17);
 if(gender==='girl'){
  ctx.fillStyle='#503421';
  ctx.beginPath();ctx.ellipse(0,-51,8,15,0,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#a8d66d';
  ctx.beginPath();ctx.arc(12,-77,4,0,Math.PI*2);ctx.fill();
 }
 ctx.restore();
}

function drawDashedPath(){
 if(collected<5||victoryStarted)return;
 const dx=ancient.x-player.x,dy=ancient.y-player.y;
 const dist=Math.hypot(dx,dy);
 if(dist<60)return;

 // Nét đứt trên mặt đất, hướng về phía cây cổ thụ
 const a=player.angle;
 const forward=dx*Math.cos(a)+dy*Math.sin(a);
 const side=-dx*Math.sin(a)+dy*Math.cos(a);
 if(forward<=0)return;

 const q=project(ancient.x,ancient.y);
 if(!q)return;

 ctx.save();
 ctx.strokeStyle='#f0ffbb';
 ctx.lineWidth=4;
 ctx.setLineDash([9,13]);
 ctx.lineDashOffset=-light*1.4;
 ctx.beginPath();
 ctx.moveTo(W/2,H-115);
 ctx.lineTo(q.x,q.y);
 ctx.stroke();
 ctx.setLineDash([]);
 ctx.restore();
}

function drawBeam(){
 if(!victoryStarted)return;
 const q=project(ancient.x,ancient.y);
 if(!q)return;
 const s=Math.min(7,q.scale*180);
 const x=q.x,y=q.y-s*1.8;
 const power=Math.min(winTimer/45,1);

 ctx.save();
 ctx.globalAlpha=power;
 const grad=ctx.createLinearGradient(x,y,x,y-650);
 grad.addColorStop(0,'rgba(255,255,190,.95)');
 grad.addColorStop(.35,'rgba(202,255,152,.6)');
 grad.addColorStop(1,'rgba(202,255,152,0)');
 ctx.fillStyle=grad;
 ctx.beginPath();
 ctx.moveTo(x-s*.22,y);ctx.lineTo(x-100,y-650);
 ctx.lineTo(x+100,y-650);ctx.lineTo(x+s*.22,y);
 ctx.closePath();ctx.fill();

 ctx.strokeStyle='#ffffd6';ctx.lineWidth=6;
 ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x,y-650);ctx.stroke();

 for(let i=0;i<25;i++){
  const yy=y-((light*5+i*37)%620);
  const xx=x+Math.sin(light*.04+i)*25;
  ctx.fillStyle=i%2?'#fff8ac':'#caffb0';
  ctx.beginPath();ctx.arc(xx,yy,2+(i%3),0,Math.PI*2);ctx.fill();
 }
 ctx.restore();
}

function update(){
 if(!running||won)return;
 let dx=0,dy=0;
 if(keys.ArrowUp||keys.w||keys.W)dy--;
 if(keys.ArrowDown||keys.s||keys.S)dy++;
 if(keys.ArrowLeft||keys.a||keys.A)dx--;
 if(keys.ArrowRight||keys.d||keys.D)dx++;

 if(dx&&dy){dx*=.707;dy*=.707}
 if(dx||dy){
  player.angle=Math.atan2(dy,dx);
  player.x+=dx*player.speed;
  player.y+=dy*player.speed;
 }
 player.x=Math.max(20,Math.min(WORLD-20,player.x));
 player.y=Math.max(20,Math.min(WORLD-20,player.y));

 for(const g of gems){
  if(!g.got&&Math.hypot(g.x-player.x,g.y-player.y)<48){
   g.got=true;collected++;
   document.getElementById('gemTag').textContent='💎 Ngọc: '+collected+'/5';
  }
 }

 if(collected>=5&&!victoryStarted&&
    Math.hypot(ancient.x-player.x,ancient.y-player.y)<100){
  victoryStarted=true;
  winTimer=0;
 }
 if(victoryStarted){
  winTimer++;
  if(winTimer>105){
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
 drawBackground();

 // Vẽ vật thể xa trước, gần sau để tạo cảm giác chiều sâu
 const visible=trees.map(t=>{
  const q=project(t.x,t.y);
  return {t,q};
 }).filter(o=>o.q&&o.q.x>-150&&o.q.x<W+150&&o.q.y<H+160)
   .sort((a,b)=>b.q.depth-a.q.depth);

 for(const o of visible)drawTree(o.t);

 // Cổ thụ và ngọc
 drawAncientTree();
 for(const g of gems)drawGem(g);

 drawDashedPath();
 drawBeam();
 drawPlayer();

 if(!won&&collected<5){
  ctx.fillStyle='#fff5c9';
  ctx.font='bold 16px Arial';
  ctx.textAlign='center';
  ctx.fillText('Tìm đủ 5 viên ngọc để đánh thức Cây Cổ Thụ',W/2,30);
 }
 if(!won&&collected>=5&&!victoryStarted){
  ctx.fillStyle='#f0ffbd';
  ctx.font='bold 17px Arial';
  ctx.textAlign='center';
  ctx.fillText('Đi theo đường nét đứt để tìm Cây Cổ Thụ!',W/2,30);
 }

 requestAnimationFrame(loop);
}

window.addEventListener('keydown',e=>{
 if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight',' '].includes(e.key))e.preventDefault();
 keys[e.key]=true;
});
window.addEventListener('keyup',e=>keys[e.key]=false);

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

makeWorld();
drawBackground();
drawPlayer();
</script>
</body>
</html>
"""

components.html(game, height=690, scrolling=False)
vv
