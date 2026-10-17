
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Heo Chủ Tịch", layout="wide")

st.title("🐷 HEO CHỦ TỊCH")
st.caption("A/D hoặc phím mũi tên: đổi làn • SPACE: nhảy • S hoặc mũi tên xuống: cúi")

game = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body { margin:0; overflow:hidden; background:#87ceeb; font-family:Arial; }
#hud {
 position:absolute; top:12px; left:12px; z-index:5;
 color:white; font-size:20px; font-weight:bold;
 text-shadow:2px 2px 4px #333;
}
#help {
 position:absolute; bottom:10px; left:0; right:0;
 text-align:center; color:white; font-weight:bold;
 text-shadow:2px 2px 4px #333;
}
#message {
 display:none; position:absolute; inset:0; z-index:10;
 background:#0009; color:white; text-align:center;
 padding-top:18%; font-size:30px;
}
button { padding:12px 25px; font-size:20px; cursor:pointer; }
</style>
</head>
<body>
<div id="hud">🥩 Điểm: <span id="score">0</span> / 50</div>
<div id="help">← → đổi làn | SPACE nhảy | ↓ cúi</div>
<div id="message">
 <div id="msgtext">Bạn đã thắng!</div><br>
 <button onclick="restart()">CHƠI LẠI</button>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x83d8ff);
scene.fog = new THREE.Fog(0x83d8ff, 28, 100);

const camera = new THREE.PerspectiveCamera(
 65, window.innerWidth/window.innerHeight, 0.1, 200
);
camera.position.set(0, 5.2, 10);
camera.lookAt(0, 1, -5);

const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
document.body.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xffffff, 0x65734b, 2));
const sun = new THREE.DirectionalLight(0xffffff, 2);
sun.position.set(-5, 12, 8);
sun.castShadow = true;
scene.add(sun);

const mat = c => new THREE.MeshStandardMaterial({color:c});
const green = mat(0x248b3d);
const brown = mat(0x79502b);
const hay = mat(0xd8a447);
const white = mat(0xffffff);
const roadMat = mat(0x666666);

function box(w,h,d,material,x,y,z) {
 const o = new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material);
 o.position.set(x,y,z);
 o.castShadow = true;
 o.receiveShadow = true;
 scene.add(o);
 return o;
}
function ball(rx,ry,rz,material,x,y,z,parent=scene) {
 const o = new THREE.Mesh(
  new THREE.SphereGeometry(1,16,12), material
 );
 o.scale.set(rx,ry,rz);
 o.position.set(x,y,z);
 o.castShadow = true;
 parent.add(o);
 return o;
}

// Mặt đất và đường xám
box(200,0.2,200,mat(0x65a94d),0,-0.2,-45);
box(8,0.1,200,roadMat,0,-0.05,-45);

// Vạch đường
const marks=[];
for(let z=8;z>-150;z-=8){
 for(let x of [-1.33,1.33]){
  marks.push(box(0.09,0.025,3,white,x,0.02,z));
 }
}

// Cây đứng yên hai bên đường
for(let z=8;z>-130;z-=9){
 for(let side of [-1,1]){
  const x=side*(6+Math.random()*2);
  box(0.38,2.2,0.38,brown,x,1.1,z);
  ball(1.25,1.3,1.15,green,x,2.65,z);
  ball(0.9,0.95,0.9,mat(0x319b50),x-0.45,3.05,z);
  ball(0.9,0.95,0.9,mat(0x3ba653),x+0.45,2.95,z);
 }
}

// Heo mặc vest xanh, đứng bằng hai chân sau
const pig = new THREE.Group();
scene.add(pig);
pig.position.set(0,0,3);

const pink=mat(0xf5a7b8);
const darkPink=mat(0xe47f98);
const blue=mat(0x1768ce);
const black=mat(0x202020);
const gold=mat(0xffd34e);

