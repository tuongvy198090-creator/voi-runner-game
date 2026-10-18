
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Giải cứu thế giới",
    page_icon="🌳",
    layout="wide"
)

st.markdown("""
<style>
#MainMenu,footer,header{visibility:hidden}
.block-container{padding:0!important;max-width:100%!important}
iframe{border:0!important}
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
 background:linear-gradient(#102d20ed,#07180df5)
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
 <p>Hãy tìm đá quý và giải cứu cây cổ thụ!</p>
</div>

<div id="hud" style="display:none">
 🌟 Người chơi: <span id="nameLabel"></span><br>
 💎 Đá quý: <span id="gemsLabel">0</span>/5<br>
 🌳 Hãy khám phá khu rừng!
</div>

<div id="help" style="display:none">
 <b>DI CHUYỂN</b><br>
 Máy tính: WASD hoặc phím mũi tên<br>
 Kéo nút tròn để di chuyển
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
addEventListener("resize",resize);
resize();

let running=false,won=false,treeGreen=false;
let playerName="Nhà thám hiểm",gender="boy";
let px=0,pz=0,gems=0,lastTime=0;
let keys={},joyX=0,joyY=0;
let collected=new Set();

const WORLD_END=220;
const TREE_Z=210;

// Chỉ có 12 viên đá quý.
// Mỗi viên có tọa độ thế giới cố định: x là vị trí ngang, z là vị trí xa/gần.
const gemPositions=[
 {x:-3.0,z:18,color:"#58f5ff"},
 {x: 2.8,z:34,color:"#ff72e8"},
 {x:-4.0,z:49,color:"#fff36b"},
 {x: 4.0,z:66,color:"#a8a0ff"},
 {x: 1.8,z:83,color:"#76ff8b"},
 {x:-2.8,z:101,color:"#58f5ff"},
 {x: 4.2,z:121,color:"#ff72e8"},
 {x:-4.1,z:139,color:"#fff36b"},
 {x: 2.6,z:157,color:"#a8a0ff"},
 {x:-3.7,z:174,color:"#76ff8b"},
 {x: 3.8,z:191,color:"#58f5ff"},
 {x: 0.8,z:201,color:"#ff72e8"}
];

// Đường uốn cong cố định, không tạo đường mới khi di chuyển.
function roadCurve(z){
 return Math.sin(z*0.035)*1.15
      + Math.sin(z*0.078)*0.38
      + Math.sin(z*0.014)*0.65;
}

// Phép chiếu từ thế giới ra màn hình.
// Tọa độ z của vật thể không đổi; chỉ phối cảnh thay đổi khi người chơi tiến lên.
function project(z){
 const dz=z-pz;
 const depth=Math.max(0,Math.min(1,1-dz/90));
 const y=H*0.405+depth*depth*H*0.66;
 const center=W*0.5+roadCurve(z)*W*0.055;
 return {x:center,y,depth,center};
}

function worldXToScreen(worldX,z){
 const p=project(z);
 return p.center+(worldX-px)*W*(0.025+p.depth*0.13);
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

// Joystick
const joystick=document.getElementById("joystick");
const knob=document.getElementById("knob");
let joyActive=false;

function moveJoy(e){
 const r=joystick.getBoundingClientRect();
 let dx=e.clientX-(r.left+r.width/2);
 let dy=e.clientY-(r.top+r.height/2);
 const max=r.width*.32,len=Math.hypot(dx,dy);
 if(len>max){dx=dx/len*max;dy=dy/len*max;}
 joyX=dx/max;joyY=dy/max;
 knob.style.left=(r.width/2-26+dx)+"px";
 knob.style.top=(r.height/2-26+dy)+"px";
}

joystick.addEventListener("pointerdown",e=>{
 joyActive=true;
 joystick.setPointerCapture(e.pointerId);
 moveJoy(e);
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
 sky.addColorStop(.35,"#c6dfb0");
 sky.addColorStop(.405,"#355b32");
 sky.addColorStop(1,"#102519");
 ctx.fillStyle=sky;
 ctx.fillRect(0,0,W,H);

 ctx.fillStyle="#476f3c";
 ctx.beginPath();
 ctx.moveTo(0,H*.43);
 for(let x=0;x<=W;x+=25)
  ctx.lineTo(x,H*.39+Math.sin(x*.009)*H*.035);
 ctx.lineTo(W,H);
 ctx.lineTo(0,H);
 ctx.fill();
}

function drawRoad(){
 const segments=100;

 ctx.fillStyle="#92794b";
 ctx.beginPath();

 for(let i=0;i<=segments;i++){
  const dz=90-(i/segments)*90;
  const z=pz+dz;
  const p=project(z);
  const half=W*(.006+p.depth*.075);
  if(i===0)ctx.moveTo(p.center-half,p.y);
  else ctx.lineTo(p.center-half,p.y);
 }

 for(let i=segments;i>=0;i--){
  const dz=90-(i/segments)*90;
  const z=pz+dz;
  const p=project(z);
  const half=W*(.006+p.depth*.075);
  ctx.lineTo(p.center+half,p.y);
 }

 ctx.closePath();
 ctx.fill();

 ctx.strokeStyle="#b99a61";
 ctx.lineWidth=3;

 for(const side of [-1,1]){
  ctx.beginPath();
  for(let i=0;i<=segments;i++){
   const z=pz+90-(i/segments)*90;
   const p=project(z);
   const half=W*(.006+p.depth*.075);
   const x=p.center+side*half;
   if(i===0)ctx.moveTo(x,p.y);
   else ctx.lineTo(x,p.y);
  }
  ctx.stroke();
 }

 ctx.strokeStyle="#e8d7a7";
 ctx.lineWidth=2;
 ctx.setLineDash([10,15]);
 ctx.lineDashOffset=-pz*12;
 ctx.beginPath();

 for(let i=0;i<=segments;i++){
  const z=pz+90-(i/segments)*90;
  const p=project(z);
  if(i===0)ctx.moveTo(p.center,p.y);
  else ctx.lineTo(p.center,p.y);
 }
 ctx.stroke();
 ctx.setLineDash([]);
}

// Cây rừng lớn, dày đặc; từng cây có vị trí z cố định.
function drawForest(){
 for(let i=0;i<115;i++){
  const z=i*2.15+2;
  const dz=z-pz;
  if(dz< -2||dz>92)continue;

  const p=project(z);
  const depth=p.depth;
  const size=24+depth*190;

  for(const side of [-1,1]){
   const offset=(0.95+depth*4.5)
      +(Math.sin(i*43.71+side)*.45);
   const worldX=roadCurve(z)+side*offset;
   const x=worldXToScreen(worldX,z);
   const groundY=p.y+size*.04;

   // Thân cây
   ctx.fillStyle=["#3d2b1c","#523824","#60442a"][i%3];
   ctx.fillRect(x-size*.12,groundY-size*.72,size*.24,size*.72);

   // Cành lớn
   ctx.strokeStyle="#49321e";
   ctx.lineWidth=Math.max(2,size*.10);
   ctx.beginPath();
   ctx.moveTo(x,groundY-size*.30);
   ctx.lineTo(x-size*.34,groundY-size*.57);
   ctx.moveTo(x,groundY-size*.39);
   ctx.lineTo(x+size*.34,groundY-size*.59);
   ctx.stroke();

   // Nhiều lớp tán lá
   const greens=["#103a21","#154a28","#1a592e",
                 "#226832","#2b7138"];
   ctx.fillStyle=greens[i%greens.length];
   ctx.beginPath();
   ctx.arc(x,groundY-size*.79,size*.43,0,Math.PI*2);
   ctx.arc(x-size*.27,groundY-size*.68,size*.34,0,Math.PI*2);
   ctx.arc(x+size*.27,groundY-size*.68,size*.34,0,Math.PI*2);
   ctx.arc(x,groundY-size*1.02,size*.32,0,Math.PI*2);
   ctx.fill();

   ctx.fillStyle=greens[(i+2)%greens.length];
   ctx.beginPath();
   ctx.arc(x-size*.17,groundY-size*.90,size*.23,0,Math.PI*2);
   ctx.arc(x+size*.18,groundY-size*.89,size*.23,0,Math.PI*2);
   ctx.fill();
  }
 }
}

// Đá quý rải rác giữa rừng, không xếp thành hàng trên đường.
function drawGems(){
 for(let i=0;i<gemPositions.length;i++){
  if(collected.has(i))continue;

  const g=gemPositions[i];
  const dz=g.z-pz;
  if(dz<.5||dz>90)continue;

  const p=project(g.z);
  const x=worldXToScreen(g.x,g.z);
  const y=p.y-5-p.depth*12;
  const r=4+p.depth*16;

  ctx.save();
  ctx.translate(x,y);
  ctx.shadowBlur=15;
  ctx.shadowColor=g.color;
  ctx.fillStyle=g.color;

  ctx.beginPath();
  ctx.moveTo(0,-r);
  ctx.lineTo(r*.7,-r*.2);
  ctx.lineTo(r*.5,r*.8);
  ctx.lineTo(0,r);
  ctx.lineTo(-r*.5,r*.8);
  ctx.lineTo(-r*.7,-r*.2);
  ctx.closePath();
  ctx.fill();
  ctx.restore();
 }
}

// Cây cổ thụ rất lớn ở cuối đường.
// TREE_Z và tọa độ ngang của cây không phụ thuộc px của người chơi.
function drawAncientTree(){
 const dz=TREE_Z-pz;
 if(dz< -4||dz>100)return;

 const p=project(TREE_Z);
 const x=p.center;
 const y=p.y;

 // Kích thước lớn, tán rộng.
 const size=55+p.depth*300;

 // Bóng dưới gốc cây
 ctx.fillStyle="#09180b77";
 ctx.beginPath();
 ctx.ellipse(x,y,size*.48,size*.10,0,0,Math.PI*2);
 ctx.fill();

 // Thân cây to
 ctx.fillStyle="#49301c";
 ctx.beginPath();
 ctx.moveTo(x-size*.13,y);
 ctx.lineTo(x-size*.10,y-size*.72);
 ctx.lineTo(x+size*.10,y-size*.72);
 ctx.lineTo(x+size*.15,y);
 ctx.closePath();
 ctx.fill();

 // Rễ lớn
 ctx.strokeStyle="#49301c";
 ctx.lineWidth=Math.max(5,size*.075);
 ctx.lineCap="round";
 ctx.beginPath();
 ctx.moveTo(x,y-size*.18);
 ctx.lineTo(x-size*.35,y-size*.04);
 ctx.moveTo(x,y-size*.18);
 ctx.lineTo(x+size*.36,y-size*.04);
 ctx.stroke();

 // Cành vươn rộng
 ctx.lineWidth=Math.max(5,size*.055);
 ctx.beginPath();
 ctx.moveTo(x,y-size*.48);
 ctx.lineTo(x-size*.40,y-size*.70);
 ctx.lineTo(x-size*.48,y-size*.82);
 ctx.moveTo(x,y-size*.43);
 ctx.lineTo(x+size*.40,y-size*.68);
 ctx.lineTo(x+size*.49,y-size*.80);
 ctx.moveTo(x,y-size*.60);
 ctx.lineTo(x+size*.05,y-size*.88);
 ctx.stroke();

 // Tán cây khổng lồ, nhiều lớp
 ctx.fillStyle=treeGreen?"#28bb49":"#554d37";
 ctx.beginPath();
 ctx.arc(x,y-size*.88,size*.34,0,Math.PI*2);
 ctx.arc(x-size*.25,y-size*.78,size*.31,0,Math.PI*2);
 ctx.arc(x+size*.25,y-size*.78,size*.31,0,Math.PI*2);
 ctx.arc(x-size*.43,y-size*.72,size*.23,0,Math.PI*2);
 ctx.arc(x+size*.43,y-size*.72,size*.23,0,Math.PI*2);
 ctx.arc(x,y-size*1.10,size*.25,0,Math.PI*2);
 ctx.fill();

 if(treeGreen){
  // Ánh sáng bắn lên trời
  ctx.save();
  ctx.globalAlpha=.82;
  const beam=ctx.createLinearGradient(x,0,x,y);
  beam.addColorStop(0,"#eaff9a00");
  beam.addColorStop(.45,"#d7ff8bcc");
  beam.addColorStop(1,"#eaff9a00");
  ctx.fillStyle=beam;
  ctx.beginPath();
  ctx.moveTo(x-size*.20,y-size*1.08);
  ctx.lineTo(x+size*.20,y-size*1.08);
  ctx.lineTo(x+size*.85,0);
  ctx.lineTo(x-size*.85,0);
  ctx.closePath();
  ctx.fill();
  ctx.restore();
 }

 if(dz<38&&dz>0){
  ctx.fillStyle="white";
  ctx.font="bold 17px Arial";
  ctx.textAlign="center";
  ctx.fillText(
   gems>=5?"CÂY CỔ THỤ":"Hãy tìm đủ 5 viên đá quý",
   x,y-size*1.20
  );
 }
}

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
  ctx.beginPath();
  ctx.arc(x-15,y-78,6,0,Math.PI*2);
  ctx.arc(x+15,y-78,6,0,Math.PI*2);
  ctx.fill();
 }
}

function update(dt){
 if(!running||won)return;

 let dx=0,dz=0;
 if(keys["arrowleft"]||keys["a"])dx--;
 if(keys["arrowright"]||keys["d"])dx++;
 if(keys["arrowup"]||keys["w"])dz++;
 if(keys["arrowdown"]||keys["s"])dz--;

 dx+=joyX;
 dz-=joyY;

 const len=Math.hypot(dx,dz);
 if(len>1){dx/=len;dz/=len;}

 const speed=dt*.012;
 px=Math.max(-5,Math.min(5,px+dx*speed*2.2));
 pz=Math.max(0,Math.min(WORLD_END,pz+dz*speed*3.5));

 // Nhặt đá quý dựa vào tọa độ cố định trong thế giới
 for(let i=0;i<gemPositions.length;i++){
  if(collected.has(i))continue;
  const g=gemPositions[i];

  if(Math.abs(g.z-pz)<1.8&&Math.abs(g.x-px)<1.4){
   collected.add(i);
   gems++;
   updateHud();
  }
 }

 if(pz>=TREE_Z-2&&gems>=5){
  won=true;
  treeGreen=true;
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
