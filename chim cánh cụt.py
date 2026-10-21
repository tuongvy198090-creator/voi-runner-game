
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Chim Cánh Cụt Vượt Sông Băng",
    page_icon="🐧",
    layout="wide"
)

html = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box}
body{margin:0;font-family:Arial;background:#9ddfff}
#game{height:740px;width:100%;position:relative;overflow:hidden;border-radius:14px}
canvas{display:block}
#hud{position:absolute;top:8px;left:2%;width:96%;z-index:2;pointer-events:none}
#panel{background:#f1faffed;border:3px solid #83d2ff;border-radius:18px;
padding:10px;text-align:center;color:#164a78;box-shadow:0 4px 12px #123e5b55}
#progress{font-weight:bold;font-size:12px;color:#1384c8}
#question{font-weight:bold;font-size:clamp(15px,2.4vw,23px);margin:7px 0}
#answers{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}
.answer{border:2px solid white;background:#ffdc70;border-radius:12px;
padding:10px 3px;font-size:clamp(12px,1.8vw,18px);font-weight:bold;color:#64410b}
#message{margin:6px auto;background:#174d77eF;color:white;border-radius:12px;
padding:7px 12px;text-align:center;font-size:14px;font-weight:bold;width:fit-content}
#controls{position:absolute;bottom:12px;left:0;width:100%;z-index:3;
display:flex;justify-content:space-between;align-items:end;padding:0 12px}
.pad{display:grid;grid-template-columns:47px 47px 47px;grid-template-rows:47px 47px;gap:3px}
.ctrl{width:47px;height:47px;border:2px solid white;border-radius:50%;
background:#15558bdd;color:white;font-size:25px;touch-action:none}
#jump{height:76px;width:76px;border:3px solid white;border-radius:50%;
background:#ffb842;color:#593600;font-weight:bold;font-size:15px;touch-action:none}
.overlay{position:absolute;inset:0;z-index:5;background:#10435feF;color:white;
display:flex;flex-direction:column;align-items:center;justify-content:center;
text-align:center;padding:22px}
.overlay h1{font-size:clamp(25px,5vw,42px)}
.overlay p{font-size:16px;line-height:1.65;max-width:620px}
.bigbtn{background:#ffdf75;border:0;border-radius:14px;padding:14px 24px;
font-size:20px;font-weight:bold;color:#5b400a;cursor:pointer}
#end{display:none}
@media(max-width:520px){
#game{height:720px}
#panel{padding:7px}
.answer{padding:9px 1px;font-size:12px}
#question{font-size:15px}
}
</style>
</head>
<body>
<div id="game">
<div id="hud">
 <div id="panel">
  <div id="progress">🐧 CUỘC PHIÊU LƯU CỦA HAI MẸ CON</div>
  <div id="question">Vượt sông băng để lấy xô cá!</div>
  <div id="answers"></div>
 </div>
 <div id="message">Bấm BẮT ĐẦU để chơi</div>
</div>
<div id="controls">
 <div class="pad">
  <div></div><button class="ctrl" data-key="up">▲</button><div></div>
  <button class="ctrl" data-key="left">◀</button>
  <button class="ctrl" data-key="down">▼</button>
  <button class="ctrl" data-key="right">▶</button>
 </div>
 <button id="jump">NHẢY ⬆</button>
</div>
<div id="start" class="overlay">
 <h1>🐧 CHIM CÁNH CỤT VƯỢT SÔNG BĂNG</h1>
 <p>Giúp chim mẹ và chim con vượt 5 bức tường bằng cách trả lời câu hỏi.<br>
Đến bờ bên kia, lấy xô cá rồi nhảy qua các tảng băng yếu để trở về.<br>
Laptop: dùng WASD hoặc phím mũi tên, nhấn Space để nhảy.<br>
Điện thoại: dùng các nút điều khiển ở phía dưới.</p>
 <button class="bigbtn" id="startBtn">BẮT ĐẦU CHƠI</button>
</div>
<div id="end" class="overlay">
 <h1 id="endTitle">🐟 HOÀN THÀNH!</h1>
 <p id="endText"></p>
 <button class="bigbtn" id="againBtn">CHƠI LẠI</button>
</div>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
(()=>{
const root=document.getElementById("game");
const questionEl=document.getElementById("question");
const progressEl=document.getElementById("progress");
const answersEl=document.getElementById("answers");
const messageEl=document.getElementById("message");
const startEl=document.getElementById("start");
const endEl=document.getElementById("end");

if(!window.THREE){
 questionEl.textContent="Không tải được thư viện 3D. Hãy kiểm tra Internet rồi tải lại.";
 return;
}

const questions=[
 {subject:"TOÁN ĐẠI SỐ",q:"Câu 1. Thu gọn 3x²y · 2xy², ta được:",a:["5x³y³","6x²y²","6x³y³","6x³y²"],c:2},
 {subject:"HÓA HỌC",q:"Câu 2. Hòa tan 10 g muối vào 90 g nước. Nồng độ phần trăm là:",a:["5%","10%","15%","20%"],c:1},
 {subject:"VẬT LÝ",q:"Câu 3. Công thức tính khối lượng riêng là:",a:["D = mV","D = V/m","D = m/V","D = m + V"],c:2},
 {subject:"SINH HỌC",q:"Câu 4. Bộ phận nào thuộc hệ vận động của người?",a:["Tim","Phổi","Xương","Dạ dày"],c:2},
 {subject:"ĐỊA LÝ",q:"Câu 5. Việt Nam nằm ở khu vực nào của châu Á?",a:["Đông Á","Tây Á","Đông Nam Á","Nam Á"],c:2}
];

const scene=new THREE.Scene();
scene.background=new THREE.Color(0x9edfff);
scene.fog=new THREE.Fog(0x9edfff,42,125);

const camera=new THREE.PerspectiveCamera(63,1,.1,300);
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
renderer.shadowMap.enabled=true;
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.domElement.style.cssText="position:absolute;inset:0;width:100%;height:100%";
root.insertBefore(renderer.domElement,root.firstChild);

scene.add(new THREE.HemisphereLight(0xe9f8ff,0x426b87,2.0));
const sun=new THREE.DirectionalLight(0xffffff,2.4);
sun.position.set(-10,20,12);sun.castShadow=true;scene.add(sun);

function material(color,roughness=.65,transparent=false,opacity=1){
 return new THREE.MeshStandardMaterial({color,roughness,transparent,opacity});
}
const snow=material(0xf2fbff);
const ice=material(0x69d6ff,.23);
const darkIce=material(0x1688c6,.2);
const water=material(0x0879bd,.25);
const wood=material(0x855637);
const penguinBlack=material(0x263448);
const white=material(0xffffff);
const orange=material(0xffa12b);
const scarfBlue=material(0x53b9ff);
const barrierMat=material(0x48b9f2,.2,true,.63);

function box(parent,w,h,d,mat,x,y,z){
 const mesh=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);
 mesh.position.set(x,y,z);
 mesh.castShadow=true;mesh.receiveShadow=true;
 parent.add(mesh);return mesh;
}
function sphere(parent,x,y,z,sx,sy,sz,mat){
 const mesh=new THREE.Mesh(new THREE.SphereGeometry(1,18,14),mat);
 mesh.position.set(x,y,z);mesh.scale.set(sx,sy,sz);
 mesh.castShadow=true;parent.add(mesh);return mesh;
}
function cone(parent,x,y,z,r,h,mat){
 const mesh=new THREE.Mesh(new THREE.ConeGeometry(r,h,7),mat);
 mesh.position.set(x,y,z);mesh.castShadow=true;parent.add(mesh);return mesh;
}

// Sông xanh với lớp băng mỏng, bờ tuyết và cảnh vật cố định.
box(scene,12,.4,175,water,0,-.55,-70);
box(scene,12,.06,175,material(0x65d8ff,.2,true,.35),0,-.32,-70);
box(scene,19,.55,14,snow,0,-.05,9);
box(scene,19,.55,14,snow,0,-.05,-145);

for(const side of [-1,1]){
 box(scene,4,2.2,175,material(0x91c5e7),side*8,-.2,-70);
 box(scene,4,.5,175,snow,side*8,.95,-70);
 for(let z=14;z>-158;z-=10){
  const x=side*(7.1+Math.random()*1.1);
  box(scene,.45,2,.45,wood,x,1.6,z);
  cone(scene,x,3,z,1.3,2.6,material(0x267f70));
  cone(scene,x,4.1,z,.95,2.2,material(0x3c9b81));
 }
}

// Tạo một chú chim cánh cụt dễ thương.
// Chim con đi cạnh chim mẹ; xô cá xuất hiện khi quay về.
function makePenguin(scale,withBucket){
 const g=new THREE.Group();
 sphere(g,0,1,0,.48,.66,.43,penguinBlack);
 sphere(g,0,1.02,-.32,.34,.45,.13,white);
 sphere(g,0,1.83,0,.4,.4,.37,penguinBlack);
 sphere(g,-.13,1.88,-.32,.16,.15,.08,white);
 sphere(g,.13,1.88,-.32,.16,.15,.08,white);
 sphere(g,-.13,1.88,-.395,.045,.06,.025,material(0x111820));
 sphere(g,.13,1.88,-.395,.045,.06,.025,material(0x111820));
 cone(g,0,1.72,-.43,.13,.19,orange).rotation.x=Math.PI/2;
 sphere(g,-.49,1.08,0,.15,.42,.19,penguinBlack);
 sphere(g,.49,1.08,0,.15,.42,.19,penguinBlack);
 box(g,.76,.15,.76,scarfBlue,0,1.43,0);
 box(g,.2,.48,.12,scarfBlue,.18,1.2,-.39);
 box(g,.25,.13,.36,orange,-.23,.15,-.08);
 box(g,.25,.13,.36,orange,.23,.15,-.08);
 if(withBucket){
  const b=box(g,.35,.3,.31,material(0xa7d9ed),-.62,.63,-.05);
  b.rotation.z=-.08;
  const rim=box(g,.39,.06,.35,material(0x7da8c0),-.62,.8,-.05);
  rim.rotation.z=-.08;
  for(let i=0;i<3;i++)sphere(g,-.7+i*.09,.82,-.08,.055,.07,.06,orange);
  const handle=new THREE.Mesh(
   new THREE.TorusGeometry(.19,.025,7,18,Math.PI),
   material(0x7897a9)
  );
  handle.position.set(-.62,.82,-.05);handle.rotation.z=Math.PI;
  g.add(handle);
 }
 g.scale.setScalar(scale);
 return g;
}

const mother=makePenguin(1.05,false);
const baby=makePenguin(.58,false);
scene.add(mother);scene.add(baby);

// Các tảng băng: bốn ô trên một hàng, mỗi ô thẳng hàng với đáp án.
const laneX=[-3.3,-1.1,1.1,3.3];
const rowZ=Array.from({length:5},(_,i)=>-5-i*12);
const questionTiles=[];
const questionWalls=[];
const returnTiles=[];
const returnWalls=[];

for(let r=0;r<5;r++){
 const tiles=[];
 for(let lane=0;lane<4;lane++){
  const group=new THREE.Group();
  scene.add(group);
  const top=box(group,1.75,.42,2.05,ice,laneX[lane],-.05,rowZ[r]);
  box(group,1.82,.12,2.12,material(0xc9f5ff),laneX[lane],.19,rowZ[r]);
  for(let k=0;k<3;k++){
   const shard=box(group,.12,.22,.12,darkIce,
     laneX[lane]-.55+k*.55,-.32,rowZ[r]+.1);
   shard.rotation.z=.4;
  }
  tiles.push({group,top,lane,row:r});
 }
 questionTiles.push(tiles);

 // Vách cao, trong mờ để vẫn nhìn thấy hàng phía sau.
 const wall=box(scene,10,.0+3.8,.5,barrierMat,0,1.9,rowZ[r]-2.3);
 box(scene,10,.12,.58,material(0xe2fbff),0,3.84,rowZ[r]-2.3);
 questionWalls.push({wall,open:false,progress:0,baseY:1.9});
}

// Xô cá và đích ở bờ đối diện.
const bucketGroup=new THREE.Group();
scene.add(bucketGroup);
const bucketBody=box(bucketGroup,.75,.65,.65,material(0x9bcce0),-.65,.45,-145);
bucketBody.rotation.z=-.08;
box(bucketGroup,.82,.1,.7,wood,-.65,.8,-145);
for(let i=0;i<5;i++){
 sphere(bucketGroup,-.9+(i%3)*.23,.88+(i%2)*.08,-145+(i%2)*.13,.09,.1,.1,orange);
}
bucketGroup.visible=false;

box(scene,10,.12,.4,material(0xffffff),0,.7,-147);
for(let z=-138;z>-160;z-=3){
 sphere(scene,-7,1,z,.6,.6,.6,snow);
 sphere(scene,7,1,z,.6,.6,.6,snow);
}

// Màn quay về: các hàng băng yếu và vách cao giữa các hàng.
for(let r=0;r<5;r++){
 const z=rowZ[r];
 const tiles=[];
 for(let lane=0;lane<4;lane++){
  const group=new THREE.Group();scene.add(group);
  const top=box(group,1.75,.42,2.05,ice,laneX[lane],-.05,z);
  box(group,1.82,.12,2.12,material(0xc9f5ff),laneX[lane],.19,z);
  tiles.push({group,top,lane,row:r,weak:false,used:false,collapsed:false});
 }
 returnTiles.push(tiles);
 const wall=box(scene,10,3.8,.5,barrierMat,0,1.9,z+3.0);
 box(scene,10,.12,.58,material(0xe2fbff),0,3.84,z+3.0);
 returnWalls.push({wall,open:false,progress:0,baseY:1.9});
}

// Tuyết rơi.
const snowGroup=new THREE.Group();scene.add(snowGroup);
const snowDots=[];
for(let i=0;i<140;i++){
 const dot=new THREE.Mesh(new THREE.SphereGeometry(.045,5,5),white);
 dot.position.set((Math.random()-.5)*26,Math.random()*12,Math.random()*-165+12);
 snowGroup.add(dot);snowDots.push(dot);
}

let phase="start",started=false,finished=false;
let px=0,pz=8,py=0,jumpV=0;
let qIndex=0,returnIndex=4,weakCount=0,score=0;
let hasBucket=false,attemptLocked=false;
let keys={},touch={};
let lastTime=0,lastJump=false;
let lastRowEvent=-1;

function setMessage(text,color){
 messageEl.textContent=text;
 messageEl.style.background=color||"#174d77eF";
}
function showQuestion(){
 const q=questions[qIndex];
 progressEl.textContent="BỨC TƯỜNG "+(qIndex+1)+"/5 · "+q.subject;
 questionEl.textContent=q.q;
 answersEl.innerHTML="";
 q.a.forEach((a,i)=>{
  const b=document.createElement("button");
  b.className="answer";
  b.textContent=String.fromCharCode(65+i)+". "+a;
  answersEl.appendChild(b);
 });
}
function showReturnUI(){
 progressEl.textContent="🐟 ĐÃ LẤY XÔ CÁ · CHẶNG QUAY VỀ";
 questionEl.textContent="Nhảy qua băng để đưa cá về bờ! Băng yếu: "+weakCount+"/3";
 answersEl.innerHTML="";
}
function openQuestionWall(i){
 const w=questionWalls[i];
 if(w.open)return;
 w.open=true;
 w.progress=0;
 score++;
}
function resetGame(){
 phase="question";started=true;finished=false;
 px=0;pz=8;py=0;jumpV=0;
 qIndex=0;returnIndex=4;weakCount=0;score=0;
 hasBucket=false;attemptLocked=false;lastRowEvent=-1;
 questionWalls.forEach(w=>{w.open=false;w.progress=0;w.wall.position.y=w.baseY;w.wall.scale.y=1;});
 returnWalls.forEach(w=>{w.open=false;w.progress=0;w.wall.position.y=w.baseY;w.wall.scale.y=1;});
 questionTiles.forEach(row=>row.forEach(t=>{
  t.group.visible=true;t.top.material=ice;t.top.position.y=-.05;
 }));
 returnTiles.forEach(row=>row.forEach(t=>{
  t.group.visible=true;t.top.material=ice;t.top.position.y=-.05;t.used=false;t.collapsed=false;
  t.weak=false;
 }));
 // Mỗi hàng quay về có đúng một băng yếu được chọn ngẫu nhiên.
 returnTiles.forEach(row=>{
  row[Math.floor(Math.random()*4)].weak=true;
 });
 mother.position.set(0,0,8);
 baby.position.set(1.15,0,8.7);
 mother.rotation.y=Math.PI;
 baby.rotation.y=Math.PI;
 bucketGroup.visible=false;
 mother.children.forEach(c=>{});
 startEl.style.display="none";endEl.style.display="none";
 answersEl.style.display="grid";
 showQuestion();
 setMessage("Di chuyển tới hàng băng, chọn làn đáp án rồi nhấn NHẢY.");
 keys={};touch={};
}
function endGame(won,title,text){
 finished=true;phase=won?"won":"lost";
 document.getElementById("endTitle").textContent=title;
 document.getElementById("endText").textContent=text;
 endEl.style.display="flex";
}
function beginReturn(){
 phase="return";
 hasBucket=true;
 bucketGroup.visible=true;
 mother=attachBucketToMother();
 returnIndex=4;
 px=0;pz=rowZ[4]-3;
 mother.position.set(px,py,pz);
 baby.position.set(px+1.05,py,pz+.65);
 // Đổi hướng quay về bờ xuất phát.
 mother.rotation.y=0;baby.rotation.y=0;
 showReturnUI();
 setMessage("Cầm xô cá! Nhảy qua từng hàng băng để về bờ.", "#177d69");
}
function attachBucketToMother(){
 const old=mother;
 const replacement=makePenguin(1.05,true);
 scene.add(replacement);
 replacement.position.copy(old.position);
 replacement.rotation.copy(old.rotation);
 scene.remove(old);
 return replacement;
}

function evaluateQuestion(lane){
 if(phase!=="question"||attemptLocked||qIndex>=5)return;
 const q=questions[qIndex];
 attemptLocked=true;
 if(lane===q.c){
  openQuestionWall(qIndex);
  setMessage("ĐÚNG RỒI! Vách băng đang chìm xuống! 🎉","#16845b");
  setTimeout(()=>{
   if(phase!=="question")return;
   qIndex++;
   attemptLocked=false;
   lastRowEvent=-1;
   if(qIndex>=5){
    phase="bucket";
    progressEl.textContent="ĐÃ VƯỢT QUA 5 BỨC TƯỜNG!";
    questionEl.textContent="Bờ bên kia có xô cá đang chờ em!";
    answersEl.innerHTML="";
    setMessage("Đi tới xô cá ở bờ bên kia để bắt đầu chặng quay về.","#177d69");
   }else{
    showQuestion();
    setMessage("Tiếp tục tới hàng tiếp theo!");
   }
  },1200);
 }else{
  setMessage("Chưa đúng! Hãy thử nhảy vào tảng băng khác nhé.","#b33d50");
  setTimeout(()=>{attemptLocked=false;},550);
 }
}
function triggerJump(){
 if(!started||finished)return;
 if(py<=.02){jumpV=7.4;}
}

function nearRow(z,row){
 return Math.abs(z-row)<1.25;
}

function checkQuestionRow(){
 if(phase!=="question"||qIndex>=5||py<.2||attemptLocked)return;
 const z=rowZ[qIndex];
 if(nearRow(pz,z)&&lastRowEvent!==qIndex){
  const lane=laneX.reduce((best,x,i)=>
   Math.abs(px-x)<Math.abs(px-laneX[best])?i:best,0);
  if(Math.abs(px-laneX[lane])<.95){
   lastRowEvent=qIndex;
   evaluateQuestion(lane);
  }
 }
}
function checkBucket(){
 if(phase!=="bucket")return;
 // Xô cá nằm ở bờ bên kia; tiến sát bờ là nhận xô.
 if(pz<-141){
  beginReturn();
 }
}
function checkReturnRow(){
 if(phase!=="return"||returnIndex<0||py<.2)return;
 const z=rowZ[returnIndex];
 if(!nearRow(pz,z)||lastRowEvent===returnIndex)return;
 const lane=laneX.reduce((best,x,i)=>
  Math.abs(px-x)<Math.abs(px-laneX[best])?i:best,0);
 if(Math.abs(px-laneX[lane])>.95)return;
 lastRowEvent=returnIndex;
 const tile=returnTiles[returnIndex][lane];
 tile.used=true;
 if(tile.weak){
  tile.collapsed=true;
  tile.top.material=material(0x135f94,.25);
  tile.top.position.y=-.85;
  tile.group.position.y=-.85;
  weakCount++;
  setMessage("Ối! Băng yếu chìm xuống! "+weakCount+"/3","#b33d50");
  questionEl.textContent="Băng yếu: "+weakCount+"/3";
  if(weakCount>=3){
   setTimeout(()=>{
    endGame(false,"💦 Ôi không!","Chim mẹ và chim con bị chìm xuống nước! Em hãy thử lại từ bờ có thùng cá nhé.");
   },500);
   return;
  }
 }else{
  setMessage("Giỏi quá! Tảng băng này chắc chắn! 🧊","#177d69");
 }
 returnWalls[returnIndex].open=true;
 returnWalls[returnIndex].progress=0;
 returnIndex--;
 lastRowEvent=-1;
 if(returnIndex<0){
  endGame(true,"🏆 VỀ ĐẾN BỜ RỒI!","Em đã mang xô cá về an toàn! Điểm câu hỏi: "+score+"/5. Hai mẹ con chim cánh cụt cảm ơn em!");
 }
}

function blockedByWall(oldZ,newZ){
 if(phase==="question"&&qIndex<5&&!questionWalls[qIndex].open){
  const wallZ=rowZ[qIndex]-2.3;
  if(oldZ>wallZ&&newZ<=wallZ)return wallZ+.18;
 }
 if(phase==="return"&&returnIndex>=0&&!returnWalls[returnIndex].open){
  const wallZ=rowZ[returnIndex]+3;
  if(oldZ<wallZ&&newZ>=wallZ)return wallZ-.18;
 }
 return newZ;
}

function resize(){
 const w=root.clientWidth,h=root.clientHeight;
 renderer.setSize(w,h,false);
 camera.aspect=w/h;camera.updateProjectionMatrix();
}
new ResizeObserver(resize).observe(root);resize();

window.addEventListener("keydown",e=>{
 const k=e.key.toLowerCase();
 keys[k]=true;
 if(e.code==="Space"){
  e.preventDefault();
  if(!lastJump)triggerJump();
  lastJump=true;
 }
});
window.addEventListener("keyup",e=>{
 keys[e.key.toLowerCase()]=false;
 if(e.code==="Space")lastJump=false;
});
window.addEventListener("blur",()=>{keys={};touch={};lastJump=false;});

document.querySelectorAll(".ctrl").forEach(b=>{
 const k=b.dataset.key;
 b.addEventListener("pointerdown",e=>{e.preventDefault();touch[k]=true;});
 ["pointerup","pointercancel","pointerleave"].forEach(ev=>
  b.addEventListener(ev,e=>{e.preventDefault();touch[k]=false;})
 );
});
document.getElementById("jump").addEventListener("pointerdown",e=>{
 e.preventDefault();if(!touch.jump)triggerJump();touch.jump=true;
});
["pointerup","pointercancel","pointerleave"].forEach(ev=>
 document.getElementById("jump").addEventListener(ev,e=>{
  e.preventDefault();touch.jump=false;
 })
);

function forward(){return keys.w||keys.arrowup||touch.up;}
function backward(){return keys.s||keys.arrowdown||touch.down;}
function left(){return keys.a||keys.arrowleft||touch.left;}
function right(){return keys.d||keys.arrowright||touch.right;}

function update(dt,time){
 if(!started||finished)return;
 const oldZ=pz;
 const move=5.5*dt;
 if(left())px-=move;
 if(right())px+=move;
 px=Math.max(-4.3,Math.min(4.3,px));

 let dz=0;
 if(phase==="question"||phase==="bucket"){
  if(forward())dz-=move;
  if(backward())dz+=move;
 }else if(phase==="return"){
  if(forward())dz+=move;
  if(backward())dz-=move;
 }
 const candidate=blockedByWall(oldZ,pz+dz);
 pz=candidate;

 jumpV-=17*dt;
 py+=jumpV*dt;
 if(py<0){py=0;jumpV=0;}

 // Tự động mở dần các vách đã được trả lời đúng.
 questionWalls.forEach(w=>{
  if(w.open&&w.progress<1){
   w.progress=Math.min(1,w.progress+dt*1.1);
   const t=w.progress;
   w.wall.position.y=w.baseY*(1-t)-.3*t;
   w.wall.scale.y=Math.max(.02,1-t);
  }
 });
 returnWalls.forEach(w=>{
  if(w.open&&w.progress<1){
   w.progress=Math.min(1,w.progress+dt*1.4);
   const t=w.progress;
   w.wall.position.y=w.baseY*(1-t)-.3*t;
   w.wall.scale.y=Math.max(.02,1-t);
  }
 });

 if(phase==="question")checkQuestionRow();
 if(phase==="bucket")checkBucket();
 if(phase==="return")checkReturnRow();

 mother.position.set(px,py,pz);
 baby.position.set(px+1.05,py,pz+.65);
 mother.rotation.y=phase==="return"?0:Math.PI;
 baby.rotation.y=mother.rotation.y;

 // Lắc nhẹ khi đi; hai mẹ con cùng nhảy.
 const walking=forward()||backward()||left()||right();
 mother.rotation.z=walking?Math.sin(time*.009)*.035:0;
 baby.rotation.z=walking?Math.sin(time*.009+1)*.04:0;

 // Camera bám theo phía sau chim mẹ.
 const target=new THREE.Vector3(px,py+4.2,pz+(phase==="return"?8.5:8.5));
 camera.position.lerp(target,Math.min(1,dt*4.5));
 camera.lookAt(px,py+1.0,pz+(phase==="return"?-3.5:-4.5));

 for(const dot of snowDots){
  dot.position.y-=dt*1.5;
  dot.position.x+=Math.sin(time*.001+dot.position.z)*dt*.15;
  if(dot.position.y<0){
   dot.position.y=10+Math.random()*3;
   dot.position.z=pz-25-Math.random()*90;
  }
 }

 if(phase==="question"){
  progressEl.textContent="BỨC TƯỜNG "+(qIndex+1)+"/5 · "+questions[qIndex].subject;
 }else if(phase==="bucket"){
  progressEl.textContent="ĐÃ VƯỢT QUA 5 BỨC TƯỜNG!";
  questionEl.textContent="Tiến đến bờ bên kia để lấy xô cá!";
 }else if(phase==="return"){
  progressEl.textContent="CHẶNG QUAY VỀ · HÀNG "+(5-returnIndex)+"/5";
  questionEl.textContent="Băng yếu: "+weakCount+"/3 · Chọn tảng băng và nhảy!";
 }
}

function animate(time){
 requestAnimationFrame(animate);
 const dt=Math.min((time-lastTime)/1000||0,.04);
 lastTime=time;
 update(dt,time);
 renderer.render(scene,camera);
}
requestAnimationFrame(animate);

document.getElementById("startBtn").onclick=resetGame;
document.getElementById("againBtn").onclick=()=>{
 resetGame();
};
})();
</script>
</body>
</html>
"""

components.html(html, height=750, scrolling=False)
