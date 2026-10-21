
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Chim Cánh Cụt Vượt Sông Băng", page_icon="🐧", layout="wide")

st.markdown("""
<style>
.stApp {background:#dff5ff}
.block-container {padding-top:1rem;max-width:1200px}
h1 {text-align:center;color:#164b70}
</style>
""", unsafe_allow_html=True)

st.title("🐧 Chim Cánh Cụt Vượt Sông Băng")
st.caption("Giúp chim mẹ lấy cá và đưa cá trở về an toàn!")

game = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box}
body{margin:0;font-family:Arial;background:#b9eaff;color:#163d58}
#game{position:relative;width:100%;height:650px;overflow:hidden;
border-radius:16px;border:3px solid white;background:#9edcf6}
canvas{display:block}
#hud{position:absolute;top:8px;left:8px;right:8px;display:flex;
justify-content:space-between;gap:5px;flex-wrap:wrap;pointer-events:none}
.tag{background:#ffffffed;border-radius:10px;padding:8px;font-weight:bold;font-size:13px}
#quiz{position:absolute;top:52px;left:3%;width:94%;text-align:center;pointer-events:none}
#question{display:inline-block;background:#ffffffed;border-radius:10px;
padding:9px 14px;font-weight:bold;max-width:100%;font-size:15px}
#answers{display:flex;justify-content:center;gap:8px;margin-top:8px;pointer-events:auto}
.answer{flex:1;max-width:180px;min-width:0;padding:10px 3px;border:2px solid white;
border-radius:10px;background:#ffdf9f;color:#563b19;font-weight:bold;font-size:13px;
box-shadow:0 3px 0 #bd9455;overflow-wrap:anywhere}
.answer:disabled{opacity:.7}
#notice{position:absolute;left:50%;top:44%;transform:translate(-50%,-50%);
width:85%;max-width:400px;text-align:center;background:#ffffffef;border-radius:16px;
padding:18px;box-shadow:0 5px 20px #164e7544;display:none}
#notice h2{margin:0 0 8px;font-size:22px}
#notice button{background:#1379b2;color:white;border:0;border-radius:10px;
padding:12px 20px;font-weight:bold;font-size:15px}
#controls{position:absolute;bottom:10px;left:10px;right:10px;
display:flex;justify-content:space-between;align-items:end;pointer-events:none}
.pad{display:grid;grid-template-columns:repeat(3,43px);gap:4px}
.pad button,#jump{pointer-events:auto;background:#ffffffed;color:#164e70;
border:2px solid #75b9d7;border-radius:12px;font-size:19px;padding:8px}
.pad .empty{visibility:hidden}
#jump{border-radius:50%;width:65px;height:65px}
#help{text-align:center;font-size:12px;padding:7px}
@media(max-width:500px){
 #game{height:590px}
 #question{font-size:13px}
 .answer{font-size:11px;padding:8px 2px}
 #answers{gap:4px}
}
</style>
</head>
<body>
<div id="game">
 <div id="hud">
  <div class="tag" id="stageTag">🐟 Chặng 1: Đi lấy cá</div>
  <div class="tag" id="progress">Câu 1/5</div>
  <div class="tag" id="danger">⚠️ Băng yếu: 0/3</div>
 </div>
 <div id="quiz">
  <div id="question">Bấm BẮT ĐẦU để chơi!</div>
  <div id="answers"></div>
 </div>
 <div id="notice">
  <h2 id="noticeTitle"></h2>
  <p id="noticeText"></p>
  <button id="noticeButton" onclick="buttonAction()">BẮT ĐẦU ▶</button>
 </div>
 <div id="controls">
  <div class="pad">
   <button class="empty"> </button><button onclick="move(0,-1)">⬆️</button><button class="empty"> </button>
   <button onclick="move(-1,0)">⬅️</button><button onclick="move(0,1)">⬇️</button><button onclick="move(1,0)">➡️</button>
  </div>
  <button id="jump" onclick="jump()">⬆ NHẢY</button>
 </div>
</div>
<div id="help">Chọn đáp án để nhảy tới tảng băng tương ứng · Chặng về: dùng phím mũi tên hoặc nút điều khiển.</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
const root=document.getElementById('game');
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.setSize(root.clientWidth,root.clientHeight);
renderer.shadowMap.enabled=true;
renderer.outputColorSpace=THREE.SRGBColorSpace;
root.prepend(renderer.domElement);

