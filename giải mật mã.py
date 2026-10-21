
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Thoát Khỏi Căn Phòng",
    page_icon="🔐",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101d2d, #203b43);
    color: white;
}
h1 {
    text-align: center;
    color: #7df9ff;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🔐 THOÁT KHỎI CĂN PHÒNG")
st.markdown(
    "<p style='text-align:center'>"
    "Tìm manh mối • Giải mật mã • Tìm chìa khóa • Thoát ra!"
    "</p>",
    unsafe_allow_html=True
)

GAME_HTML = r'''
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
*{box-sizing:border-box}
body{margin:0;background:#101820;color:white;font-family:Arial}
canvas{display:block}
#hud{position:absolute;top:10px;left:10px;background:#10202ddd;
padding:12px;border:1px solid #67e8f9;border-radius:12px;z-index:3}
#msg{color:#ffe58a;margin-top:8px;max-width:270px}
#cross{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
font-size:24px;pointer-events:none}
#hands{position:absolute;bottom:-35px;left:50%;transform:translateX(-50%);
width:240px;height:170px;pointer-events:none}
.arm{position:absolute;bottom:0;width:65px;height:130px;
background:linear-gradient(90deg,#b97955,#f1bd91,#b97955);
border-radius:35px 35px 12px 12px;border:2px solid #81533e}
.left{left:12px;transform:rotate(18deg)}
.right{right:12px;transform:rotate(-18deg)}
.hand{position:absolute;bottom:105px;width:55px;height:50px;
background:#edb68c;border-radius:50%;border:2px solid #81533e}
.hand.left{left:4px}.hand.right{right:4px}
#controls{position:absolute;bottom:12px;left:10px;display:grid;
grid-template-columns:48px 48px 48px;gap:4px;z-index:4}
#controls button:first-child{grid-column:2}
#controls button:nth-child(2){grid-column:1}
#controls button:nth-child(3){grid-column:2}
#controls button:nth-child(4){grid-column:3}
#actions{position:absolute;right:10px;bottom:15px;display:flex;
flex-direction:column;gap:6px;z-index:4}
button{background:#183b4a;color:white;border:1px solid #67e8f9;
padding:11px;border-radius:10px;font-size:14px;cursor:pointer}
#modal{display:none;position:absolute;inset:0;background:#000b;
align-items:center;justify-content:center;z-index:8}
.box{background:#15283b;border:2px solid #67e8f9;border-radius:16px;
padding:22px;width:min(320px,90%);text-align:center}
input{width:100%;padding:12px;font-size:20px;margin:10px 0;
text-align:center;border-radius:8px}
#start{position:absolute;inset:0;z-index:10;background:#07111bee;
display:flex;align-items:center;justify-content:center;text-align:center;
padding:20px}
#start h1{color:#67e8f9}
</style>
</head>
<body>
<div id="hud">
<b>🔐 THOÁT KHỎI CĂN PHÒNG</b>
<div id="items">🎒 Chưa có vật phẩm</div>
<div id="msg">Tìm manh mối trong căn phòng!</div>
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
<button onclick="turn(-0.25)">↶ Quay trái</button>
<button onclick="turn(0.25)">↷ Quay phải</button>
<button onclick="interact()">🔎 Tương tác (E)</button>
</div>
<div id="modal"><div class="box">
<h2 id="ptitle">Mật mã</h2>
<p id="ptext"></p>
<input id="answer" placeholder="Nhập đáp án">
<button onclick="submitAnswer()">Xác nhận</button>
<button onclick="closeModal()">Đóng</button>
</div></div>
<div id="start"><div>
<h1>🚪 THOÁT KHỎI CĂN PHÒNG</h1>
<p>Bạn tỉnh dậy trong một căn phòng xa lạ.</p>
<p>Hãy tìm manh mối, giải mật mã và mở cửa!</p>
<button onclick="startGame()">BẮT ĐẦU CHƠI</button>
</div></div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
let scene,camera,renderer,yaw=0,started=false;
let objects=[],inventory=[],drawerOpen=false,chestOpen=false,won=false;
let puzzle="";

function material(c){return new THREE.MeshStandardMaterial({color:c,roughness:.8})}
scene=new THREE.Scene();
scene.background=new THREE.Color(0x8296a1);
scene.fog=new THREE.Fog(0x8296a1,12,30);

camera=new THREE.PerspectiveCamera(75,innerWidth/innerHeight,.1,100);
camera.position.set(0,1.65,4.5);
camera.rotation.order="YXZ";

renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setSize(innerWidth,innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled=true;
document.body.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xe0efff,0x59452f,2));
let light=new THREE.DirectionalLight(0xffe1b5,2.5);
light.position.set(-3,8,4);scene.add(light);

function cube(name,x,y,z,sx,sy,sz,color,action=null){
 let m=new THREE.Mesh(new THREE.BoxGeometry(sx,sy,sz),material(color));
 m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;scene.add(m);
 if(name)objects.push({name,mesh:m,action});
 return m;
}

// Phòng
cube(null,0,-.15,0,12,.3,14,0x665548);
cube(null,0,3,-7,12,6,.25,0xc7b99f);
cube(null,-6,3,0,.25,6,14,0xb5a48e);
cube(null,6,3,0,.25,6,14,0xb5a48e);
cube(null,0,6,0,12,.25,14,0x393b46);
cube(null,0,3,7,12,6,.25,0xb5a48e);

// Cửa
let door=cube("Cửa",0,1.8,-6.8,1.8,3.6,.18,0x71482e,doorAction);
cube(null,-3.2,3,-6.8,1.5,1.4,.12,0x39576b);
cube(null,-3.2,3,-6.7,.08,1.5,.08,0xd8b66a);
cube(null,-3.2,3,-6.7,1.6,.08,.08,0xd8b66a);

// Bàn và ngăn kéo
cube(null,2,1,-1.5,2.5,.18,1.2,0x74482d);
for(let x of [1,3])for(let z of [-1.9,-1.1])
 cube(null,x,.45,z,.13,.9,.13,0x493020);

let drawer=cube("Ngăn kéo",2,1,-.85,1,.4,.15,0x493020,drawerAction);
cube(null,2,1,-.75,.16,.07,.04,0xd9b45c);

// Hộp bí mật
let chest=cube("Hộp bí mật",2,1.4,-1.5,.8,.5,.7,0x244259,chestAction);
cube(null,2,1.4,-1.12,.2,.12,.06,0xe0bb59);

// Kệ sách
cube(null,-4,1.4,-2,1.5,2.8,.5,0x67412b);
for(let y of [.5,1.3,2.1])cube(null,-4,y,-1.72,1.4,.08,.1,0x35251d);
for(let i=0;i<10;i++){
 let colors=[0x9d4944,0x47735a,0x3e5381,0xc19b52];
 cube(null,-4.5+(i%5)*.23,.7+Math.floor(i/5)*.8,-1.65,
 .16,.35+(i%3)*.12,.16,colors[i%4]);
}

// Đồng hồ có manh mối
cube("Đồng hồ",-2.4,3.5,-6.7,.8,.8,.12,0xf3e5c7,
 ()=>say("Đồng hồ chỉ 8 giờ. Hãy ghi nhớ số 8."));
cube(null,-2.4,3.5,-6.6,.04,.35,.03,0x30261e);
cube(null,-2.4,3.5,-6.6,.28,.04,.03,0x30261e);

// Giấy ghi số 3
cube("Tờ giấy",-1,1,1,.5,.04,.4,0xf6e9ba,
 ()=>say("Mảnh giấy ghi: SỐ ĐẦU TIÊN LÀ 3."));

// Đèn trần
cube(null,0,5.7,0,1.2,.12,1.2,0xe8cf91);
let lamp=new THREE.PointLight(0xffd99a,25,15);
lamp.position.set(0,4.8,0);scene.add(lamp);

// Chậu cây
cube(null,-4,.3,2,.6,.6,.6,0x92543a);
let plant=new THREE.Mesh(new THREE.SphereGeometry(.65,12,10),material(0x3d8748));
plant.position.set(-4,1.1,2);scene.add(plant);

function say(t){document.getElementById("msg").textContent=t}
function startGame(){
 document.getElementById("start").style.display="none";
 started=true;say("Tìm tờ giấy và đồng hồ để khám phá manh mối!");
}
function turn(a){if(started)yaw+=a}
function move(dx,dz){
 if(!started||won)return;
 let fx=Math.sin(yaw),fz=-Math.cos(yaw);
 let rx=Math.cos(yaw),rz=Math.sin(yaw);
 let nx=camera.position.x+(rx*dx+fx*dz)*.55;
 let nz=camera.position.z+(rz*dx+fz*dz)*.55;
 if(nx>-5.4&&nx<5.4&&nz>-6.2&&nz<6.2){
  camera.position.x=nx;camera.position.z=nz;
 }
}
function interact(){
 if(!started)return;
 let best=null,dist=2.8;
 for(let o of objects){
  if(!o.action)continue;
  let d=camera.position.distanceTo(o.mesh.position);
  if(d<dist){best=o;dist=d}
 }
 if(best)best.action();
 else say("Hãy đến gần một đồ vật rồi nhấn tương tác!");
}
function openPuzzle(title,text,type){
 puzzle=type;
 document.getElementById("ptitle").textContent=title;
 document.getElementById("ptext").textContent=text;
 document.getElementById("answer").value="";
 document.getElementById("modal").style.display="flex";
}
function closeModal(){document.getElementById("modal").style.display="none"}
function drawerAction(){
 if(drawerOpen){say("Ngăn kéo đã mở rồi!");return}
 openPuzzle("🔐 MẬT MÃ NGĂN KÉO",
 "Gợi ý: Số đầu tiên trên giấy là 3, đồng hồ là 8. Nhập mã 2 chữ số.","drawer");
}
function chestAction(){
 if(!drawerOpen){say("Hãy giải mã và mở ngăn kéo trước!");return}
 if(chestOpen){say("Bạn đã lấy chìa khóa trong hộp!");return}
 openPuzzle("📦 HỘP BÍ MẬT","Giải phép tính: 6 × 7 = ?","chest");
}
function doorAction(){
 if(!chestOpen){say("Cửa bị khóa! Hãy tìm chìa khóa trong hộp bí mật.");return}
 won=true;
 door.material=material(0x36b879);
 document.getElementById("ptitle").textContent="🎉 CHÚC MỪNG!";
 document.getElementById("ptext").textContent=
 "BẠN ĐÃ THOÁT KHỎI CĂN PHÒNG THÀNH CÔNG!";
 document.getElementById("answer").style.display="none";
 document.getElementById("modal").style.display="flex";
}
function submitAnswer(){
 let a=document.getElementById("answer").value.trim();
 if(puzzle==="drawer"&&a==="38"){
  drawerOpen=true;
  drawer.scale.y=.15;
  inventory.push("Chìa khóa nhỏ");
  document.getElementById("items").textContent="🎒 "+inventory.join(", ");
  say("Đã mở ngăn kéo! Tìm hộp bí mật trên bàn.");
  closeModal();
 }else if(puzzle==="chest"&&a==="42"){
  chestOpen=true;chest.material=material(0xc99b40);
  inventory.push("Chìa khóa cửa");
  document.getElementById("items").textContent="🎒 "+inventory.join(", ");
  say("Đã lấy chìa khóa! Đi đến cửa để thoát.");
  closeModal();
 }else{
  document.getElementById("ptext").textContent="Chưa đúng rồi! Thử lại nhé.";
 }
}
addEventListener("keydown",e=>{
 if(e.key.toLowerCase()==="w"||e.key==="ArrowUp")move(0,1);
 if(e.key.toLowerCase()==="s"||e.key==="ArrowDown")move(0,-1);
 if(e.key.toLowerCase()==="a"||e.key==="ArrowLeft")move(-1,0);
 if(e.key.toLowerCase()==="d"||e.key==="ArrowRight")move(1,0);
 if(e.key.toLowerCase()==="e")interact();
 if(e.key==="Escape")closeModal();
});
addEventListener("resize",()=>{
 camera.aspect=innerWidth/innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
});
function animate(){
 requestAnimationFrame(animate);
 camera.rotation.y=yaw;
 renderer.render(scene,camera);
}
animate();
</script>
</body>
</html>
'''

components.html(GAME_HTML, height=700, scrolling=False)
st.caption("Điều khiển: WASD hoặc các nút mũi tên. Nhấn E để tương tác.")
