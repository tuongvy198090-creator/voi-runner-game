
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Giải cứu thế giới",
    page_icon="🌳",
    layout="wide"
)

st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}
.block-container {padding:0!important;max-width:100%!important;}
iframe {border:0!important;}
</style>
""", unsafe_allow_html=True)

game_code = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}
body{margin:0;overflow:hidden;font-family:Arial;background:#102719}
canvas{width:100%;height:100vh;display:block;touch-action:none}
#menu,#win{
 position:fixed;inset:0;z-index:5;color:white;
 display:flex;flex-direction:column;align-items:center;
 justify-content:center;text-align:center;padding:20px;
 background:linear-gradient(#102d20e8,#07180df5)
}
h1{color:#c4ff91;text-shadow:0 0 18px #54e66d}
#menu h1{font-size:clamp(30px,6vw,55px)}
input,select,button{font-size:17px;padding:12px 16px;
 border:0;border-radius:12px;margin:7px}
button{background:#a1f16c;color:#17391c;font-weight:bold;cursor:pointer}
#hud,#help{
 position:fixed;z-index:2;color:white;background:#102b20dc;
 padding:12px;border-radius:12px;line-height:1.6
}
#hud{top:10px;left:10px;font-weight:bold}
#help{top:10px;right:10px;font-size:12px;max-width:190px}
#joystick{
 position:fixed;z-index:3;bottom:22px;left:22px;width:125px;height:125px;
 border:3px solid #ffffffbb;background:#ffffff26;border-radius:50%;
 touch-action:none
}
#knob{
 position:absolute;left:34px;top:34px;width:52px;height:52px;
 border-radius:50%;background:#e6ffca;border:3px solid #579d46;
 box-shadow:0 0 14px #baff83;pointer-events:none
}
#win{display:none}
.small{font-size:13px;opacity:.85}
@media(max-width:600px){
 #help{max-width:145px;font-size:11px}
 #joystick{width:115px;height:115px}
 #knob{left:29px;top:29px}
}
</style>
</head>
<body>
<canvas id="game"></canvas>

<div id="menu">
 <h1>🌍 GIẢI CỨU THẾ GIỚI 🌳</h1>
 <p>Khu rừng bí ẩn đang chờ em khám phá!</p>
 <input id="playerName" placeholder="Nhập tên của em" maxlength="18">
 <select id="gender">
  <option value="boy">Nhân vật nam</option>
  <option value="girl">Nhân vật nữ</option>
 </select>
 <button id="startBtn">▶ BẮT ĐẦU</button>
 <p class="small">Tìm đá quý và giải cứu cây cổ thụ ở cuối con đường.</p>
</div>

<div id="hud" style="display:none">
 🌟 Người chơi: <span id="nameLabel"></span><br>
 💎 Đá quý: <span id="gemsLabel">0</span>/5<br>
 🌳 Hãy khám phá khu rừng!
</div>
<div id="help" style="display:none">
 <b>DI CHUYỂN</b><br>
 Máy tính: WASD hoặc phím mũi tên<br>
 Kéo nút tròn để đi 8 hướng
</div>
<div id="joystick" style="display:none"><div id="knob"></div></div>

<div id="win">
 <h1>🌎 BẠN ĐÃ GIẢI CỨU THẾ GIỚI THÀNH CÔNG! 🌳</h1>
 <p id="winText"></p>
 <p>Cây cổ thụ đã xanh tươi trở lại!</p>
 <button id="againBtn">🔄 CHƠI LẠI</button>
</div>

<script>
const canvas=document.getElementById("game");
const ctx=canvas.getContext("2d");
let W=0,H=0;
function resize(){
 W=canvas.width=innerWidth;
 H=canvas.height=innerHeight;
}
addEventListener("resize",resize);resize();

let running=false,won=false,treeGreen=false;
let playerName="Nhà thám hiểm",gender="boy";
let px=0,pz=0,gems=0,lastTime=0;
let keys={},joyX=0,joyY=0,collected=new Set();

const WORLD_END=220;
const TREE_Z=210;

// Đá quý được đặt cố định rải khắp con đường dài.
const gemPositions=[];
for(let i=0;i<95;i++){
 const z=7+i*2.12;
 const side=(Math.sin(i*12.37)*1.65);
 gemPositions.push({
  x:side,
  z:z,
  color:["#58f5ff","#ff72e8","#fff36b",
         "#a8a0ff","#76ff8b"][i%5]
 });
}

// Tọa độ đường cong cố định trong thế giới.
// Đường uốn trái phải liên tục, không được tạo lại ngẫu nhiên.
function roadCurve(z){
 return Math.sin(z*0.035)*1.15+
        Math.sin(z*0.078)*0.38+
        Math.sin(z*0.014)*0.65;
}

// Chiếu một vị trí trong thế giới ra màn hình.
// dz là khoảng cách từ nhân vật tới vật thể.
function project(z,side=0){
 const dz=z-pz;
 const depth=1-dz/90;
 const t=Math.max(0,Math.min(1,depth));
 const y=H*0.405+t*t*H*0.66;
 const center=W*0.5+roadCurve(z)*W*0.055;
 const scale=0.10+t*0.90;
 return {
  x:center+side*W*(0.025+t*0.13),
  y:y,
  depth:t,
  scale:scale,
  center:center
 };
}

function startGame(){
 playerName=document.getElementById("playerName").value.trim()
  ||"Nhà thám hiểm";
 gender=document.getElementById("gender").value;
 px=0;pz=0;gems=0;collected.clear();
 won=false;treeGreen=false;running=true;
 document.getElementById("menu").style.display="none";
 document.getElementById("win").style.display="none";
 document.getElementById("hud").style.display="block";
 document.getElementById("help").style.display="block";
 document.getElementById("joystick").style.display="block";
 document.getElementById("nameLabel").textContent=playerName;
 updateHud();
}
document.getElementById("startBtn").onclick=startGame;
document.getElementById("againBtn").onclick=()=>{
 running=false;
 document.getElementById("menu").style.display="flex";
 document.getElementById("win").style.display="none";
 document.getElementById("hud").style.display="none";
 document.getElementById("help").style.display="none";
 document.getElementById("joystick").style.display="none";
};
function updateHud(){
 document.getElementById("gemsLabel").textContent=gems;
}

addEventListener("keydown",e=>{
 const k=e.key.toLowerCase();
 if(["arrowup","arrowdown","arrowleft","arrowright"," "].includes(k))
  e.preventDefault();
 keys[k]=true;
});
addEventListener("keyup",e=>keys[e.key.toLowerCase()]=false);
addEventListener("blur",()=>keys={});

// Joystick tròn
const joystick=document.getElementById("joystick");
const knob=document.getElementById("knob");
let joyActive=false;
function moveJoy(e){
 const r=joystick.getBoundingClientRect();
 let dx=e.clientX-(r.left+r.width/2);
 let dy=e.clientY-(r.top+r.height/2);
 const max=r.width*0.32,len=Math.hypot(dx,dy);
 if(len>max){dx=dx/len*max;dy=dy/len*max;}
 joyX=dx/max;joyY=dy/max;
 knob.style.left=(r.width/2-26+dx)+"px";
 knob.style.top=(r.height/2-26+dy)+"px";
}
joystick.addEventListener("pointerdown",e=>{
 joyActive=true;joystick.setPointerCapture(e.pointerId);moveJoy(e);
});
joystick.addEventListener("pointermove",e=>{
 if(joyActive)moveJoy(e);
});
function releaseJoy(){
 joyActive=false;joyX=0;joyY=0;
 const r=joystick.getBoundingClientRect();
 knob.style.left=(r.width/2-26)+"px";
 knob.style.top=(r.height/2-26)+"px";
}
joystick.addEventListener("pointerup",releaseJoy);
joystick.addEventListener("pointercancel",releaseJoy);

function drawSky(){
 const sky=ctx.createLinearGradient(0,0,0,H);
 sky.addColorStop(0,"#5da9bd");
 sky.addColorStop(0.35,"#c6dfb0");
 sky.addColorStop(0.405,"#355b32");
 sky.addColorStop(1,"#102519");
 ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);

 ctx.fillStyle="#476f3c";
 ctx.beginPath();ctx.moveTo(0,H*.43);
 for(let x=0;x<=W;x+=25)
  ctx.lineTo(x,H*.39+Math.sin(x*.009)*H*.035);
 ctx.lineTo(W,H);ctx.lineTo(0,H);ctx.fill();
}

// Đường rất dài; phần đường trước mắt luôn được vẽ theo tọa độ thế giới.
function drawRoad(){
 const horizon=H*.405;
 const segments=100;
 ctx.fillStyle="#92794b";
 ctx.beginPath();
 for(let i=0;i<=segments;i++){
  const dz=90-(i/segments)*90;
  const z=pz+dz;
  const p=project(z);
  const half=W*(0.008+p.depth*0.105);
  if(i===0)ctx.moveTo(p.center-half,p.y);
  else ctx.lineTo(p.center-half,p.y);
 }
 for(let i=segments;i>=0;i--){
  const dz=90-(i/segments)*90;
  const z=pz+dz;
  const p=project(z);
  const half=W*(0.008+p.depth*0.105);
  ctx.lineTo(p.center+half,p.y);
 }
 ctx.closePath();ctx.fill();

 // Hai mép đường
 ctx.strokeStyle="#c1a56c";ctx.lineWidth=3;
 for(const side of [-1,1]){
  ctx.beginPath();
  for(let i=0;i<=segments;i++){
   const z=pz+90-(i/segments)*90;
   const p=project(z);
   const half=W*(0.008+p.depth*0.105);
   const x=p.center+side*half;
   if(i===0)ctx.moveTo(x,p.y);else ctx.lineTo(x,p.y);
  }
  ctx.stroke();
 }

 // Vạch giữa đường uốn theo đường cong
 ctx.strokeStyle="#e8d7a7";ctx.lineWidth=2;
 ctx.setLineDash([10,15]);ctx.lineDashOffset=-pz*12;
 ctx.beginPath();
 for(let i=0;i<=segments;i++){
  const z=pz+90-(i/segments)*90;
  const p=project(z);
  if(i===0)ctx.moveTo(p.center,p.y);else ctx.lineTo(p.center,p.y);
 }
 ctx.stroke();ctx.setLineDash([]);
}

// Rừng rậm: nhiều cây lớn, tán cây dày, mọc sát đất.
// Vị trí từng cây cố định theo z trong thế giới.
function drawForest(){
 for(let i=0;i<100;i++){
  const z=i*2.65+3;
  const dz=z-pz;
  if(dz< -2||dz>95)continue;

  const p=project(z);
  const depth=p.depth;
  const size=(18+depth*155);
  const sideDistance=W*(0.10+depth*0.42);
  const jitter=(Math.sin(i*45.7)*W*0.045);

  for(const side of [-1,1]){
   const x=p.center+side*sideDistance+jitter;
   const groundY=p.y+size*0.05;

   // Thân cây: gốc luôn đặt tại mặt đất
   ctx.fillStyle=["#3d2b1c","#523824","#60442a"][i%3];
   ctx.fillRect(x-size*.13,groundY-size*.72,size*.26,size*.72);

   // Cành lớn
   ctx.strokeStyle="#49321e";
   ctx.lineWidth=Math.max(2,size*.10);
   ctx.beginPath();
   ctx.moveTo(x,groundY-size*.32);
   ctx.lineTo(x-size*.35,groundY-size*.58);
   ctx.moveTo(x,groundY-size*.40);
   ctx.lineTo(x+size*.34,groundY-size*.60);
   ctx.stroke();

   // Tán nhiều lớp để tạo cảm giác rừng rậm
   const greens=["#123d24","#17502b","#1d5c30",
                 "#246b35","#2d7338"];
   ctx.fillStyle=greens[i%greens.length];
   ctx.beginPath();
   ctx.arc(x,groundY-size*.82,size*.42,0,Math.PI*2);
   ctx.arc(x-size*.28,groundY-size*.70,size*.34,0,Math.PI*2);
   ctx.arc(x+size*.28,groundY-size*.70,size*.34,0,Math.PI*2);
   ctx.arc(x,groundY-size*1.03,size*.31,0,Math.PI*2);
   ctx.fill();

   // Tán phụ làm rừng kín hơn
   ctx.fillStyle=greens[(i+2)%greens.length];
   ctx.beginPath();
   ctx.arc(x-size*.17,groundY-size*.90,size*.22,0,Math.PI*2);
   ctx.arc(x+size*.18,groundY-size*.88,size*.23,0,Math.PI*2);
   ctx.fill();
  }
 }
}

// Đá quý nằm ở những vị trí cố định trên đường.
// Chúng chỉ biến mất khi người chơi nhặt được.
function drawGems(){
 for(let i=0;i<gemPositions.length;i++){
  if(collected.has(i))continue;
  const g=gemPositions[i];
  const dz=g.z-pz;
  if(dz<0.5||dz>90)continue;

  const p=project(g.z);
  const x=p.center+(g.x-px)*W*(0.025+p.depth*.13);
  const y=p.y-5-p.depth*12;
  const r=4+p.depth*17;

  ctx.save();
  ctx.translate(x,y);
  ctx.shadowBlur=16;ctx.shadowColor=g.color;
  ctx.fillStyle=g.color;
  ctx.beginPath();
  ctx.moveTo(0,-r);
  ctx.lineTo(r*.7,-r*.2);
  ctx.lineTo(r*.5,r*.8);
  ctx.lineTo(0,r);
  ctx.lineTo(-r*.5,r*.8);
  ctx.lineTo(-r*.7,-r*.2);
  ctx.closePath();ctx.fill();
  ctx.restore();
 }
}

// Cây cổ thụ được đặt ở cuối đường tại TREE_Z.
// Không tạo vị trí mới theo nhân vật; chỉ phối cảnh thay đổi khi tiến gần.
function drawAncientTree(){
 const dz=TREE_Z-pz;
 if(dz< -4||dz>100)return;

 const p=project(TREE_Z);
 const x=p.center;
 const y=p.y;
 const size=22+p.depth*190;

 // Thân lớn
 ctx.fillStyle="#49321f";
 ctx.fillRect(x-size*.13,y-size*.70,size*.26,size*.70);

 // Cành
 ctx.strokeStyle="#49321f";
 ctx.lineWidth=Math.max(4,size*.09);
 ctx.beginPath();
 ctx.moveTo(x,y-size*.30);
 ctx.lineTo(x-size*.36,y-size*.60);
 ctx.moveTo(x,y-size*.42);
 ctx.lineTo(x+size*.36,y-size*.61);
 ctx.stroke();

 // Tán cổ thụ
 ctx.fillStyle=treeGreen?"#36db51":"#655c42";
 ctx.beginPath();
 ctx.arc(x,y-size*.78,size*.34,0,Math.PI*2);
 ctx.arc(x-size*.25,y-size*.65,size*.28,0,Math.PI*2);
 ctx.arc(x+size*.25,y-size*.65,size*.28,0,Math.PI*2);
 ctx.arc(x,y-size*.96,size*.26,0,Math.PI*2);
 ctx.fill();

 if(treeGreen){
  ctx.save();
  ctx.globalAlpha=.8;
  const beam=ctx.createLinearGradient(x,0,x,y);
  beam.addColorStop(0,"#eaff9a00");
  beam.addColorStop(.5,"#d7ff8b99");
  beam.addColorStop(1,"#eaff9a00");
  ctx.fillStyle=beam;
  ctx.beginPath();
  ctx.moveTo(x-size*.15,y-size*.95);
  ctx.lineTo(x+size*.15,y-size*.95);
  ctx.lineTo(x+size*.8,0);
  ctx.lineTo(x-size*.8,0);
  ctx.closePath();ctx.fill();
  ctx.restore();
 }

 if(dz<32&&dz>0){
  ctx.fillStyle="white";
  ctx.font="bold 16px Arial";
  ctx.textAlign="center";
  ctx.fillText(gems>=5?"CÂY CỔ THỤ":"Hãy tìm 5 viên đá quý",x,y-size*1.12);
 }
}

// Nhân vật luôn đứng gần giữa phía dưới màn hình
function drawPlayer(){
 const x=W*.5,y=H*.83;
 const moving=Math.abs(joyX)>.1||Math.abs(joyY)>.1||
  keys["w"]||keys["a"]||keys["s"]||keys["d"]||
  keys["arrowup"]||keys["arrowdown"]||
  keys["arrowleft"]||keys["arrowright"];
 const stride=moving?Math.sin(performance.now()*.018)*7:0;

 ctx.fillStyle="#07160b88";
 ctx.beginPath();ctx.ellipse(x,y+4,27,9,0,0,Math.PI*2);ctx.fill();

 ctx.strokeStyle="#202a35";ctx.lineWidth=12;ctx.lineCap="round";
 ctx.beginPath();
 ctx.moveTo(x-8,y-29);ctx.lineTo(x-10-stride,y-4);
 ctx.moveTo(x+8,y-29);ctx.lineTo(x+10+stride,y-4);
 ctx.stroke();

 ctx.fillStyle=gender==="girl"?"#e95b9d":"#3585e8";
 ctx.beginPath();ctx.roundRect(x-19,y-70,38,43,10);ctx.fill();

 ctx.strokeStyle=gender==="girl"?"#e95b9d":"#3585e8";
 ctx.lineWidth=10;ctx.beginPath();
 ctx.moveTo(x-17,y-62);ctx.lineTo(x-28,y-39);
 ctx.moveTo(x+17,y-62);ctx.lineTo(x+28,y-39);
 ctx.stroke();

 ctx.fillStyle="#e9b98c";
 ctx.beginPath();ctx.arc(x,y-82,16,0,Math.PI*2);ctx.fill();

 ctx.fillStyle="#392719";
 ctx.beginPath();ctx.arc(x,y-87,17,Math.PI,Math.PI*2);
 ctx.lineTo(x+16,y-79);ctx.lineTo(x-16,y-79);ctx.fill();

 if(gender==="girl"){
  ctx.beginPath();ctx.arc(x-15,y-78,6,0,Math.PI*2);
  ctx.arc(x+15,y-78,6,0,Math.PI*2);ctx.fill();
 }
}

function update(dt){
 if(!running||won)return;

 let dx=0,dz=0;
 if(keys["arrowleft"]||keys["a"])dx--;
 if(keys["arrowright"]||keys["d"])dx++;
 if(keys["arrowup"]||keys["w"])dz++;
 if(keys["arrowdown"]||keys["s"])dz--;

 dx+=joyX;dz-=joyY;
 const len=Math.hypot(dx,dz);
 if(len>1){dx/=len;dz/=len;}

 const speed=dt*.012;
 px=Math.max(-3.5,Math.min(3.5,px+dx*speed*2.2));
 pz=Math.max(0,Math.min(WORLD_END,pz+dz*speed*3.5));

 // Nhặt đá quý theo khoảng cách thực tế trong thế giới
 for(let i=0;i<gemPositions.length;i++){
  if(collected.has(i))continue;
  const g=gemPositions[i];
  if(Math.abs(g.z-pz)<1.8&&Math.abs(g.x-px)<1.8){
   collected.add(i);
   gems++;
   updateHud();
  }
 }

 // Chạm tới cây cổ thụ và đã có ít nhất 5 viên thì thắng
 if(pz>=TREE_Z-2&&gems>=5){
  won=true;treeGreen=true;
  document.getElementById("winText").textContent=
   "Chúc mừng "+playerName+"! Em đã thu thập đủ đá quý và hồi sinh cây cổ thụ.";
  document.getElementById("win").style.display="flex";
 }
}

function draw(){
 drawSky();
 drawRoad();
 drawForest();
 drawGems();
 drawAncientTree();
 drawPlayer();
}

function frame(t){
 const dt=Math.min(40,t-(lastTime||t));
 lastTime=t;
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