ball(0.43,0.48,0.35,pink,0,1.35,0,pig);
ball(0.48,0.43,0.4,pink,0,2.05,0,pig);
ball(0.18,0.22,0.16,pink,-0.29,2.4,0,pig);
ball(0.18,0.22,0.16,pink,0.29,2.4,0,pig);
ball(0.15,0.1,0.09,darkPink,0,2.03,0.37,pig);
ball(0.045,0.055,0.035,black,-0.15,2.17,0.35,pig);
ball(0.045,0.055,0.035,black,0.15,2.17,0.35,pig);

// Vest xanh
box(0.72,0.62,0.48,blue,0,1.35,0,pig);
box(0.08,0.48,0.03,white,0,1.38,0.25,pig);
for(let y of [1.2,1.4,1.6]) ball(0.035,0.035,0.025,gold,0,y,0.29,pig);

// Hai chân sau
const legs=[];
for(let x of [-0.23,0.23]){
 const leg=box(0.2,0.42,0.24,pink,x,0.5,0,pig);
 legs.push(leg);
 box(0.23,0.12,0.28,black,x,0.25,0.03,pig);
}

// Hai tay
const arms=[];
for(let x of [-0.48,0.48]){
 const arm=box(0.18,0.48,0.2,pink,x,1.42,0,pig);
 arms.push(arm);
}

// Mũ
const hat=mat(0x173f91);
box(0.62,0.13,0.52,hat,0,2.48,0,pig);
box(0.43,0.25,0.42,hat,0,2.62,-0.02,pig);
box(0.8,0.06,0.2,gold,0,2.51,0.2,pig);

// Đồ chơi di chuyển phía trước
let obstacles=[];
let meats=[];
let ramps=[];
let score=0;
let speed=0.22;
let lane=0;
let jumpY=0;
let jumpV=0;
let duckTime=0;
let running=true;
let frame=0;
let skyPhase=-1;

function makeHay(x,z,w=0.9,h=0.7,d=0.7){
 const o=box(w,h,d,hay,x,h/2,z);
 ball(w*0.47,h*0.48,d*0.48,mat(0xe8bd61),x,h/2,z);
 return o;
}

function addObstacle(type,z){
 const g=new THREE.Group();
 scene.add(g);
 const x=[-2,0,2][Math.floor(Math.random()*3)];
 g.position.set(x,0,z);

 if(type===1){
  // Cổng rơm cao, có khoảng trống bên dưới để cúi qua
  box(0.22,1.35,0.5,hay,-0.48,1.15,0,g);
  box(0.22,1.35,0.5,hay,0.48,1.15,0,g);
  box(1.2,0.3,0.5,hay,0,1.9,0,g);
 } else if(type===2){
  // Rơm thấp, cần nhảy qua
  makeHay(0,0,1.15,0.48,0.8).position.y=0.24;
 } else {
  // Bậc rơm lên rồi xuống
  makeHay(-0.65,0,0.55,0.45,0.65);
  const a=makeHay(0,0,0.55,0.85,0.65);
  a.position.y=0.425;
  makeHay(0.65,0,0.55,0.45,0.65);
 }
 obstacles.push({group:g,type:type,lane:Math.round((x+2)/2),z:z});
}

function addMeat(z){
 const g=new THREE.Group();
 scene.add(g);
 const meatMat=mat(0xd72d36);
 ball(0.24,0.14,0.12,meatMat,0,0,0,g);
 ball(0.08,0.08,0.08,white,-0.18,0.02,0,g);
 ball(0.08,0.08,0.08,white,0.18,0.02,0,g);
 g.position.set([-2,0,2][Math.floor(Math.random()*3)],1,z);
 meats.push(g);
}

function updateSky(){
 let bg;
 if(score<10) bg=0x83d8ff;
 else if(score<20) bg=0x8aa6b7;
 else if(score<30) bg=0xf08b59;
 else if(score<40) bg=0x19213f;
 else if(score<50) bg=0xe7a6a1;
 else bg=0x83d8ff;

 scene.background.setHex(bg);
 scene.fog.color.setHex(bg);
 sun.intensity=score>=30&&score<40?0.35:1.8;
}

