
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Chim Cánh Cụt Vượt Băng 3D",
    page_icon="🐧",
    layout="wide"
)

GAME = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
*{box-sizing:border-box}
body{margin:0;font-family:Arial,sans-serif;background:#08243c;color:white}
#wrap{position:relative;width:100%;height:700px;overflow:hidden;background:linear-gradient(#63c7ed,#d7f6ff)}
#game{width:100%;height:100%;display:block}
#hud{position:absolute;top:10px;left:10px;right:10px;display:flex;justify-content:space-between;gap:8px;pointer-events:none}
.pill{background:#062944e8;border:2px solid #b8f2ff;border-radius:14px;padding:9px 12px;font-weight:bold;font-size:14px}
#question{position:absolute;top:65px;left:50%;transform:translateX(-50%);width:min(94%,560px);background:#082c4ded;border:2px solid #b7efff;border-radius:16px;padding:12px;text-align:center;display:none}
#qtext{font-size:17px;font-weight:bold;margin-bottom:10px}
#answers{
  display:grid;
  grid-template-columns:repeat(4,minmax(0,1fr));
  gap:6px;
}
.answer{
  background:#e9faff;
  color:#082b46;
  border:2px solid #73d9f7;
  border-radius:10px;
  padding:10px 3px;
  font-size:14px;
  font-weight:bold;
  text-align:center;
  overflow-wrap:anywhere;
}
x solid #73d9f7;border-radius:10px;padding:9px 5px;font-size:14px;font-weight:bold}
#message{position:absolute;bottom:105px;left:50%;transform:translateX(-50%);background:#062944e8;border-radius:12px;padding:9px 13px;text-align:center;width:max-content;max-width:94%;font-weight:bold}
#overlay{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:#04182dbb;padding:16px}
#panel{width:min(94%,440px);max-height:94%;overflow:auto;text-align:center;background:linear-gradient(145deg,#146c8c,#071c3d);border:3px solid #80eaff;border-radius:24px;padding:23px 20px;box-shadow:0 10px 35px #00152699}
#panel h1{color:#8df0ff;font-size:26px;margin:0 0 14px}
#panel p{line-height:1.5}
.mainbtn{border:2px solid white;border-radius:14px;background:#ffcb4d;color:#15263d;font-size:17px;font-weight:bold;padding:13px 26px;margin:8px;cursor:pointer}
#controls{position:absolute;bottom:10px;left:10px;right:10px;display:flex;justify-content:space-between;align-items:end}
.pad{display:grid;grid-template-columns:repeat(3,48px);grid-template-rows:repeat(2,44px);gap:5px}
.ctrl{border:2px solid #d5f7ff;background:#062944dd;color:white;border-radius:13px;font-size:22px;font-weight:bold;touch-action:manipulation}
#jump{height:70px;min-width:95px;border-radius:50%;background:#ffcb4d;color:#10263c;border:3px solid white;font-weight:bold;font-size:16px;touch-action:manipulation}
.small{font-size:12px;opacity:.9}
@media(max-width:520px){#wrap{height:690px}#question{top:60px}#qtext{font-size:15px}.answer{font-size:12px;padding:8px 3px}#panel h1{font-size:22px}.pill{font-size:12px;padding:7px}}
</style>
</head>
<body>
<div id="wrap">
<canvas id="game"></canvas>
<div id="hud">
  <div class="pill" id="stage">🐧 CHẶNG ĐI</div>
  <div class="pill" id="progress">Hàng 1/8</div>
</div>
<div id="question">
  <div id="qtext"></div>
  <div id="answers"></div>
</div>
<div id="message">Nhấn BẮT ĐẦU để chơi!</div>
<div id="controls">
  <div class="pad">
    <div></div><button class="ctrl" id="up">↑</button><div></div>
    <button class="ctrl" id="left">←</button><button class="ctrl" id="down">↓</button><button class="ctrl" id="right">→</button>
  </div>
  <button id="jump">NHẢY<br>SPACE</button>
</div>
<div id="overlay">
  <div id="panel">
    <h1>🐧 CHIM CÁNH CỤT VƯỢT BĂNG</h1>
    <p><b>CHẶNG ĐI:</b> Nhảy lên tảng băng có đáp án đúng để vượt qua 8 hàng câu hỏi.</p>
    <p>🐟 Lấy xô cá rồi quay về bờ xuất phát.</p>
    <p>🧊 Đường về mỗi hàng có 2 tảng băng yếu và 2 tảng an toàn. Rơi xuống nước sẽ được thử lại, vị trí băng yếu thay đổi.</p>
    <p>⌨️ Laptop: phím ← → để chọn hướng, SPACE để nhảy.</p>
    <p>📱 Điện thoại: dùng các nút điều khiển trên màn hình.</p>
    <button class="mainbtn" id="start">BẮT ĐẦU</button>
    <p class="small">Trò chơi kiến thức lớp 8 • 3D</p>
  </div>
</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
(function(){
"use strict";
const $=id=>document.getElementById(id);
const canvas=$("game");
if(!window.THREE){
  $("message").textContent="Không tải được thư viện 3D. Hãy kiểm tra Internet rồi tải lại trang.";
  $("start").addEventListener("click",function(){
    $("panel").innerHTML="<h1>Không tải được 3D</h1><p>Hãy kiểm tra kết nối Internet rồi nhấn F5 để tải lại.</p>";
  });
  return;
}
let scene,camera,renderer,clock;
try{
  scene=new THREE.Scene();
  scene.background=new THREE.Color(0x79d5f2);
  scene.fog=new THREE.Fog(0x79d5f2,35,150);
  camera=new THREE.PerspectiveCamera(60,1,0.1,250);
  renderer=new THREE.WebGLRenderer({canvas:canvas,antialias:true});
  renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
  renderer.shadowMap.enabled=true;
  renderer.shadowMap.type=THREE.PCFSoftShadowMap;
  clock=new THREE.Clock();
}catch(e){
  $("message").textContent="Trình duyệt chưa khởi tạo được đồ họa 3D. Hãy thử Chrome mới nhất.";
  return;
}
scene.add(new THREE.HemisphereLight(0xdff8ff,0x3b718b,2.0));
const sun=new THREE.DirectionalLight(0xffffff,2.2);
sun.position.set(-10,22,12);
sun.castShadow=true;
scene.add(sun);

const mat=(color,roughness)=>new THREE.MeshStandardMaterial({color:color,roughness:roughness===undefined?0.75:roughness});
const waterMat=new THREE.MeshStandardMaterial({color:0x168fce,roughness:0.25,metalness:0.12});
const iceMat=mat(0xb9efff,0.22);
const iceTop=mat(0xe9fcff,0.2);
const weakMat=mat(0x82cce5,0.25);
const darkMat=mat(0x142332);
const whiteMat=mat(0xffffff);
const orangeMat=mat(0xffa629);
const blackMat=mat(0x101923);
const brownMat=mat(0x754a27);
const snowMat=mat(0xffffff);

const floor=new THREE.Mesh(new THREE.PlaneGeometry(180,220),waterMat);
floor.rotation.x=-Math.PI/2;
floor.position.set(0,-0.65,-60);
floor.receiveShadow=true;
scene.add(floor);

function box(w,h,d,material,x,y,z){
  const mesh=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material);
  mesh.position.set(x,y,z);
  mesh.castShadow=true;
  mesh.receiveShadow=true;
  scene.add(mesh);
  return mesh;
}
function makeShore(z){
  box(22,0.7,12,mat(0xe8f0d2),0,-0.25,z);
  for(let i=0;i<18;i++){
    const x=(Math.random()-0.5)*20;
    const tree= new THREE.Group();
    const trunk=new THREE.Mesh(new THREE.CylinderGeometry(0.12,0.2,2,7),brownMat);
    trunk.position.y=1;
    tree.add(trunk);
    const crown=new THREE.Mesh(new THREE.ConeGeometry(1.1,2.7,7),mat(i%2?0x32865b:0x24734d));
    crown.position.y=2.7;
    tree.add(crown);
    tree.position.set(x,0,z+(Math.random()-0.5)*9);
    scene.add(tree);
  }
}
makeShore(20);
makeShore(-91);

// Tạo chim cánh cụt 3D
const penguin=new THREE.Group();
scene.add(penguin);
const body=new THREE.Mesh(new THREE.SphereGeometry(0.65,20,16),darkMat);
body.scale.set(0.82,1.25,0.7);
body.position.y=1.0;
body.castShadow=true;
penguin.add(body);
const belly=new THREE.Mesh(new THREE.SphereGeometry(0.49,18,14),whiteMat);
belly.scale.set(0.78,1.0,0.35);
belly.position.set(0,0.95,0.37);
penguin.add(belly);
const head=new THREE.Mesh(new THREE.SphereGeometry(0.43,18,14),darkMat);
head.position.set(0,2.05,0.03);
penguin.add(head);
const eyeMat=mat(0xffffff,0.3);
for(const x of [-0.15,0.15]){
  const eye=new THREE.Mesh(new THREE.SphereGeometry(0.075,10,8),eyeMat);
  eye.position.set(x,2.1,0.405);
  penguin.add(eye);
  const pupil=new THREE.Mesh(new THREE.SphereGeometry(0.035,8,6),blackMat);
  pupil.position.set(x,2.1,0.47);
  penguin.add(pupil);
}
const beak=new THREE.Mesh(new THREE.ConeGeometry(0.14,0.34,8),orangeMat);
beak.rotation.x=Math.PI/2;
beak.position.set(0,1.96,0.53);
penguin.add(beak);
for(const x of [-0.65,0.65]){
  const wing=new THREE.Mesh(new THREE.SphereGeometry(0.22,12,10),darkMat);
  wing.scale.set(0.65,1.5,0.45);
  wing.position.set(x,1.0,0);
  wing.rotation.z=x<0?0.2:-0.2;
  penguin.add(wing);
}
for(const x of [-0.28,0.28]){
  const foot=new THREE.Mesh(new THREE.BoxGeometry(0.32,0.12,0.43),orangeMat);
  foot.position.set(x,0.12,0.18);
  penguin.add(foot);
}
function makeBucket(){
  const group=new THREE.Group();
  const bucket=new THREE.Mesh(new THREE.CylinderGeometry(0.35,0.25,0.48,12,1,true),mat(0xd6e1e8));
  bucket.position.y=0.3;
  group.add(bucket);
  const rim=new THREE.Mesh(new THREE.TorusGeometry(0.34,0.035,8,18),mat(0xffffff));
  rim.rotation.x=Math.PI/2;
  rim.position.y=0.54;
  group.add(rim);
  for(let i=0;i<3;i++){
    const fish=new THREE.Mesh(new THREE.SphereGeometry(0.1,8,6),i%2?orangeMat:mat(0x9bd8ed));
    fish.scale.set(1,0.6,1.7);
    fish.position.set((i-1)*0.13,0.52,0);
    group.add(fish);
  }
  group.position.set(0,0.1,0.7);
  group.visible=false;
  penguin.add(group);
  return group;
}
const bucket=makeBucket();

const questions=[
 {q:"Toán: Phân tích x² − 9 thành nhân tử.",a:["(x−3)(x+3)","(x−9)(x+1)","(x−3)²","x(x−9)"],c:0},
 {q:"Toán: Hình bình hành có hai đường chéo…",a:["Luôn bằng nhau","Cắt nhau tại trung điểm mỗi đường","Luôn vuông góc","Không cắt nhau"],c:1},
 {q:"KHTN: Đơn vị của lực là gì?",a:["Jun (J)","Oát (W)","Niutơn (N)","Mét (m)"],c:2},
 {q:"Hóa học: Công thức hóa học của nước là gì?",a:["CO₂","O₂","H₂","H₂O"],c:3},
 {q:"Sinh học: Cơ quan chủ yếu trao đổi khí ở người là…",a:["Phổi","Dạ dày","Thận","Gan"],c:0},
 {q:"Địa lí: Đường xích đạo chia Trái Đất thành…",a:["Đông và Tây","Bắc và Nam","4 đại dương","3 phần"],c:1},
 {q:"Lịch sử: Chiến thắng Bạch Đằng năm 938 gắn với ai?",a:["Trần Hưng Đạo","Lê Lợi","Ngô Quyền","Quang Trung"],c:2},
 {q:"Tiếng Anh: Quá khứ của “go” là…",a:["Goed","Gone yesterday","Going","Went"],c:3}
];
let rows=[];
const laneX=[-4.2,-1.4,1.4,4.2];
const startZ=8;
const stepZ=10;
for(let r=0;r<8;r++){
  const z=startZ-(r+1)*stepZ;
  const row={z:z,platforms:[],labels:[],gate:null,weak:[],q:null};
  for(let lane=0;lane<4;lane++){
    const g=new THREE.Group();
    const base=new THREE.Mesh(new THREE.BoxGeometry(2.25,0.38,2.5),iceMat);
    base.position.y=0;
    base.castShadow=true;
    base.receiveShadow=true;
    g.add(base);
    const top=new THREE.Mesh(new THREE.BoxGeometry(2.12,0.06,2.35),iceTop);
    top.position.y=0.22;
    g.add(top);
    g.position.set(laneX[lane],-0.1,z);
    scene.add(g);
    row.platforms.push({group:g,base:base,top:top});
  }
  row.gate=box(12,2.5,0.25,mat(0x557b92),0,1.1,z+4.3);
  rows.push(row);
}
function makeLabel(text,x,y,z){
  const c=document.createElement("canvas");
  c.width=256;c.height=128;
  const ctx=c.getContext("2d");
  ctx.fillStyle="#083653";
  ctx.fillRect(0,0,256,128);
  ctx.strokeStyle="#ffffff";ctx.lineWidth=8;
  ctx.strokeRect(4,4,248,120);
  ctx.fillStyle="#ffffff";ctx.font="bold 60px Arial";
  ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText(text,128,64);
  const texture=new THREE.CanvasTexture(c);
  const sprite=new THREE.Sprite(new THREE.SpriteMaterial({map:texture,transparent:false}));
  sprite.scale.set(2.1,1.05,1);
  sprite.position.set(x,y,z);
  scene.add(sprite);
  return sprite;
}
function shuffle(arr){
  const a=arr.slice();
  for(let i=a.length-1;i>0;i--){
    const j=Math.floor(Math.random()*(i+1));
    [a[i],a[j]]=[a[j],a[i]];
  }
  return a;
}
function clearLabels(){
  rows.forEach(row=>{
    row.labels.forEach(label=>{
      scene.remove(label);
      if(label.material.map)label.material.map.dispose();
      label.material.dispose();
    });
    row.labels=[];
  });
}
function prepareQuestions(){
  clearLabels();
  const shuffledQ=shuffle(questions);
  rows.forEach((row,r)=>{
    row.q=shuffledQ[r];
   const order=[0,1,2,3];
row.correctLane=row.q.c;

order.forEach((answerIndex,lane)=>{
  const letter=["A","B","C","D"][answerIndex];
  row.labels.push(
    makeLabel(letter,laneX[lane],0.9,row.z)
  );
});
  });
}
function setWeakPlatforms(){
  rows.forEach(row=>{
    row.weak=shuffle([0,1,2,3]).slice(0,2);
    row.platforms.forEach((p,lane)=>{
      p.base.material=row.weak.includes(lane)?weakMat:iceMat;
      p.top.material=row.weak.includes(lane)?weakMat:iceTop;
      p.base.scale.set(1,1,1);
      p.group.visible=true;
    });
  });
}
let phase="intro";
let running=false;
let lane=1;
let rowIndex=0;
let returnIndex=7;
let jumpStart=null;
let jumpFromZ=18;
let jumpToZ=18;
let jumpFromX=laneX[1];
let jumpToX=laneX[1];
let messageTimer=null;
function say(text){$("message").textContent=text;}
function updateHUD(){
  if(phase==="out"){
    $("stage").textContent="🐧 CHẶNG ĐI";
    $("progress").textContent="Hàng "+Math.min(rowIndex+1,8)+"/8";
  }else if(phase==="return"){
    $("stage").textContent="🐟 MANG CÁ VỀ";
    $("progress").textContent="Còn "+(returnIndex+1)+" hàng";
  }else{
    $("stage").textContent="🐧 CHIM CÁNH CỤT";
  }
}
function showQuestion(){
  const row=rows[rowIndex];
  $("question").style.display="block";
  $("qtext").textContent="Câu "+(rowIndex+1)+"/8: "+row.q.q;
  $("answers").innerHTML="";
  row.q.a.forEach((answer,i)=>{
    const b=document.createElement("div");
    b.className="answer";
    b.textContent=["A. ","B. ","C. ","D. "][i]+answer;
    $("answers").appendChild(b);
  });
}
function hideQuestion(){$("question").style.display="none";}
function startGame(){
  $("overlay").style.display="none";
  prepareQuestions();
  setWeakPlatforms();
  phase="out";
  running=true;
  rowIndex=0;returnIndex=7;lane=1;
  bucket.visible=false;
  penguin.position.set(laneX[lane],0,18);
  jumpStart=null;
  rows.forEach(row=>{row.gate.visible=true;row.gate.position.y=1.1;});
  showQuestion();
  updateHUD();
  say("Dùng ← → chọn tảng băng, rồi nhấn SPACE để nhảy!");
}
function showPanel(title,body,buttonText,callback){
  $("overlay").style.display="flex";
  $("panel").innerHTML="";
  const h=document.createElement("h1");h.textContent=title;$("panel").appendChild(h);
  const p=document.createElement("p");p.textContent=body;$("panel").appendChild(p);
  const b=document.createElement("button");b.className="mainbtn";b.textContent=buttonText;
  b.addEventListener("click",callback);$("panel").appendChild(b);
}
function startReturn(){
  phase="return";running=true;returnIndex=7;lane=1;
  bucket.visible=true;
  penguin.position.set(laneX[lane],0,rows[7].z+4);
  rows.forEach(row=>{row.gate.visible=false;});
  hideQuestion();updateHUD();
  say("Đang mang xô cá về! Cẩn thận băng yếu nhé.");
}
function retryReturn(){
  setWeakPlatforms();
  lane=1;returnIndex=7;
  penguin.position.set(laneX[lane],0,rows[7].z+4);
  jumpStart=null;phase="return";running=true;
  $("overlay").style.display="none";
  updateHUD();
  say("Vị trí băng yếu đã đổi! Thử đường về lần nữa.");
}
function fallReturn(){
  running=false;jumpStart=null;
  penguin.position.set(laneX[1],0,18);
  showPanel("💦 Ôi! Băng vỡ mất rồi!","Em vẫn giữ được xô cá. Vị trí 2 tảng băng yếu mỗi hàng sẽ được xáo lại khi thử lại.","THỬ LẠI ĐƯỜNG VỀ",retryReturn);
}
function winGame(){
  running=false;phase="win";hideQuestion();
  showPanel("🏆 CHIẾN THẮNG!","Em đã vượt qua 8 câu hỏi, né được băng yếu và mang xô cá về bờ an toàn! 🐧🐟","CHƠI LẠI",startGame);
}
function failQuestion(){
  running=false;hideQuestion();
  showPanel("💙 Thử lại nhé!","Chưa đúng đáp án rồi. Em có thể bắt đầu lại chặng đi và thử lần nữa.","CHƠI LẠI CHẶNG ĐI",startGame);
}
function jump(){
  if(!running||jumpStart!==null)return;
  jumpStart=clock.elapsedTime;
  jumpFromX=penguin.position.x;
  jumpToX=laneX[lane];
  jumpFromZ=penguin.position.z;
  if(phase==="out"){
    jumpToZ=rows[rowIndex].z;
    say("Đang nhảy tới tảng băng...");
  }else if(phase==="return"){
    jumpToZ=returnIndex>0?rows[returnIndex-1].z:18;
    say("Đang nhảy qua băng...");
  }
}
function land(){
  jumpStart=null;
  if(phase==="out"){
    const row=rows[rowIndex];
    if(lane!==row.correctLane){
      failQuestion();return;
    }
    row.gate.visible=false;
    say("🎉 Chính xác! Vách chắn đã hạ xuống!");
    rowIndex++;
    if(rowIndex>=8){
      hideQuestion();phase="fish";running=false;bucket.visible=true;
      updateHUD();
      showPanel("🐟 Đã lấy được xô cá!","Giờ hãy quay về bờ xuất phát. Mỗi hàng đường về có 2 tảng băng yếu và 2 tảng an toàn.","BẮT ĐẦU ĐƯỜNG VỀ",startReturn);
      return;
    }
    showQuestion();updateHUD();
  }else if(phase==="return"){
    const targetIndex=returnIndex-1;
    if(targetIndex>=0&&rows[targetIndex].weak.includes(lane)){
      const p=rows[targetIndex].platforms[lane];
      p.base.material=mat(0x47798a);
      p.top.material=mat(0x47798a);
      fallReturn();return;
    }
    returnIndex=targetIndex;
    updateHUD();
    if(returnIndex<0){
      winGame();return;
    }
    say("Băng an toàn! Tiếp tục nhé!");
  }
}
function moveLeft(){if(!running||jumpStart!==null)return;lane=Math.max(0,lane-1);}
function moveRight(){if(!running||jumpStart!==null)return;lane=Math.min(3,lane+1);}
$("start").addEventListener("click",startGame);
$("left").addEventListener("click",moveLeft);
$("right").addEventListener("click",moveRight);
$("up").addEventListener("click",jump);
$("down").addEventListener("click",jump);
$("jump").addEventListener("click",jump);
window.addEventListener("keydown",function(e){
  if(["ArrowLeft","ArrowRight","ArrowUp","ArrowDown"," "].includes(e.key))e.preventDefault();
  if(e.key==="ArrowLeft"||e.key.toLowerCase()==="a")moveLeft();
  if(e.key==="ArrowRight"||e.key.toLowerCase()==="d")moveRight();
  if(e.key===" "||e.key==="ArrowUp"||e.key==="ArrowDown")jump();
});
function resize(){
  const w=canvas.clientWidth||window.innerWidth;
  const h=canvas.clientHeight||700;
  renderer.setSize(w,h,false);
  camera.aspect=w/h;
  camera.updateProjectionMatrix();
}
window.addEventListener("resize",resize);
resize();
camera.position.set(0,7,28);
camera.lookAt(0,1,-15);
function animate(){
  requestAnimationFrame(animate);
  const dt=clock.getDelta();
  const elapsed=clock.elapsedTime;
  if(running){
    const targetX=laneX[lane];
    if(jumpStart!==null){
      const t=Math.min(1,(elapsed-jumpStart)/0.65);
      penguin.position.x=jumpFromX+(jumpToX-jumpFromX)*t;
      penguin.position.z=jumpFromZ+(jumpToZ-jumpFromZ)*t;
      penguin.position.y=Math.sin(t*Math.PI)*2.1;
      penguin.rotation.z=(jumpToX-jumpFromX)*0.04;
      if(t>=1){
        penguin.position.y=0;
        penguin.rotation.z=0;
        land();
      }
    }else{
      penguin.position.x+=(targetX-penguin.position.x)*Math.min(1,dt*10);
      penguin.position.y=0.04*Math.sin(elapsed*5);
    }
  }
  // Camera luôn nhìn từ sau lưng chim cánh cụt
  const desiredCam=new THREE.Vector3(penguin.position.x*0.35,7,penguin.position.z+12);
  camera.position.lerp(desiredCam,0.055);
  camera.lookAt(penguin.position.x*0.35,1.3,penguin.position.z-12);
  renderer.render(scene,camera);
}
animate();
updateHUD();
})();
</script>
</body>
</html>
"""

components.html(GAME, height=710, scrolling=False)
