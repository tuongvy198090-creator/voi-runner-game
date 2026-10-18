
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
*{box-sizing:border-box}
body{margin:0;background:#102719;color:white;font-family:Arial}
#game{position:relative;width:100%;max-width:1200px;margin:auto;overflow:hidden}
canvas{width:100%;height:auto;display:block}
.panel{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:#07190fdd;padding:12px;z-index:5}
.card{width:min(480px,96%);padding:22px;text-align:center;background:linear-gradient(145deg,#355d36,#10291c);border:3px solid #b7dc85;border-radius:20px}
h1{color:#e2ffad;font-size:clamp(23px,4vw,34px);margin:8px 0}
p{line-height:1.5}
input,select,button{width:100%;font-size:16px;padding:12px;border-radius:10px;border:0;margin-top:8px}
button{background:#d4f69a;color:#17351d;font-weight:bold;cursor:pointer}
#hud{position:absolute;top:10px;left:10px;right:10px;display:flex;justify-content:space-between;gap:8px;pointer-events:none}
.tag{background:#102719e8;border:2px solid #c5e99b;border-radius:12px;padding:10px;font-weight:bold}
#controls{position:absolute;bottom:12px;left:12px;display:grid;grid-template-columns:48px 48px 48px;grid-template-rows:44px 44px;gap:4px}
#controls button{margin:0;padding:4px;font-size:22px;background:#153b2bdc;border:1px solid #e0ffc0;color:white;touch-action:none}
#up{grid-column:2;grid-row:1}#left{grid-column:1;grid-row:2}#down{grid-column:2;grid-row:2}#right{grid-column:3;grid-row:2}
#hint{position:absolute;right:12px;bottom:14px;background:#102719e8;border-radius:10px;padding:10px;font-size:12px;max-width:48%}
</style>
</head>
<body>
<div id="game">
<canvas id="canvas" width="1000" height="650"></canvas>

<div id="hud" style="display:none">
 <div class="tag" id="nameTag"></div>
 <div class="tag" id="gemTag">💎 Ngọc: 0/5</div>
</div>

<div id="controls" style="display:none">
 <button id="up">▲</button><button id="left">◀</button>
 <button id="down">▼</button><button id="right">▶</button>
</div>
<div id="hint" style="display:none">WASD hoặc phím mũi tên để chạy</div>

<div class="panel" id="start">
 <div class="card">
  <div style="font-size:38px">🌿 🌳 🌲</div>
  <h1>CHÀO MỪNG BẠN ĐẾN VỚI TRÒ CHƠI</h1>
  <h1>GIẢI CỨU THẾ GIỚI</h1>
  <p>Thu thập 5 viên ngọc để đánh thức Cây Cổ Thụ!</p>
  <input id="playerName" maxlength="18" placeholder="Nhập tên nhân vật">
  <p><b>CHỌN NHÂN VẬT</b></p>
  <select id="gender">
   <option value="girl">Nhân vật nữ</option>
   <option value="boy">Nhân vật nam</option>
  </select>
  <button onclick="startGame()">▶ BẮT ĐẦU</button>
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
const canvas=document.getElementById("canvas");
const ctx=canvas.getContext("2d");
const W=1000,H=650;
const keys={};
let running=false,won=false,gender="girl";
let playerName="Nhà thám hiểm",collected=0,victoryStarted=false;
let player={x:0,z:0,speed:0.13};
let trees=[],gems=[];
const ancient={x:0,z:48};

function rand(n){
 let v=Math.sin(n*127.1+311.7)*43758.5453;
 return v-Math.floor(v);
}

// Thế giới cố định: cây không tự di chuyển
function makeWorld(){
 trees=[];gems=[];
 for(let i=0;i<500;i++){
  const side=rand(i+3)<0.5?-1:1;
  trees.push({
   x:side*(4+rand(i+70)*28),
   z:5+rand(i+140)*95,
   size:0.7+rand(i+200)*1.5
  });
 }
 const spots=[
  [-3,12],[4,19],[-5,28],[5,36],[0,43]
 ];
 spots.forEach((p,i)=>gems.push({
  x:p[0],z:p[1],got:false,
  color:["#76f5ff","#e6a8ff","#fff19b","#a5c8ff","#b2ff9b"][i]
 }));
}

// Góc nhìn từ phía sau nhân vật.
// Thế giới chỉ đổi vị trí trên màn hình khi người chơi di chuyển.
function screenPoint(x,z){
 const depth=z-player.z;
 if(depth<0.8)return null;
 const scale=360/depth;
 return {
  x:W/2+(x-player.x)*scale,
  y:H*0.48+(player.z+4-z)*scale*0.35,
  scale:scale,
  depth:depth
 };
}

function drawBackground(){
 const sky=ctx.createLinearGradient(0,0,0,H);
 sky.addColorStop(0,"#183b2b");
 sky.addColorStop(0.55,"#355b35");
 sky.addColorStop(1,"#1b301e");
 ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);

 // Mặt đất
 ctx.fillStyle="#30492b";
 ctx.beginPath();
 ctx.moveTo(0,H*0.43);ctx.lineTo(W,H*0.43);
 ctx.lineTo(W,H);ctx.lineTo(0,H);ctx.fill();

 // Đường mòn
 ctx.fillStyle="#68563a";
 ctx.beginPath();
 ctx.moveTo(W*0.42,H);ctx.lineTo(W*0.49,H*0.43);
 ctx.lineTo(W*0.52,H*0.43);ctx.lineTo(W*0.72,H);ctx.fill();

 // Tán cây phủ trên cao
 for(let i=0;i<18;i++){
  const x=i*62-20,r=60+rand(i+90)*40;
  ctx.fillStyle=["#173b23","#204a29","#285532"][i%3];
  ctx.beginPath();ctx.arc(x,15+rand(i+30)*35,r,0,Math.PI*2);ctx.fill();
 }
}

function drawTree(t){
 const p=screenPoint(t.x,t.z);
 if(!p||p.depth>110)return;
 const s=Math.min(150,p.scale*0.62*t.size);
 if(p.x<-s*2||p.x>W+s*2)return;
 const x=p.x,y=p.y;

 // Thân cây
 ctx.fillStyle="#493522";
 ctx.fillRect(x-s*0.12,y-s*1.8,s*0.24,s*1.9);
 ctx.fillStyle="#705035";
 ctx.fillRect(x-s*0.04,y-s*1.7,s*0.06,s*1.8);

 // Tán cây nhiều tầng
 for(let j=0;j<4;j++){
  const yy=y-s*(1.6-j*0.3);
  const ww=s*(0.9-j*0.12);
  ctx.fillStyle=["#153d23","#1b4b29","#245a30","#34723a"][j];
  ctx.beginPath();
  ctx.moveTo(x,yy-s*0.85);
  ctx.lineTo(x-ww,yy+s*0.4);
  ctx.lineTo(x+ww,yy+s*0.4);
  ctx.closePath();ctx.fill();
 }
}

function drawAncientTree(){
 const p=screenPoint(ancient.x,ancient.z);
 if(!p)return;
 const s=Math.min(230,p.scale*1.05);
 const x=p.x,y=p.y;
 if(x<-s*3||x>W+s*3)return;

 ctx.fillStyle=won?"#745337":"#57402a";
 ctx.fillRect(x-s*0.13,y-s*1.9,s*0.26,s*2);

 ctx.strokeStyle=won?"#735037":"#57402a";
 ctx.lineWidth=Math.max(3,s*0.13);
 ctx.beginPath();
 ctx.moveTo(x,y-s*0.8);
 ctx.lineTo(x-s*0.8,y-s*1.8);
 ctx.moveTo(x,y-s*1.1);
 ctx.lineTo(x+s*0.8,y-s*1.9);
 ctx.moveTo(x,y-s*1.2);
 ctx.lineTo(x-s*0.4,y-s*2.2);
 ctx.moveTo(x,y-s*1.2);
 ctx.lineTo(x+s*0.4,y-s*2.2);
 ctx.stroke();

 if(won){
  for(let i=0;i<45;i++){
   ctx.fillStyle=["#2d873d","#46a84b","#78c957","#b2e77b"][i%4];
   ctx.beginPath();
   ctx.arc(x+(rand(i+300)-0.5)*s*2.5,
    y-s*(1.3+rand(i+500)*1.1),s*0.12,0,Math.PI*2);
   ctx.fill();
  }
 }else{
  ctx.strokeStyle="#96704a";ctx.lineWidth=2;
  for(let i=0;i<12;i++){
   ctx.beginPath();ctx.moveTo(x,y-s*1.2);
   ctx.lineTo(x+(rand(i+30)-0.5)*s*2,y-s*(1.5+rand(i+60)));
   ctx.stroke();
  }
 }
}

function drawGem(g){
 if(g.got)return;
 const p=screenPoint(g.x,g.z);
 if(!p||p.depth>60)return;
 const s=Math.max(5,p.scale*0.09);
 ctx.fillStyle=g.color;
 ctx.beginPath();
 ctx.moveTo(p.x,p.y-s);ctx.lineTo(p.x+s*0.7,p.y);
 ctx.lineTo(p.x,p.y+s);ctx.lineTo(p.x-s*0.7,p.y);
 ctx.closePath();ctx.fill();
 ctx.strokeStyle="white";ctx.stroke();
}

function drawPlayer(){
 const x=W/2,y=H-85;
 const moving=keys.ArrowUp||keys.w||keys.W||
  keys.ArrowDown||keys.s||keys.S||
  keys.ArrowLeft||keys.a||keys.A||
  keys.ArrowRight||keys.d||keys.D;
 const bounce=moving?Math.sin(Date.now()/65)*4:0;

 // Bóng
 ctx.fillStyle="#172219";
 ctx.beginPath();ctx.ellipse(x,y+12,30,10,0,0,Math.PI*2);ctx.fill();

 // Chân đang chạy
 ctx.fillStyle="#26364c";
 ctx.save();
 ctx.translate(x-9,y-28+bounce);
 ctx.rotate(moving?Math.sin(Date.now()/65)*0.35:0);
 ctx.fillRect(-6,0,12,33);ctx.restore();
 ctx.save();
 ctx.translate(x+9,y-28-bounce);
 ctx.rotate(moving?-Math.sin(Date.now()/65)*0.35:0);
 ctx.fillRect(-6,0,12,33);ctx.restore();

 // Áo
 ctx.fillStyle=gender==="girl"?"#e98cbd":"#4c9ce8";
 ctx.beginPath();ctx.moveTo(x-24,y-72);ctx.lineTo(x+24,y-72);
 ctx.lineTo(x+30,y-30);ctx.lineTo(x-30,y-30);
 ctx.closePath();ctx.fill();

 // Đầu nhìn từ phía sau
 ctx.fillStyle="#edc19b";
 ctx.beginPath();ctx.arc(x,y-87,19,0,Math.PI*2);ctx.fill();

 // Tóc
 ctx.fillStyle=gender==="girl"?"#38251e":"#29221d";
 ctx.beginPath();ctx.arc(x,y-92,20,Math.PI,Math.PI*2);
 ctx.lineTo(x+19,y-75);
 if(gender==="girl")ctx.lineTo(x+24,y-38);
 ctx.lineTo(x-20,y-74);ctx.closePath();ctx.fill();

 // Ba lô
 ctx.fillStyle="#c9a84e";
 ctx.fillRect(x-22,y-67,9,23);ctx.fillRect(x+13,y-67,9,23);
}

function drawPath(){
 if(collected<5)return;
 const p=screenPoint(ancient.x,ancient.z);
 if(!p)return;
 ctx.setLineDash([10,12]);
 ctx.strokeStyle="#fff49a";ctx.lineWidth=4;
 ctx.beginPath();ctx.moveTo(W/2,H-85);ctx.lineTo(p.x,p.y);
 ctx.stroke();ctx.setLineDash([]);
}

function drawBeam(){
 if(!victoryStarted)return;
 const p=screenPoint(ancient.x,ancient.z);
 if(!p)return;
 const s=Math.min(230,p.scale*1.05);
 const grad=ctx.createLinearGradient(p.x,p.y-s*2.2,p.x,p.y);
 grad.addColorStop(0,"#fffbdc00");
 grad.addColorStop(0.5,"#e6ffb8aa");
 grad.addColorStop(1,"#fff6a8dd");
 ctx.fillStyle=grad;ctx.fillRect(p.x-18,p.y-s*2.2,36,s*2.2);
}

function update(){
 if(!running||won)return;
 let dx=0,dz=0;
 if(keys.ArrowUp||keys.w||keys.W)dz+=player.speed;
 if(keys.ArrowDown||keys.s||keys.S)dz-=player.speed;
 if(keys.ArrowLeft||keys.a||keys.A)dx-=player.speed;
 if(keys.ArrowRight||keys.d||keys.D)dx+=player.speed;

 // Không có phím bấm thì vị trí thế giới giữ nguyên
 player.x=Math.max(-25,Math.min(25,player.x+dx));
 player.z=Math.max(0,Math.min(100,player.z+dz));

 gems.forEach(g=>{
  if(!g.got&&Math.hypot(player.x-g.x,player.z-g.z)<1.6){
   g.got=true;collected++;
   document.getElementById("gemTag").textContent="💎 Ngọc: "+collected+"/5";
  }
 });

 if(collected===5&&Math.hypot(player.x-ancient.x,player.z-ancient.z)<2.2){
  won=true;victoryStarted=true;
  setTimeout(()=>document.getElementById("win").style.display="flex",1800);
 }
}

function loop(){
 drawBackground();
 trees.slice().sort((a,b)=>b.z-a.z).forEach(drawTree);
 drawAncientTree();
 gems.forEach(drawGem);
 drawPath();
 drawBeam();
 drawPlayer();
 update();
 requestAnimationFrame(loop);
}

function startGame(){
 playerName=document.getElementById("playerName").value.trim()||"Nhà thám hiểm";
 gender=document.getElementById("gender").value;
 document.getElementById("nameTag").textContent="🧭 "+playerName;
 document.getElementById("start").style.display="none";
 document.getElementById("hud").style.display="flex";
 document.getElementById("controls").style.display="grid";
 document.getElementById("hint").style.display="block";
 running=true;
}

function restartGame(){
 player={x:0,z:0,speed:0.13};
 collected=0;won=false;victoryStarted=false;
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
 if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight"," "].includes(e.key))e.preventDefault();
});
window.addEventListener("keyup",e=>keys[e.key]=false);

["up","down","left","right"].forEach(id=>{
 const el=document.getElementById(id);
 const map={up:"ArrowUp",down:"ArrowDown",left:"ArrowLeft",right:"ArrowRight"};
 el.addEventListener("pointerdown",e=>{e.preventDefault();keys[map[id]]=true;});
 ["pointerup","pointerleave","pointercancel"].forEach(ev=>
  el.addEventListener(ev,()=>keys[map[id]]=false));
});

makeWorld();
loop();
</script>
</body>
</html>
"""

components.html(game, height=690, scrolling=False)
vvv
