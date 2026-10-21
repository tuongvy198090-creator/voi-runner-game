
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Giải Cứu Thế Giới",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    header, footer, #MainMenu {visibility: hidden;}
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

game_html = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box}
body{margin:0;font-family:Arial,sans-serif;background:#102b20;color:white;overflow:hidden}
#game{position:relative;width:100%;height:820px;min-height:600px;overflow:hidden;background:#173d2b}
canvas{display:block;width:100%;height:100%}
#hud{position:absolute;top:12px;left:12px;right:12px;display:none;
     justify-content:space-between;gap:8px;flex-wrap:wrap;pointer-events:none}
.badge{background:#10291fdc;border:1px solid #7acb91;border-radius:12px;
       padding:9px 12px;font-size:14px;font-weight:bold}
#overlay{position:absolute;inset:0;background:#06190edc;display:flex;
         align-items:center;justify-content:center;padding:16px;z-index:5;overflow:auto}
.panel{width:min(520px,100%);max-height:96%;overflow:auto;text-align:center;
       background:linear-gradient(145deg,#194b32,#10291f);
       border:2px solid #9ce8a7;border-radius:24px;padding:24px 22px;
       box-shadow:0 0 35px #4ee98b55}
h1{font-size:clamp(26px,5vw,42px);margin:8px 0;color:#c7ffd1}
h2{font-size:clamp(22px,4vw,30px);color:#d5ffdb;margin:10px 0}
p{line-height:1.65;font-size:16px}
.small{font-size:13px;color:#c8e8ce}
button{font-size:16px;font-weight:bold;border:0;border-radius:12px;
       padding:12px 17px;cursor:pointer;margin:5px;background:#b8f6c1;color:#123322}
button:hover{filter:brightness(1.1)}
button:disabled{opacity:.45;cursor:not-allowed}
.primary{background:#e8ce76;color:#30280c;width:100%;margin-top:12px}
.answers{display:grid;grid-template-columns:1fr;gap:7px;margin-top:14px}
.answers button{background:#e1f5e5;color:#183b24}
#controls{position:absolute;bottom:16px;left:0;right:0;display:none;
          justify-content:space-between;align-items:end;padding:0 18px;pointer-events:none}
.pad{display:grid;grid-template-columns:52px 52px 52px;grid-template-rows:48px 48px 48px;
     gap:4px;pointer-events:auto}
.pad button,.action button{padding:0;margin:0;background:#10291fc9;color:white;
     border:1px solid #a6eeb5;font-size:23px;touch-action:none}
.pad .up{grid-column:2;grid-row:1}
.pad .left{grid-column:1;grid-row:2}
.pad .down{grid-column:2;grid-row:2}
.pad .right{grid-column:3;grid-row:2}
.action{display:flex;flex-direction:column;gap:7px;pointer-events:auto}
.action button{font-size:14px;padding:12px}
#toast{position:absolute;top:90px;left:50%;transform:translateX(-50%);
       background:#10291fee;border:1px solid #c7ffd1;border-radius:12px;
       padding:12px 16px;display:none;z-index:3;text-align:center;max-width:90%}
.score{font-size:42px;color:#ffdf79;font-weight:bold;margin:12px}
.stat{display:flex;justify-content:space-between;gap:12px;padding:9px 0;
      border-bottom:1px solid #ffffff25}
@media(max-width:500px){
 #game{height:90vh;min-height:600px}
 .panel{padding:18px 14px}
 p{font-size:14px}
 .badge{font-size:12px;padding:7px}
}
</style>
</head>
<body>
<div id="game">
  <div id="hud">
    <div class="badge" id="levelHud">MÀN 1/5</div>
    <div class="badge" id="gemHud">💎 Đá quý: 0/5</div>
    <div class="badge" id="scoreHud">⭐ Điểm: 0</div>
    <div class="badge" id="timeHud">⏱ 90 giây</div>
  </div>
  <div id="toast"></div>
  <div id="overlay">
    <div class="panel" id="panel"></div>
  </div>
  <div id="controls">
    <div class="pad">
      <button class="up" data-move="forward">↑</button>
      <button class="left" data-move="left">←</button>
      <button class="down" data-move="back">↓</button>
      <button class="right" data-move="right">→</button>
    </div>
    <div class="action">
      <button id="hintBtn">💡 Gợi ý</button>
      <button id="pauseBtn">Ⅱ Tạm dừng</button>
    </div>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.0/three.min.js"></script>
<script>
(function(){
const $=id=>document.getElementById(id);
const panel=$('panel'), overlay=$('overlay');
const levels=[
 {name:"Rừng Ngọc Lục Bảo",subtitle:"Đá Quý Sự Sống",
  intro:"Chào mừng nhà thám hiểm! Hãy khám phá khu rừng, tìm 3 mảnh bản đồ phát sáng rồi thu thập Đá Quý Sự Sống. Cẩn thận với những ngã rẽ đánh lừa!",
  hint:"Tìm các vật phẩm phát sáng dọc con đường. Viên đá quý chỉ xuất hiện khi em thu thập đủ 3 mảnh bản đồ.",
  sky:0x9bd9a5,ground:0x356c3b,path:0x8c7955,leaf:0x247342,crystal:0x50ff9d,time:90},
 {name:"Thung Lũng Thủy Tinh",subtitle:"Đá Quý Nguồn Nước",
  intro:"Dòng sông đã chắn mất lối đi! Hãy thu thập 3 dấu ấn nước, quan sát những phiến đá và tìm đường sang bờ bên kia để lấy viên đá quý.",
  hint:"Đi theo các dấu ấn xanh dương. Hãy tránh những vật cản quanh bờ sông.",
  sky:0x9bd9ef,ground:0x547d76,path:0x8faaa6,leaf:0x348c87,crystal:0x4ddfff,time:85},
 {name:"Tàn Tích Ánh Sáng",subtitle:"Đá Quý Ánh Sáng",
  intro:"Ngôi đền cổ chỉ mở cửa cho người giải được câu đố. Tìm 3 cổ tự phát sáng, sau đó trả lời chính xác 3 câu hỏi liên tiếp để lấy Đá Quý Ánh Sáng.",
  hint:"Tìm đủ 3 cổ tự trước. Khi câu đố xuất hiện, đọc kỹ câu hỏi rồi chọn đáp án.",
  sky:0xd9bd80,ground:0x68634d,path:0x95856a,leaf:0x526c40,crystal:0xffdb62,time:100},
 {name:"Thung Lũng Bão Gió",subtitle:"Đá Quý Gió",
  intro:"Gió mạnh đang cản đường! Thu thập 3 dấu ấn gió, né những chướng ngại vật và tìm Đá Quý Gió. Em chỉ được va chạm tối đa 3 lần.",
  hint:"Quan sát trước khi di chuyển. Đừng chạy thẳng vào những chướng ngại vật lớn.",
  sky:0x9baacb,ground:0x5d695f,path:0x8b8d83,leaf:0x566d63,crystal:0xd7e8ff,time:80},
 {name:"Thánh Địa Hy Vọng",subtitle:"Đá Quý Hy Vọng",
  intro:"Đây là thử thách cuối cùng! Thu thập 3 dấu ấn, ghi nhớ chuỗi biểu tượng bí mật và hoàn thành câu đố để lấy viên đá cuối cùng. Cây Cổ Thụ đang chờ em!",
  hint:"Tìm đủ 3 dấu ấn trước. Hãy quan sát thật kỹ chuỗi biểu tượng khi thử thách trí nhớ xuất hiện.",
  sky:0x4d557e,ground:0x344c42,path:0x756b69,leaf:0x247a5b,crystal:0xffdf78,time:100}
];
const questions=[
 {q:"Đâu là công thức tính diện tích hình chữ nhật?",a:["Dài × rộng","Dài + rộng","Dài × 2 + rộng"],correct:0},
 {q:"Nước sôi ở khoảng bao nhiêu độ C trong điều kiện thường?",a:["50°C","100°C","150°C"],correct:1},
 {q:"Hành tinh nào được gọi là hành tinh đỏ?",a:["Sao Kim","Sao Hỏa","Sao Mộc"],correct:1}
];

let scene,camera,renderer,clock,world,player;
let objects=[],tokens=[],obstacles=[],gem=null,fragments=[];
let running=false,mode="welcome",stage=0,totalScore=0,stageScore=0;
let collected=0,gemCount=0,timeLeft=90,hits=0;
let quizIndex=0,quizRun=0,memorized=[],memoryInput=[];
let keys={},moving={},lastTime=0,toastTimer=null;
let startedAt=0,checkpointStage=0;
let playerSpeed=6;
let playerGroup;

function init3D(){
 scene=new THREE.Scene();
 scene.background=new THREE.Color(0x9bd9a5);
 scene.fog=new THREE.Fog(0x9bd9a5,22,75);
 camera=new THREE.PerspectiveCamera(65,1,0.1,150);
 renderer=new THREE.WebGLRenderer({antialias:true});
 renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,1.7));
 renderer.shadowMap.enabled=true;
 renderer.shadowMap.type=THREE.PCFSoftShadowMap;
 renderer.outputEncoding=THREE.sRGBEncoding;
 $('game').insertBefore(renderer.domElement,$('game').firstChild);
 renderer.domElement.style.position="absolute";
 renderer.domElement.style.inset="0";
 renderer.domElement.style.zIndex="0";
 scene.add(new THREE.HemisphereLight(0xeafff0,0x30432d,1.5));
 const sun=new THREE.DirectionalLight(0xfff5d7,2.0);
 sun.position.set(-8,18,10);sun.castShadow=true;
 sun.shadow.mapSize.set(1024,1024);scene.add(sun);
 clock=new THREE.Clock();
 player=new THREE.Group();
 buildPlayer();
 scene.add(player);
 resize();
 window.addEventListener('resize',resize);
 animate();
}
function resize(){
 if(!renderer)return;
 const w=$('game').clientWidth,h=$('game').clientHeight;
 renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();
}
function mat(color,rough=0.9,metal=0){
 return new THREE.MeshStandardMaterial({color,roughness:rough,metalness:metal});
}
function box(group,x,y,z,sx,sy,sz,color){
 const m=new THREE.Mesh(new THREE.BoxGeometry(sx,sy,sz),mat(color));
 m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;group.add(m);return m;
}
function sphere(group,x,y,z,r,color){
 const m=new THREE.Mesh(new THREE.SphereGeometry(r,16,12),mat(color));
 m.position.set(x,y,z);m.castShadow=true;group.add(m);return m;
}
function buildPlayer(){
 playerGroup=new THREE.Group();
 const body=new THREE.Mesh(new THREE.CapsuleGeometry(0.38,0.75,4,8),mat(0x3b78d8));
 body.position.y=1.05;body.castShadow=true;playerGroup.add(body);
 const head=sphere(playerGroup,0,1.85,0,0.32,0xffd1a3);
 const hair=sphere(playerGroup,0,2.04,-0.04,0.30,0x493323);
 hair.scale.set(1,0.5,1);
 const eyeMat=mat(0x202020);
 for(const x of [-0.11,0.11]){
  const eye=new THREE.Mesh(new THREE.SphereGeometry(0.035,8,8),eyeMat);
  eye.position.set(x,1.88,0.28);playerGroup.add(eye);
 }
 for(const x of [-0.18,0.18]){
  const arm=new THREE.Mesh(new THREE.CapsuleGeometry(0.11,0.48,3,6),mat(0xffd1a3));
  arm.position.set(x,1.13,0);arm.rotation.z=x<0?-0.15:0.15;playerGroup.add(arm);
  const leg=new THREE.Mesh(new THREE.CapsuleGeometry(0.13,0.45,3,6),mat(0x243c55));
  leg.position.set(x*0.65,0.35,0);playerGroup.add(leg);
 }
 player.add(playerGroup);
}
function clearWorld(){
 if(world)scene.remove(world);
 world=new THREE.Group();scene.add(world);
 objects=[];tokens=[];obstacles=[];fragments=[];gem=null;
}
function addTree(x,z,size,leafColor){
 const trunk=new THREE.Mesh(new THREE.CylinderGeometry(0.22*size,0.36*size,2.4*size,8),mat(0x60452d));
 trunk.position.set(x,1.2*size,z);trunk.castShadow=true;world.add(trunk);
 for(let i=0;i<3;i++){
  const crown=new THREE.Mesh(new THREE.ConeGeometry((1.15-i*0.15)*size,1.7*size,8),mat(leafColor));
  crown.position.set(x,(2.4+i*0.65)*size,z);crown.castShadow=true;world.add(crown);
 }
}
function addCrystal(x,z,color,kind){
 const group=new THREE.Group();
 const crystal=new THREE.Mesh(new THREE.OctahedronGeometry(0.42,0),new THREE.MeshStandardMaterial({
  color,emissive:color,emissiveIntensity:0.55,metalness:0.2,roughness:0.25
 }));
 crystal.position.y=0.8;crystal.rotation.y=0.3;crystal.castShadow=true;group.add(crystal);
 const ring=new THREE.Mesh(new THREE.TorusGeometry(0.55,0.035,8,24),mat(color,0.3,0.4));
 ring.rotation.x=Math.PI/2;ring.position.y=0.35;group.add(ring);
 group.position.set(x,0,z);group.userData={kind,baseY:0};
 world.add(group);objects.push(group);
 if(kind==="token")tokens.push(group);
 if(kind==="fragment")fragments.push(group);
 if(kind==="gem")gem=group;
 return group;
}
function addObstacle(x,z,color,kind){
 let m;
 if(kind==="rock"){
  m=new THREE.Mesh(new THREE.DodecahedronGeometry(0.8,0),mat(color));
  m.position.set(x,0.55,z);
 }else if(kind==="log"){
  m=new THREE.Mesh(new THREE.CylinderGeometry(0.3,0.35,2.4,8),mat(0x6d492d));
  m.position.set(x,0.35,z);m.rotation.z=Math.PI/2;
 }else{
  m=new THREE.Mesh(new THREE.ConeGeometry(0.65,1.8,7),mat(color));
  m.position.set(x,0.9,z);
 }
 m.castShadow=true;world.add(m);obstacles.push(m);
}
function buildWorld(){
 clearWorld();
 const L=levels[stage];
 scene.background=new THREE.Color(L.sky);scene.fog.color=new THREE.Color(L.sky);
 scene.fog.near=25;scene.fog.far=70;
 const ground=new THREE.Mesh(new THREE.PlaneGeometry(100,110),mat(L.ground));
 ground.rotation.x=-Math.PI/2;ground.position.set(0,-0.08,-15);
 ground.receiveShadow=true;world.add(ground);
 // winding path segments
 const pts=[[-1,12],[0,6],[0,-1],[2,-7],[-1,-13],[1,-20],[0,-27]];
 for(let i=0;i<pts.length-1;i++){
  const a=pts[i],b=pts[i+1];
  const dx=b[0]-a[0],dz=b[1]-a[1];
  const len=Math.sqrt(dx*dx+dz*dz);
  const road=new THREE.Mesh(new THREE.BoxGeometry(3.7,0.08,len),mat(L.path));
  road.position.set((a[0]+b[0])/2,0,(a[1]+b[1])/2);
  road.rotation.y=Math.atan2(dx,dz);world.add(road);
 }
 // landscape differs by stage
 if(stage===1){
  const water=new THREE.Mesh(new THREE.BoxGeometry(18,0.08,5),new THREE.MeshStandardMaterial({color:0x248eb4,roughness:0.25,metalness:0.25}));
  water.position.set(0,0.02,-7);world.add(water);
  for(let i=0;i<5;i++){
   const rock=new THREE.Mesh(new THREE.CylinderGeometry(0.65,0.7,0.25,8),mat(0xb5c7c3));
   rock.position.set(-3+i*1.5,0.18,-7+(i%2)*1.3);world.add(rock);
  }
 }
 if(stage===2){
  for(let i=0;i<4;i++){
   box(world,-2.4+i*1.6,1.2,-9,0.35,2.4,0.35,0x76664c);
   box(world,-2.4+i*1.6,2.4,-9,0.35,0.3,0.35,0xb59a63);
  }
  // temple entrance
  box(world,-2,1.5,-18,0.5,3,0.6,0x706b52);
  box(world,2,1.5,-18,0.5,3,0.6,0x706b52);
  box(world,0,3,-18,4.5,0.45,0.7,0x857758);
 }
 if(stage===3){
  for(let i=0;i<4;i++)addObstacle((i%2===0?-2.4:2.4),-5-i*4,0x84948b,i%2===0?"log":"rock");
 }
 if(stage===4){
  // ancient tree in the distance
  const trunk=new THREE.Mesh(new THREE.CylinderGeometry(0.8,1.4,8,12),mat(0x66503b));
  trunk.position.set(0,4,-26);trunk.castShadow=true;world.add(trunk);
  const crown=new THREE.Mesh(new THREE.SphereGeometry(4,14,12),mat(0x3cae6c));
  crown.position.set(0,8,-26);crown.castShadow=true;world.add(crown);
  for(let i=0;i<4;i++)addCrystal(-2+i*1.3,-23,0x9effb5,"decoration");
 }
 // trees / vegetation along sides
 for(let i=0;i<32;i++){
  const side=i%2===0?-1:1;
  const x=side*(4.3+(i%4)*1.5);
  const z=10-Math.floor(i/2)*2.7;
  addTree(x,z,0.8+(i%3)*0.18,L.leaf);
 }
 // rocks and flowers
 for(let i=0;i<12;i++){
  const x=(i%2===0?-1:1)*(3.8+(i%3)*0.7);
  const z=5-i*2.4;
  sphere(world,x,0.16,z,0.22,stage===1?0x7bc8e8:0xc4d99a);
 }
 player.position.set(0,0,10);
 // 3 collectibles before crystal
 const tokenColor=[0x9dffb0,0x58dfff,0xffd85d,0xd7e8ff,0xffc9ff][stage];
 const tokenPositions=[[-2.1,2],[2.1,-3],[-1.8,-11]];
 tokenPositions.forEach((p,i)=>addCrystal(p[0],p[1],tokenColor,"token"));
 collected=0;hits=0;gem=null;
 // crystal appears only after challenge is completed
 updateHUD();
}
function showPanel(html){
 panel.innerHTML=html;overlay.style.display="flex";
}
function hidePanel(){overlay.style.display="none";}
function welcome(){
 mode="welcome";running=false;
 $('hud').style.display="none";$('controls').style.display="none";
 showPanel(`
  <div style="font-size:52px">🌳💎✨</div>
  <h1>GIẢI CỨU THẾ GIỚI</h1>
  <p>Một thế lực bí ẩn đang khiến Cây Cổ Thụ héo úa. Hãy vượt qua 5 vùng đất, tìm đủ 5 viên đá quý và khôi phục sự sống cho khu rừng!</p>
  <p>🎮 Di chuyển bằng WASD, phím mũi tên hoặc các nút điều khiển trên màn hình.</p>
  <button class="primary" id="startBtn">🌿 BẮT ĐẦU PHIÊU LƯU</button>
  <p class="small">Đồ họa 3D • 5 màn chơi • Điểm thưởng • Thử thách kiến thức</p>
 `);
 $('startBtn').onclick=()=>{stage=0;totalScore=0;gemCount=0;introStage();};
}
function introStage(){
 mode="intro";running=false;
 $('hud').style.display="none";$('controls').style.display="none";
 const L=levels[stage];
 showPanel(`
  <div style="font-size:42px">${["🌳","💧","🏛️","🌬️","✨"][stage]}</div>
  <p class="small">CHẶNG ${stage+1} / 5</p>
  <h2>${L.name}</h2>
  <p><b>Nhiệm vụ: ${L.subtitle}</b></p>
  <p>${L.intro}</p>
  <div class="stat"><span>Thời gian</span><b>${L.time} giây</b></div>
  <div class="stat"><span>Vật phẩm cần tìm</span><b>3 dấu ấn + 1 đá quý</b></div>
  <button class="primary" id="beginBtn">▶ BẮT ĐẦU MÀN CHƠI</button>
 `);
 $('beginBtn').onclick=beginStage;
}
function beginStage(){
 buildWorld();
 stageScore=0;timeLeft=levels[stage].time;startedAt=performance.now();
 mode="playing";running=true;
 $('hud').style.display="flex";$('controls').style.display="flex";
 hidePanel();updateHUD();
}
function updateHUD(){
 $('levelHud').textContent=`MÀN ${stage+1}/5 · ${levels[stage].name}`;
 $('gemHud').textContent=`💎 Đá quý: ${gemCount}/5`;
 $('scoreHud').textContent=`⭐ Điểm: ${totalScore+stageScore}`;
 $('timeHud').textContent=`⏱ ${Math.max(0,Math.ceil(timeLeft))} giây`;
}
function showToast(msg){
 const t=$('toast');t.textContent=msg;t.style.display="block";
 clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.style.display="none",2300);
}
function spawnGem(){
 if(gem)return;
 addCrystal(0,-22,levels[stage].crystal,"gem");
 showToast("✨ Đã thu thập đủ 3 dấu ấn! Viên đá quý đã xuất hiện.");
 if(stage===2){quizRun=0;setTimeout(showQuiz,350);}
 if(stage===4){setTimeout(showMemory,350);}
}
function showQuiz(){
 running=false;mode="quiz";
 const q=questions[quizRun%questions.length];
 showPanel(`<div style="font-size:38px">🏛️</div><h2>CÂU ĐỐ ${quizRun+1}/3</h2>
 <p>${q.q}</p><div class="answers">${q.a.map((a,i)=>`<button data-answer="${i}">${a}</button>`).join("")}</div>
 <p class="small">Trả lời đúng cả 3 câu để mở khóa viên đá quý.</p>`);
 panel.querySelectorAll('[data-answer]').forEach(b=>b.onclick=()=>{
  if(Number(b.dataset.answer)===q.correct){
   quizRun++;stageScore+=10;
   if(quizRun>=3){hidePanel();running=true;mode="playing";showToast("Cửa đền đã mở! Hãy lấy viên đá quý.");}
   else showQuiz();
  }else{
   showToast("Chưa đúng rồi! Thử lại câu này nhé.");
  }
  updateHUD();
 });
}
function showMemory(){
 running=false;mode="memory";
 const colors=["🔴","🔵","🟡","🟢"];
 memorized=Array.from({length:4},()=>Math.floor(Math.random()*4));
 memoryInput=[];
 showPanel(`<div style="font-size:38px">🧠</div><h2>THỬ THÁCH TRÍ NHỚ</h2>
 <p>Ghi nhớ chuỗi biểu tượng này, sau đó nhập lại đúng thứ tự!</p>
 <h1 id="sequence">${memorized.map(n=>colors[n]).join(" ")}</h1>
 <button id="readyMemory" class="primary">ĐÃ GHI NHỚ — BẮT ĐẦU</button>`);
 $('readyMemory').onclick=()=>{
  showPanel(`<h2>NHẬP LẠI CHUỖI</h2><p>Chọn đúng 4 biểu tượng theo thứ tự.</p>
  <div class="answers" style="grid-template-columns:1fr 1fr">${colors.map((c,i)=>`<button data-color="${i}">${c}</button>`).join("")}</div>
  <p id="memoryProgress">Đã chọn: 0/4</p>`);
  panel.querySelectorAll('[data-color]').forEach(b=>b.onclick=()=>{
   memoryInput.push(Number(b.dataset.color));
   $('memoryProgress').textContent=`Đã chọn: ${memoryInput.length}/4`;
   if(memoryInput.length===4){
    if(memoryInput.every((v,i)=>v===memorized[i])){
     stageScore+=30;hidePanel();running=true;mode="playing";showToast("Tuyệt vời! Em đã vượt qua thử thách trí nhớ.");
    }else{
     memoryInput=[];showToast("Sai thứ tự rồi! Em được thử lại.");
     $('memoryProgress').textContent="Đã chọn: 0/4";
    }
   }
  });
 };
}
function completeStage(){
 running=false;mode="results";
 const bonus=Math.max(0,Math.floor(timeLeft/2));
 stageScore+=40+bonus;
 totalScore+=stageScore;gemCount++;
 checkpointStage=stage+1;
 $('hud').style.display="none";$('controls').style.display="none";
 const isFinal=stage===4;
 showPanel(`
  <div style="font-size:48px">${isFinal?"🏆🌳✨":"💎🎉"}</div>
  <h1>${isFinal?"GIẢI CỨU THẾ GIỚI!":"HOÀN THÀNH MÀN "+(stage+1)+"!"}</h1>
  <h2>${isFinal?"Cây Cổ Thụ đã hồi sinh!":levels[stage].name}</h2>
  <div class="score">+${stageScore} điểm</div>
  <div class="stat"><span>Điểm màn này</span><b>${stageScore}</b></div>
  <div class="stat"><span>Thưởng thời gian</span><b>${bonus} điểm</b></div>
  <div class="stat"><span>Đá quý thu thập</span><b>${gemCount}/5</b></div>
  <div class="stat"><span>Tổng điểm tích lũy</span><b>${totalScore}</b></div>
  <p>${isFinal?"Em đã thu thập đủ 5 viên đá quý và cứu thế giới thành công!":"Em đã mở khóa vùng đất tiếp theo. Hãy sẵn sàng cho thử thách mới!"}</p>
  <button class="primary" id="nextBtn">${isFinal?"🔄 CHƠI LẠI":"➡️ MÀN TIẾP THEO"}</button>
 `);
 $('nextBtn').onclick=()=>{
  if(isFinal){stage=0;totalScore=0;gemCount=0;introStage();}
  else{stage++;introStage();}
 };
}
function failStage(reason){
 running=false;mode="failed";
 $('hud').style.display="none";$('controls').style.display="none";
 showPanel(`<div style="font-size:42px">🌿</div><h2>${reason}</h2>
 <p>Đừng lo! Em sẽ quay lại điểm lưu gần nhất. Những màn đã hoàn thành và điểm số của chúng vẫn được giữ nguyên.</p>
 <div class="stat"><span>Điểm đã tích lũy</span><b>${totalScore}</b></div>
 <button class="primary" id="retryBtn">↩️ QUAY LẠI ĐIỂM LƯU</button>`);
 $('retryBtn').onclick=()=>introStage();
}
function pauseGame(){
 if(mode==="playing"){
  running=false;mode="paused";
  showPanel(`<h2>TẠM DỪNG</h2><p>Nhà thám hiểm nghỉ một chút nhé!</p>
  <button class="primary" id="resumeBtn">▶ TIẾP TỤC CHƠI</button>
  <button id="exitBtn">Về màn hình đầu</button>`);
  $('resumeBtn').onclick=()=>{hidePanel();mode="playing";running=true;};
  $('exitBtn').onclick=welcome;
 }
}
$('pauseBtn').onclick=pauseGame;
$('hintBtn').onclick=()=>showToast(levels[stage].hint);

function setMove(k,on){moving[k]=on;}
document.querySelectorAll('[data-move]').forEach(btn=>{
 const k=btn.dataset.move;
 btn.addEventListener('pointerdown',e=>{e.preventDefault();setMove(k,true);});
 ['pointerup','pointerleave','pointercancel'].forEach(ev=>btn.addEventListener(ev,()=>setMove(k,false)));
});
window.addEventListener('keydown',e=>{
 const k=e.key.toLowerCase();
 keys[k]=true;
 if(["arrowup","arrowdown","arrowleft","arrowright"," "].includes(k))e.preventDefault();
 if(k==="escape")pauseGame();
});
window.addEventListener('keyup',e=>keys[e.key.toLowerCase()]=false);
function isDown(name){
 if(name==="forward")return keys.w||keys.arrowup||moving.forward;
 if(name==="back")return keys.s||keys.arrowdown||moving.back;
 if(name==="left")return keys.a||keys.arrowleft||moving.left;
 if(name==="right")return keys.d||keys.arrowright||moving.right;
 return false;
}
function updateGame(dt){
 if(!running||mode!=="playing")return;
 timeLeft-=dt;
 if(timeLeft<=0){timeLeft=0;updateHUD();failStage("Hết thời gian!");return;}
 let dx=0,dz=0;
 if(isDown("forward"))dz-=1;
 if(isDown("back"))dz+=1;
 if(isDown("left"))dx-=1;
 if(isDown("right"))dx+=1;
 if(dx||dz){
  const n=Math.sqrt(dx*dx+dz*dz);dx/=n;dz/=n;
  player.position.x+=dx*playerSpeed*dt;
  player.position.z+=dz*playerSpeed*dt;
  player.rotation.y=Math.atan2(dx,dz)+Math.PI;
  playerGroup.position.y=Math.abs(Math.sin(performance.now()*0.012))*0.06;
 }
 player.position.x=Math.max(-7,Math.min(7,player.position.x));
 player.position.z=Math.max(-29,Math.min(11,player.position.z));
 // animate collectibles
 for(const o of objects){
  if(o.userData.kind!=="decoration"){
   o.rotation.y+=dt*1.2;
   o.position.y=0.1+Math.sin(performance.now()*0.003+o.position.z)*0.12;
  }
 }
 // Collect tokens
 for(let i=tokens.length-1;i>=0;i--){
  const o=tokens[i];
  if(!o.parent)continue;
  if(player.position.distanceTo(o.position)<1.35){
   world.remove(o);tokens.splice(i,1);collected++;
   stageScore+=20;showToast("✨ Đã tìm được dấu ấn "+collected+"/3!");
   updateHUD();
   if(collected>=3)spawnGem();
  }
 }
 // obstacles can cause damage, with short collision cooldown
 if(!window.hitCooldown)window.hitCooldown=0;
 window.hitCooldown=Math.max(0,window.hitCooldown-dt);
 for(const o of obstacles){
  if(player.position.distanceTo(o.position)<1.1&&window.hitCooldown===0){
   hits++;window.hitCooldown=1.2;showToast("Cẩn thận! Va chạm "+hits+"/3");
   if(stage===3&&hits>=3){failStage("Em đã va chạm quá 3 lần!");return;}
   player.position.z=Math.min(10,player.position.z+1.4);
  }
 }
 if(gem&&gem.parent&&player.position.distanceTo(gem.position)<1.5){
  if(stage===2&&quizRun<3)return;
  if(stage===4&&mode==="memory")return;
  world.remove(gem);gem=null;completeStage();return;
 }
 updateHUD();
}
function animate(){
 requestAnimationFrame(animate);
 const dt=Math.min(clock.getDelta(),0.05);
 updateGame(dt);
 if(player){
  const target=new THREE.Vector3(player.position.x,player.position.y+1,player.position.z);
  camera.position.lerp(new THREE.Vector3(player.position.x,player.position.y+5.2,player.position.z+8.5),0.09);
  camera.lookAt(new THREE.Vector3(target.x,target.y+0.3,target.z-2));
 }
 if(renderer&&scene&&camera)renderer.render(scene,camera);
}
init3D();
welcome();
})();
</script>
</div>
</body>
</html>
"""

components.html(game_html, height=830, scrolling=False)
