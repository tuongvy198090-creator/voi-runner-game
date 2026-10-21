
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Chim Cánh Cụt Vượt Tường 3D",
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
body{margin:0;font-family:Arial;background:#9ce4ff}
#game{height:680px;width:100%;position:relative;overflow:hidden}
canvas{display:block}
#hud{position:absolute;top:8px;left:2%;width:96%;z-index:2}
#question{background:white;color:#173d63;padding:12px;border-radius:15px;
font-weight:bold;font-size:clamp(16px,2.5vw,23px);text-align:center;
box-shadow:0 3px 10px #3456}
#answers{display:flex;justify-content:center;flex-wrap:wrap;gap:8px;margin-top:8px}
.answer{background:#ffe16b;border:3px solid white;border-radius:13px;
padding:12px 16px;font-size:clamp(17px,2.4vw,23px);font-weight:bold;
color:#423500;cursor:pointer;min-width:110px}
.answer:disabled{opacity:.8}
#message{background:#16466bde;color:white;padding:8px 12px;
border-radius:12px;margin:7px auto;text-align:center;font-weight:bold;
width:fit-content;max-width:98%;font-size:15px}
#mobile{position:absolute;bottom:12px;left:0;width:100%;
display:flex;justify-content:space-between;align-items:end;padding:0 14px}
.pad{display:grid;grid-template-columns:45px 45px 45px;
grid-template-rows:45px 45px 45px;gap:3px}
.ctrl{width:45px;height:45px;border:2px solid white;border-radius:50%;
background:#16466bdb;color:white;font-size:23px;touch-action:none}
#jump{height:73px;width:73px;border:3px solid white;border-radius:50%;
background:#ffbd45;font-weight:bold;font-size:16px;color:#493500;touch-action:none}
.overlay{position:absolute;inset:0;z-index:5;background:#103c59ed;color:white;
display:flex;flex-direction:column;align-items:center;justify-content:center;
text-align:center;padding:20px}
.overlay h1{font-size:clamp(26px,5vw,43px)}
.overlay p{font-size:18px;line-height:1.6}
.bigbtn{background:#ffe16b;border:0;border-radius:14px;padding:14px 25px;
font-size:21px;font-weight:bold;cursor:pointer;color:#423500}
#win{display:none;background:#063e37ed}
@media(max-width:500px){
#game{height:720px}
.answer{min-width:43%;padding:10px 5px}
#question{padding:9px}
}
</style>
</head>
<body>
<div id="game">
<div id="hud">
  <div id="question">🐧 Chào mừng đến với thử thách 14 bức tường!</div>
  <div id="answers"></div>
  <div id="message">Bấm BẮT ĐẦU CHƠI để bắt đầu cuộc phiêu lưu!</div>
</div>

<div id="mobile">
  <div class="pad">
    <div></div><button class="ctrl" data-key="up">▲</button><div></div>
    <button class="ctrl" data-key="left">◀</button>
    <button class="ctrl" data-key="down">▼</button>
    <button class="ctrl" data-key="right">▶</button>
    <div></div><div></div><div></div>
  </div>
  <button id="jump">NHẢY ⬆</button>
</div>

<div id="start" class="overlay">
  <h1>🐧 CHIM CÁNH CỤT VƯỢT TƯỜNG 3D</h1>
  <p>14 câu hỏi kiến thức lớp 8 đang chờ em!<br>
  Trả lời đúng để hạ từng bức tường.<br>
  Laptop: WASD hoặc phím mũi tên, Space để nhảy.<br>
  Điện thoại: dùng các nút điều khiển phía dưới.</p>
  <button id="startBtn" class="bigbtn">BẮT ĐẦU CHƠI</button>
</div>

<div id="win" class="overlay">
  <h1>🏆 EM ĐÃ CHIẾN THẮNG!</h1>
  <p id="result"></p>
  <button id="restartBtn" class="bigbtn">CHƠI LẠI</button>
</div>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
(function(){
const root=document.getElementById("game");
const qbox=document.getElementById("question");
const abox=document.getElementById("answers");
const msg=document.getElementById("message");
const startScreen=document.getElementById("start");
const winScreen=document.getElementById("win");

if(!window.THREE){
 qbox.textContent="Không tải được 3D. Em kiểm tra Internet rồi tải lại trang nhé!";
 return;
}

const questions=[
{cat:"Toán đại số",q:"Câu 1. Biểu thức nào là đơn thức?",a:["2x + 3","5x²y","x − y","x² + 1"],c:1},
{cat:"Toán đại số",q:"Câu 2. Thu gọn 3x²y · 2xy², ta được:",a:["5x³y³","6x²y²","6x³y³","6x³y²"],c:2},
{cat:"Toán hình học",q:"Câu 3. Tổng bốn góc trong của một tứ giác bằng:",a:["180°","270°","360°","90°"],c:2},
{cat:"Toán hình học",q:"Câu 4. Hình thang cân có tính chất nào?",a:["Hai cạnh bên song song","Hai góc kề một đáy bằng nhau","Bốn cạnh bằng nhau","Hai đường chéo luôn vuông góc"],c:1},
{cat:"Hóa học",q:"Câu 5. Dấu hiệu nào có thể cho thấy đã xảy ra phản ứng hóa học?",a:["Nước đá tan","Đường nghiền nhỏ","Xuất hiện khí khi trộn hai dung dịch","Nước bay hơi"],c:2},
{cat:"Hóa học",q:"Câu 6. Hòa tan 10 g muối vào 90 g nước. Nồng độ phần trăm là bao nhiêu?",a:["5%","10%","15%","20%"],c:1},
{cat:"Vật lý",q:"Câu 7. Công thức tính khối lượng riêng là:",a:["D = mV","D = V/m","D = m/V","D = m + V"],c:2},
{cat:"Vật lý",q:"Câu 8. Dụng cụ nào hoạt động dựa trên nguyên lý đòn bẩy?",a:["Cái kéo","Nhiệt kế","Bóng đèn","Đồng hồ điện tử"],c:0},
{cat:"Sinh học",q:"Câu 9. Bộ phận nào thuộc hệ vận động của người?",a:["Tim","Phổi","Xương","Dạ dày"],c:2},
{cat:"Sinh học",q:"Câu 10. Hệ cơ quan nào trao đổi khí giữa cơ thể và môi trường?",a:["Hệ tiêu hóa","Hệ hô hấp","Hệ tuần hoàn","Hệ bài tiết"],c:1},
{cat:"Địa lý",q:"Câu 11. Việt Nam nằm ở khu vực nào của châu Á?",a:["Đông Á","Tây Á","Đông Nam Á","Nam Á"],c:2},
{cat:"Địa lý",q:"Câu 12. Đặc điểm nổi bật của địa hình Việt Nam là:",a:["Chủ yếu là đồng bằng","Chủ yếu là đồi núi","Chủ yếu là hoang mạc","Hoàn toàn là núi cao"],c:1},
{cat:"Lịch sử",q:"Câu 13. Cách mạng tư sản Anh diễn ra vào thế kỉ nào?",a:["Thế kỉ XV","Thế kỉ XVI","Thế kỉ XVII","Thế kỉ XIX"],c:2},
{cat:"Lịch sử",q:"Câu 14. Tuyên ngôn Độc lập của 13 thuộc địa Anh ở Bắc Mỹ được công bố năm nào?",a:["1776","1789","1640","1812"],c:0}
];

const scene=new THREE.Scene();
scene.background=new THREE.Color(0x9ce4ff);
scene.fog=new THREE.Fog(0x9ce4ff,40,115);

const camera=new THREE.PerspectiveCamera(65,1,0.1,250);
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
renderer.shadowMap.enabled=true;
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.domElement.style.position="absolute";
renderer.domElement.style.inset="0";
renderer.domElement.style.width="100%";
renderer.domElement.style.height="100%";
root.insertBefore(renderer.domElement,root.firstChild);

scene.add(new THREE.HemisphereLight(0xffffff,0x567d91,2));
const sun=new THREE.DirectionalLight(0xffffff,2);
sun.position.set(-8,18,10);
sun.castShadow=true;
scene.add(sun);

function mat(color){return new THREE.MeshStandardMaterial({color,roughness:.82});}
function block(parent,w,h,d,m,x,y,z){
 const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);
 o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;
 parent.add(o);return o;
}
function ball(parent,x,y,z,sx,sy,sz,m){
 const o=new THREE.Mesh(new THREE.SphereGeometry(1,18,14),m);
 o.position.set(x,y,z);o.scale.set(sx,sy,sz);o.castShadow=true;
 parent.add(o);return o;
}

block(scene,16,.5,220,mat(0xe9f7ff),0,-.3,-96);
block(scene,16,.06,220,mat(0xb8eafa),0,-.02,-96);

// Cây đứng yên dọc hai bên đường.
for(let z=12;z>-205;z-=7){
 for(const side of [-1,1]){
  const x=side*(5.6+Math.random()*1.2);
  block(scene,.5,2,.5,mat(0x79563b),x,1,z);
  const crown=new THREE.Mesh(
   new THREE.ConeGeometry(1.55,3.2,7),
   mat([0x247d65,0x318b62,0x4a9c71][Math.floor(Math.random()*3)])
  );
  crown.position.set(x,3.4,z);crown.castShadow=true;scene.add(crown);
 }
}

// Nhân vật chim cánh cụt.
const penguin=new THREE.Group();scene.add(penguin);
const dark=mat(0x202938),white=mat(0xffffff),orange=mat(0xffa02a),black=mat(0x080d15);
ball(penguin,0,1.05,0,.52,.72,.43,dark);
ball(penguin,0,1,-.34,.37,.48,.12,white);
ball(penguin,0,1.95,0,.43,.42,.39,dark);
ball(penguin,-.16,1.97,-.32,.22,.2,.14,white);
ball(penguin,.16,1.97,-.32,.22,.2,.14,white);
ball(penguin,-.14,1.97,-.45,.06,.08,.04,black);
ball(penguin,.14,1.97,-.45,.06,.08,.04,black);
ball(penguin,0,1.82,-.48,.13,.08,.15,orange);
const wingL=block(penguin,.19,.62,.28,dark,-.52,1.13,0);
const wingR=block(penguin,.19,.62,.28,dark,.52,1.13,0);
const footL=block(penguin,.3,.12,.42,orange,-.25,.12,-.1);
const footR=block(penguin,.3,.12,.42,orange,.25,.12,-.1);

// 14 bức tường, mỗi bức ứng với một câu hỏi.
const gates=[];
for(let i=0;i<questions.length;i++){
 const z=-10-i*12;
 const group=new THREE.Group();scene.add(group);
 const colors=[0x3b9dd1,0x7766c8,0x45a99a,0xd39a49,0x5388d9];
 const wall=block(group,13,3.5,.8,mat(colors[i%colors.length]),0,1.75,z);
 block(group,13.2,.18,1,mat(0xffffff),0,3.55,z);
 block(group,.45,4,1.1,mat(0xffffff),-6.7,2,z);
 block(group,.45,4,1.1,mat(0xffffff),6.7,2,z);
 gates.push({z,wall,open:false,anim:0});
}

let gateIndex=0,started=false,finished=false;
let playerX=0,playerZ=4,playerY=0,jumpV=0;
let keys={},touch={},score=0,lastTime=0;

function showQuestion(){
 if(gateIndex>=questions.length)return;
 const q=questions[gateIndex];
 qbox.textContent=q.cat+" — "+q.q;
 abox.innerHTML="";
 q.a.forEach((a,i)=>{
  const b=document.createElement("button");
  b.className="answer";
  b.textContent=String.fromCharCode(65+i)+". "+a;
  b.onclick=()=>answer(i);
  abox.appendChild(b);
 });
}
function answer(i){
 if(!started||finished||gateIndex>=questions.length||gates[gateIndex].open)return;
 const q=questions[gateIndex];
 if(i===q.c){
  score++;
  gates[gateIndex].open=true;
  msg.textContent="🎉 Chính xác! Tường đang hạ xuống!";
  msg.style.background="#18864c";
  [...abox.children].forEach(b=>b.disabled=true);
 }else{
  msg.textContent="Chưa đúng rồi! Em hãy chọn lại nhé.";
  msg.style.background="#b63a45";
 }
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
 if(e.code==="Space"){keys.jump=true;e.preventDefault();}
});
window.addEventListener("keyup",e=>{
 keys[e.key.toLowerCase()]=false;
 if(e.code==="Space")keys.jump=false;
});
window.addEventListener("blur",()=>{keys={};touch={};});

document.querySelectorAll(".ctrl").forEach(b=>{
 const k=b.dataset.key;
 b.addEventListener("pointerdown",e=>{e.preventDefault();touch[k]=true;});
 ["pointerup","pointercancel","pointerleave"].forEach(ev=>
  b.addEventListener(ev,e=>{e.preventDefault();touch[k]=false;})
 );
});
const jumpBtn=document.getElementById("jump");
jumpBtn.addEventListener("pointerdown",e=>{e.preventDefault();touch.jump=true;});
["pointerup","pointercancel","pointerleave"].forEach(ev=>
 jumpBtn.addEventListener(ev,e=>{e.preventDefault();touch.jump=false;})
);

function forward(){return keys.w||keys.arrowup||touch.up;}
function backward(){return keys.s||keys.arrowdown||touch.down;}
function left(){return keys.a||keys.arrowleft||touch.left;}
function right(){return keys.d||keys.arrowright||touch.right;}

function update(dt){
 if(!started||finished)return;
 const speed=7*dt;
 let dz=0,dx=0;
 if(forward())dz-=speed;
 if(backward())dz+=speed;
 if(left())dx-=speed;
 if(right())dx+=speed;
 playerX=Math.max(-5.4,Math.min(5.4,playerX+dx));

 if((keys.jump||touch.jump)&&playerY<=.01)jumpV=7;
 keys.jump=false;touch.jump=false;
 jumpV-=18*dt;playerY+=jumpV*dt;
 if(playerY<0){playerY=0;jumpV=0;}

 if(gateIndex<gates.length){
  const g=gates[gateIndex];
  const stopZ=g.z+1.25;
  if(!g.open){
   if(playerZ+dz<stopZ)playerZ=stopZ;
   else playerZ+=dz;
  }else{
   playerZ+=dz;
   g.anim=Math.min(1,g.anim+dt*1.5);
   g.wall.position.y=1.75*(1-g.anim);
   if(playerZ<g.z-2){
    gateIndex++;
    if(gateIndex<gates.length){
     showQuestion();
     msg.textContent="Cửa "+(gateIndex+1)+"/14 đang chờ em!";
     msg.style.background="#16466bde";
    }else{
     finished=true;
     document.getElementById("result").textContent=
      "Em đã vượt qua đủ 14 bức tường! Trả lời đúng "+score+"/14 câu hỏi. Tuyệt vời!";
     winScreen.style.display="flex";
    }
   }
  }
 }else playerZ+=dz;

 penguin.position.set(playerX,playerY,playerZ);
 const walking=forward()||backward()||left()||right();
 const t=performance.now()*.009;
 wingL.rotation.z=walking?Math.sin(t)*.35:0;
 wingR.rotation.z=walking?-Math.sin(t)*.35:0;
 footL.rotation.x=walking?Math.sin(t)*.35:0;
 footR.rotation.x=walking?-Math.sin(t)*.35:0;

 camera.position.lerp(new THREE.Vector3(playerX,playerY+4.4,playerZ+8.5),Math.min(1,dt*5));
 camera.lookAt(playerX,playerY+1.1,playerZ-5);

 if(gateIndex<14){
  msg.textContent="🐧 Bức tường "+(gateIndex+1)+"/14 | Đúng: "+score+" câu";
 }
}

function animate(time){
 requestAnimationFrame(animate);
 const dt=Math.min((time-lastTime)/1000||0,.04);
 lastTime=time;update(dt);renderer.render(scene,camera);
}
requestAnimationFrame(animate);

function reset(){
 playerX=0;playerZ=4;playerY=0;jumpV=0;
 gateIndex=0;score=0;finished=false;started=true;
 keys={};touch={};
 gates.forEach(g=>{g.open=false;g.anim=0;g.wall.position.y=1.75;});
 startScreen.style.display="none";
 winScreen.style.display="none";
 msg.style.background="#16466bde";
 showQuestion();
}
document.getElementById("startBtn").onclick=reset;
document.getElementById("restartBtn").onclick=reset;
showQuestion();
})();
</script>
</body>
</html>
"""

components.html(html, height=700, scrolling=False)
