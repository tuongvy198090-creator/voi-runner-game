
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Chim Cánh Cụt Vượt Băng 3D", page_icon="🐧", layout="wide")
st.title("🐧 CHIM CÁNH CỤT VƯỢT BĂNG 3D")
st.caption("← → đổi hướng · SPACE nhảy · Đi lấy cá, rồi vượt băng yếu trở về!")

html = r"""
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box}body{margin:0;font-family:Arial;background:#06182d;color:white}
#game{height:740px;position:relative;overflow:hidden;border-radius:16px;background:#72d9f5}
#view{position:absolute;inset:0}canvas{display:block}
#hud{position:absolute;z-index:2;top:10px;left:10px;right:10px;text-align:center;
background:#05213be8;border:2px solid #a3efff;border-radius:15px;padding:12px}
#subject{color:#83f1ff;font-size:13px;font-weight:bold}
#question{font-weight:bold;font-size:18px;margin:7px}
#info{font-size:14px;color:#ffe9a3}
#hint{position:absolute;bottom:105px;left:8px;right:8px;text-align:center;
font-weight:bold;text-shadow:1px 2px 3px #000;z-index:2}
#controls{position:absolute;z-index:3;bottom:12px;left:0;right:0;
display:flex;justify-content:space-between;align-items:center;padding:0 16px}
.grp{display:flex;gap:10px}
button{width:60px;height:60px;border-radius:50%;border:2px solid white;
background:#092b4deF;color:white;font-size:25px;font-weight:bold;touch-action:manipulation}
#jump{width:92px;height:68px;border-radius:18px;background:#ffbd38;color:#17304b;font-size:15px}
#overlay{position:absolute;inset:0;z-index:5;background:#04162bce;display:flex;
align-items:center;justify-content:center;padding:18px}
#panel{width:100%;max-width:440px;background:linear-gradient(145deg,#14638a,#071c3b);
border:3px solid #91ecff;border-radius:24px;text-align:center;padding:24px}
#panel h2{color:#a4f5ff}#panel p{line-height:1.55}
#start{width:auto;height:auto;border-radius:14px;padding:13px 25px;
background:#ffce54;color:#142c40;font-size:18px}
@media(max-width:600px){#game{height:690px}#question{font-size:16px}button{width:55px;height:55px}}
</style></head>
<body>
<div id="game">
<div id="view"></div>
<div id="hud">
<div id="subject">CHUYẾN PHIÊU LƯU 3D</div>
<div id="question">Chim cánh cụt sẵn sàng chưa?</div>
<div id="info">8 hàng băng · 15 giây mỗi câu</div>
</div>
<div id="hint">← → CHỌN HƯỚNG · SPACE ĐỂ NHẢY</div>
<div id="controls">
<div class="grp"><button id="left">◀</button><button id="right">▶</button></div>
<button id="jump">NHẢY</button>
</div>
<div id="overlay"><div id="panel">
<h2>🐧 CHIM CÁNH CỤT VƯỢT BĂNG</h2>
<p>Chặng đi: nhảy vào tảng băng mang đáp án đúng để qua 8 câu hỏi.</p>
<p>🐟 Lấy được xô cá, em sẽ quay về qua những hàng băng yếu.</p>
<p>🧊 Mỗi hàng đường về có 2 băng yếu và 2 băng an toàn. Rơi xuống nước thì quay lại chỗ lấy cá, vị trí băng yếu được đổi.</p>
<p>← → chọn hướng · SPACE nhảy.</p>
<button id="start">BẮT ĐẦU</button>
</div></div>
</div>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
(()=>{
const host=document.getElementById('view');
const questionEl=document.getElementById('question');
const subjectEl=document.getElementById('subject');
const info=document.getElementById('info');
const hint=document.getElementById('hint');
const overlay=document.getElementById('overlay');
const panel=document.getElementById('panel');
if(!window.THREE){questionEl.textContent="Không tải được 3D. Hãy tải lại trang.";return;}

const scene=new THREE.Scene();
scene.background=new THREE.Color(0x77d9f4);
scene.fog=new THREE.Fog(0x77d9f4,45,125);
const camera=new THREE.PerspectiveCamera(65,host.clientWidth/host.clientHeight,.1,300);
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setSize(host.clientWidth,host.clientHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio||1,2));
renderer.shadowMap.enabled=true;
renderer.outputColorSpace=THREE.SRGBColorSpace;
host.appendChild(renderer.domElement);
scene.add(new THREE.HemisphereLight(0xe5fbff,0x214b70,2.2));
const sun=new THREE.DirectionalLight(0xffffff,2.4);
sun.position.set(-8,18,12);sun.castShadow=true;scene.add(sun);

const material=(c,r=.45,m=0)=>new THREE.MeshStandardMaterial({color:c,roughness:r,metalness:m});
const ice=material(0x83def4,.22,.12),topIce=material(0xe0fbff,.18,.08);
const safeIce=material(0x7fe7f5,.2,.12),weakIce=material(0x77b5d0,.35,.08);
const waterMat=material(0x087da9,.23,.2);
const snow=material(0xf0ffff,.65),dark=material(0x172536);
const orange=material(0xffa52e),white=material(0xf7fbff);
function box(parent,w,h,d,mat,x,y,z){
 const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);
 o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;parent.add(o);return o;
}

// Biển băng và hai bờ
const water=new THREE.Mesh(new THREE.PlaneGeometry(180,200),waterMat);
water.rotation.x=-Math.PI/2;water.position.set(0,-.7,-35);scene.add(water);
box(scene,26,1.3,15,snow,0,-.1,15);
box(scene,26,1.3,15,snow,0,-.1,-91);
box(scene,26,.25,15,white,0,.65,15);
box(scene,26,.25,15,white,0,.65,-91);
for(let i=0;i<65;i++){
 let x=(Math.random()-.5)*48,z=10-Math.random()*110,s=.3+Math.random()*.9;
 let f=box(scene,s*2,.15,s*1.5,ice,x,-.35,z);
 f.rotation.y=Math.random()*3;
}
// Những tinh thể băng hai bên
for(let side of [-1,1])for(let i=0;i<22;i++){
 const c=new THREE.Mesh(new THREE.OctahedronGeometry(.6+Math.random()*.5),ice);
 c.position.set(side*(7+Math.random()*3,.4+Math.random()*1.4,7-i*5);
 c.scale.y=1.5;c.castShadow=true;scene.add(c);
}

// Chim cánh cụt 3D
const penguin=new THREE.Group();scene.add(penguin);
const body=new THREE.Mesh(new THREE.SphereGeometry(.62,24,20),dark);
body.scale.set(.83,1.25,.75);body.position.y=1.18;body.castShadow=true;penguin.add(body);
const belly=new THREE.Mesh(new THREE.SphereGeometry(.48,24,20),white);
belly.scale.set(.8,1.08,.23);belly.position.set(0,1.12,-.39);penguin.add(belly);
const head=new THREE.Mesh(new THREE.SphereGeometry(.43,24,20),dark);
head.position.set(0,2.13,0);head.castShadow=true;penguin.add(head);
const face=new THREE.Mesh(new THREE.SphereGeometry(.3,20,16),white);
face.scale.set(1,.8,.25);face.position.set(0,2.08,-.32);penguin.add(face);
for(let x of [-.16,.16]){
 const eye=new THREE.Mesh(new THREE.SphereGeometry(.055,12,12),material(0x050505,.2));
 eye.position.set(x,2.18,-.405);penguin.add(eye);
}
const beak=new THREE.Mesh(new THREE.ConeGeometry(.13,.28,5),orange);
beak.rotation.x=-Math.PI/2;beak.position.set(0,1.99,-.51);penguin.add(beak);
const wings=[];
for(let s of [-1,1]){
 const w=new THREE.Mesh(new THREE.SphereGeometry(.2,16,12),dark);
 w.scale.set(.65,1.5,.4);w.position.set(s*.51,1.25,0);penguin.add(w);wings.push(w);
 const foot=new THREE.Mesh(new THREE.BoxGeometry(.3,.12,.38),orange);
 foot.position.set(s*.23,.28,-.12);penguin.add(foot);
}

// Xô cá đeo phía sau lưng
const bucket=new THREE.Group();penguin.add(bucket);
const bucketMat=material(0x5686a4,.35,.3);
const bucketBody=new THREE.Mesh(new THREE.CylinderGeometry(.22,.17,.32,14),bucketMat);
bucketBody.position.set(0,.8,.72);bucket.add(bucketBody);
const rim=new THREE.Mesh(new THREE.TorusGeometry(.21,.035,8,18),white);
rim.rotation.x=Math.PI/2;rim.position.set(0,.97,.72);bucket.add(rim);
for(let i=0;i<3;i++){
 const fish=new THREE.Mesh(new THREE.SphereGeometry(.07,10,8),orange);
 fish.scale.set(1.5,.5,.5);fish.position.set((i-1)*.1,.96,.72);bucket.add(fish);
}
bucket.visible=false;

// Câu hỏi lớp 8
const bank=[
 {s:"TOÁN ĐẠI SỐ",q:"(x + 2)(x - 2) bằng gì?",a:["x² + 4","x² - 4","x² - 2","2x - 4"],c:1},
 {s:"TOÁN HÌNH",q:"Tổng góc trong tứ giác bằng bao nhiêu?",a:["180°","270°","360°","90°"],c:2},
 {s:"TIẾNG ANH",q:"She ___ to school every day.",a:["go","goes","going","gone"],c:1},
 {s:"VẬT LÝ",q:"Công thức khối lượng riêng là gì?",a:["D=m/V","D=V/m","D=m×V","D=m+V"],c:0},
 {s:"HÓA HỌC",q:"Kí hiệu hóa học của oxi là gì?",a:["Ox","O","Oi","O₂⁻"],c:1},
 {s:"SINH HỌC",q:"Bộ phận nào chủ yếu hút nước cho cây?",a:["Lá","Hoa","Rễ","Quả"],c:2},
 {s:"LỊCH SỬ",q:"Ngô Quyền chiến thắng quân Nam Hán năm nào?",a:["938","981","1009","1077"],c:0},
 {s:"ĐỊA LÝ",q:"Việt Nam thuộc châu lục nào?",a:["Châu Âu","Châu Á","Châu Phi","Châu Mỹ"],c:1}
];
const lanes=[-3.75,-1.25,1.25,3.75],rows=[];
const startZ=8,step=-10;

function labelSprite(text){
 const c=document.createElement('canvas');c.width=512;c.height=180;
 const ctx=c.getContext('2d');
 ctx.fillStyle='rgba(3,31,57,.94)';ctx.beginPath();ctx.roundRect(8,8,496,164,22);ctx.fill();
 ctx.strokeStyle='#b5f5ff';ctx.lineWidth=6;ctx.stroke();
 ctx.fillStyle='white';ctx.textAlign='center';ctx.textBaseline='middle';
 let words=text.split(' '),lines=[],line='';
 ctx.font='bold 35px Arial';
 for(const word of words){
  const t=line?line+' '+word:word;
  if(ctx.measureText(t).width>450&&line){lines.push(line);line=word;}else line=t;
 }
 if(line)lines.push(line);lines=lines.slice(0,3);
 const sy=lines.length===1?90:lines.length===2?65:45;
 lines.forEach((t,i)=>ctx.fillText(t,256,sy+i*43));
 const tex=new THREE.CanvasTexture(c);tex.colorSpace=THREE.SRGBColorSpace;
 const sp=new THREE.Sprite(new THREE.SpriteMaterial({map:tex,transparent:true}));
 sp.scale.set(2.5,.88,1);return sp;
}
function shuffledQuestion(q){
 const correct=q.a[q.c],a=q.a.slice();
 for(let i=a.length-1;i>0;i--){let j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}
 return {...q,a,c:a.indexOf(correct)};
}
function buildRows(){
 rows.forEach(r=>scene.remove(r.group));rows.length=0;
 for(let r=0;r<8;r++){
  const z=startZ+step*(r+1),g=new THREE.Group();scene.add(g);
  const platforms=[],labels=[];
  for(let l=0;l<4;l++){
   box(g,2.15,.55,3.7,ice,lanes[l],.05,z);
   box(g,2,.14,3.5,topIce,lanes[l],.39,z);
   const label=labelSprite("?");
   label.position.set(lanes[l],1.65,z);g.add(label);
   labels.push(label);platforms.push(g.children[g.children.length-2]);
  }
  const wall=new THREE.Group();g.add(wall);
  box(wall,10.7,.28,.32,ice,0,1.1,z-4.1);
  box(wall,.3,1.4,.4,safeIce,-5.2,.6,z-4.1);
  box(wall,.3,1.4,.4,safeIce,5.2,.6,z-4.1);
  rows.push({z,g,platforms,labels,wall,lowered:false,weak:[]});
 }
}
buildRows();

let phase='start',current=0,lane=0,jumping=false,locked=false,run=false;
let timeLeft=15,jumpT=0,jumpFrom=new THREE.Vector3(),jumpTo=new THREE.Vector3();
let lastTime=performance.now(),lastSecond=performance.now(),token=0;
let returnIndex=7,returnStartZ=-72;

function setHint(t){hint.textContent=t;}
function hud(){
 if(phase==='out'){
  subjectEl.textContent=bank[current].s;
  questionEl.textContent=bank[current].q;
  info.textContent=`Câu ${current+1}/8 · Còn ${Math.max(0,Math.ceil(timeLeft))} giây`;
 }else if(phase==='return'){
  subjectEl.textContent='CHẶNG VỀ · MANG XÔ CÁ VỀ BỜ';
  questionEl.textContent='Chọn băng an toàn để nhảy về!';
  info.textContent=`Hàng băng ${8-returnIndex}/8 · Cẩn thận: mỗi hàng có 2 băng yếu!`;
 }else if(phase==='fish'){
  subjectEl.textContent='ĐÃ LẤY ĐƯỢC XÔ CÁ!';
  questionEl.textContent='Bắt đầu vượt các tảng băng yếu để trở về.';
  info.textContent='Mỗi hàng có 2 băng yếu · Vị trí thay đổi khi chơi lại chặng về.';
 }
}
function visuals(){
 rows.forEach((r,ri)=>r.platforms.forEach((p,i)=>{
  if(phase==='return'){
   p.material=r.weak.includes(i)?weakIce:safeIce;
  }else p.material=ice;
  p.scale.y=(ri===current&&i===lane&&phase==='out')?.1+1:1;
  if(ri===current&&i===lane&&phase==='out')p.material=material(0xffd44f,.2,.1);
 }));
}
function show(title,text,button,fn){
 overlay.style.display='flex';panel.innerHTML='';
 const h=document.createElement('h2');h.textContent=title;
 const p=document.createElement('p');p.textContent=text;
 const b=document.createElement('button');b.id='start';b.textContent=button;b.onclick=fn;
 panel.append(h,p,b);
}
function makeReturnWeak(){
 rows.forEach(r=>{
  const choices=[0,1,2,3];
  for(let i=3;i>0;i--){const j=Math.floor(Math.random()*(i+1));[choices[i],choices[j]]=[choices[j],choices[i]];}
  r.weak=choices.slice(0,2);
  r.lowered=false;r.wall.visible=true;r.wall.position.y=0;
 });
}
function resetWorld(){
 token++;phase='out';current=0;lane=0;jumping=false;locked=false;run=true;
 timeLeft=15;bucket.visible=false;
 const qs=bank.map(shuffledQuestion);
 qs.forEach((q,i)=>{
  rows[i].labels.forEach((sp,j)=>{
   rows[i].g.remove(sp);sp.material.map.dispose();sp.material.dispose();
   const lab=labelSprite(String.fromCharCode(65+j)+'. '+q.a[j]);
   lab.position.set(lanes[j],1.65,rows[i].z);rows[i].g.add(lab);rows[i].labels[j]=lab;
  });
  rows[i].correct=q.c;rows[i].q=q;
 });
 rows.forEach(r=>{r.lowered=false;r.wall.visible=true;r.wall.position.y=0;});
 penguin.position.set(lanes[0],.7,18);penguin.rotation.y=0;
 camera.position.set(0,5.5,26);
 lastSecond=performance.now();hud();visuals();
 overlay.style.display='none';setHint('← → CHỌN ĐÁP ÁN · SPACE ĐỂ NHẢY');
}
function beginReturn(){
 phase='return';run=true;locked=false;jumping=false;
 bucket.visible=true;returnIndex=7;lane=0;
 makeReturnWeak();
 penguin.position.set(lanes[0],.7,rows[7].z);
 penguin.rotation.y=Math.PI;
 timeLeft=15;hud();visuals();
 setHint('ĐƯỜNG VỀ: 2 BĂNG YẾU MỖI HÀNG! ← → RỒI SPACE');
}
function move(d){
 if(!run||jumping||locked)return;
 lane=Math.max(0,Math.min(3,lane+d));visuals();
}
function jump(){
 if(!run||jumping||locked)return;
 jumping=true;locked=true;jumpT=0;jumpFrom.copy(penguin.position);
 if(phase==='out'){
  jumpTo.set(lanes[lane],.7,rows[current].z);
 }else{
  const nextZ=returnIndex>0?rows[returnIndex-1].z:-83;
  jumpTo.set(lanes[lane],.7,nextZ);
 }
 setHint('🐧 ĐANG NHẢY...');
}
function fallAndRetry(){
 run=false;jumping=false;penguin.position.y=-1.2;
 setHint('💦 BĂNG VỠ! RƠI XUỐNG NƯỚC!');
 const my=token;
 setTimeout(()=>{
  if(my!==token)return;
  // Quay lại bờ lấy cá, vẫn giữ chặng về; tạo lại vị trí băng yếu
  makeReturnWeak();phase='fish';run=false;locked=false;
  penguin.position.set(0,.7,-87);penguin.rotation.y=Math.PI;bucket.visible=true;
  hud();
  show('💦 RƠI XUỐNG NƯỚC!','Em vẫn giữ được tiến trình lấy cá. Hãy quay lại chỗ lấy cá và thử chặng đường về lần nữa. Vị trí băng yếu đã thay đổi!','THỬ LẠI ĐƯỜNG VỀ',()=>{
   token++;phase='return';run=true;current=0;lane=0;returnIndex=7;
   penguin.position.set(lanes[0],.7,rows[7].z);penguin.rotation.y=Math.PI;
   timeLeft=15;locked=false;hud();visuals();overlay.style.display='none';
   setHint('ĐƯỜNG VỀ: CHỌN BĂNG AN TOÀN RỒI NHẤN SPACE');
  });
 },700);
}
function landed(){
 jumping=false;
 if(phase==='out'){
  const row=rows[current],q=row.q;
  if(lane===q.c){
   setHint('✅ ĐÚNG! VÁCH CHẮN ĐANG HẠ!');
   const my=token,start=performance.now();
   function lower(now){
    if(my!==token)return;
    const t=Math.min(1,(now-start)/450);
    row.wall.position.y=-2*t;
    if(t<1)requestAnimationFrame(lower);
    else{
     row.wall.visible=false;current++;locked=false;timeLeft=15;lastSecond=performance.now();
     if(current>=8){
      phase='fish';run=false;bucket.visible=true;
      penguin.position.set(0,.7,-87);penguin.rotation.y=Math.PI;
      hud();show('🐟 ĐÃ LẤY ĐƯỢC XÔ CÁ!','Giờ hãy vượt đường băng yếu để mang cá về bờ xuất phát. Mỗi hàng có 2 băng yếu!','BẮT ĐẦU ĐƯỜNG VỀ',beginReturn);
     }else{hud();visuals();setHint('ĐÚNG RỒI! Chọn tảng băng cho câu tiếp theo.');}
    }
   }
   requestAnimationFrame(lower);
  }else fallAndRetry();
 }else if(phase==='return'){
  const row=rows[returnIndex];
  if(row.weak.includes(lane)){
   row.platforms[lane].material=material(0x6b8796);
   setTimeout(fallAndRetry,250);
  }else{
   row.platforms[lane].material=material(0x64f5c4,.2,.1);
   returnIndex--;
   if(returnIndex<0){
    phase='win';run=false;bucket.visible=true;
    show('🏆 CHIẾN THẮNG!','Chim cánh cụt đã mang xô cá về bờ an toàn. Em đã vượt qua cả hai chặng!','CHƠI LẠI TỪ ĐẦU',resetWorld);
    setHint('🎉 HOÀN THÀNH NHIỆM VỤ!');
   }else{
    locked=false;lane=lane;hud();visuals();
    setHint('🧊 An toàn! Chọn một tảng băng ở hàng kế tiếp rồi nhấn SPACE.');
   }
  }
 }
}
function onKey(e){
 if(['ArrowLeft','ArrowRight','ArrowUp','Space'].includes(e.code))e.preventDefault();
 if(e.code==='ArrowLeft'||e.code==='KeyA')move(-1);
 if(e.code==='ArrowRight'||e.code==='KeyD')move(1);
 if(e.code==='Space'||e.code==='ArrowUp'||e.code==='KeyW')jump();
}
window.addEventListener('keydown',onKey);
document.getElementById('left').onclick=()=>move(-1);
document.getElementById('right').onclick=()=>move(1);
document.getElementById('jump').onclick=jump;
document.getElementById('start').onclick=resetWorld;

function animate(now){
 requestAnimationFrame(animate);
 const dt=Math.min((now-lastTime)/1000,.04);lastTime=now;
 if(run&&phase==='out'&&!jumping&&!locked&&now-lastSecond>=1000){
  timeLeft--;lastSecond=now;hud();
  if(timeLeft<=0)fallAndRetry();
 }
 if(jumping){
  jumpT+=dt/.8;const t=Math.min(1,jumpT);
  penguin.position.x=jumpFrom.x+(jumpTo.x-jumpFrom.x)*t;
  penguin.position.z=jumpFrom.z+(jumpTo.z-jumpFrom.z)*t;
  penguin.position.y=.7+Math.sin(t*Math.PI)*2.5;
  wings.forEach((w,i)=>w.rotation.z=Math.sin(now*.025)*(i?1:-1)*.5);
  if(t>=1){penguin.position.copy(jumpTo);landed();}
 }else if(run){
  wings.forEach((w,i)=>w.rotation.z=Math.sin(now*.008)*(i?1:-1)*.1);
 }
 camera.position.x+=(penguin.position.x-camera.position.x)*.08;
 camera.position.y+=(5.2-camera.position.y)*.05;
 camera.position.z+=((penguin.position.z+7.5)-camera.position.z)*.08;
 camera.lookAt(penguin.position.x*.3,1.1,penguin.position.z-6);
 renderer.render(scene,camera);
}
window.addEventListener('resize',()=>{
 camera.aspect=host.clientWidth/host.clientHeight;
 camera.updateProjectionMatrix();renderer.setSize(host.clientWidth,host.clientHeight);
});
hud();requestAnimationFrame(animate);
})();
</script></body></html>
"""

components.html(html, height=755, scrolling=False)
