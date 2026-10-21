
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Phiêu lưu cùng chim cánh cụt",
    page_icon="🐧",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(#d9f5ff, #eafaff);
}
.block-container {
    padding-top: 1rem;
    max-width: 1200px;
}
h1 {text-align:center; color:#164e75;}
</style>
""", unsafe_allow_html=True)

st.title("🐧 HÀNH TRÌNH ĐI LẤY CÁ")
st.caption("Giúp chim cánh cụt mẹ và chim con vượt qua dòng sông băng!")

game = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* {box-sizing:border-box}
body {margin:0;font-family:Arial;background:#b8eaff;color:#12324b}
#scene {width:100%;height:560px;position:relative;overflow:hidden;
        border-radius:18px;background:#a5dcf3;border:3px solid white}
canvas {display:block;width:100%;height:100%}
#hud {position:absolute;top:10px;left:10px;right:10px;
      display:flex;justify-content:space-between;gap:6px;flex-wrap:wrap;
      pointer-events:none}
.pill {background:#fffF; padding:9px 12px;border-radius:12px;
       font-weight:bold;box-shadow:0 2px 5px #42657a44}
#panel {position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
        width:min(90%,460px);background:#ffffffF5;padding:20px;
        border-radius:20px;text-align:center;box-shadow:0 8px 25px #164e7544}
#panel h2 {margin:0 0 10px;color:#145580}
#answers {display:grid;grid-template-columns:1fr 1fr;gap:9px}
button {border:0;border-radius:12px;padding:12px;background:#167bb5;
        color:white;font-size:15px;font-weight:bold;cursor:pointer}
button:active {transform:scale(.97)}
button:disabled {opacity:.5}
#message {font-weight:bold;min-height:24px;margin-top:10px}
#controls {position:absolute;bottom:10px;left:10px;right:10px;
           display:flex;justify-content:space-between;align-items:end;
           pointer-events:none}
.pad {display:grid;grid-template-columns:repeat(3,43px);gap:4px}
.pad button,#jump {pointer-events:auto;background:#ffffffE8;color:#155477;
                   border:2px solid #7bbbd7;font-size:19px;padding:8px}
.pad .empty {visibility:hidden}
#jump {border-radius:50%;width:65px;height:65px}
#help {text-align:center;font-size:13px;padding:8px}
@media(max-width:500px) {
 #scene {height:510px}
 #panel {padding:13px}
 button {padding:10px;font-size:14px}
}
</style>
</head>
<body>
<div id="scene">
  <div id="hud">
    <div class="pill" id="stage">🐟 Chặng 1: Đi lấy cá</div>
    <div class="pill" id="score">💎 0/5 hàng</div>
    <div class="pill" id="lives">🧊 Băng yếu: 0/3</div>
  </div>
  <div id="panel">
    <h2 id="title">🐧 Cuộc phiêu lưu bắt đầu!</h2>
    <p id="question">Hãy giúp mẹ con chim cánh cụt vượt qua sông băng để lấy cá nhé!</p>
    <div id="answers"></div>
    <div id="message"></div>
    <button id="start" onclick="startGame()">BẮT ĐẦU CHƠI ▶</button>
  </div>
  <div id="controls">
    <div class="pad">
      <button class="empty"> </button>
      <button onclick="move(0,-1)">⬆️</button>
      <button class="empty"> </button>
      <button onclick="move(-1,0)">⬅️</button>
      <button onclick="move(0,1)">⬇️</button>
      <button onclick="move(1,0)">➡️</button>
    </div>
    <button id="jump" onclick="jump()">⬆</button>
  </div>
</div>
<div id="help">
Dùng WASD hoặc phím mũi tên để di chuyển · Space để nhảy.
Trên điện thoại, dùng các nút điều khiển.
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
const sceneBox = document.getElementById('scene');
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.setSize(sceneBox.clientWidth,sceneBox.clientHeight);
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.outputColorSpace=THREE.SRGBColorSpace;
sceneBox.prepend(renderer.domElement);

const world = new THREE.Scene();
world.background = new THREE.Color(0x9bdcf6);
world.fog = new THREE.Fog(0x9bdcf6, 35, 100);

const camera = new THREE.PerspectiveCamera(
  62, sceneBox.clientWidth/sceneBox.clientHeight, 0.1, 180
);
camera.position.set(0,5,10);

world.add(new THREE.HemisphereLight(0xe5f8ff,0x547e9b,2.0));
const sun = new THREE.DirectionalLight(0xffffff,2.7);
sun.position.set(-8,18,8);
sun.castShadow=true;
sun.shadow.mapSize.set(1024,1024);
world.add(sun);

const mat=(color,roughness=.72,metalness=0)=>
 new THREE.MeshStandardMaterial({color,roughness,metalness});
const snow=mat(0xeaf8ff), ice=mat(0x8bd8f3,.23,.1);
const iceTop=mat(0xc5f1ff,.2,.1), water=mat(0x078bc9,.22,.1);
const wallMat=new THREE.MeshPhysicalMaterial({
 color:0x9cecff,transparent:true,opacity:.43,
 roughness:.12,metalness:.08,depthWrite:false
});
const dark=mat(0x202f40), white=mat(0xffffff), orange=mat(0xffa62b);
const black=mat(0x111d2b), pink=mat(0xffa8c6);

function box(w,h,d,material,x,y,z){
 const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material);
 m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;
 world.add(m);return m;
}
function sphere(rx,ry,rz,material,x,y,z,parent){
 const m=new THREE.Mesh(new THREE.SphereGeometry(1,24,18),material);
 m.scale.set(rx,ry,rz);m.position.set(x,y,z);
 m.castShadow=true;m.receiveShadow=true;
 (parent||world).add(m);return m;
}
function cylinder(rt,rb,h,material,x,y,z,parent){
 const m=new THREE.Mesh(new THREE.CylinderGeometry(rt,rb,h,20),material);
 m.position.set(x,y,z);m.castShadow=true;
 (parent||world).add(m);return m;
}

// Tạo nhân vật 3D tròn trịa, có mắt, mỏ, cánh và chân.
function penguin(scale, baby=false){
 const g=new THREE.Group();
 const bodyMat=mat(baby?0x6a9fc3:0x253d58);
 sphere(.48,.65,.39,bodyMat,0,.78,0,g).scale.multiplyScalar(scale);
 sphere(.35,.48,.31,white,0,.72,.24,g).scale.multiplyScalar(scale);
 sphere(.39,.39,.37,bodyMat,0,1.35,0,g).scale.multiplyScalar(scale);
 sphere(.065,.075,.045,white,-.14,1.39,.325,g).scale.multiplyScalar(scale);
 sphere(.065,.075,.045,white,.14,1.39,.325,g).scale.multiplyScalar(scale);
 sphere(.03,.04,.025,black,-.13,1.39,.364,g).scale.multiplyScalar(scale);
 sphere(.03,.04,.025,black,.15,1.39,.364,g).scale.multiplyScalar(scale);
 const beak= new THREE.Mesh(new THREE.ConeGeometry(.105,.22,12),orange);
 beak.rotation.x=Math.PI/2;beak.position.set(0,1.29,.42);
 beak.scale.setScalar(scale);g.add(beak);
 sphere(.12,.055,.20,orange,-.23,.19,.04,g).scale.multiplyScalar(scale);
 sphere(.12,.055,.20,orange,.23,.19,.04,g).scale.multiplyScalar(scale);
 const wing1=sphere(.13,.35,.12,bodyMat,-.43,.85,0,g);
 const wing2=sphere(.13,.35,.12,bodyMat,.43,.85,0,g);
 wing1.rotation.z=-.25;wing2.rotation.z=.25;
 g.scale.setScalar(scale);
 world.add(g);return g;
}

const mother=penguin(1.0,false);
const baby=penguin(.65,true);
mother.position.set(-.38,0,3);
baby.position.set(.48,0,3.6);

const floor=box(13,.5,110,snow,0,-.55,-42);
const river=box(40,.3,110,water,0,-1.0,-42);
const banks=[];
banks.push(box(4,.5,110,snow,-8,-.45,-42));
banks.push(box(4,.5,110,snow,8,-.45,-42));

// Các cụm tuyết và cây thông để tạo chiều sâu.
for(let i=0;i<38;i++){
 const z=-i*2.9+7;
 for(const side of [-1,1]){
  const x=side*(8+Math.random()*5);
  sphere(.65+Math.random()*.5,.3+Math.random()*.35,
         .8+Math.random()*.5,snow,x,-.12,z);
  if(i%2===0){
   cylinder(.10,.20,1.3,mat(0x72533f),x,.55,z);
   const foliage=mat(0x347b8a);
   for(let j=0;j<3;j++){
    const cone=new THREE.Mesh(
     new THREE.ConeGeometry(1.0-j*.18,1.5,8),foliage);
    cone.position.set(x,1.3+j*.65,z);world.add(cone);
   }
  }
 }
}

let walls=[],tiles=[],fishBucket=null,fish=[];
let stage=0,row=0,weakHits=0,started=false,locked=false;
let xLane=0,progress=0,jumpTime=0,score=0;
let questionIndex=0, returnRow=0, usedRows=new Set();
let messageTimer=0;

const questions=[
 {q:"Nước tinh khiết sôi ở nhiệt độ bao nhiêu (áp suất thường)?",
  a:["50°C","100°C","150°C","200°C"],c:1},
 {q:"Công thức tính khối lượng riêng là gì?",
  a:["D = m/V","D = V/m","D = m × V","D = V − m"],c:0},
 {q:"Đòn bẩy có tác dụng nào?",
  a:["Luôn làm vật nhẹ hơn","Có thể đổi hướng lực","Tạo ra năng lượng","Làm mất trọng lực"],c:1},
 {q:"Số đối của −8 là số nào?",
  a:["−8","0","8","16"],c:2},
 {q:"Khí nào chiếm phần lớn trong không khí?",
  a:["Oxygen","Nitrogen","Carbon dioxide","Hydrogen"],c:1}
];

function clearObjects(list){
 list.forEach(o=>world.remove(o));
 list.length=0;
}
function makeBucket(){
 const g=new THREE.Group();
 cylinder(.30,.36,.48,mat(0xefa83e),0,.24,0,g);
 cylinder(.31,.31,.05,mat(0x9a652c),0,.48,0,g);
 cylinder(.035,.035,.48,mat(0x8c6a42),-.27,.70,0,g).rotation.z=-.5;
 cylinder(.035,.035,.48,mat(0x8c6a42),.27,.70,0,g).rotation.z=.5;
 for(let i=0;i<5;i++){
  const f=sphere(.075,.055,.15,orange,-.18+(i%3)*.16,.56,
                 -.10+Math.floor(i/3)*.13,g);
  f.rotation.z=.3;
 }
 world.add(g);g.position.set(.35,.02,-1);return g;
}
function makeRow(z,index,isReturn){
 // Bốn tảng băng nằm thành hàng ngang.
 for(let lane=0;lane<4;lane++){
  const x=(lane-1.5)*1.75;
  const t=box(1.53,.45,1.65,ice,x,-.1,z);
  const top=box(1.49,.10,1.60,iceTop,x,.17,z);
  const group={x,z,lane,meshes:[t,top],weak:false,used:false};
  if(isReturn){
   group.weak=(lane===Math.floor(Math.random()*4));
  }else{
   // Mỗi hàng có một vách cao, trong suốt ngăn đường đi.
  }
  tiles.push(group);
 }
 if(!isReturn){
  const wall=box(8,.0, .16,wallMat,0,0,z-1.15);
  wall.geometry.dispose();
  wall.geometry=new THREE.BoxGeometry(8,3.2,.16);
  wall.position.y=1.5;
  walls.push({mesh:wall,row:index,down:false});
 }
}
function resetCourse(isReturn){
 clearObjects(walls.map(w=>w.mesh));
 clearObjects(tiles.flatMap(t=>t.meshes));
 tiles=[];walls=[];
 for(let i=0;i<5;i++) makeRow(-i*8-3,i,isReturn);
 floor.position.z=-17;
 mother.position.set(-.38,0,3);
 baby.position.set(.48,0,3.6);
 xLane=0;progress=0;row=0;returnRow=0;
 camera.position.set(0,5,10);
 camera.lookAt(0,1,-2);
}
function updateHud(){
 document.getElementById('stage').textContent=
  stage===1?'🐟 Chặng 1: Đi lấy cá':'🪣 Chặng 2: Đưa cá về';
 document.getElementById('score').textContent=
  stage===1?`🧊 ${Math.min(row,5)}/5 hàng`:`🏁 ${Math.min(returnRow,5)}/5 hàng`;
 document.getElementById('lives').textContent=`⚠️ Băng yếu: ${weakHits}/3`;
}
function panel(title,q,buttons=[],msg=''){
 document.getElementById('title').textContent=title;
 document.getElementById('question').textContent=q;
 document.getElementById('message').textContent=msg;
 const ans=document.getElementById('answers');ans.innerHTML='';
 buttons.forEach((b,i)=>{
  const btn=document.createElement('button');btn.textContent=b;
  btn.onclick=()=>answer(i);ans.appendChild(btn);
 });
}
function startGame(){
 started=true;stage=1;row=0;weakHits=0;score=0;locked=false;
 resetCourse(false);
 document.getElementById('panel').style.display='none';
 updateHud();showQuestion();
}
function showQuestion(){
 locked=true;
 if(row>=5){getFish();return;}
 const q=questions[row];
 document.getElementById('panel').style.display='block';
 panel(`Câu hỏi ${row+1}/5`,q.q,q.a,'Chọn đáp án đúng để hạ vách băng!');
}
function answer(i){
 if(!locked)return;
 const q=questions[row];
 if(i===q.c){
  locked=false;
  const w=walls.find(w=>w.row===row);
  if(w) w.down=true;
  document.getElementById('panel').style.display='none';
  row++;score++;
  progress=Math.max(progress,row);
  updateHud();
  if(row>=5){setTimeout(getFish,1200);}
  else{
   // Đưa nhân vật tới hàng kế tiếp.
   mother.position.z=-row*8+1;
   baby.position.z=mother.position.z+.6;
   setTimeout(showQuestion,1000);
  }
 }else{
  panel('Chưa đúng rồi! 🐧',q.q,q.a,'Hãy thử lại nhé!');
 }
}
function getFish(){
 stage=2;locked=true;
 mother.position.set(-.3,0,-39);
 baby.position.set(.6,0,-39.5);
 if(fishBucket)world.remove(fishBucket);
 fishBucket=makeBucket();
 fishBucket.position.set(.5,0,-39);
 resetCourse(true);
 mother.position.set(-.3,0,3);
 baby.position.set(.6,0,3.6);
 fishBucket.position.set(-.8,.1,2.3);
 // Thể hiện xô cá ngay cạnh chim mẹ.
 document.getElementById('panel').style.display='block';
 document.getElementById('start').style.display='none';
 document.getElementById('answers').innerHTML='';
 panel('🎉 Đã lấy được cá!','Chặng quay về bắt đầu. Hãy cẩn thận với băng yếu.',[],
       'Đi qua 5 hàng băng để đưa cá về nhà.');
 setTimeout(()=>{
  document.getElementById('panel').style.display='none';
  locked=false;updateHud();
 },1800);
}

function move(dx,dz){
 if(!started||locked)return;
 xLane=Math.max(-2.6,Math.min(2.6,xLane+dx*1.05));
 mother.position.x=xLane-.3;
 baby.position.x=xLane+.6;
 if(dz<0){
  mother.position.z-=1.0;baby.position.z-=1.0;
  checkTiles();
 }else if(dz>0){
  mother.position.z+=.7;baby.position.z+=.7;
 }
}
function jump(){
 if(!started||locked)return;
 jumpTime=.65;
 mother.userData.jumping=true;
 baby.userData.jumping=true;
}
function checkTiles(){
 if(stage!==2)return;
 const z=mother.position.z;
 const r=Math.floor((3-z)/8);
 if(r>=0&&r<5&&r>=returnRow){
  const lane=Math.max(0,Math.min(3,Math.round((xLane+2.625)/1.75)));
  const tile=tiles.find(t=>t.lane===lane&&Math.abs(t.z-(-r*8-3))<.2);
  if(tile&&!tile.used){
   tile.used=true;
   if(tile.weak&&jumpTime<=0){
    weakHits++;
    // Băng yếu chìm xuống thật sự.
    tile.meshes.forEach(m=>m.userData.sink=true);
    if(weakHits>=3){fallAndRestart();return;}
   }
   returnRow=r+1;
   updateHud();
   if(returnRow>=5){winGame();}
  }
 }
}
function fallAndRestart(){
 locked=true;
 panel('💦 Ôi! Băng bị vỡ!', 'Chim cánh cụt đã rơi xuống sông băng.',
       [],'Em sẽ quay lại bờ xuất phát cùng thùng cá.');
 mother.userData.falling=true;
 baby.userData.falling=true;
 setTimeout(()=>{
  mother.userData.falling=false;baby.userData.falling=false;
  mother.position.set(-.3,0,3);baby.position.set(.6,0,3.6);
  if(fishBucket)fishBucket.position.set(-.8,.1,2.3);
  xLane=0;returnRow=0;weakHits=0;locked=false;
  tiles.forEach(t=>{t.used=false;t.meshes.forEach(m=>{
   m.position.y=t.meshes.indexOf(m)===0?-.1:.17;
   m.userData.sink=false;
  });});
  panel('Bắt đầu lại nhé! 🐧','Em vẫn có thể đưa cá về nhà!',[],
        'Hãy thử chọn đường đi khác và nhảy qua băng yếu.');
  document.getElementById('start').style.display='block';
  document.getElementById('start').textContent='TIẾP TỤC ▶';
  document.getElementById('start').onclick=()=>{
   document.getElementById('panel').style.display='none';
   locked=false;
  };
 },1600);
}
function winGame(){
 locked=true;
 panel('🎉 VỀ NHÀ AN TOÀN!','Chim mẹ và chim con đã mang cá về nhà!',
       [],'Em đã hoàn thành cả hai chặng phiêu lưu!');
 document.getElementById('start').style.display='block';
 document.getElementById('start').textContent='CHƠI LẠI 🔄';
 document.getElementById('start').onclick=()=>{
  document.getElementById('start').textContent='BẮT ĐẦU CHƠI ▶';
  document.getElementById('start').onclick=startGame;
  document.getElementById('start').style.display='block';
  startGame();
 };
}
function onKey(e){
 if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight',' '].includes(e.key))
  e.preventDefault();
 if(e.key==='ArrowUp'||e.key==='w')move(0,-1);
 if(e.key==='ArrowDown'||e.key==='s')move(0,1);
 if(e.key==='ArrowLeft'||e.key==='a')move(-1,0);
 if(e.key==='ArrowRight'||e.key==='d')move(1,0);
 if(e.key===' ')jump();
}
window.addEventListener('keydown',onKey);
window.move=move;window.jump=jump;window.startGame=startGame;window.answer=answer;

function animate(){
 requestAnimationFrame(animate);
 const dt=.016;
 if(jumpTime>0){
  jumpTime-=dt;
  const h=Math.sin((.65-jumpTime)/.65*Math.PI)*1.1;
  mother.position.y=Math.max(0,h);
  baby.position.y=Math.max(0,h*.7);
 }else{
  mother.position.y+=(0-mother.position.y)*.2;
  baby.position.y+=(0-baby.position.y)*.2;
 }
 if(mother.userData.falling){
  mother.position.y-=.07;baby.position.y-=.06;
 }
 walls.forEach(w=>{
  if(w.down&&w.mesh.position.y>-2.1){
   w.mesh.position.y-=.045;
  }
 });
 tiles.forEach(t=>{
  t.meshes.forEach(m=>{
   if(m.userData.sink&&m.position.y> -1.5){
    m.position.y-=.045;
   }
  });
 });
 // Góc máy theo sau nhân vật.
 const target=new THREE.Vector3(mother.position.x,1.1,mother.position.z+6.8);
 camera.position.lerp(target,.08);
 camera.lookAt(mother.position.x,1.0,mother.position.z-5);
 if(fishBucket&&stage===2){
  fishBucket.position.x=mother.position.x-.5;
  fishBucket.position.z=mother.position.z+.5;
 }
 renderer.render(world,camera);
}
window.addEventListener('resize',()=>{
 camera.aspect=sceneBox.clientWidth/sceneBox.clientHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(sceneBox.clientWidth,sceneBox.clientHeight);
});
animate();
</script>
</body>
</html>
"""

components.html(game, height=650, scrolling=False)