const scene=new THREE.Scene();
scene.background=new THREE.Color(0x9edcf6);
scene.fog=new THREE.Fog(0x9edcf6,35,100);
const camera=new THREE.PerspectiveCamera(62,root.clientWidth/root.clientHeight,.1,150);
scene.add(new THREE.HemisphereLight(0xe9faff,0x52788a,2.1));
const sun=new THREE.DirectionalLight(0xffffff,2.5);
sun.position.set(-8,18,10);sun.castShadow=true;scene.add(sun);

const mat=(c,rough=.65,metal=0)=>new THREE.MeshStandardMaterial({color:c,roughness:rough,metalness:metal});
const snow=mat(0xf0fbff), ice=mat(0x91dff5,.23,.1);
const topIce=mat(0xc9f4ff,.2,.1), water=mat(0x047fb9,.22,.1);
const black=mat(0x202d40), white=mat(0xffffff), orange=mat(0xffa52b);
const wallMat=new THREE.MeshPhysicalMaterial({color:0x8eeaff,transparent:true,opacity:.42,roughness:.16,depthWrite:false});

function cube(w,h,d,m,x,y,z){
 const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);
 o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;scene.add(o);return o;
}
function ball(rx,ry,rz,m,x,y,z,parent=scene){
 const o=new THREE.Mesh(new THREE.SphereGeometry(1,24,18),m);
 o.scale.set(rx,ry,rz);o.position.set(x,y,z);o.castShadow=true;
 parent.add(o);return o;
}
function penguin(scale,bodyColor){
 const g=new THREE.Group(), body=mat(bodyColor);
 ball(.43,.58,.35,body,0,.72,0,g);
 ball(.31,.43,.28,white,0,.69,.20,g);
 ball(.35,.35,.32,body,0,1.25,0,g);
 ball(.045,.05,.025,white,-.12,1.29,.29,g);
 ball(.045,.05,.025,white,.12,1.29,.29,g);
 ball(.022,.03,.02,black,-.12,1.29,.315,g);
 ball(.022,.03,.02,black,.12,1.29,.315,g);
 const beak=new THREE.Mesh(new THREE.ConeGeometry(.09,.19,12),orange);
 beak.rotation.x=Math.PI/2;beak.position.set(0,1.19,.36);g.add(beak);
 ball(.11,.05,.17,orange,-.19,.17,.02,g);
 ball(.11,.05,.17,orange,.19,.17,.02,g);
 const a=ball(.12,.29,.1,body,-.39,.79,0,g);
 const b=ball(.12,.29,.1,body,.39,.79,0,g);
 a.rotation.z=-.2;b.rotation.z=.2;
 g.scale.setScalar(scale);scene.add(g);return g;
}

// Nền tuyết hai bên và sông nước chưa đóng băng ở giữa.
cube(7,.5,115,snow,-7,-.45,-43);
cube(7,.5,115,snow,7,-.45,-43);
cube(8,.2,120,water,0,-1.0,-43);
cube(40,.2,120,water,0,-1.35,-43);

for(let i=0;i<32;i++){
 const z=6-i*3.3;
 for(const side of [-1,1]){
  const x=side*(7.8+Math.random()*2.5);
  cube(.18,1.2,.18,mat(0x795642),x,.3,z);
  for(let j=0;j<3;j++){
   const cone=new THREE.Mesh(new THREE.ConeGeometry(1.05-j*.22,1.5,8),mat(0x287c87));
   cone.position.set(x,.9+j*.65,z);scene.add(cone);
  }
  ball(.8,.3,1,snow,x,-.1,z);
 }
}

const mother=penguin(1,0x253d58);
const baby=penguin(.65,0x6b9fc3);
// Chim con đứng yên ở bờ xuất phát.
baby.position.set(2.0,0,4.0);
let bucket=null;

function makeBucket(){
 const g=new THREE.Group();
 const bm=mat(0xe8a53a);
 const c=new THREE.Mesh(new THREE.CylinderGeometry(.25,.32,.42,20),bm);
 c.position.y=.23;g.add(c);
 const rim=new THREE.Mesh(new THREE.TorusGeometry(.28,.035,8,20),mat(0x885629));
 rim.rotation.x=Math.PI/2;rim.position.y=.45;g.add(rim);
 for(let i=0;i<4;i++){
  ball(.07,.05,.13,orange,-.12+(i%2)*.24,.48, -.08+Math.floor(i/2)*.13,g);
 }
 scene.add(g);return g;
}

