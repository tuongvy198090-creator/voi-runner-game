
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Vượt Băng Lấy Cá 3D", page_icon="🐧", layout="wide")

GAME = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}
body{margin:0;font-family:Arial,sans-serif;background:#061b38;color:white}
#wrap{height:720px;position:relative;overflow:hidden;background:#70d7f3}
#game{width:100%;height:100%;display:block}
#hud{position:absolute;top:12px;left:12px;right:12px;display:flex;justify-content:space-between;gap:8px;pointer-events:none}
.pill{padding:10px 14px;border-radius:15px;background:#073b62eF;border:1px solid #a7f5ff;font-weight:bold;font-size:14px;box-shadow:0 3px 12px #00334c55}
#question{display:none;position:absolute;top:65px;left:50%;transform:translateX(-50%);width:min(94%,600px);background:#07365eee;border:2px solid #a8f4ff;border-radius:18px;padding:12px;text-align:center;box-shadow:0 0 20px #a8f4ff66}
#qtext{font-size:18px;font-weight:bold;line-height:1.4}
#answers{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px;margin-top:10px}
.answer{padding:9px 3px;border-radius:10px;background:linear-gradient(#efffff,#a9e9ff);color:#07365e;font-size:12px;font-weight:bold;overflow-wrap:anywhere}
#message{display:none;position:absolute;bottom:91px;left:50%;transform:translateX(-50%);width:min(92%,520px);background:#07365eee;padding:11px;border-radius:13px;text-align:center;font-weight:bold;border:1px solid #a8f4ff}
#overlay{position:absolute;inset:0;z-index:10;display:flex;align-items:center;justify-content:center;padding:16px;background:linear-gradient(150deg,#063c64ed,#078ea5ed)}
.card{width:min(94%,500px);text-align:center;padding:26px 23px;border-radius:26px;background:linear-gradient(145deg,#092e51,#075a79);border:2px solid #b7faff;box-shadow:0 0 35px #8cf5ff77}
.card h1{font-size:clamp(25px,5vw,38px);color:#b9faff;text-shadow:0 0 14px #2ad5ff;margin:10px 0}
.card p{line-height:1.65}
#start{width:100%;padding:16px;background:linear-gradient(90deg,#42f5c8,#b1ffff);color:#053653;font-size:21px;margin-top:10px;cursor:pointer;border:0;border-radius:14px;font-weight:bold}
#start:hover{filter:brightness(1.12);transform:scale(1.02)}
#controls{position:absolute;bottom:12px;left:50%;transform:translateX(-50%);display:flex;gap:9px;align-items:center}
.ctrl{width:50px;height:48px;border:1px solid #d0fbff;border-radius:14px;background:#073c62eF;color:white;font-size:22px;cursor:pointer;touch-action:manipulation}
#jump{width:85px;background:linear-gradient(135deg,#00bfa5,#59e6e9);font-size:14px;font-weight:bold}
#hint{position:absolute;bottom:17px;right:10px;background:#f0ffffd9;color:#073653;padding:7px 9px;border-radius:9px;font-size:11px}
@media(max-width:520px){#wrap{height:700px}#qtext{font-size:15px}.answer{font-size:10px;padding:8px 2px}.ctrl{width:44px;height:44px}#hint{display:none}}
</style>
</head>
<body>
<div id="wrap">
 <canvas id="game"></canvas>
 <div id="hud">
  <div class="pill" id="stage">❄️ THẾ GIỚI BĂNG TUYẾT</div>
  <div class="pill" id="progress">Sẵn sàng!</div>
 </div>
 <div id="question">
  <div id="qtext"></div>
  <div id="answers"></div>
 </div>
 <div id="message"></div>
 <div id="controls">
  <button class="ctrl" id="left">◀</button>
  <button class="ctrl" id="jump">NHẢY</button>
  <button class="ctrl" id="right">▶</button>
 </div>
 <div id="hint">← → chọn đáp án · Space nhảy</div>
 <div id="overlay">
  <div class="card">
   <div style="font-size:55px">🐧 ❄️ 🐟</div>
   <h1>VƯỢT BĂNG LẤY CÁ</h1>
   <p>Chào mừng nhà thám hiểm!</p>
   <p>Vượt qua 5 câu hỏi, sang bờ bên kia lấy xô cá rồi tìm đường trở về qua những tảng băng bí ẩn.</p>
   <button id="start">▶ BẮT ĐẦU TRÒ CHƠI</button>
   <p style="font-size:12px;color:#b8f7ff">Hãy quan sát đáp án và lựa chọn thật cẩn thận nhé!</p>
  </div>
 </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
(function(){
"use strict";
const $=id=>document.getElementById(id);
const canvas=$("game");
let scene,camera,renderer,penguin,world,bucket;
let started=false,phase="menu",busy=false,falling=false,jumping=false;
let fallTime=0,jumpTime=0,lane=1,row=0,step=0,fallCallback=null;
let rows=[],returnTiles=[],messageTimer;
const questions=[
 {q:"Câu 1: 3² + 4 bằng bao nhiêu?",a:["7","9","13","16"],c:2},
 {q:"Câu 2: Phân tích x² − 9 thành nhân tử.",a:["(x−3)²","(x−3)(x+3)","x(x−9)","(x+3)²"],c:1},
 {q:"Câu 3: Hình chữ nhật có bao nhiêu góc vuông?",a:["1","2","3","4"],c:3},
 {q:"Câu 4: 25% của 200 bằng bao nhiêu?",a:["25","40","50","75"],c:2},
 {q:"Câu 5: Đơn thức 3x²y có bậc là bao nhiêu?",a:["2","3","4","6"],c:1}
];
function msg(s,ms=1800){
 $("message").textContent=s;$("message").style.display="block";
 clearTimeout(messageTimer);
 if(ms)messageTimer=setTimeout(()=>$("message").style.display="none",ms);
}
function hud(a,b){$("stage").textContent=a;$("progress").textContent=b}
function mat(color,roughness=.45,metalness=.05){
 return new THREE.MeshStandardMaterial({color,roughness,metalness});
}
function box(parent,w,h,d,material,x,y,z){
 const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),material);
 m.position.set(x,y,z);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;
}
function ball(parent,material,x,y,z,sx,sy,sz){
 const m=new THREE.Mesh(new THREE.SphereGeometry(1,24,18),material);
 m.position.set(x,y,z);m.scale.set(sx,sy,sz);m.castShadow=true;parent.add(m);return m;
}
function init(){
 if(!window.THREE)throw Error("Không tải được thư viện 3D. Em kiểm tra kết nối Internet nhé.");
 scene=new THREE.Scene();
 scene.background=new THREE.Color(0x8cdef8);
 scene.fog=new THREE.Fog(0x9adff5,35,85);
 camera=new THREE.PerspectiveCamera(58,1,.1,150);
 renderer=new THREE.WebGLRenderer({canvas,antialias:true});
 renderer.setPixelRatio(Math.min(devicePixelRatio||1,2));
 renderer.shadowMap.enabled=true;
 renderer.shadowMap.type=THREE.PCFSoftShadowMap;
 renderer.outputColorSpace=THREE.SRGBColorSpace;
 renderer.toneMapping=THREE.ACESFilmicToneMapping;
 renderer.toneMappingExposure=1.15;
 scene.add(new THREE.HemisphereLight(0xe5faff,0x527b9c,2.2));
 const sun=new THREE.DirectionalLight(0xffffff,3.2);
 sun.position.set(-8,15,8);sun.castShadow=true;scene.add(sun);
 const glow=new THREE.PointLight(0x64e5ff,18,32);
 glow.position.set(0,5,-15);scene.add(glow);

 // Biển xanh ngọc
 const water=new THREE.Mesh(
  new THREE.PlaneGeometry(140,140),
  new THREE.MeshStandardMaterial({color:0x087fac,roughness:.22,metalness:.22})
 );
 water.rotation.x=-Math.PI/2;water.position.set(0,-.85,-20);scene.add(water);
 // Những vệt sóng phản chiếu
 for(let i=0;i<110;i++){
  const m=new THREE.Mesh(
   new THREE.BoxGeometry(.3+Math.random()*1.6,.018,.025),
   new THREE.MeshBasicMaterial({color:i%3?0x70e9fa:0xd5ffff,transparent:true,opacity:.25+Math.random()*.5})
  );
  m.position.set((Math.random()-.5)*34,-.81,-Math.random()*68);
  m.userData.phase=Math.random()*6.28;scene.add(m);
  waves.push(m);
 }
 // Núi tuyết phía xa
 for(let i=0;i<13;i++){
  const x=(i-6)*7.5;
  const h=5+Math.random()*9;
  const mountain=new THREE.Mesh(
   new THREE.ConeGeometry(4+Math.random()*2,h,5),
   mat(i%2?0x80b9d5:0x699fca,.85)
  );
  mountain.position.set(x,h/2-1,-48-Math.random()*7);
  mountain.rotation.y=Math.random();scene.add(mountain);
  const snow=new THREE.Mesh(
   new THREE.ConeGeometry(1.8+Math.random()*1.2,h*.42,5),
   mat(0xf2ffff,.8)
  );
  snow.position.set(x,h*.72-1,-48-Math.random()*2);
  snow.rotation.y=mountain.rotation.y;scene.add(snow);
 }
 // Mặt trời
 const sunBall=new THREE.Mesh(new THREE.SphereGeometry(2.2,24,18),new THREE.MeshBasicMaterial({color:0xfff5cc}));
 sunBall.position.set(-15,14,-40);scene.add(sunBall);
 const halo=new THREE.Mesh(new THREE.SphereGeometry(3.1,24,18),new THREE.MeshBasicMaterial({color:0xb6f8ff,transparent:true,opacity:.18}));
 halo.position.copy(sunBall.position);scene.add(halo);

 world=new THREE.Group();scene.add(world);
 // Hai bờ tuyết
 for(const z of [3,-29]){
  const bank=box(world,14,.75,6,mat(0xf1ffff,.85),0,-.13,z);
  bank.receiveShadow=true;
  for(let i=0;i<10;i++){
   const ice=new THREE.Mesh(new THREE.ConeGeometry(.25+Math.random()*.25,.7+Math.random()*.8,5),mat(0x9cecff,.25,.15));
   ice.position.set((Math.random()-.5)*12,.2,z+(Math.random()-.5)*4);
   world.add(ice);
  }
 }
 // Chim cánh cụt hoạt hình, nhìn lưng
 penguin=new THREE.Group();
 const black=mat(0x182e48,.72),white=mat(0xf7ffff,.55),orange=mat(0xffa52f,.4);
 ball(penguin,black,0,.05,0,.57,.72,.45);
 ball(penguin,white,0,-.1,-.29,.38,.49,.16);
 ball(penguin,black,0,.72,0,.44,.43,.4);
 // Mặt hướng về phía trước, mỏ và mắt
 const beak=new THREE.Mesh(new THREE.ConeGeometry(.13,.23,12),orange);
 beak.rotation.x=-Math.PI/2;beak.position.set(0,.65,-.43);penguin.add(beak);
 ball(penguin,mat(0xffffff),-.16,.76,-.33,.065,.07,.035);
 ball(penguin,mat(0xffffff),.16,.76,-.33,.065,.07,.035);
 ball(penguin,mat(0x14253b),-.16,.76,-.36,.03,.04,.018);
 ball(penguin,mat(0x14253b),.16,.76,-.36,.03,.04,.018);
 const wings=[
  ball(penguin,black,-.53,.03,0,.15,.4,.2),
  ball(penguin,black,.53,.03,0,.15,.4,.2)
 ];
 penguin.userData.wings=wings;
 ball(penguin,orange,-.23,-.62,-.03,.18,.08,.22);
 ball(penguin,orange,.23,-.62,-.03,.18,.08,.22);
 penguin.position.set(0,.55,2);scene.add(penguin);

 // Bờ xa có xô cá
 bucket=new THREE.Group();
 const silver=mat(0xc7e8f5,.25,.65);
 const body=new THREE.Mesh(new THREE.CylinderGeometry(.4,.29,.65,24,1,true),silver);
 body.position.y=.35;bucket.add(body);
 const rim=new THREE.Mesh(new THREE.TorusGeometry(.39,.05,10,28),silver);
 rim.position.y=.69;bucket.add(rim);
 for(let i=0;i<5;i++){
  const fish=ball(bucket,mat(i%2?0xffbd4a:0xffe5a1),Math.sin(i*2)*.19,.68+(i%2)*.08,Math.cos(i*2)*.15,.12,.07,.2);
  fish.rotation.y=i*.7;
 }
 bucket.position.set(0,.3,-29);bucket.visible=false;world.add(bucket);

 makeRows();resize();window.addEventListener("resize",resize);animate();
}
const waves=[];
function makeIce(x,z,weak=false){
 const g=new THREE.Group();
 const side=mat(weak?0x77c5da:0x8adcf4,.2,.18);
 const top=mat(weak?0xc3edf5:0xf1ffff,.22,.05);
 box(g,2.25,.34,2,side,0,0,0);
 box(g,2.08,.035,1.82,top,0,.19,0);
 // Khối băng trong ở cạnh
 const crystal= new THREE.Mesh(
  new THREE.BoxGeometry(2.2,.13,1.96),
  new THREE.MeshStandardMaterial({color:0x80e8ff,transparent:true,opacity:.24,metalness:.2,roughness:.12})
 );
 crystal.position.y=-.08;g.add(crystal);
 if(weak){
  const crackMat=new THREE.MeshBasicMaterial({color:0x4a8fa9});
  for(let i=0;i<4;i++){
   const c=box(g,.025,.012,.72,crackMat,(i-1.5)*.24,.215,0);
   c.rotation.y=(i-1.5)*.22;
  }
 }
 g.position.set(x,-.3,z);world.add(g);
 g.userData.weak=weak;g.userData.broken=false;
 return g;
}
function label(text,x,z){
 const c=document.createElement("canvas");c.width=512;c.height=150;
 const ctx=c.getContext("2d");
 const grad=ctx.createLinearGradient(0,0,512,150);
 grad.addColorStop(0,"#f4ffff");grad.addColorStop(1,"#a6eaff");
 ctx.fillStyle=grad;ctx.fillRect(0,0,512,150);
 ctx.strokeStyle="#45b8e0";ctx.lineWidth=8;ctx.strokeRect(4,4,504,142);
 ctx.fillStyle="#07385a";ctx.textAlign="center";ctx.textBaseline="middle";
 ctx.font="bold 27px Arial";
 const words=String(text).split(" ");let lines=[""];
 for(const w of words){
  let n=lines.length-1,t=(lines[n]+" "+w).trim();
  if(ctx.measureText(t).width>455)lines.push(w);else lines[n]=t;
 }
 lines.slice(0,2).forEach((s,i)=>ctx.fillText(s,256,75+(i-(Math.min(lines.length,2)-1)/2)*35));
 const texture=new THREE.CanvasTexture(c);texture.colorSpace=THREE.SRGBColorSpace;
 const m=new THREE.Mesh(new THREE.PlaneGeometry(2.1,.62),new THREE.MeshBasicMaterial({map:texture,side:THREE.DoubleSide}));
 m.position.set(x,1.2,z);world.add(m);return m;
}
function makeRows(){
 for(let r=0;r<5;r++){
  const z=-r*4.5-2,tiles=[];
  for(let l=0;l<4;l++){
   const x=(l-1.5)*2.65;
   tiles.push(makeIce(x,z));
   label(String.fromCharCode(65+l)+". "+questions[r].a[l],x,z-.25);
  }
  rows.push(tiles);
 }
}
function showQuestion(){
 const q=questions[row];
 $("question").style.display="block";
 $("qtext").textContent=q.q;
 $("answers").innerHTML="";
 q.a.forEach((a,i)=>{
  const d=document.createElement("div");d.className="answer";
  d.textContent=String.fromCharCode(65+i)+". "+a;
  $("answers").appendChild(d);
 });
 hud("🧊 CHẶNG 1: TRẢ LỜI","Câu hỏi "+(row+1)+"/5");
}
function startGame(){
 if(!renderer){
  try{init()}catch(e){msg("Lỗi đồ họa 3D: "+e.message,0);return}
 }
 $("overlay").style.display="none";$("message").style.display="none";
 $("question").style.display="block";
 started=true;phase="outbound";busy=false;falling=false;jumping=false;
 row=0;lane=1;
 penguin.position.set((lane-1.5)*2.65,.55,2);
 camera.position.set(0,5.5,10);camera.lookAt(0,1,-5);
 showQuestion();msg("Chọn đáp án bằng ◀ ▶, rồi nhấn NHẢY!",2400);
}
function move(d){
 if(!started||busy||falling||jumping)return;
 lane=Math.max(0,Math.min(3,lane+d));
 penguin.position.x=(lane-1.5)*2.65;
}
function crack(tile){
 if(!tile)return;
 tile.userData.broken=true;
 tile.traverse(o=>{
  if(o.isMesh&&o.material&&o.material.color)o.material.color.set(0x478ca5);
 });
 tile.rotation.z=.08;
 setTimeout(()=>{tile.position.y=-2.8;tile.rotation.z=.25},160);
}
function fall(callback){
 busy=true;falling=true;fallTime=0;fallCallback=callback;
 jumping=false;
}
function resetStart(){
 falling=false;busy=false;phase="outbound";row=0;lane=1;
 penguin.rotation.x=0;penguin.position.set((lane-1.5)*2.65,.55,2);
 $("question").style.display="block";showQuestion();
 msg("Chim đã trở về xuất phát. Hãy thử lại nhé!");
}
function reachShore(){
 phase="shore";busy=true;$("question").style.display="none";
 bucket.visible=true;penguin.position.set(0,.55,-29);
 hud("🐟 ĐÃ LẤY ĐƯỢC CÁ!","Hoàn thành 5/5");
 msg("Tuyệt vời! Em đã lấy được xô cá!",2000);
 setTimeout(()=>{
  if(phase!=="shore")return;
  startReturn();
 },2100);
}
function startReturn(){
 returnTiles=[];
 const slots=[0,1,2,3].sort(()=>Math.random()-.5);
 for(let i=0;i<4;i++){
  const x=(i-1.5)*2.65,z=-29+i*4.5;
  const weak=i===slots[0]||i===slots[1];
  returnTiles.push(makeIce(x,z,weak));
  label(weak?"⚠ BĂNG YẾU":"BĂNG THƯỜNG",x,z-.25);
 }
 phase="return";busy=false;step=0;lane=1;
 penguin.position.set(0,.55,-31);
 camera.position.set(0,5.5,-22);camera.lookAt(0,1,-28);
 hud("🐟 CHẶNG 2: TRỞ VỀ","Tảng băng 0/4");
 msg("Có 2 tảng băng yếu và 2 tảng chắc. Hãy chọn đường!",2600);
}
function jump(){
 if(!started||busy||falling||jumping)return;
 if(phase==="outbound"){
  const q=questions[row];
  if(lane!==q.c){
   crack(rows[row][lane]);msg("Sai đáp án! Băng vỡ, chim rơi xuống nước!",1400);
   fall(resetStart);return;
  }
  busy=true;jumping=true;jumpTime=0;
  msg("Chính xác! Tảng băng vẫn an toàn! ✔",1000);
  setTimeout(()=>{
   if(phase!=="outbound")return;
   jumping=false;busy=false;row++;
   if(row>=5)reachShore();
   else{lane=1;penguin.position.set((lane-1.5)*2.65,.55,2);showQuestion()}
  },800);
 }else if(phase==="return"){
  const tile=returnTiles[step];
  if(!tile)return;
  penguin.position.x=(lane-1.5)*2.65;
  if(tile.userData.weak){
   crack(tile);msg("Băng yếu nứt rồi! Em rơi xuống nước!",1300);
   fall(resetBucket);
  }else{
   busy=true;jumping=true;jumpTime=0;
   msg("Băng chắc chắn! Tiếp tục nào!",1000);
   setTimeout(()=>{
    jumping=false;busy=false;step++;
    if(step>=4)win();
    else{
     penguin.position.z=returnTiles[step].position.z+1.8;
     hud("🐟 CHẶNG 2: TRỞ VỀ","Tảng băng "+step+"/4");
    }
   },800);
  }
 }
}
function resetBucket(){
 falling=false;busy=false;phase="return";step=0;lane=1;
 penguin.rotation.x=0;penguin.position.set(0,.55,-31);
 camera.position.set(0,5.5,-22);camera.lookAt(0,1,-28);
 hud("🐟 THỬ LẠI ĐƯỜNG VỀ","Tảng băng 0/4");
 msg("Em quay lại bờ lấy cá. Hãy chọn đường khác!",2200);
}
function win(){
 phase="win";busy=true;$("question").style.display="none";
 hud("🏆 CHIẾN THẮNG!","Đã hoàn thành");
 $("overlay").style.display="flex";
 $("overlay").innerHTML='<div class="card"><div style="font-size:62px">🐧 🐟 🏆</div><h1>CHIẾN THẮNG!</h1><p>Em đã vượt qua 5 câu hỏi, lấy được xô cá và trở về an toàn!</p><button id="start" style="width:100%;padding:16px;background:linear-gradient(90deg,#42f5c8,#b1ffff);color:#053653;font-size:21px;margin-top:10px">↻ CHƠI LẠI</button></div>';
 $("start").addEventListener("click",()=>location.reload());
}
function resize(){
 if(!renderer)return;
 const w=canvas.clientWidth||innerWidth,h=canvas.clientHeight||720;
 renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();
}
function animate(){
 requestAnimationFrame(animate);
 if(!renderer)return;
 const t=performance.now()*.001;
 waves.forEach(w=>{w.position.x+=Math.sin(t+w.userData.phase)*.002;w.material.opacity=.25+(.25*Math.sin(t*2+w.userData.phase)+.25)});
 if(penguin){
  if(jumping){
   jumpTime+=.055;
   penguin.position.y=.55+Math.sin(Math.min(1,jumpTime)*Math.PI)*1.3;
   if(jumpTime>=1){jumping=false;penguin.position.y=.55}
  }
  if(falling){
   fallTime+=.04;penguin.position.y=.55-fallTime*fallTime*3;
   penguin.rotation.x=Math.min(1.5,fallTime*1.8);
   if(fallTime>.7){
    falling=false;penguin.rotation.x=0;
    if(fallCallback){const cb=fallCallback;fallCallback=null;cb()}
   }
  }
  const targetX=penguin.position.x*.25;
  camera.position.x+=(targetX-camera.position.x)*.06;
  camera.position.z+=(penguin.position.z+7.5-camera.position.z)*.045;
  camera.position.y+=(5.3-camera.position.y)*.05;
  camera.lookAt(penguin.position.x*.4,1.0,penguin.position.z-5);
  const wings=penguin.userData.wings;
  if(!jumping&&!falling){
   wings[0].rotation.z=Math.sin(t*5)*.1;
   wings[1].rotation.z=-Math.sin(t*5)*.1;
  }
 }
 if(bucket&&bucket.visible)bucket.rotation.y=Math.sin(t)*.12;
 renderer.render(scene,camera);
}
document.addEventListener("keydown",e=>{
 if(["ArrowLeft","ArrowRight","ArrowUp"," ","Enter","a","d","A","D"].includes(e.key))e.preventDefault();
 if(e.key==="ArrowLeft"||e.key==="a"||e.key==="A")move(-1);
 if(e.key==="ArrowRight"||e.key==="d"||e.key==="D")move(1);
 if(e.key===" "||e.key==="ArrowUp"||e.key==="Enter")jump();
});
$("left").addEventListener("click",()=>move(-1));
$("right").addEventListener("click",()=>move(1));
$("jump").addEventListener("click",jump);
$("start").addEventListener("click",startGame);
try{init()}catch(e){msg("Không khởi tạo được 3D: "+e.message,0)}
})();
</script>
</body>
</html>
"""

components.html(GAME, height=730, scrolling=False)
