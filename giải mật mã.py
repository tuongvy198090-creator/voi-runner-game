
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Thoát Khỏi Căn Phòng</title>
<style>
*{box-sizing:border-box}
body{margin:0;overflow:hidden;font-family:Arial;background:#111;color:white}
canvas{display:block}
#hud{position:absolute;top:12px;left:12px;background:#101820dd;padding:12px 16px;border:1px solid #67e8f9;border-radius:12px;z-index:5}
#msg{color:#fde68a;margin-top:6px;font-size:14px}
#cross{position:absolute;left:50%;top:50%;font-size:25px;transform:translate(-50%,-50%);pointer-events:none}
#hands{position:absolute;bottom:-35px;left:50%;transform:translateX(-50%);width:260px;height:190px;pointer-events:none;z-index:3}
.arm{position:absolute;bottom:0;width:75px;height:145px;background:linear-gradient(90deg,#bd815d,#f0bd91,#bd815d);border:3px solid #89583f;border-radius:40px 40px 10px 10px}
.arm.left{left:15px;transform:rotate(20deg)}
.arm.right{right:15px;transform:rotate(-20deg)}
.hand{position:absolute;bottom:110px;width:65px;height:60px;background:#e9b28a;border-radius:45% 45% 35% 35%;border:2px solid #9b6648}
.hand.left{left:5px}.hand.right{right:5px}
#controls{position:absolute;bottom:18px;left:15px;display:grid;grid-template-columns:55px 55px 55px;gap:5px;z-index:8}
button{background:#263746ee;color:white;border:1px solid #8be9fd;border-radius:10px;padding:12px;cursor:pointer;font-size:16px}
button:active{background:#087e8b}
#controls button:nth-child(1){grid-column:2}
#controls button:nth-child(2){grid-column:1;grid-row:2}
#controls button:nth-child(3){grid-column:2;grid-row:2}
#controls button:nth-child(4){grid-column:3;grid-row:2}
#actions{position:absolute;bottom:25px;right:15px;display:flex;flex-direction:column;gap:8px;z-index:8}
#panel{display:none;position:absolute;inset:0;background:#000b;z-index:10;align-items:center;justify-content:center}
.box{background:#172535;border:2px solid #67e8f9;border-radius:16px;padding:24px;width:min(340px,90vw);text-align:center}
input{width:100%;padding:12px;font-size:22px;text-align:center;margin:12px 0;border-radius:8px;border:1px solid #67e8f9}
#start{position:absolute;inset:0;background:linear-gradient(#081827dd,#020609ee);z-index:20;display:flex;align-items:center;justify-content:center;text-align:center;padding:20px}
#start h1{color:#67e8f9}
.small{font-size:13px;color:#cbd5e1}
</style>
</head>
<body>
<div id="hud">
  <b>🔐 THOÁT KHỎI CĂN PHÒNG</b>
  <div id="inventory">🎒 Đồ vật: chưa có</div>
  <div id="msg">Tìm manh mối để thoát ra!</div>
</div>
<div id="cross">+</div>
<div id="hands">
  <div class="arm left"></div><div class="arm right"></div>
  <div class="hand left"></div><div class="hand right"></div>
</div>
<div id="controls">
  <button onclick="move(0,1)">▲</button>
  <button onclick="move(-1,0)">◀</button>
  <button onclick="move(0,-1)">▼</button>
  <button onclick="move(1,0)">▶</button>
</div>
<div id="actions">
  <button onclick="turn(-0.22)">↶ Quay trái</button>
  <button onclick="turn(0.22)">↷ Quay phải</button>
  <button onclick="interact()">🔎 Tương tác</button>
</div>
<div id="panel"><div class="box">
  <h2 id="panelTitle">Mật mã</h2>
  <p id="panelText">Nhập câu trả lời</p>
  <input id="answer" maxlength="12" placeholder="Nhập ở đây">
  <button onclick="submitAnswer()">Xác nhận</button>
  <button onclick="closePanel()">Đóng</button>
</div></div>
<div id="start"><div>
  <h1>🚪 THOÁT KHỎI CĂN PHÒNG</h1>
  <p>Bạn tỉnh dậy trong căn phòng xa lạ.</p>
  <p>Tìm manh mối, giải mật mã và mở cửa để thoát!</p>
  <p class="small">Dùng các nút điều khiển hoặc phím WASD. Nhấn E để tương tác.</p>
  <button onclick="startGame()">BẮT ĐẦU CHƠI</button>
</div></div>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
let scene,camera,renderer,player,started=false,yaw=0;
let objects=[],inventory=[],drawerOpen=false,boxOpen=false,doorOpen=false;
let near=null,walk=0;
const msg=document.getElementById('msg');
const inv=document.getElementById('inventory');
const panel=document.getElementById('panel');
const answer=document.getElementById('answer');
let puzzle='';

scene=new THREE.Scene();
scene.background=new THREE.Color(0x8799a8);
scene.fog=new THREE.Fog(0x8799a8,12,32);
camera=new THREE.PerspectiveCamera(75,innerWidth/innerHeight,0.1,100);
camera.position.set(0,1.65,5);
scene.add(camera);

renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setSize(innerWidth,innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled=true;
renderer.outputColorSpace=THREE.SRGBColorSpace;
document.body.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xddeeff,0x514438,2));
let light=new THREE.DirectionalLight(0xffe0b0,2.5);
light.position.set(-3,8,5);scene.add(light);

function mat(color,roughness=0.85){return new THREE.MeshStandardMaterial({color,roughness})}
const wall=mat(0xc5b9a5),floorMat=mat(0x6b5849),wood=mat(0x70472e),darkWood=mat(0x3c291f),metal=mat(0xd3b15f),cloth=mat(0x263d56);
function cube(name,x,y,z,sx,sy,sz,material,interact=null){
 let m=new THREE.Mesh(new THREE.BoxGeometry(sx,sy,sz),material);
 m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;scene.add(m);
 if(name)objects.push({name,mesh:m,interact});
 return m;
}
cube(null,0,-.15,0,12,.3,14,floorMat);
cube(null,0,3,-7,12,6,.25,wall);
cube(null,-6,3,0,.25,6,14,wall);
cube(null,6,3,0,.25,6,14,wall);
cube(null,0,6,0,12,.25,14,mat(0x393d49));
cube(null,0,3,7,12,6,.25,wall);

// Cửa phía trước
const door=cube('Cửa khóa',0,1.8,-6.82,1.8,3.6,.15,wood,()=>doorPuzzle());
cube(null,0,1.8,-6.70,.16,3.6,.05,darkWood);
const knob=new THREE.Mesh(new THREE.SphereGeometry(.09,16,12),metal);
knob.position.set(.58,1.6,-6.58);scene.add(knob);

// Thảm và cửa sổ
cube(null,0,.02,1,3,.04,3,mat(0x8b493b));
cube(null,-3.3,3,-6.82,1.6,1.4,.1,mat(0x334d60));
cube(null,-3.3,3,-6.72,.08,1.5,.08,metal);
cube(null,-3.3,3,-6.70,1.7,.08,.08,metal);

// Bàn
cube(null,2,1,-1.5,2.4,.18,1.1,wood);
for(let x of [1.05,2.95])for(let z of [-1.9,-1.1])cube(null,x,.48,z,.14,1, .14,darkWood);
// Ngăn kéo
const drawer=cube('Ngăn kéo',2,1,-.88,1,.45,.12,darkWood,()=>drawerPuzzle());
cube(null,2,1,-.79,.18,.08,.05,metal);

// Hộp bí mật trên bàn
const chest=cube('Hộp bí mật',2,1.35,-1.5,.8,.48,.65,mat(0x243b52),()=>chestPuzzle());
cube(null,2,1.36,-1.15,.18,.14,.08,metal);

// Kệ sách
cube(null,-4,1.5,-2,1.5,3,.5,wood);
for(let y of [.55,1.35,2.15])cube(null,-4,y,-1.72,1.4,.09,.12,darkWood);
for(let i=0;i<10;i++){
 let h=.35+Math.random()*.35;
 cube(null,-4.55+(i%5)*.24,.65+Math.floor(i/5)*.8,-1.68,.16,h,.15,mat([0x9b443d,0x355c52,0x384b76,0xb38a43][i%4]));
}

// Đồng hồ và tranh có manh mối
const clock=cube('Đồng hồ',-2.5,3.5,-6.78,.9,.9,.12,mat(0xefe3c9),()=>clue('Đồng hồ dừng ở 8 giờ. Hãy nhớ số 8.'));
cube(null,-2.5,3.5,-6.68,.05,.4,.03,darkWood);
cube(null,-2.5,3.5,-6.66,.3,.05,.03,darkWood);
const note=cube('Tờ giấy',-1,1.1,1,.45,.04,.35,mat(0xf6e8b5),()=>clue('Mảnh giấy ghi: “Số đầu tiên là 3”.'));
cube(null,-1,1.14,1,.3,.015,.02,mat(0x45392a));

// Chậu cây
cube(null,-4,.35,2,.65,.7,.65,mat(0x9d593d));
let stem=new THREE.Mesh(new THREE.CylinderGeometry(.06,.1,.9,8),mat(0x3c7544));stem.position.set(-4,.95,2);scene.add(stem);
for(let i=0;i<5;i++){
 let leaf=new THREE.Mesh(new THREE.SphereGeometry(.35,12,10),mat(0x3e8c53));
 leaf.position.set(-4+Math.sin(i*1.4)*.4,1.25+(i%2)*.25,2+Math.cos(i*1.4)*.3);scene.add(leaf);
}

// Đèn trần
let lamp=new THREE.Mesh(new THREE.CylinderGeometry(.5,.7,.12,20),mat(0xf2d79a));
lamp.position.set(0,5.65,0);scene.add(lamp);
let point=new THREE.PointLight(0xffdca0,35,15);point.position.set(0,5,0);scene.add(point);

function startGame(){document.getElementById('start').style.display='none';started=true;msg.textContent='Tìm tờ giấy trên sàn và khám phá căn phòng!';}
function turn(a){if(!started)return;yaw+=a;camera.rotation.y=yaw;}
function move(dx,dz){
 if(!started)return;
 const speed=.55;
 const fx=Math.sin(yaw),fz=-Math.cos(yaw);
 const rx=Math.cos(yaw),rz=Math.sin(yaw);
 let nx=camera.position.x+(rx*dx+fx*dz)*speed;
 let nz=camera.position.z+(rz*dx+fz*dz)*speed;
 if(nx>-5.4&&nx<5.4&&nz>-6.1&&nz<6.1){
 camera.position.x=nx;camera.position.z=nz;walk+=1;
 document.getElementById('hands').style.transform=`translateX(-50%) translateY(${walk%2?4:0}px)`;
 }
}
function nearest(){
 let best=null,dist=2.5;
 for(const o of objects){
  if(!o.interact)continue;
  let d=camera.position.distanceTo(o.mesh.position);
  if(d<dist){dist=d;best=o;}
 }
 return best;
}
function interact(){
 if(!started)return;
 near=nearest();
 if(!near){msg.textContent='Chưa có đồ vật gần bạn. Hãy di chuyển lại gần!';return;}
 near.interact();
}
function clue(text){msg.textContent=text;}
function openPuzzle(title,text,type){
 puzzle=type;document.getElementById('panelTitle').textContent=title;
 document.getElementById('panelText').textContent=text;
 answer.value='';panel.style.display='flex';answer.focus();
}
function closePanel(){panel.style.display='none';}
function drawerPuzzle(){
 if(drawerOpen){clue('Ngăn kéo đã mở. Bên trong có một chiếc chìa khóa nhỏ!');return;}
 openPuzzle('🔐 Mật mã ngăn kéo','Gợi ý: Trên tờ giấy có số 3, đồng hồ chỉ số 8. Nhập mã 2 chữ số.','drawer');
}
function chestPuzzle(){
 if(!drawerOpen){clue('Hộp bí mật bị khóa. Hãy mở ngăn kéo trước!');return;}
 if(boxOpen){clue('Bạn đã lấy được chìa khóa cửa!');return;}
 openPuzzle('📦 Hộp bí mật','Giải câu đố: 6 × 7 = ? Nhập đáp án.','chest');
}
function doorPuzzle(){
 if(!boxOpen){clue('Cửa vẫn khóa. Bạn cần tìm chìa khóa trong hộp bí mật!');return;}
 doorOpen=true;
 door.material=mat(0x397d55);
 door.rotation.y=-Math.PI/2;
 document.getElementById('panelTitle').textContent='🎉 BẠN ĐÃ THOÁT!';
 document.getElementById('panelText').textContent='Chúc mừng! Bạn đã giải hết mật mã và thoát khỏi căn phòng thành công!';
 answer.style.display='none';
 panel.style.display='flex';
}
function submitAnswer(){
 let a=answer.value.trim();
 if(puzzle==='drawer'&&a==='38'){
 drawerOpen=true;inventory.push('🗝️ Chìa khóa nhỏ');
 drawer.scale.set(1,.1,1);
 inv.textContent='🎒 Đồ vật: '+inventory.join(', ');
 msg.textContent='Mở ngăn kéo thành công! Hãy tìm hộp bí mật trên bàn.';
 closePanel();
 }else if(puzzle==='chest'&&a==='42'){
 boxOpen=true;inventory.push('🗝️ Chìa khóa cửa');
 chest.material=mat(0xc69b42);
 inv.textContent='🎒 Đồ vật: '+inventory.join(', ');
 msg.textContent='Bạn đã lấy được chìa khóa cửa! Hãy tới cánh cửa.';
 closePanel();
 }else{
 document.getElementById('panelText').textContent='Sai mất rồi! Hãy suy nghĩ và thử lại nhé.';
 }
}
addEventListener('keydown',e=>{
 if(e.key==='w'||e.key==='ArrowUp')move(0,1);
 if(e.key==='s'||e.key==='ArrowDown')move(0,-1);
 if(e.key==='a'||e.key==='ArrowLeft')move(-1,0);
 if(e.key==='d'||e.key==='ArrowRight')move(1,0);
 if(e.key==='e'||e.key==='Enter')interact();
 if(e.key==='Escape')closePanel();
});
addEventListener('resize',()=>{
 camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
});
function animate(){
 requestAnimationFrame(animate);
 camera.rotation.order='YXZ';
 renderer.render(scene,camera);
}
animate();
</script>
</body>
</html>