const questions=[
 {q:"1. Số đối của −8 là số nào?",a:["A. −8","B. 0","C. 8","D. 16"],c:2},
 {q:"2. Công thức khối lượng riêng?",a:["A. D = m/V","B. D = V/m","C. D = mV","D. D = m+V"],c:0},
 {q:"3. Đòn bẩy có thể giúp gì?",a:["A. Tạo năng lượng","B. Đổi hướng lực","C. Xóa trọng lực","D. Tạo vật chất"],c:1},
 {q:"4. Nước tinh khiết sôi ở áp suất thường?",a:["A. 0°C","B. 50°C","C. 100°C","D. 200°C"],c:2},
 {q:"5. Khí chiếm phần lớn không khí?",a:["A. Oxygen","B. Nitrogen","C. Hydrogen","D. Helium"],c:1}
];

let stage=0, row=0, weakHits=0, lane=1, locked=true, jumping=false;
let tiles=[],walls=[],returnRow=0,returnLane=1,returnProgress=0;
let jumpT=0, jumpStart=null, jumpEnd=null, moving=false, sinkY=0;

function clearCourse(){
 for(const t of tiles){scene.remove(t.base);scene.remove(t.top);}
 for(const w of walls)scene.remove(w.mesh);
 tiles=[];walls=[];
}
function buildQuestionRow(index){
 const z=-index*7-2;
 for(let i=0;i<4;i++){
  const x=(i-1.5)*2.0;
  const base=cube(1.7,.42,1.8,ice,x,-.05,z);
  const top=cube(1.65,.10,1.75,topIce,x,.21,z);
  tiles.push({base,top,x,z,lane:i,weak:false,used:false});
 }
 const mesh=cube(8,3,.16,wallMat,0,1.5,z-1.4);
 walls.push({mesh,down:false,index});
}
function buildReturnCourse(){
 clearCourse();
 for(let r=0;r<5;r++){
  const z=-r*5.5-2;
  const weak=Math.floor(Math.random()*4);
  for(let i=0;i<4;i++){
   const x=(i-1.5)*2.0;
   const base=cube(1.65,.35,1.65,ice,x,-.05,z);
   const top=cube(1.60,.09,1.60,topIce,x,.17,z);
   tiles.push({base,top,x,z,lane:i,weak:i===weak,used:false,row:r});
  }
  const mesh=cube(8,3,.16,wallMat,0,1.5,z-1.4);
  walls.push({mesh,down:false,index:r});
 }
}
function updateHud(){
 document.getElementById('stageTag').textContent=stage===1?'🐟 Chặng 1: Đi lấy cá':'🪣 Chặng 2: Đưa cá về';
 document.getElementById('progress').textContent=stage===1?`Câu ${Math.min(row+1,5)}/5`:`Hàng ${Math.min(returnRow+1,5)}/5`;
 document.getElementById('danger').textContent=`⚠️ Băng yếu: ${weakHits}/3`;
}
function setAnswers(){
 const q=questions[row];
 document.getElementById('question').textContent=q.q;
 const ans=document.getElementById('answers');ans.innerHTML='';
 q.a.forEach((txt,i)=>{
  const b=document.createElement('button');
  b.className='answer';b.textContent=txt;
  b.onclick=()=>chooseAnswer(i);
  ans.appendChild(b);
 });
 updateHud();
}
function notice(title,text,button,action){
 document.getElementById('noticeTitle').textContent=title;
 document.getElementById('noticeText').textContent=text;
 document.getElementById('noticeButton').textContent=button;
 document.getElementById('notice').style.display='block';
 document.getElementById('noticeButton').onclick=action;
}
function buttonAction(){startGame();}
function startGame(){
 document.getElementById('notice').style.display='none';
 stage=1;row=0;weakHits=0;lane=1;returnRow=0;returnLane=1;
 mother.position.set(0,0,4);
 if(bucket)scene.remove(bucket);bucket=null;
 clearCourse();
 for(let r=0;r<5;r++)buildQuestionRow(r);
 locked=false;setAnswers();
}
function chooseAnswer(i){
 if(stage!==1||locked)return;
 locked=true;
 const q=questions[row];
 if(i!==q.c){
  document.getElementById('question').textContent='Chưa đúng rồi! Hãy chọn lại nhé.';
  locked=false;return;
 }
 const target=tiles.filter(t=>t.lane===i&&Math.abs(t.z-(-row*7-2))<.2)[0];
 if(target){
  jumpStart=mother.position.clone();
  jumpEnd=new THREE.Vector3(target.x,0,target.z);
  jumpT=0;jumping=true;moving=true;
 }
 const wall=walls.find(w=>w.index===row);
 if(wall)wall.down=true;
 document.getElementById('answers').innerHTML='';
 document.getElementById('question').textContent='Đúng rồi! Chim mẹ nhảy qua vách băng!';
 setTimeout(()=>{
  row++;
  if(row>=5){
   stage=2;buildReturnCourse();
   mother.position.set(0,0,4);
   bucket=makeBucket();
   bucket.position.set(-.7,.05,3.1);
   document.getElementById('question').textContent='Đã lấy được cá! Chọn đường về cẩn thận.';
   document.getElementById('answers').innerHTML='';
   returnRow=0;returnLane=1;locked=false;updateHud();
  }else{
   mother.position.set(0,0,-row*7+4);
   locked=false;setAnswers();
  }
 },1000);
}
function move(dx,dz){
 if(stage!==2||locked||moving)return;
 if(dx!==0)returnLane=Math.max(0,Math.min(3,returnLane+dx));
 if(dz<0){
  const t=tiles.find(t=>t.row===returnRow&&t.lane===returnLane);
  if(!t)return;
  jumpStart=mother.position.clone();
  jumpEnd=new THREE.Vector3(t.x,0,t.z);
  jumpT=0;jumping=true;moving=true;
  t.used=true;
  if(t.weak){
   weakHits++;t.base.userData.sink=true;t.top.userData.sink=true;
  }
  returnRow++;
  updateHud();
  setTimeout(()=>{
   if(weakHits>=3){gameOver();}
   else if(returnRow>=5){win();}
  },900);
 }else if(dz>0){
  mother.position.z+=.5;
 }
}
function jump(){
 if(stage===2)move(0,-1);
}
function gameOver(){
 locked=true;
 notice('💦 Băng bị vỡ!','Chim mẹ rơi xuống sông. Hãy bắt đầu lại từ bờ có thùng cá.','CHƠI LẠI 🔄',startGame);
 mother.position.y=-1.5;
}
function win(){
 locked=true;
 notice('🎉 VỀ NHÀ AN TOÀN!','Chim mẹ đã đưa cá về bờ thành công!','CHƠI LẠI 🔄',startGame);
}
function key(e){
 if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight',' '].includes(e.key))e.preventDefault();
 if(e.key==='ArrowLeft'||e.key==='a')move(-1,0);
 if(e.key==='ArrowRight'||e.key==='d')move(1,0);
 if(e.key==='ArrowUp'||e.key==='w')move(0,-1);
 if(e.key==='ArrowDown'||e.key==='s')move(0,1);
 if(e.key===' ')jump();
}
window.addEventListener('keydown',key);
window.move=move;window.jump=jump;window.startGame=startGame;

