
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Heo Chủ Tịch", page_icon="🐷")

st.title("🐷 HEO CHỦ TỊCH")
st.write("Thu thập 10 giỏ thức ăn để cứu nông trại!")

game = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body { margin:0; font-family:Arial; }
#hud {
 position:absolute; top:10px; left:10px;
 z-index:2; background:white; padding:10px;
 border-radius:10px; font-weight:bold;
}
#hint {
 position:absolute; bottom:10px; left:10px;
 z-index:2; background:white; padding:8px;
 border-radius:8px;
}
</style>
</head>
<body>
<div id="hud">🐷 Heo Chủ Tịch | 🧺 <span id="score">0</span>/10</div>
<div id="hint">Dùng WASD hoặc phím mũi tên để di chuyển</div>
<div id="game" style="width:100%;height:580px"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
const root = document.getElementById("game");
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x9edcff);

const camera = new THREE.PerspectiveCamera(
 65, root.clientWidth/root.clientHeight, 0.1, 200
);
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(root.clientWidth, root.clientHeight);
root.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xffffff,0x668844,2));

const sun = new THREE.DirectionalLight(0xffffff,2);
sun.position.set(-5,15,10);
scene.add(sun);

function mat(color) {
 return new THREE.MeshStandardMaterial({color:color});
}
function box(x,y,z,sx,sy,sz,color) {
 const m = new THREE.Mesh(
  new THREE.BoxGeometry(sx,sy,sz),mat(color)
 );
 m.position.set(x,y,z);
 scene.add(m);
 return m;
}
function ball(parent,x,y,z,sx,sy,sz,color) {
 const m = new THREE.Mesh(
  new THREE.SphereGeometry(1,16,12),mat(color)
 );
 m.position.set(x,y,z);
 m.scale.set(sx,sy,sz);
 parent.add(m);
 return m;
}

// Mặt đất và đường làng
const ground = new THREE.Mesh(
 new THREE.PlaneGeometry(100,200),mat(0x76bd55)
);
ground.rotation.x=-Math.PI/2;
ground.position.z=-40;
scene.add(ground);

const road = new THREE.Mesh(
 new THREE.PlaneGeometry(10,200),mat(0xc69a66)
);
road.rotation.x=-Math.PI/2;
road.position.set(0,0.02,-40);
scene.add(road);

// Cây hai bên đường
for(let z=10;z>-120;z-=12) {
 for(const x of [-9,9]) {
  const trunk=box(x,0.8,z,0.4,1.6,0.4,0x81502b);
  ball(scene,x,2,z,1.2,1.3,1.2,0x32934b);
 }
}

// Nhân vật heo
const pig=new THREE.Group();
scene.add(pig);
ball(pig,0,0.7,0,0.65,0.5,0.75,0xffa4b5);
ball(pig,0,1.35,-0.35,0.52,0.5,0.5,0xffa4b5);
ball(pig,0,1.22,-0.8,0.28,0.2,0.12,0xe66f83);

for(const x of [-0.2,0.2]) {
 ball(pig,x,1.5,-0.77,0.06,0.07,0.04,0x222222);
 ball(pig,x*1.8,1.8,-0.3,0.13,0.22,0.1,0xe66f83);
}
for(const x of [-0.4,0.4]) {
 for(const z of [-0.4,0.4]) {
  box(x,0.25,z,0.22,0.4,0.22,0xe66f83);
 }
}

// Nón lá
const hat=new THREE.Mesh(
 new THREE.ConeGeometry(0.6,0.3,20),mat(0xe5c66c)
);
hat.position.set(0,1.85,-0.3);
pig.add(hat);

// Giỏ thức ăn
const baskets=[];
for(let i=0;i<10;i++) {
 const g=new THREE.Group();
 g.position.set([-3,0,3][i%3],0,-8-i*9);
 scene.add(g);
 const b=new THREE.Mesh(
  new THREE.CylinderGeometry(0.25,0.18,0.35,12),
  mat(0xb97937)
 );
 b.position.y=0.25;
 g.add(b);
 ball(g,-0.08,0.47,0,0.12,0.1,0.12,0x54bd43);
 ball(g,0.1,0.47,0,0.12,0.1,0.12,0xe74a4a);
 baskets.push(g);
}

// Đống rơm
const obstacles=[];
for(let i=0;i<10;i++) {
 const x=[-3,0,3][i%3];
 const z=-5-i*10;
 box(x,0.55,z,1.5,1.1,1.3,0xe9bd48);
 obstacles.push({x:x,z:z});
}

pig.position.set(0,0,5);
const keys={};
let score=0;
let running=true;

document.addEventListener("keydown",e=>{
 keys[e.key.toLowerCase()]=true;
});
document.addEventListener("keyup",e=>{
 keys[e.key.toLowerCase()]=false;
});

function animate() {
 requestAnimationFrame(animate);

 if(running) {
  let dx=0,dz=0;
  if(keys["arrowleft"]||keys["a"])dx-=1;
  if(keys["arrowright"]||keys["d"])dx+=1;
  if(keys["arrowup"]||keys["w"])dz-=1;
  if(keys["arrowdown"]||keys["s"])dz+=1;

  const len=Math.hypot(dx,dz)||1;
  dx/=len; dz/=len;

  const ox=pig.position.x,oz=pig.position.z;
  pig.position.x=Math.max(-4,Math.min(4,ox+dx*0.16));
  pig.position.z=Math.min(10,oz+dz*0.16);

  for(const o of obstacles) {
   if(Math.hypot(pig.position.x-o.x,pig.position.z-o.z)<1.2) {
    pig.position.x=ox;
    pig.position.z=oz;
   }
  }

  for(let i=0;i<baskets.length;i++) {
   if(baskets[i].visible &&
    Math.hypot(
     pig.position.x-baskets[i].position.x,
     pig.position.z-baskets[i].position.z
    )<1.2) {
     baskets[i].visible=false;
     score++;
     document.getElementById("score").textContent=score;
     if(score>=10) {
      running=false;
      alert("🎉 Heo Chủ Tịch đã cứu được nông trại!");
     }
   }
  }
 }

 camera.position.lerp(
  new THREE.Vector3(pig.position.x,5.5,pig.position.z+9),0.08
 );
 camera.lookAt(pig.position.x,1,pig.position.z-3);
 renderer.render(scene,camera);
}
animate();

window.addEventListener("resize",()=>{
 camera.aspect=root.clientWidth/root.clientHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(root.clientWidth,root.clientHeight);
});
</script>
</body>
</html>
"""

components.html(game, height=600, scrolling=False)
