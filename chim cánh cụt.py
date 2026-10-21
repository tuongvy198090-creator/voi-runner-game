
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Chim Cánh Cụt Vượt Sông Băng",
    page_icon="🐧",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #dff5ff;
}
.block-container {
    max-width: 1200px;
    padding-top: 1rem;
}
h1 {
    text-align: center;
    color: #155574;
}
</style>
""", unsafe_allow_html=True)

st.title("🐧 Gia đình chim cánh cụt vượt sông băng")
st.markdown(
    "<p style='text-align:center'>"
    "Góc nhìn 3D từ sau lưng · Trả lời câu hỏi · Lấy cá về cho gia đình"
    "</p>",
    unsafe_allow_html=True
)

game = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}
body{margin:0;font-family:Arial;background:#b9e8fa;color:#123b52}
#hud{
 position:absolute;z-index:5;top:10px;left:10px;right:10px;
 display:flex;gap:8px;align-items:flex-start;justify-content:space-between;
 pointer-events:none
}
.card{
 background:#ffffffed;border-radius:13px;padding:10px 13px;
 box-shadow:0 3px 12px #174d6722;max-width:75%
}
#question{font-size:16px;font-weight:bold;line-height:1.4}
#info{font-size:12px;margin-top:5px}
#message{font-size:13px;font-weight:bold;margin-top:5px}
#help{font-size:11px;line-height:1.4}
#game{width:100%;height:76vh;min-height:480px;position:relative;overflow:hidden}
canvas{display:block;width:100%;height:100%}
#start{
 position:absolute;inset:0;z-index:10;background:#d9f3ffed;
 display:flex;align-items:center;justify-content:center;text-align:center;padding:20px
}
#startbox{max-width:450px;background:white;border-radius:22px;padding:25px;box-shadow:0 8px 30px #326b8333}
#startbox .penguins{font-size:55px}
button{
 border:0;border-radius:12px;background:#087fa7;color:white;
 font-weight:bold;padding:12px 16px;cursor:pointer;margin-top:8px
}
button:hover{background:#086888}
#actions{position:absolute;z-index:6;bottom:12px;left:0;right:0;text-align:center;pointer-events:none}
#actions button{pointer-events:auto;margin:3px}
#crosshair{
 position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
 color:white;font-size:22px;text-shadow:0 1px 5px #123b52;pointer-events:none
}
#hint{position:absolute;bottom:67px;left:10px;right:10px;text-align:center;
 font-size:12px;color:white;text-shadow:0 1px 4px #16445a;pointer-events:none}
@media(max-width:600px){
 #game{height:75vh;min-height:460px}
 #question{font-size:14px}
 .card{padding:8px}
 #help{font-size:10px}
}
</style>
</head>
<body>
<div id="game">
 <div id="hud">
  <div class="card">
   <div id="phase"><b>🐧 HÀNH TRÌNH BẮC CỰC</b></div>
   <div id="question">Chuẩn bị vượt sông băng!</div>
   <div id="info">Câu 1/9</div>
   <div id="message">Hãy bắt đầu cuộc phiêu lưu!</div>
  </div>
  <div class="card" id="help">
   <b>ĐIỀU KHIỂN</b><br>
   Kéo màn hình để xoay camera.<br>
   Bấm tảng băng để nhảy tới.<br>
   Chọn đáp án nổi trên băng.
  </div>
 </div>
 <div id="crosshair">+</div>
 <div id="hint">Câu hỏi và đáp án đang lơ lửng trên bầu trời</div>
 <div id="actions">
  <button onclick="resetGame()">🔄 Chơi lại</button>
  <button onclick="toggleCamera()">🎥 Đổi góc nhìn</button>
 </div>
 <div id="start">
  <div id="startbox">
   <div class="penguins">🐧 🐧 🐧 🐧 🐧</div>
   <h2>Gia đình chim cánh cụt</h2>
   <p>Vượt qua 9 hàng băng, trả lời câu hỏi, lấy thùng cá rồi trở về với mẹ và 4 chim con.</p>
   <p>Hãy cẩn thận! Mỗi hàng có một tảng băng yếu.</p>
   <button onclick="startGame()">❄️ BẮT ĐẦU</button>
  </div>
 </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
if (!window.THREE) {
 document.getElementById("question").textContent =
 "Không tải được thư viện 3D. Hãy kiểm tra kết nối mạng rồi tải lại trang.";
 throw new Error("Three.js failed to load");
}

const questions = [
 {q:"Toán: 3/4 + 1/4 bằng bao nhiêu?",a:["1","1/2","2"],c:0},
 {q:"Địa lí: Bắc Cực nằm quanh vùng biển nào?",a:["Địa Trung Hải","Bắc Băng Dương","Biển Đỏ"],c:1},
 {q:"Tiếng Anh: 'Penguin' nghĩa là gì?",a:["Chim cánh cụt","Cá heo","Đại bàng"],c:0},
 {q:"Khoa học: Nước đóng băng ở khoảng bao nhiêu độ C?",a:["100°C","50°C","0°C"],c:2},
 {q:"Ngữ văn: Từ nào là từ láy?",a:["Long lanh","Học sinh","Bàn ghế"],c:0},
 {q:"Toán: 7 × 8 bằng bao nhiêu?",a:["54","56","64"],c:1},
 {q:"Sinh học: Con nào là động vật có vú?",a:["Cá mập","Ếch","Cá voi"],c:2},
 {q:"Băng tan thành gì?",a:["Nước","Cát","Khói"],c:0},
 {q:"Tiếng Anh: 'Fish' nghĩa là gì?",a:["Chim","Cá","Băng"],c:1}
];

let scene,camera,renderer,clock;
let penguin, motherGroup, familyGroup, fishBox;
let platforms=[], floatingLabels=[], questionSprite;
let phase="start", row=0, returning=false, finished=false;
let weak=[], weakHits=[], rowOptions=[], order=[];
let busy=false, cameraAlt=false, drag=null;
let lastTime=0;
const platformW=2.0, platformD=1.7, rowGap=3.0;
const startZ=5.5;
const mats={};

function mat(color,roughness=0.8){
 return new THREE.MeshStandardMaterial({color,roughness});
}

function box(parent,w,h,d,material,x,y,z){
 const mesh=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material);
 mesh.position.set(x,y,z);
 parent.add(mesh);
 return mesh;
}

function sphere(parent,rx,ry,rz,material,x,y,z){
 const mesh=new THREE.Mesh(new THREE.SphereGeometry(1,20,16),material);
 mesh.scale.set(rx,ry,rz);
 mesh.position.set(x,y,z);
 parent.add(mesh);
 return mesh;
}

function makeTextSprite(text,opts={}){
 const canvas=document.createElement("canvas");
 const ctx=canvas.getContext("2d");
 canvas.width=opts.width||512;
 canvas.height=opts.height||128;
 ctx.fillStyle=opts.bg||"rgba(255,255,255,0.95)";
 ctx.strokeStyle=opts.border||"#72c7e4";
 ctx.lineWidth=7;
 ctx.beginPath();
 ctx.roundRect(5,5,canvas.width-10,canvas.height-10,18);
 ctx.fill();ctx.stroke();
 ctx.fillStyle=opts.color||"#16445b";
 ctx.font="bold "+(opts.font||30)+"px Arial";
 ctx.textAlign="center";ctx.textBaseline="middle";
 const max=opts.maxChars||26;
 const words=text.split(" ");
 let lines=[],line="";
 for(const word of words){
  const test=line?line+" "+word:word;
  if(test.length>max&&line){lines.push(line);line=word}
  else line=test;
 }
 if(line)lines.push(line);
 const lineHeight=(opts.font||30)+7;
 const startY=canvas.height/2-(lines.length-1)*lineHeight/2;
 lines.slice(0,3).forEach((s,i)=>ctx.fillText(s,canvas.width/2,startY+i*lineHeight));
 const texture=new THREE.CanvasTexture(canvas);
 const sprite=new THREE.Sprite(new THREE.SpriteMaterial({map:texture,transparent:true,depthTest:false}));
 sprite.scale.set(opts.sw||3.2,opts.sh||0.8,1);
 return sprite;
}

function makePenguin(parent,x,y,z,scale=1){
 const g=new THREE.Group();
 g.position.set(x,y,z);g.scale.setScalar(scale);parent.add(g);
 const black=mat("#172c3b"),white=mat("#f7fbff"),orange=mat("#ff9d36"),eye=mat("#101820");
 sphere(g,.43,.64,.34,black,0,.67,0);
 sphere(g,.31,.45,.075,white,0,.61,.29);
 sphere(g,.32,.32,.3,black,0,1.25,0);
 sphere(g,.045,.045,.035,eye,-.12,1.31,.28);
 sphere(g,.045,.045,.035,eye,.12,1.31,.28);
 const beak= new THREE.Mesh(new THREE.ConeGeometry(.10,.23,8),orange);
 beak.rotation.x=Math.PI/2;beak.position.set(0,1.22,.35);g.add(beak);
 sphere(g,.16,.10,.23,black,-.43,.65,0);
 sphere(g,.16,.10,.23,black,.43,.65,0);
 sphere(g,.17,.075,.25,orange,-.2,.12,.12);
 sphere(g,.17,.075,.25,orange,.2,.12,.12);
 return g;
}

function makeWorld(){
 scene=new THREE.Scene();
 scene.background=new THREE.Color("#a9e6fa");
 scene.fog=new THREE.Fog("#a9e6fa",28,85);
 camera=new THREE.PerspectiveCamera(65,1,.1,150);
 camera.position.set(0,4.5,12);
 renderer=new THREE.WebGLRenderer({antialias:true});
 renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
 renderer.shadowMap.enabled=true;
 renderer.shadowMap.type=THREE.PCFSoftShadowMap;
 renderer.outputColorSpace=THREE.SRGBColorSpace;
 const old=document.querySelector("#game canvas");
 if(old)old.remove();
 document.getElementById("game").appendChild(renderer.domElement);
 clock=new THREE.Clock();

 scene.add(new THREE.HemisphereLight("#eafaff","#5e91a7",2.1));
 const sun=new THREE.DirectionalLight("#ffffff",2.4);
 sun.position.set(-8,15,9);sun.castShadow=true;scene.add(sun);

 const waterMat=new THREE.MeshStandardMaterial({
  color:"#32b9e3",roughness:.24,metalness:.05
 });
 box(scene,28,.3,42,waterMat,0,-.55,-9);

 // Hai bờ băng lớn.
 const bankMat=mat("#e9fbff");
 box(scene,11,1.3,7,bankMat,0,-.1,8.4);
 box(scene,11,1.3,7,bankMat,0,-.1,-23.5);

 // Núi băng xa xa.
 const mountainMat=mat("#d5f3ff");
 for(let i=0;i<10;i++){
  const m=new THREE.Mesh(
   new THREE.ConeGeometry(2+Math.random()*2,4+Math.random()*5,5),
   mountainMat
  );
  m.position.set(-22+i*4,1,-29-Math.random()*3);
  scene.add(m);
 }

 // Tuyết lấp lánh.
 const snowGeo=new THREE.BufferGeometry();
 const snowPos=[];
 for(let i=0;i<500;i++){
  snowPos.push((Math.random()-.5)*60,Math.random()*20-2,(Math.random()-.5)*65);
 }
 snowGeo.setAttribute("position",new THREE.Float32BufferAttribute(snowPos,3));
 const snow=new THREE.Points(snowGeo,new THREE.PointsMaterial({color:"#ffffff",size:.10}));
 scene.add(snow);

 familyGroup=new THREE.Group();
 scene.add(familyGroup);
 makePenguin(familyGroup,-1.25,.65,9.3,1.12);
 makePenguin(familyGroup,-.05,.65,9.7,.68);
 makePenguin(familyGroup,.85,.65,9.5,.68);
 makePenguin(familyGroup,-.5,.65,10.3,.68);
 makePenguin(familyGroup,.55,.65,10.4,.68);

 // Thùng cá ở bờ đối diện.
 fishBox=new THREE.Group();scene.add(fishBox);
 const wood=mat("#a96d3a"),darkWood=mat("#704522"),fish=mat("#ffb14e");
 box(fishBox,1.8,1.1,1.3,wood,0,.6,-25);
 for(let i=-1;i<=1;i++){
  box(fishBox,.07,1.15,1.35,darkWood,i*.55,.6,-25);
 }
 for(let i=0;i<4;i++){
  sphere(fishBox,.18,.10,.38,fish,-.45+i*.3,1.3,-25);
 }

 // Tảng băng ở 9 hàng, ba cột.
 const iceMat=mat("#b9efff",.3);
 const edgeMat=mat("#effcff",.25);
 for(let r=0;r<9;r++){
  platforms[r]=[];
  for(let c=0;c<3;c++){
   const g=new THREE.Group();
   g.position.set((c-1)*3,0,-r*rowGap);
   scene.add(g);
   const base=box(g,platformW,.48,platformD,iceMat,0,-.35,0);
   base.userData={r,c};
   const top=box(g,platformW-.13,.12,platformD-.13,edgeMat,0,-.08,0);
   top.userData={r,c};
   const crack=new THREE.Group();
   const crackMat=mat("#3a90b2");
   for(let k=0;k<3;k++){
    const line=box(crack,.025,.018,.55,crackMat,(k-1)*.18,0,0);
    line.rotation.y=(k-1)*.55;
   }
   crack.position.set(0,.0,.1);
   crack.visible=false;
   g.add(crack);

   const label=makeTextSprite("",{sw:1.8,sh:.6,font:26,maxChars:20});
   label.position.set(0,1.9,0);
   g.add(label);

   const badge=makeTextSprite("A",{sw:.75,sh:.48,font:25,maxChars:8});
   badge.position.set(0,1.25,0);
   g.add(badge);

   platforms[r][c]={g,base,top,crack,label,badge,r,c};
  }
 }

 penguin=makePenguin(scene,0,0,startZ,1.15);
 penguin.rotation.y=Math.PI;

 questionSprite=makeTextSprite("CÂU HỎI",{sw:7.5,sh:1.35,font:31,maxChars:42});
 questionSprite.position.set(0,5.6,0);
 scene.add(questionSprite);

 window.addEventListener("resize",resize);
 renderer.domElement.addEventListener("pointerdown",pointerDown);
 renderer.domElement.addEventListener("pointerup",pointerUp);
 renderer.domElement.addEventListener("pointermove",pointerMove);
 resize();
 animate();
}

function resize(){
 if(!renderer||!camera)return;
 const el=document.getElementById("game");
 const w=el.clientWidth,h=el.clientHeight;
 renderer.setSize(w,h,false);
 camera.aspect=w/h;camera.updateProjectionMatrix();
}

function startGame(){
 document.getElementById("start").style.display="none";
 resetGame();
}

function resetGame(){
 order=[0,1,2,3,4,5,6,7,8].sort(()=>Math.random()-.5);
 weak=[];weakHits=[];rowOptions=[];
 for(let r=0;r<9;r++){
  weak[r]=Math.floor(Math.random()*3);
  weakHits[r]=0;
  let opts=[0,1,2].sort(()=>Math.random()-.5);
  rowOptions[r]=opts;
 }
 row=0;phase="out";returning=false;finished=false;busy=false;
 penguin.position.set(0,0,startZ);
 penguin.rotation.y=Math.PI;
 fishBox.visible=true;
 questionSprite.visible=true;
 familyGroup.visible=true;
 for(let r=0;r<9;r++){
  for(let c=0;c<3;c++){
   const p=platforms[r][c];
   p.g.visible=true;p.g.position.y=0;
   p.crack.visible=false;
  }
 }
 updateGame();
}

function updateGame(){
 const q=questions[order[Math.min(row,8)]];
 if(phase==="out"){
  document.getElementById("phase").textContent="🐧 LƯỢT ĐI";
  document.getElementById("question").textContent=q.q;
  document.getElementById("info").textContent="Câu "+Math.min(row+1,9)+"/9";
  document.getElementById("message").textContent=
   "Nhảy lên tảng băng mang đáp án đúng.";
  questionSprite.material.map.dispose();
  questionSprite.material.map=makeTextSprite(q.q,{sw:8,sh:1.35,font:26,maxChars:45}).material.map;
  questionSprite.material.needsUpdate=true;
 }else if(phase==="back"){
  document.getElementById("phase").textContent="🐟 LƯỢT VỀ";
  document.getElementById("question").textContent="Đã lấy cá! Hãy trở về với gia đình.";
  document.getElementById("info").textContent="Về qua hàng "+(row+1)+"/9";
  document.getElementById("message").textContent="Chọn một tảng băng chắc chắn để nhảy.";
  questionSprite.material.map=makeTextSprite("ĐƯA CÁ VỀ NHÀ",{sw:7,sh:1.2,font:30}).material.map;
  questionSprite.material.needsUpdate=true;
 }else if(phase==="win"){
  document.getElementById("phase").textContent="🏆 CHIẾN THẮNG";
  document.getElementById("question").textContent="Cả gia đình đã đoàn tụ!";
  document.getElementById("info").textContent="Hoàn thành 9 câu hỏi";
  document.getElementById("message").textContent="🐟 Em đã mang cá về an toàn!";
 }
 for(let r=0;r<9;r++){
  const qrow=questions[order[r]];
  for(let c=0;c<3;c++){
   const p=platforms[r][c];
   const isWeak=weak[r]===c;
   p.crack.visible=isWeak&&weakHits[r]>0&&weakHits[r]<3;
   if(isWeak&&weakHits[r]===1)p.g.position.y=-.18;
   else if(isWeak&&weakHits[r]===2)p.g.position.y=-.42;
   else if(isWeak&&weakHits[r]>=3)p.g.position.y=-1.4;
   else p.g.position.y=0;
   if(phase==="out"){
    const original=rowOptions[r][c];
    p.label.material.map=makeTextSprite(qrow.a[original],{sw:1.8,sh:.62,font:24,maxChars:14}).material.map;
    p.label.material.needsUpdate=true;
    p.badge.material.map=makeTextSprite(["A","B","C"][c],{sw:.65,sh:.42,font:24}).material.map;
    p.badge.material.needsUpdate=true;
    p.label.visible=true;p.badge.visible=true;
   }else{
    p.label.material.map=makeTextSprite("VỀ NHÀ",{sw:1.7,sh:.6,font:22}).material.map;
    p.label.material.needsUpdate=true;
    p.badge.visible=false;p.label.visible=true;
   }
  }
 }
}

function moveToPlatform(r,c,callback){
 if(busy)return;
 busy=true;
 const target=platforms[r][c].g.position.clone();
 const start=penguin.position.clone();
 const end=new THREE.Vector3(target.x,.02,target.z);
 penguin.rotation.y=Math.atan2(end.x-start.x,end.z-start.z);
 const duration=800;
 const t0=performance.now();
 function step(now){
  const t=Math.min(1,(now-t0)/duration);
  const smooth=t*t*(3-2*t);
  penguin.position.lerpVectors(start,end,smooth);
  penguin.position.y=Math.sin(t*Math.PI)*1.1;
  if(t<1)requestAnimationFrame(step);
  else{
   penguin.position.copy(end);
   busy=false;
   callback();
  }
 }
 requestAnimationFrame(step);
}

function choosePlatform(r,c){
 if(busy||finished)return;
 if(phase==="out"&&r!==row)return;
 if(phase==="back"&&r!==row)return;
 if(phase!=="out"&&phase!=="back")return;

 if(phase==="out"&&weak[r]===c&&weakHits[r]>=2){
  document.getElementById("message").textContent="Tảng băng này đã chìm! Hãy chọn tảng khác.";
  return;
 }
 moveToPlatform(r,c,()=>{
  const isWeak=weak[r]===c;
  if(isWeak){
   weakHits[r]++;
   if(weakHits[r]===1){
    document.getElementById("message").textContent="⚠️ Băng nứt và chìm một nửa!";
   }else if(weakHits[r]===2){
    document.getElementById("message").textContent="⚠️ Băng chìm sâu hơn!";
   }else{
    document.getElementById("message").textContent="💦 Băng chìm hẳn! Trở về bờ và thử lại.";
    setTimeout(()=>resetGame(),1300);
    return;
   }
  }
  if(phase==="out"){
   const correct=questions[order[r]].c;
   const selected=rowOptions[r][c];
   if(selected!==correct){
    document.getElementById("message").textContent="❄️ Sai đáp án! Thử tảng băng khác ở hàng này.";
    return;
   }
   row++;
   if(row>=9){
    phase="fish";
    penguin.position.set(0,0,-25);
    fishBox.visible=true;
    document.getElementById("phase").textContent="🐟 ĐÃ ĐẾN BỜ KHO CÁ";
    document.getElementById("question").textContent="Em đã trả lời xong 9 câu!";
    document.getElementById("info").textContent="Nhấn thùng cá để quay về";
    document.getElementById("message").textContent="Bấm vào thùng cá trên bờ.";
    questionSprite.material.map=makeTextSprite("ĐÃ TÌM THẤY THÙNG CÁ!",{sw:7,sh:1.2,font:28}).material.map;
    questionSprite.material.needsUpdate=true;
   }else updateGame();
  }else if(phase==="back"){
   row--;
   if(row<0){
    phase="win";finished=true;
    penguin.position.set(0,0,startZ);
    updateGame();
   }else updateGame();
  }
 });
}

function beginReturn(){
 phase="back";row=8;
 penguin.position.set(0,0,-25);
 fishBox.visible=false;
 updateGame();
}

function pointerDown(e){
 drag={x:e.clientX,y:e.clientY,moved:false};
}
function pointerMove(e){
 if(!drag)return;
 const dx=e.clientX-drag.x;
 const dy=e.clientY-drag.y;
 if(Math.abs(dx)+Math.abs(dy)>5)drag.moved=true;
 if(drag.moved){
  camera.rotation.y-=dx*.003;
  camera.rotation.x=Math.max(-.2,Math.min(.25,camera.rotation.x+dy*.001));
  drag.x=e.clientX;drag.y=e.clientY;
 }
}
function pointerUp(e){
 if(!drag)return;
 const wasDrag=drag.moved;
 drag=null;
 if(wasDrag)return;
 const rect=renderer.domElement.getBoundingClientRect();
 const mouse=new THREE.Vector2(
  ((e.clientX-rect.left)/rect.width)*2-1,
  -((e.clientY-rect.top)/rect.height)*2+1
 );
 const ray=new THREE.Raycaster();
 ray.setFromCamera(mouse,camera);
 const hits=ray.intersectObjects(scene.children,true);
 for(const h of hits){
  let o=h.object;
  while(o){
   if(o===fishBox&&phase==="fish"){beginReturn();return;}
   if(o.userData&&o.userData.r!==undefined){
    choosePlatform(o.userData.r,o.userData.c);return;
   }
   o=o.parent;
  }
 }
}

function toggleCamera(){
 cameraAlt=!cameraAlt;
}

function animate(){
 requestAnimationFrame(animate);
 if(!renderer)return;
 const t=clock.getElapsedTime();
 // Camera bám theo chim cánh cụt từ phía sau.
 if(penguin){
  const distance=cameraAlt?7.5:10;
  const desired=new THREE.Vector3(
   penguin.position.x,
   penguin.position.y+4.2,
   penguin.position.z+distance
  );
  camera.position.lerp(desired,.06);
  const look=new THREE.Vector3(penguin.position.x,2,penguin.position.z-5);
  camera.lookAt(look);
 }
 // Câu hỏi luôn lơ lửng phía trước.
 if(questionSprite){
  questionSprite.position.y=5.6+Math.sin(t*1.6)*.12;
 }
 // Băng nổi nhẹ trên mặt nước.
 for(let r=0;r<9;r++){
  for(let c=0;c<3;c++){
   const p=platforms[r][c];
   if(p.g.position.y>-.5&&p.g.position.y<0){
    p.g.position.y=-.18+Math.sin(t*2+r+c)*.035;
   }
  }
 }
 renderer.render(scene,camera);
}

makeWorld();
</script>
</body>
</html>
"""

components.html(game, height=900, scrolling=False)
st.caption(
    "Nếu cảnh 3D chưa hiện, hãy kiểm tra kết nối mạng vì trò chơi tải Three.js từ CDN."
)