function animate(){
 requestAnimationFrame(animate);
 if(moving&&jumpStart&&jumpEnd){
  jumpT+=.035;
  const t=Math.min(jumpT,1);
  mother.position.lerpVectors(jumpStart,jumpEnd,t);
  mother.position.y=Math.sin(t*Math.PI)*1.25;
  if(t>=1){
   mother.position.y=0;moving=false;jumping=false;
   jumpStart=null;jumpEnd=null;
  }
 }
 for(const w of walls){
  if(w.down&&w.mesh.position.y>-2.5)w.mesh.position.y-=.055;
 }
 for(const t of tiles){
  if(t.base.userData.sink){
   t.base.position.y-=.035;t.top.position.y-=.035;
  }
 }
 if(bucket&&stage===2){
  bucket.position.x=mother.position.x-.65;
  bucket.position.z=mother.position.z+.1;
 }
 // Camera luôn theo sau lưng chim mẹ.
 const desired=new THREE.Vector3(mother.position.x,4.6,mother.position.z+8.5);
 camera.position.lerp(desired,.09);
 camera.lookAt(mother.position.x,.9,mother.position.z-5);
 renderer.render(scene,camera);
}
window.addEventListener('resize',()=>{
 camera.aspect=root.clientWidth/root.clientHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(root.clientWidth,root.clientHeight);
});
notice('🐧 Bắt đầu cuộc phiêu lưu!','Chim con sẽ đứng chờ ở bờ. Chim mẹ vượt qua 5 câu hỏi để lấy cá.','BẮT ĐẦU ▶',startGame);
animate();
</script>
</body>
</html>
"""

components.html(game, height=680, scrolling=False)
