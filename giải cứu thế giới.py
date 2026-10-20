
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="GIẢI CỨU THẾ GIỚI", page_icon="🌳", layout="wide")
st.markdown("""<style>#MainMenu,header,footer{visibility:hidden}.block-container{padding:0!important;max-width:100%!important}[data-testid="stAppViewContainer"]{background:#071b12}iframe{border:0!important}</style>""", unsafe_allow_html=True)

game_html = r"""
<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}
html,body,#world{margin:0;width:100%;height:100%;overflow:hidden;background:#071b12;font-family:Arial;color:white}
#world{position:fixed;inset:0}
canvas{display:block}
.overlay{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:#03180fc9;padding:12px}
.panel{width:min(550px,96vw);max-height:94vh;overflow:auto;padding:22px;border:2px solid #b6ef83;border-radius:22px;background:#103b27f5;text-align:center;box-shadow:0 0 30px #173e25}
h1{color:#d4ff9b;font-size:clamp(27px,5vw,43px);line-height:1.1}
p{line-height:1.45}
input{width:100%;padding:12px;border-radius:10px;border:0;font-size:16px;margin:8px 0}
button{border:0;border-radius:12px;padding:11px 13px;background:#d4ff9b;color:#153820;font-size:15px;font-weight:bold;cursor:pointer}
.row{display:flex;gap:10px;margin:10px 0}.row button{flex:1}
.secondary{background:#28563a;color:white;border:1px solid #a3d984}
.selected{outline:3px solid white}
#hud{position:absolute;top:10px;left:10px;right:10px;display:none;justify-content:space-between;gap:8px;pointer-events:none}
.pill{background:#092a1ee8;border:1px solid #c0ed98;border-radius:12px;padding:9px;font-weight:bold}
#hint{position:absolute;top:60px;left:50%;transform:translateX(-50%);background:#092a1ee8;border-radius:9px;padding:8px;text-align:center;font-size:13px;max-width:94%;display:none}
#pad{position:absolute;bottom:18px;left:18px;width:140px;height:140px;display:none;border-radius:50%;border:2px solid #d4ff9b;background:rgba(10,45,27,.65);touch-action:none;user-select:none}
#joystick{position:absolute;left:50%;top:50%;width:48px;height:48px;margin-left:-24px;margin-top:-24px;border-radius:50%;border:2px solid white;background:#d4ff9b;box-shadow:0 0 10px #9cff8a;pointer-events:none}
#question,#win{display:none}
.answer{display:block;width:100%;text-align:left;margin:7px 0;background:#efffe3;color:#153820;transition:background .2s,color .2s}
.answer.correct{background:#22a447!important;color:white!important}
.answer.wrong{background:#d93030!important;color:white!important}
#feedback{min-height:22px;color:#ffe99b;font-weight:bold}
#confetti{position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:20;display:none}
@media(max-width:600px){.panel{padding:18px 12px}.pill{font-size:12px;padding:8px}#hud{top:6px;left:6px;right:6px}#pad{left:7px;bottom:7px;width:132px;height:132px}}
</style>
</head>
<body>
<div id="world"></div>
<canvas id="confetti"></canvas>

<div id="menu" class="overlay">
 <div class="panel">
  <h1>🌿 GIẢI CỨU<br>THẾ GIỚI 🌿</h1>
  <p>Khu rừng đang héo úa! Tìm 3 viên đá quý và mở 2 rương kho báu bằng cách trả lời câu hỏi để có đủ 5 viên, rồi đến Cây Cổ Thụ.</p>
  <input id="playerName" maxlength="18" value="Nhà thám hiểm" placeholder="Tên nhân vật">
  <div class="row">
   <button id="boy" class="secondary selected">🧑 Nhân vật nam</button>
   <button id="girl" class="secondary">👩 Nhân vật nữ</button>
  </div>
  <button id="start" style="width:100%;font-size:18px">BẮT ĐẦU PHIÊU LƯU ▶</button>
  <p style="font-size:12px">Dùng WASD / phím mũi tên hoặc joystick tròn để di chuyển.</p>
 </div>
</div>

<div id="hud">
 <div class="pill">🧭 <span id="nameHud"></span></div>
 <div class="pill">💎 Đá quý: <span id="count">0</span>/5</div>
</div>
<div id="hint">Khám phá khu rừng để tìm đá quý và rương kho báu!</div>
<div id="pad"><div id="joystick"></div></div>

<div id="question" class="overlay">
 <div class="panel">
  <h1 style="font-size:30px">🎁 RƯƠNG KHO BÁU</h1>
  <p id="questionText"></p>
  <div id="answers"></div>
  <div id="feedback"></div>
 </div>
</div>

<div id="win" class="overlay">
 <div class="panel">
  <h1>🏆 BẠN ĐÃ CHIẾN THẮNG! 🏆</h1>
  <p>BẠN ĐÃ GIẢI CỨU THẾ GIỚI THÀNH CÔNG!</p>
  <p>Cây Cổ Thụ đã hồi sinh, ánh sáng phép thuật lan khắp khu rừng!</p>
  <button id="again">Chơi lại ↻</button>
 </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
(()=>{
const $=id=>document.getElementById(id),world=$('world');
if(!window.THREE){
 world.innerHTML='<div style="padding:25px">Không tải được thư viện 3D. Hãy kiểm tra Internet rồi tải lại trang.</div>';
 return;
}

const scene=new THREE.Scene();
const camera=new THREE.PerspectiveCamera(65,innerWidth/innerHeight,.1,350);
scene.background=new THREE.Color(0x91b98b);
scene.fog=new THREE.FogExp2(0x789c6e,.008);

const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio||1,1.6));
renderer.setSize(innerWidth,innerHeight);
renderer.outputColorSpace=THREE.SRGBColorSpace;
world.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xe1ffdf,0x243b20,2));
const sun=new THREE.DirectionalLight(0xffedc4,2);
sun.position.set(-20,35,15);
scene.add(sun);

const mat=c=>new THREE.MeshStandardMaterial({color:c,roughness:.9});
const greens=[mat(0x194d2a),mat(0x286235),mat(0x377b3a),mat(0x4c8a42)];
const bark=mat(0x624329),ground=mat(0x244d28),pathmat=mat(0x93815c);

function put(geo,m,x,y,z,parent=scene){
 const o=new THREE.Mesh(geo,m);
 o.position.set(x,y,z);
 parent.add(o);
 return o;
}

let seed=199;
function rand(){
 seed=(seed*1664525+1013904223)>>>0;
 return seed/4294967296;
}

put(new THREE.PlaneGeometry(240,240),ground,0,-.15,-28).rotation.x=-Math.PI/2;

function tree(x,z,s=1){
 const g=new THREE.Group();
 g.position.set(x,0,z);
 g.scale.setScalar(s);
 scene.add(g);
 put(new THREE.CylinderGeometry(.25,.48,4.6,7),bark,0,2.3,0,g);
 for(let i=0;i<4;i++){
  put(new THREE.ConeGeometry(2.2-i*.28,2.8,7),
   greens[(i+Math.floor(rand()*3))%4],
   (rand()-.5)*.5,3.2+i*.65,(rand()-.5)*.5,g);
 }
}

function bush(x,z,s){
 const o=put(new THREE.DodecahedronGeometry(.7*s,1),greens[Math.floor(rand()*4)],x,.4*s,z);
 o.scale.set(1.4,.8,1);
}

// Đường rừng nằm ngang bằng mặt đất
const curve=new THREE.CatmullRomCurve3([
 [0,-.14,13],[1,-.14,4],[-2,-.14,-5],[-5,-.14,-15],
 [-2,-.14,-25],[4,-.14,-35],[2,-.14,-45],
 [-3,-.14,-54],[0,-.14,-65],[0,-.14,-75]
].map(p=>new THREE.Vector3(...p)));

const roadPoints=curve.getPoints(180),roadVertices=[],roadIndices=[];
for(let i=0;i<roadPoints.length;i++){
 const p=roadPoints[i],prev=roadPoints[Math.max(0,i-1)],next=roadPoints[Math.min(roadPoints.length-1,i+1)];
 let dx=next.x-prev.x,dz=next.z-prev.z,len=Math.hypot(dx,dz)||1;
 const ox=-dz/len*1.65,oz=dx/len*1.65;
 roadVertices.push(p.x+ox,-.14,p.z+oz,p.x-ox,-.14,p.z-oz);
 if(i<roadPoints.length-1){
  const a=i*2,b=a+1,c=a+2,d=a+3;
  roadIndices.push(a,b,c,b,d,c);
 }
}
const roadGeometry=new THREE.BufferGeometry();
roadGeometry.setAttribute('position',new THREE.Float32BufferAttribute(roadVertices,3));
roadGeometry.setIndex(roadIndices);
roadGeometry.computeVertexNormals();
scene.add(new THREE.Mesh(roadGeometry,new THREE.MeshStandardMaterial({color:0x93815c,side:THREE.DoubleSide,roughness:1})));

for(let i=0;i<230;i++){
 let x=(rand()-.5)*120,z=(rand()-.5)*145-20;
 if(Math.abs(x)<8&&z<14&&z>-78)x+=(x<0?-1:1)*(9+rand()*14);
 tree(x,z,.65+rand()*.9);
}
for(let i=0;i<100;i++){
 let x=(rand()-.5)*120,z=(rand()-.5)*140-20;
 if(!(Math.abs(x)<5&&z<14&&z>-78))bush(x,z,.4+rand()*.7);
}

const ancient=new THREE.Group();
ancient.position.set(0,0,-78);
scene.add(ancient);
put(new THREE.CylinderGeometry(1.4,2.3,13,10),mat(0x4c3827),0,6.5,0,ancient);

const oldLeaves=[];
for(let i=0;i<7;i++){
 oldLeaves.push(put(new THREE.ConeGeometry(4.5-i*.25,5.4,8),
 mat(0x777343),Math.sin(i*2)*1.5,10+i*.8,Math.cos(i*2)*1.2,ancient));
}

const beam=put(new THREE.CylinderGeometry(.2,2.1,65,24,1,true),
 new THREE.MeshBasicMaterial({color:0xc8ff9b,transparent:true,opacity:.38,side:THREE.DoubleSide}),
 0,35,0,ancient);
beam.visible=false;

// Mũi tên nét đứt chỉ đường đến Cây Cổ Thụ
const guide=new THREE.Group();
scene.add(guide);
const guideMat=new THREE.LineDashedMaterial({color:0xfff47a,dashSize:1.2,gapSize:.65,linewidth:2});
const guideLine=new THREE.Line(new THREE.BufferGeometry(),guideMat);
guide.add(guideLine);
const arrowHead=put(new THREE.ConeGeometry(.55,1.4,6),
 new THREE.MeshBasicMaterial({color:0xfff47a}),0,0,0,guide);
guide.visible=false;

const questions=[
 {q:'Dấu hiệu nào sau đây không phải là dấu hiệu nhận biết hình bình hành?',a:['Tứ giác có hai đường chéo vuông góc.','Tứ giác có các cạnh đối bằng nhau.','Tứ giác có các góc đối bằng nhau.','Tứ giác có hai đường chéo cắt nhau tại trung điểm mỗi đường.'],c:0},
 {q:'Khối lượng nguyên tử của nguyên tố Sulfur (lưu huỳnh) xấp xỉ bằng bao nhiêu amu?',a:['40 amu.','90 amu.','32 amu.','Không có đáp án đúng.'],c:2},
 {q:'Công thức tính khối lượng riêng là gì?',a:['D = V/m','D = m/V','D = m × V','D = m + V'],c:1},
 {q:'Kết quả phân tích đa thức x² − 9 thành nhân tử là gì?',a:['(x − 3)²','(x − 9)(x + 1)','x(x − 9)','(x − 3)(x + 3)'],c:3},
 {q:'Đặc điểm nổi bật của khí hậu môi trường nhiệt đới là gì?',a:['Nhiệt độ thấp quanh năm.','Băng tuyết quanh năm.','Mưa nhiều quanh năm, không có mùa khô.','Nhiệt độ cao, có sự thay đổi theo mùa.'],c:3},
 {q:'Hệ cơ quan nào có chức năng vận chuyển oxygen và các chất dinh dưỡng đến tế bào?',a:['Hệ tiêu hóa.','Hệ tuần hoàn.','Hệ hô hấp.','Hệ bài tiết.'],c:1}
];

let player=null,gender='boy',started=false,collected=0,keys={},
joyX=0,joyY=0,joyActive=false,joyPointer=null,
gems=[],chests=[],used=[],activeChest=null,won=false,winTimer=null;

function character(type){
 const g=new THREE.Group(),skin=mat(0xe6b38c),
 shirt=mat(type==='girl'?0xe6a83d:0x3f91d0),
 pants=mat(type==='girl'?0x3887ad:0x59422f),
 hair=mat(type==='girl'?0x75412a:0x59351f),shoe=mat(0x30251f);
 for(const s of [-1,1]){
  put(new THREE.CylinderGeometry(.1,.12,.72,8),pants,s*.16,.52,0,g);
  put(new THREE.BoxGeometry(.22,.12,.32),shoe,s*.16,.13,.08,g);
  put(new THREE.CylinderGeometry(.07,.09,.6,8),skin,s*.34,1.16,0,g);
 }
 put(new THREE.CylinderGeometry(.22,.25,.53,10),shirt,0,1.08,0,g);
 put(new THREE.SphereGeometry(.24,14,12),skin,0,1.57,0,g);
 put(new THREE.SphereGeometry(.25,14,10),hair,0,1.74,-.03,g);
 if(type==='girl')put(new THREE.BoxGeometry(.32,.4,.16),hair,0,1.48,-.18,g);
 return g;
}

function addGem(x,z,color){
 const g=new THREE.Group();
 g.position.set(x,.9,z);
 scene.add(g);
 put(new THREE.OctahedronGeometry(.55),
  new THREE.MeshStandardMaterial({color,emissive:color,emissiveIntensity:.8,metalness:.3,roughness:.2}),0,0,0,g);
 const ring=put(new THREE.TorusGeometry(.66,.035,8,28),
  new THREE.MeshBasicMaterial({color}),0,0,0,g);
 ring.rotation.x=Math.PI/2;
 gems.push({group:g,found:false});
}

function addChest(x,z){
 const g=new THREE.Group();
 g.position.set(x,0,z);
 scene.add(g);
 put(new THREE.BoxGeometry(1.25,.72,.85),mat(0x75451f),0,.45,0,g);
 const lid=put(new THREE.BoxGeometry(1.3,.28,.9),mat(0x99602b),0,.91,0,g);
 put(new THREE.BoxGeometry(1.34,.12,.94),mat(0xf3c34e),0,.68,0,g);
 put(new THREE.BoxGeometry(.18,.28,.08),mat(0xf3c34e),0,.56,.47,g);
 chests.push({group:g,lid,opened:false,x,z,questionShown:false});
}

function clearCollectibles(){
 [...gems.map(g=>g.group),...chests.map(c=>c.group)].forEach(o=>scene.remove(o));
 gems=[];chests=[];
}

// Rải vật phẩm ở nhiều vị trí trong khu rừng, không chỉ dọc đường
function scatterCollectibles(){
 const colors=[0x38ff9a,0xff405c,0x3977ff,0xffd447,0xd86bff,0x42e8ff,0xff8844];
 const spots=[];
 for(let i=0;i<38;i++){
  let x=(rand()-.5)*58;
  let z=12-rand()*88;
  if(Math.abs(x)<4&&z<12&&z>-77)x+=(x<0?-1:1)*(5+rand()*8);
  if(Math.hypot(x,z+78)<7)continue;
  if(spots.some(p=>Math.hypot(p.x-x,p.z-z)<5))continue;
  spots.push({x,z});
 }
 // Ba viên đá quý cần thu thập trong rừng
 for(let i=0;i<3;i++){
  const p=spots[i];
  addGem(p.x,p.z,colors[i]);
 }
 // Hai rương nằm ở các vị trí khác nhau trong khu rừng
 for(let i=3;i<5;i++){
  const p=spots[i];
  addChest(p.x,p.z);
 }
 // Thêm đá quý trang trí có thể thu thập được, số lượng không giới hạn nhiệm vụ
 for(let i=5;i<spots.length;i++){
  const p=spots[i];
  addGem(p.x,p.z,colors[i%colors.length]);
 }
}

function reset(){
 clearCollectibles();
 collected=0;used=[];won=false;activeChest=null;
 $('count').textContent='0';
 $('hint').textContent='Khám phá khu rừng để tìm đá quý và rương kho báu!';
 guide.visible=false;beam.visible=false;
 oldLeaves.forEach(o=>o.material.color.setHex(0x777343));
 if(player)scene.remove(player);
 player=character(gender);
 player.position.set(0,0,8);
 scene.add(player);
 scatterCollectibles();
 camera.position.set(0,5,16);
 camera.lookAt(0,1,0);
}

function start(){
 gender=$('girl').classList.contains('selected')?'girl':'boy';
 reset();
 $('nameHud').textContent=($('playerName').value||'Nhà thám hiểm').trim().slice(0,18);
 $('menu').style.display='none';
 $('hud').style.display='flex';
 $('pad').style.display='block';
 $('hint').style.display='block';
 $('win').style.display='none';
 $('question').style.display='none';
 started=true;
}
$('boy').onclick=()=>{$('boy').classList.add('selected');$('girl').classList.remove('selected');};
$('girl').onclick=()=>{$('girl').classList.add('selected');$('boy').classList.remove('selected');};
$('start').onclick=start;

// Pháo giấy khi trả lời đúng
const confettiCanvas=$('confetti'),ctx=confettiCanvas.getContext('2d');
let confettiPieces=[],confettiUntil=0;
function launchConfetti(){
 confettiCanvas.width=innerWidth;
 confettiCanvas.height=innerHeight;
 confettiCanvas.style.display='block';
 confettiPieces=[];
 const palette=['#ff4040','#ffd93d','#45e879','#4ac6ff','#d56bff','#ff9f43'];
 for(let i=0;i<150;i++){
  confettiPieces.push({
   x:innerWidth*.5+(Math.random()-.5)*innerWidth*.5,
   y:innerHeight*.38,
   vx:(Math.random()-.5)*12,
   vy:-Math.random()*10-3,
   size:4+Math.random()*7,
   color:palette[Math.floor(Math.random()*palette.length)],
   rot:Math.random()*6,
   vr:(Math.random()-.5)*.3
  });
 }
 confettiUntil=performance.now()+2200;
}
function drawConfetti(now){
 if(confettiCanvas.style.display==='none')return;
 ctx.clearRect(0,0,confettiCanvas.width,confettiCanvas.height);
 confettiPieces.forEach(p=>{
  p.x+=p.vx;p.y+=p.vy;p.vy+=.19;p.rot+=p.vr;
  ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rot);
  ctx.fillStyle=p.color;ctx.fillRect(-p.size/2,-p.size/2,p.size,p.size*.65);ctx.restore();
 });
 if(now>confettiUntil){
  confettiCanvas.style.display='none';
  return;
 }
 requestAnimationFrame(drawConfetti);
}

function ask(chest){
 if(!chest||chest.opened||chest.questionShown)return;
 activeChest=chest;
 chest.questionShown=true;
 const pool=questions.map((q,i)=>i).filter(i=>!used.includes(i));
 if(!pool.length)used=[];
 const available=questions.map((q,i)=>i).filter(i=>!used.includes(i));
 const ix=available[Math.floor(Math.random()*available.length)];
 used.push(ix);
 const q=questions[ix];
 $('questionText').textContent=q.q;
 $('feedback').textContent='Chọn đáp án để mở rương!';
 const box=$('answers');
 box.innerHTML='';
 q.a.forEach((a,i)=>{
  const b=document.createElement('button');
  b.className='answer';
  b.textContent=String.fromCharCode(65+i)+'. '+a;
  b.onclick=()=>{
   if(b.classList.contains('wrong')||b.classList.contains('correct'))return;
   if(i===q.c){
    b.classList.add('correct');
    $('feedback').textContent='Chính xác! Em nhận được đá quý! 💎';
    chest.opened=true;
    chest.lid.rotation.x=-1;
    chest.lid.position.y=1.15;
    collected++;
    $('count').textContent=collected;
    launchConfetti();
    requestAnimationFrame(drawConfetti);
    box.querySelectorAll('button').forEach(x=>x.disabled=true);
    setTimeout(()=>{
     $('question').style.display='none';
     activeChest=null;
    },1100);
   }else{
    b.classList.add('wrong');
    $('feedback').textContent='Chưa đúng! Em thử đáp án khác nha.';
   }
  };
  box.appendChild(b);
 });
 $('question').style.display='flex';
 stopJoystick();
}

function updateGuide(){
 if(collected<5||won){
  guide.visible=false;
  return;
 }
 guide.visible=true;
 const from=new THREE.Vector3(player.position.x,.25,player.position.z);
 const to=new THREE.Vector3(0,.25,-78);
 const points=[];
 const steps=18;
 for(let i=0;i<=steps;i++){
  const t=i/steps;
  points.push(new THREE.Vector3(
   THREE.MathUtils.lerp(from.x,to.x,t),
   .25+Math.sin(t*Math.PI)*.45,
   THREE.MathUtils.lerp(from.z,to.z,t)
  ));
 }
 guideLine.geometry.dispose();
 guideLine.geometry=new THREE.BufferGeometry().setFromPoints(points);
 guideLine.computeLineDistances();
 arrowHead.position.set(0,.8,-75);
 arrowHead.rotation.set(Math.PI,0,0);
}

function winGame(){
 if(won)return;
 won=true;started=false;
 guide.visible=false;
 beam.visible=true;
 oldLeaves.forEach(o=>o.material.color.setHex(0x35b84c));
 $('hint').textContent='Cây Cổ Thụ đã hồi sinh!';
 $('win').style.display='flex';
}

$('again').onclick=()=>{
 started=false;
 $('win').style.display='none';
 $('menu').style.display='flex';
 $('hud').style.display='none';
 $('pad').style.display='none';
 $('hint').style.display='none';
 $('question').style.display='none';
 $('confetti').style.display='none';
};

const pad=$('pad'),joystick=$('joystick');
function moveJoystick(e){
 const rect=pad.getBoundingClientRect();
 const cx=rect.left+rect.width/2,cy=rect.top+rect.height/2;
 let dx=e.clientX-cx,dy=e.clientY-cy;
 const max=43,len=Math.hypot(dx,dy);
 if(len>max){dx=dx/len*max;dy=dy/len*max;}
 joyX=dx/max;joyY=dy/max;
 joystick.style.transform=`translate(${dx}px,${dy}px)`;
}
function stopJoystick(){
 joyActive=false;joyPointer=null;joyX=0;joyY=0;
 joystick.style.transform='translate(0px,0px)';
}
pad.addEventListener('pointerdown',e=>{
 if(!started||$('question').style.display==='flex')return;
 e.preventDefault();joyActive=true;joyPointer=e.pointerId;
 pad.setPointerCapture(e.pointerId);moveJoystick(e);
});
pad.addEventListener('pointermove',e=>{
 if(!joyActive||e.pointerId!==joyPointer)return;
 e.preventDefault();moveJoystick(e);
});
pad.addEventListener('pointerup',e=>{if(e.pointerId===joyPointer)stopJoystick();});
pad.addEventListener('pointercancel',stopJoystick);

addEventListener('keydown',e=>{
 const k=e.key.toLowerCase();
 if($('question').style.display==='flex'&&['a','b','c','d'].includes(k)){
  e.preventDefault();
  const buttons=$('answers').querySelectorAll('button');
  const index=k.charCodeAt(0)-97;
  if(buttons[index]&&!buttons[index].disabled)buttons[index].click();
  return;
 }
 keys[k]=true;
 if(e.key.startsWith('Arrow'))e.preventDefault();
});
addEventListener('keyup',e=>keys[e.key.toLowerCase()]=false);
addEventListener('blur',()=>{keys={};stopJoystick();});
addEventListener('resize',()=>{
 camera.aspect=innerWidth/innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
 confettiCanvas.width=innerWidth;confettiCanvas.height=innerHeight;
});

const clock=new THREE.Clock();
function animate(){
 requestAnimationFrame(animate);
 const dt=Math.min(clock.getDelta(),.04),t=clock.elapsedTime;

 if(started&&player&&$('question').style.display!=='flex'){
  const f=keys.w||keys.arrowup,b=keys.s||keys.arrowdown;
  const l=keys.a||keys.arrowleft,r=keys.d||keys.arrowright;
  let moveX=(r?1:0)-(l?1:0)+joyX;
  let moveZ=(b?1:0)-(f?1:0)+joyY;
  const len=Math.hypot(moveX,moveZ);
  if(len>1){moveX/=len;moveZ/=len;}
  const v=7*dt;
  player.position.x+=moveX*v;
  player.position.z+=moveZ*v;
  player.position.x=Math.max(-29,Math.min(29,player.position.x));
  player.position.z=Math.max(-84,Math.min(15,player.position.z));
  if(len>.08)player.rotation.y=Math.atan2(moveX,moveZ);

  gems.forEach(g=>{
   if(g.found)return;
   g.group.rotation.y+=dt*1.6;
   g.group.position.y=.9+Math.sin(t*2+g.group.position.z)*.13;
   if(Math.hypot(player.position.x-g.group.position.x,player.position.z-g.group.position.z)<1.7){
    g.found=true;g.group.visible=false;collected++;
    $('count').textContent=collected;
    $('hint').textContent='Đã nhặt được đá quý! 💎';
   }
  });

  const nearChest=chests.find(c=>!c.opened&&Math.hypot(player.position.x-c.x,player.position.z-c.z)<3.6);
  if(nearChest){
   nearChest.lid.rotation.x=-1;
   nearChest.lid.position.y=1.15;
   if(!nearChest.questionShown&&!activeChest)ask(nearChest);
  }

  if(collected>=5){
   $('hint').textContent='Đã đủ 5 viên đá quý! Đi theo các nét đứt đến Cây Cổ Thụ.';
   updateGuide();
   if(Math.hypot(player.position.x,player.position.z+78)<8){
    winGame();
   }
  }else{
   guide.visible=false;
  }

  const target=new THREE.Vector3(player.position.x,player.position.y+4.1,player.position.z+8.5);
  camera.position.lerp(target,1-Math.pow(.001,dt));
  camera.lookAt(player.position.x,player.position.y+1.15,player.position.z-3.4);
 }

 if(beam.visible)beam.material.opacity=.25+Math.sin(t*3)*.08;
 renderer.render(scene,camera);
}

reset();
player.visible=false;
animate();
})();
</script>
</body>
</html>
"""
components.html(game_html, height=820, scrolling=False)