function endGame(win){
 running=false;
 document.getElementById('message').style.display='block';
 document.getElementById('msgtext').innerText=
  win?'🎉 HEO CHỦ TỊCH ĐÃ THẮNG!':'💥 Ôi! Va vào chướng ngại vật rồi!';
}

function restart(){
 location.reload();
}

function moveLane(dir){
 lane=Math.max(-1,Math.min(1,lane+dir));
}

document.addEventListener('keydown',e=>{
 if(e.code==='ArrowLeft'||e.code==='KeyA') moveLane(-1);
 if(e.code==='ArrowRight'||e.code==='KeyD') moveLane(1);
 if((e.code==='Space'||e.code==='ArrowUp')&&jumpY===0&&duckTime<=0){
  jumpV=0.24;
 }
 if(e.code==='ArrowDown'||e.code==='KeyS') duckTime=35;
});

for(let z=-20;z>-130;z-=17){
 addObstacle(1+Math.floor(Math.random()*3),z);
 addMeat(z-7);
}

// Bậc rơm trang trí ở phía xa, cho thấy lối đi lên xuống
for(let i=0;i<8;i++){
 const h=i<4?0.25+i*0.22:0.25+(7-i)*0.22;
 const r=box(0.65,h,0.7,hay,2.4,h/2,-35-i*0.85);
 ramps.push(r);
}

function animate(){
 requestAnimationFrame(animate);
 if(running){
  frame++;

  // Heo tự chạy tại chỗ
  pig.position.x+=(lane*2-pig.position.x)*0.14;
  if(jumpY>0||jumpV>0){
   jumpY+=jumpV;
   jumpV-=0.018;
   if(jumpY<0){jumpY=0;jumpV=0;}
  }
  pig.position.y=jumpY;
  if(duckTime>0) duckTime--;
  pig.scale.y=duckTime>0?0.65:1;

  legs.forEach((l,i)=>l.rotation.x=Math.sin(frame*0.28+i*Math.PI)*0.45);
  arms.forEach((a,i)=>a.rotation.z=Math.sin(frame*0.28+i*Math.PI)*0.25);

  // Đường chạy lùi để tạo cảm giác chạy về phía trước
  marks.forEach(m=>{
   m.position.z+=speed;
   if(m.position.z>10)m.position.z-=160;
  });

  obstacles.forEach(o=>{
   o.group.position.z+=speed;
   if(o.z<4&&o.z>-1&&o.lane===lane){
    if(o.type===1&&duckTime<=0&&jumpY<0.5) endGame(false);
    if(o.type===2&&jumpY<0.55) endGame(false);
   }
  });
  obstacles=obstacles.filter(o=>{
   if(o.group.position.z>12){scene.remove(o.group);return false;}
   return true;
  });

  meats.forEach(m=>{
   m.position.z+=speed;
   m.rotation.y+=0.06;
   if(!m.userData.got&&Math.abs(m.position.z-pig.position.z)<0.7&&
      Math.abs(m.position.x-pig.position.x)<0.85&&jumpY<2.2){
    m.userData.got=true;
    scene.remove(m);
    score++;
    document.getElementById('score').innerText=score;
    updateSky();
    if(score>=50) endGame(true);
   }
  });
  meats=meats.filter(m=>{
   if(m.userData.got)return false;
   if(m.position.z>12){scene.remove(m);return false;}
   return true;
  });

  if(frame%80===0)addObstacle(1+Math.floor(Math.random()*3),-100);
  if(frame%65===0)addMeat(-95);
 }
 renderer.render(scene,camera);
}
animate();

window.addEventListener('resize',()=>{
 camera.aspect=window.innerWidth/window.innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(window.innerWidth,window.innerHeight);
});
</script>
</body>
</html>
"""

components.html(game, height=660, scrolling=False)
