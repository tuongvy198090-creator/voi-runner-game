
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Vượt Băng Lấy Cá 3D",
    page_icon="🐧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

GAME = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;font-family:Arial,sans-serif;background:#b9eaff}
#game{position:relative;width:100%;height:100vh;min-height:600px;overflow:hidden}
#view{position:absolute;inset:0}
canvas{display:block;width:100%;height:100%}
#hud{position:absolute;top:10px;left:10px;right:10px;display:flex;justify-content:space-between;gap:8px;pointer-events:none}
.pill{background:#092c49dd;color:white;padding:9px 13px;border-radius:15px;font-size:14px;font-weight:bold;box-shadow:0 3px 12px #0003}
#quiz{position:absolute;top:62px;left:50%;transform:translateX(-50%);width:min(94%,780px);text-align:center;pointer-events:none}
#qtext{display:inline-block;max-width:100%;padding:11px 16px;border-radius:15px;background:#082b49ed;color:white;font-size:clamp(15px,2.5vw,22px);font-weight:bold;box-shadow:0 4px 15px #0003}
#answers{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px;margin-top:8px}
.ans{padding:8px 4px;border-radius:12px;background:#ffffffed;color:#12334b;border:2px solid #a7d9ef;font-size:clamp(11px,1.7vw,15px);font-weight:bold;overflow-wrap:anywhere}
#timer{margin-top:7px;display:inline-block;padding:7px 13px;border-radius:12px;background:#082b49ed;color:#fff1a6;font-weight:bold}
#message{position:absolute;left:50%;top:43%;transform:translate(-50%,-50%);background:#062d48eF;color:white;border:2px solid #ffffffaa;border-radius:17px;padding:13px 19px;font-weight:bold;font-size:clamp(15px,2.5vw,22px);text-align:center;max-width:90%;display:none;z-index:5}
#overlay{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:linear-gradient(#06375b88,#041c36bb);z-index:10;padding:16px}
.panel{width:min(95%,510px);background:#ffffffef;color:#12324a;border-radius:24px;padding:24px;text-align:center;box-shadow:0 12px 35px #001c3677}
.panel h1{margin:0 0 10px;font-size:clamp(25px,5vw,38px)}
.panel p{line-height:1.5}
.panel button{border:0;border-radius:14px;padding:12px 20px;background:#087fba;color:white;font-size:17px;font-weight:bold;cursor:pointer;margin:5px}
.panel button:hover{filter:brightness(1.1)}
#controls{position:absolute;bottom:12px;left:12px;right:12px;display:flex;justify-content:space-between;align-items:flex-end;pointer-events:none}
.pad{display:grid;grid-template-columns:repeat(3,48px);grid-template-rows:repeat(2,45px);gap:5px;pointer-events:auto}
.ctrl{border:2px solid #ffffffb8;border-radius:14px;background:#073451c9;color:white;font-size:21px;font-weight:bold;touch-action:manipulation;user-select:none}
.ctrl:active{background:#168bc4}
#jump{width:94px;height:94px;border-radius:50%;font-size:16px;background:#0786c9eF;pointer-events:auto}
#hint{position:absolute;bottom:114px;left:50%;transform:translateX(-50%);padding:6px 10px;border-radius:10px;background:#092c49b9;color:white;font-size:12px;white-space:nowrap;pointer-events:none}
@media(max-width:520px){
 .pill{font-size:11px;padding:7px 9px}
 #quiz{top:57px}
 .ans{padding:7px 2px;font-size:10px}
 .pad{grid-template-columns:repeat(3,42px);grid-template-rows:repeat(2,40px)}
 #jump{width:82px;height:82px}
 #hint{bottom:105px;font-size:10px}
}
</style>
</head>
<body>
<div id="game">
  <div id="view"></div>
  <div id="hud">
    <div class="pill" id="stage">🐧 MÀN 1: ĐI LẤY CÁ</div>
    <div class="pill" id="progress">Câu 1/5</div>
  </div>
  <div id="quiz">
    <div id="qtext">Sẵn sàng chưa?</div>
    <div id="answers"></div>
    <div id="timer">⏱ 15 giây</div>
  </div>
  <div id="message"></div>
  <div id="hint">← → chọn băng · SPACE nhảy · WASD cũng dùng được</div>
  <div id="controls">
    <div class="pad">
      <div></div><button class="ctrl" id="up">↑</button><div></div>
      <button class="ctrl" id="left">←</button><button class="ctrl" id="down">↓</button><button class="ctrl" id="right">→</button>
    </div>
    <button class="ctrl" id="jump">NHẢY<br>❄️</button>
  </div>
  <div id="overlay">
    <div class="panel" id="panel">
      <h1>🐧 VƯỢT BĂNG LẤY CÁ</h1>
      <p>Giúp chim cánh cụt vượt qua những tảng băng, trả lời 5 câu hỏi để sang bờ bên kia lấy xô cá.</p>
      <p>❄️ Tuyết rơi trong khu băng giá<br>🌙 Chặng trở về là bầu trời đêm<br>⏱ Mỗi câu hỏi có 15 giây</p>
      <button id="start">BẮT ĐẦU CHƠI</button>
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
(function(){
const $=id=>document.getElementById(id);
const questions=[
 {q:"1. Tính: 3² + 4 bằng bao nhiêu?",a:["7","12","13","14"],c:2},
 {q:"2. Phân tích x² − 9 thành nhân tử.",a:["(x−9)(x+1)","(x−3)(x+3)","(x−3)²","x(x−9)"],c:1},
 {q:"3. Hình chữ nhật có bao nhiêu góc vuông?",a:["1","2","3","4"],c:3},
 {q:"4. Tính 25% của 200.",a:["25","40","50","75"],c:2},
 {q:"5. Bậc của đơn thức 3x²y là bao nhiêu?",a:["2","3","4","6"],c:1}
];

let scene,camera,renderer,clock;
let penguin,fishBucket,moon,skyLight,ambientLight;
let snow=null,iceRows=[],returnTiles=[],decor=[];
let started=false,phase="outbound",row=0,lane=1,step=0;
let busy=false,jumping=false,falling=false;
let jumpStart=0,jumpFrom=new THREE.Vector3(),jumpTo=new THREE.Vector3();
let fallStart=0,fallCallback=null;
let timerInterval=null,timeLeft=15,messageTimeout=null;
let night=false,worldGroup,stars=[];
const laneX=[-4.2,-1.4,1.4,4.2];
const tileZ=r=>-r*4.1;
const tileW=2.45;

function init(){
 scene=new THREE.Scene();
 scene.background=new THREE.Color(0x9cddf7);
 scene.fog=new THREE.Fog(0xb8eaff,25,85);

 camera=new THREE.PerspectiveCamera(60,innerWidth/innerHeight,0.1,250);
 renderer=new THREE.WebGLRenderer({antialias:true});
 renderer.setPixelRatio(Math.min(devicePixelRatio,2));
 renderer.setSize(innerWidth,innerHeight);
 renderer.shadowMap.enabled=true;
 renderer.shadowMap.type=THREE.PCFSoftShadowMap;
 renderer.outputColorSpace=THREE.SRGBColorSpace;
 $("view").appendChild(renderer.domElement);
 clock=new THREE.Clock();

 ambientLight=new THREE.HemisphereLight(0xe4f8ff,0x59879c,2.0);
 scene.add(ambientLight);
 skyLight=new THREE.DirectionalLight(0xffffff,2.2);
 skyLight.position.set(-8,18,8);
 skyLight.castShadow=true;
 scene.add(skyLight);

 worldGroup=new THREE.Group();scene.add(worldGroup);
 buildWater();
 buildShore(-25);
 buildShore(12);
 buildScenery();
 buildPenguin();
 buildBucket();
 buildIceRows();
 buildSnow();
 buildStars();
 camera.position.set(0,5,10);
 camera.lookAt(0,1,0);
 window.addEventListener("resize",resize);
 animate();
}
function mat(color,roughness=0.75,metalness=0){
 return new THREE.MeshStandardMaterial({color,roughness,metalness});
}
function box(w,h,d,material,x,y,z){
 const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material);
 o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;
 worldGroup.add(o);return o;
}
function buildWater(){
 const water=new THREE.Mesh(new THREE.PlaneGeometry(200,200),mat(0x6fc9e8,0.35));
 water.rotation.x=-Math.PI/2;water.position.set(0,-0.6,-15);
 worldGroup.add(water);
 for(let i=0;i<30;i++){
  const line=new THREE.Mesh(new THREE.BoxGeometry(1.3,0.025,0.035),mat(0xc8f5ff));
  line.position.set((Math.random()-.5)*38,-0.53,-30+Math.random()*50);
  worldGroup.add(line);
 }
}
function buildShore(z){
 const land=new THREE.Mesh(new THREE.BoxGeometry(24,0.8,12),mat(0xe8f5fa));
 land.position.set(0,-0.15,z);land.receiveShadow=true;worldGroup.add(land);
 for(let i=0;i<16;i++){
  const x=-11+Math.random()*22;
  const rock=new THREE.Mesh(new THREE.DodecahedronGeometry(.3+Math.random()*.4,0),mat(0xb7dce9));
  rock.position.set(x,.28,z-5+Math.random()*10);
  rock.scale.y=.45;worldGroup.add(rock);
 }
}
function buildScenery(){
 // Những núi băng lớn ở xa
 for(let i=0;i<18;i++){
  const h=5+Math.random()*10;
  const m=new THREE.Mesh(new THREE.ConeGeometry(3+Math.random()*4,h,5),mat(i%2?0xc8eefa:0xa8d9ee));
  m.position.set((Math.random()-.5)*90,h/2-0.5,-35+Math.random()*60);
  worldGroup.add(m);
 }
 // Cọc băng dọc hai bên đường
 for(let z=-28;z<13;z+=4){
  for(const side of [-1,1]){
   const h=1.3+Math.random()*2.8;
   const icicle=new THREE.Mesh(new THREE.ConeGeometry(.35+Math.random()*.4,h,5),mat(0xc9f1ff));
   icicle.position.set(side*(7.5+Math.random()*3),h/2-0.3,z+Math.random());
   worldGroup.add(icicle);
  }
 }
}
function buildPenguin(){
 penguin=new THREE.Group();
 const black=mat(0x202f43),white=mat(0xf5fbff),orange=mat(0xffa52e),eye=mat(0x101820);
 function sphere(radius,material,x,y,z,sx=1,sy=1,sz=1){
  const m=new THREE.Mesh(new THREE.SphereGeometry(radius,18,14),material);
  m.position.set(x,y,z);m.scale.set(sx,sy,sz);m.castShadow=true;penguin.add(m);return m;
 }
 sphere(.58,black,0,.9,0,.85,1.1,.72);
 sphere(.43,white,0,.9,-.39,.8,1,.25);
 sphere(.36,black,0,1.72,-.02,.9,1,.8);
 sphere(.07,eye,-.13,1.79,-.34);
 sphere(.07,eye,.13,1.79,-.34);
 sphere(.12,orange,0,1.62,-.4,1,.5,1);
 for(const s of [-1,1]){
  const wing=sphere(.18,black,s*.52,1.02,-.02,1.2,.48,.65);
  wing.rotation.z=s*.25;
  sphere(.2,orange,s*.23,.27,-.02,1,.4,1.4);
 }
 penguin.position.set(laneX[lane],0.15,4.3);
 scene.add(penguin);
}
function buildBucket(){
 fishBucket=new THREE.Group();
 const body=new THREE.Mesh(new THREE.CylinderGeometry(.42,.3,.65,16,1,true),mat(0x8cbdcc));
 body.position.y=.35;fishBucket.add(body);
 const rim=new THREE.Mesh(new THREE.TorusGeometry(.4,.045,8,20),mat(0xe4f7ff));
 rim.rotation.x=Math.PI/2;rim.position.y=.67;fishBucket.add(rim);
 const handle=new THREE.Mesh(new THREE.TorusGeometry(.29,.035,8,20,Math.PI),mat(0xeffaff));
 handle.position.y=.68;handle.rotation.z=Math.PI;fishBucket.add(handle);
 for(let i=0;i<3;i++){
  const fish=new THREE.Mesh(new THREE.SphereGeometry(.12,10,8),mat(0xffb84d));
  fish.position.set((i-1)*.17,.58,.05);fish.scale.set(1,.5,.5);fishBucket.add(fish);
 }
 fishBucket.position.set(0,0,-26.3);fishBucket.visible=false;scene.add(fishBucket);
}
function makeTile(x,z){
 const group=new THREE.Group();
 const base=new THREE.Mesh(new THREE.BoxGeometry(tileW,.32,2.5),mat(0x8fdcf4,.25,.1));
 base.position.y=0;group.add(base);
 const top=new THREE.Mesh(new THREE.BoxGeometry(tileW-.12,.09,2.36),mat(0xe8fbff,.2));
 top.position.y=.2;group.add(top);
 for(let i=0;i<3;i++){
  const crack=new THREE.Mesh(new THREE.BoxGeometry(.04,.015,.7),mat(0x468ca9));
  crack.position.set((i-1)*.45,.252,(i%2)*.3-.1);crack.rotation.y=.4;crack.visible=false;
  group.add(crack);
 }
 group.position.set(x,0,z);group.userData.cracks=group.children.slice(2);
 scene.add(group);return group;
}
function buildIceRows(){
 for(let r=0;r<5;r++){
  const tiles=[];
  for(let l=0;l<4;l++){
   const t=makeTile(laneX[l],tileZ(r));
   tiles.push(t);
  }
  iceRows.push(tiles);
 }
}
function buildSnow(){
 const count=1300;
 const positions=new Float32Array(count*3);
 const velocities=new Float32Array(count);
 for(let i=0;i<count;i++){
  positions[i*3]=(Math.random()-.5)*65;
  positions[i*3+1]=Math.random()*28;
  positions[i*3+2]=-40+Math.random()*65;
  velocities[i]=1.3+Math.random()*3.4;
 }
 const geo=new THREE.BufferGeometry();
 geo.setAttribute("position",new THREE.BufferAttribute(positions,3));
 const material=new THREE.PointsMaterial({color:0xffffff,size:.12,transparent:true,opacity:.9,sizeAttenuation:true});
 snow=new THREE.Points(geo,material);
 snow.userData.velocities=velocities;
 scene.add(snow);
}
function buildStars(){
 const positions=[];
 for(let i=0;i<450;i++){
  positions.push((Math.random()-.5)*120,8+Math.random()*45,-55+Math.random()*80);
 }
 const geo=new THREE.BufferGeometry();
 geo.setAttribute("position",new THREE.Float32BufferAttribute(positions,3));
 const m=new THREE.PointsMaterial({color:0xffffff,size:.16});
 const s=new THREE.Points(geo,m);s.visible=false;scene.add(s);stars.push(s);
 const moonMesh=new THREE.Mesh(new THREE.SphereGeometry(2,24,20),new THREE.MeshBasicMaterial({color:0xfff0bc}));
 moonMesh.position.set(13,17,-38);moonMesh.visible=false;scene.add(moonMesh);moon=moonMesh;
}
function setNight(on){
 night=on;
 if(on){
  scene.background=new THREE.Color(0x06132f);
  scene.fog=new THREE.Fog(0x101d42,22,85);
  ambientLight.color.set(0x6078b8);ambientLight.groundColor.set(0x172342);ambientLight.intensity=.8;
  skyLight.color.set(0x9ebaff);skyLight.intensity=.65;
  stars.forEach(s=>s.visible=true);moon.visible=true;
 }else{
  scene.background=new THREE.Color(0x9cddf7);
  scene.fog=new THREE.Fog(0xb8eaff,25,85);
  ambientLight.color.set(0xe4f8ff);ambientLight.groundColor.set(0x59879c);ambientLight.intensity=2;
  skyLight.color.set(0xffffff);skyLight.intensity=2.2;
  stars.forEach(s=>s.visible=false);moon.visible=false;
 }
}
function resize(){
 camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
}
function msg(text,ms=1100){
 $("message").textContent=text;$("message").style.display="block";
 clearTimeout(messageTimeout);
 if(ms>0)messageTimeout=setTimeout(()=>$("message").style.display="none",ms);
}
function stopTimer(){
 if(timerInterval!==null){clearInterval(timerInterval);timerInterval=null;}
}
function startTimer(){
 stopTimer();timeLeft=15;
 $("timer").textContent="⏱ "+timeLeft+" giây";
 $("timer").style.color="#fff1a6";
 timerInterval=setInterval(()=>{
  if(!started||phase!=="outbound"||busy){stopTimer();return;}
  timeLeft--;
  $("timer").textContent="⏱ "+timeLeft+" giây";
  if(timeLeft<=5)$("timer").style.color="#ff7777";
  if(timeLeft<=0){
   stopTimer();busy=true;
   msg("Hết giờ! Tảng băng vỡ rồi!",1500);
   breakTile(iceRows[row][lane]);
   setTimeout(()=>fall(resetStart),350);
  }
 },1000);
}
function showQuestion(){
 if(row>=questions.length){reachShore();return;}
 const q=questions[row];
 $("qtext").textContent=q.q;
 $("answers").innerHTML=q.a.map((a,i)=>'<div class="ans">'+String.fromCharCode(65+i)+". "+a+"</div>").join("");
 $("progress").textContent="Câu "+(row+1)+"/"+questions.length;
 $("stage").textContent="🐧 MÀN 1: ĐI LẤY CÁ";
 $("quiz").style.display="block";
 startTimer();
}
function move(d){
 if(!started||busy||falling||jumping)return;
 if(phase==="outbound"){
  lane=Math.max(0,Math.min(3,lane+d));
  penguin.position.x=laneX[lane];
 }else if(phase==="return"){
  lane=Math.max(0,Math.min(3,lane+d));
  penguin.position.x=laneX[lane];
 }
}
function moveDepth(d){
 if(!started||busy||falling||jumping)return;
 if(phase==="outbound"){
  if(d<0)jump();
 }else if(phase==="return"&&d<0){
  jump();
 }
}
function jump(){
 if(!started||busy||falling||jumping)return;
 if(phase==="outbound"){
  stopTimer();
  const tile=iceRows[row][lane];
  busy=true;jumping=true;
  jumpStart=performance.now();
  jumpFrom.copy(penguin.position);
  jumpTo.set(tile.position.x,.15,tile.position.z+.25);
  jumpTo.x=laneX[lane];
  penguin.userData.jumpCorrect=(lane===questions[row].c);
  msg("Đang nhảy lên tảng băng...",0);
 }else if(phase==="return"){
  const tile=returnTiles[step];
  if(!tile)return;
  busy=true;jumping=true;
  jumpStart=performance.now();
  jumpFrom.copy(penguin.position);
  jumpTo.set(tile.position.x,.15,tile.position.z+.3);
 }
}
function breakTile(tile){
 if(!tile)return;
 tile.userData.cracked=true;
 tile.userData.cracks.forEach(c=>c.visible=true);
 tile.rotation.z=.08;
 tile.position.y=-.25;
}
function fall(callback){
 if(falling)return;
 falling=true;jumping=false;busy=true;
 fallStart=performance.now();fallCallback=callback;
}
function resetStart(){
 falling=false;jumping=false;busy=false;row=0;lane=1;phase="outbound";
 penguin.position.set(laneX[lane],.15,4.3);
 penguin.rotation.set(0,0,0);
 iceRows.forEach(r=>r.forEach(t=>{
  t.position.y=0;t.rotation.z=0;t.userData.cracked=false;
  t.userData.cracks.forEach(c=>c.visible=false);
 }));
 setNight(false);
 $("quiz").style.display="block";
 showQuestion();
 msg("Về lại bờ rồi! Thử lại nhé!",1400);
}
function reachShore(){
 stopTimer();phase="shore";busy=true;
 $("quiz").style.display="none";
 penguin.position.set(0,.15,-22.5);
 fishBucket.visible=true;
 msg("Đã sang bờ! Nhảy tới xô cá nhé!",1800);
 setTimeout(()=>{
  if(!started)return;
  fishBucket.visible=false;
  startReturn();
 },1700);
}
function startReturn(){
 phase="return";step=0;lane=1;busy=false;
 setNight(true);
 returnTiles.forEach(t=>scene.remove(t));
 returnTiles=[];
 const weakIndices=[0,1,2,3].sort(()=>Math.random()-.5).slice(0,2);
 for(let i=0;i<4;i++){
  const t=makeTile(laneX[1],-26+i*4.3);
  t.position.x=laneX[1];
  t.userData.weak=weakIndices.includes(i);
  returnTiles.push(t);
 }
 penguin.position.set(laneX[1],.15,-29);
 $("stage").textContent="🌙 MÀN 2: TRỞ VỀ";
 $("progress").textContent="Băng 1/4";
 $("quiz").style.display="none";
 msg("Trời đã tối! Chọn đường băng rồi nhảy về bờ!",2000);
}
function resetBucket(){
 falling=false;jumping=false;busy=false;phase="return";step=0;lane=1;
 penguin.position.set(laneX[1],.15,-29);
 returnTiles.forEach(t=>{
  t.position.y=0;t.rotation.z=0;t.userData.cracked=false;
  t.userData.cracks.forEach(c=>c.visible=false);
 });
 $("progress").textContent="Băng 1/4";
 msg("Chim đã trở lại gần xô cá! Hãy thử đường khác!",1800);
}
function win(){
 busy=true;started=false;stopTimer();
 $("overlay").style.display="flex";
 $("panel").innerHTML='<h1>🎉 GIỎI QUÁ!</h1><p>🐧 Chim cánh cụt đã mang xô cá về an toàn!</p><p>❄️ Em đã vượt qua cả hai chặng băng giá.</p><button id="restart">CHƠI LẠI</button>';
 $("restart").onclick=()=>location.reload();
 $("quiz").style.display="none";
}
function startGame(){
 $("overlay").style.display="none";
 started=true;phase="outbound";row=0;lane=1;step=0;busy=false;
 setNight(false);
 penguin.position.set(laneX[lane],.15,4.3);
 penguin.rotation.set(0,0,0);
 fishBucket.visible=false;
 returnTiles.forEach(t=>scene.remove(t));returnTiles=[];
 iceRows.forEach(r=>r.forEach(t=>{
  t.position.y=0;t.rotation.z=0;t.userData.cracked=false;
  t.userData.cracks.forEach(c=>c.visible=false);
 }));
 showQuestion();
}
function animate(){
 requestAnimationFrame(animate);
 const dt=Math.min(clock.getDelta(),.05);
 if(snow){
  const pos=snow.geometry.attributes.position.array;
  const vel=snow.userData.velocities;
  for(let i=0;i<vel.length;i++){
   pos[i*3+1]-=vel[i]*dt;
   pos[i*3]+=Math.sin(performance.now()*.0005+i)*dt*.18;
   if(pos[i*3+1]<-.8){
    pos[i*3+1]=20+Math.random()*10;
    pos[i*3]=-32+Math.random()*64;
    pos[i*3+2]=-42+Math.random()*60;
   }
  }
  snow.geometry.attributes.position.needsUpdate=true;
 }
 if(jumping){
  const t=Math.min(1,(performance.now()-jumpStart)/650);
  penguin.position.x=THREE.MathUtils.lerp(jumpFrom.x,jumpTo.x,t);
  penguin.position.z=THREE.MathUtils.lerp(jumpFrom.z,jumpTo.z,t);
  penguin.position.y=.15+Math.sin(t*Math.PI)*1.7;
  penguin.rotation.x=Math.sin(t*Math.PI)*.12;
  if(t>=1){
   jumping=false;penguin.position.copy(jumpTo);penguin.rotation.x=0;
   if(phase==="outbound"){
    const correct=penguin.userData.jumpCorrect;
    if(correct){
     msg("Chính xác! Em đã đứng trên băng! ✔",900);
     row++;
     setTimeout(()=>{
      if(!started)return;
      busy=false;
      if(row>=questions.length)reachShore();
      else{
       penguin.position.z=tileZ(row)+2.7;
       showQuestion();
      }
     },650);
    }else{
     breakTile(iceRows[row][lane]);
     msg("Sai đáp án! Băng vỡ, chim rơi xuống nước!",1400);
     setTimeout(()=>fall(resetStart),300);
    }
   }else if(phase==="return"){
    const tile=returnTiles[step];
    if(tile.userData.weak){
     breakTile(tile);
     msg("Băng yếu vỡ rồi! Chim rơi xuống nước!",1300);
     setTimeout(()=>fall(resetBucket),300);
    }else{
     step++;
     if(step>=4){
      msg("Về tới bờ an toàn!",900);
      setTimeout(win,850);
     }else{
      penguin.position.z=returnTiles[step].position.z+2.4;
      $("progress").textContent="Băng "+(step+1)+"/4";
      msg("Băng chắc chắn! Tiếp tục nào!",850);
      setTimeout(()=>{busy=false;},650);
     }
    }
   }
  }
 }
 if(falling){
  const t=Math.min(1,(performance.now()-fallStart)/650);
  penguin.position.y=.15-t*2.8;
  penguin.rotation.x=t*1.2;
  if(t>=1){
   falling=false;
   if(fallCallback){const cb=fallCallback;fallCallback=null;setTimeout(cb,450);}
  }
 }
 // Camera theo sau chim, giữ góc nhìn từ phía sau
 const targetCam=new THREE.Vector3(penguin.position.x*.55,4.8,penguin.position.z+8.5);
 camera.position.lerp(targetCam,.07);
 camera.lookAt(penguin.position.x*.55,1.1,penguin.position.z-3.2);
 if(fishBucket.visible)fishBucket.rotation.y+=dt*.7;
 renderer.render(scene,camera);
}
$("start").addEventListener("click",startGame);
$("left").addEventListener("click",()=>move(-1));
$("right").addEventListener("click",()=>move(1));
$("up").addEventListener("click",()=>moveDepth(-1));
$("down").addEventListener("click",()=>moveDepth(1));
$("jump").addEventListener("click",jump);
window.addEventListener("keydown",e=>{
 if(["ArrowLeft","ArrowRight","ArrowUp","ArrowDown"," ","a","d","w","s"].includes(e.key))e.preventDefault();
 if(e.key==="ArrowLeft"||e.key==="a"||e.key==="A")move(-1);
 if(e.key==="ArrowRight"||e.key==="d"||e.key==="D")move(1);
 if(e.key===" "||e.key==="Enter")jump();
 if(e.key==="ArrowUp"||e.key==="w"||e.key==="W")moveDepth(-1);
 if(e.key==="ArrowDown"||e.key==="s"||e.key==="S")moveDepth(1);
});
init();
})();
</script>
</body>
</html>
"""

components.html(GAME, height=760, scrolling=False)
