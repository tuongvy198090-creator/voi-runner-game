
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Giải cứu thế giới</title>
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;font-family:Arial;background:#183d2b;color:white}
canvas{display:block;width:100vw;height:100vh;touch-action:none}
.panel{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#081b1ddd;padding:16px;z-index:5}
.card{width:min(500px,94vw);padding:25px;border:1px solid #b5e5a5;border-radius:22px;background:#19442f;text-align:center;box-shadow:0 12px 50px #0008}
h1{color:#d9ffb0;font-size:clamp(28px,5vw,44px);margin:0 0 12px}
p{line-height:1.5}
input{width:100%;padding:12px;border-radius:10px;font-size:17px;margin:8px 0 14px}
.choices{display:flex;gap:10px;margin:12px 0}
.choices button,.mainbtn{flex:1;padding:12px;border-radius:12px;border:2px solid #a9d9a0;cursor:pointer;font-size:17px}
.choices button{background:#285b42;color:white}
.choices .selected,.mainbtn{background:#d9ffb0;color:#173b29;font-weight:bold}
.mainbtn{width:100%;border:0}
#hud,#hint,#restart{position:fixed;z-index:2;background:#092217d9;border:1px solid #a9d6a0;border-radius:12px;padding:10px}
#hud{top:12px;left:12px;line-height:1.6;pointer-events:none}
#hint{top:12px;left:50%;transform:translateX(-50%);text-align:center;font-size:13px;pointer-events:none}
#restart{right:12px;top:12px;color:white;cursor:pointer}
#joystick{position:fixed;z-index:3;left:22px;bottom:22px;width:150px;height:150px;border-radius:50%;border:3px solid #e7f3e0c9;background:#eaffef26;touch-action:none;user-select:none}
#stick{position:absolute;left:44px;top:44px;width:56px;height:56px;border-radius:50%;background:#91a7ff;border:3px solid #e3e8ff;box-shadow:0 3px 10px #0007;pointer-events:none}
@media(max-width:600px){
#joystick{width:132px;height:132px;left:14px;bottom:14px}
#stick{left:38px;top:38px;width:50px;height:50px}
#hint{top:auto;bottom:12px;left:auto;right:10px;transform:none;max-width:48vw;font-size:11px}
}
</style>
</head>
<body>
<canvas id="game"></canvas>

<div id="hud">
🌟 <b>GIẢI CỨU THẾ GIỚI</b><br>
Ngọc: <span id="gems">0</span>/5<br>
<span id="playerName">Nhà thám hiểm</span>
</div>

<div id="hint">Kéo nút tròn để di chuyển<br>Máy tính: WASD / phím mũi tên</div>
<button id="restart" onclick="location.reload()">Chơi lại ↻</button>

<div class="panel" id="start">
<div class="card">
<h1>GIẢI CỨU<br>THẾ GIỚI</h1>
<p>Khu rừng cổ đang mất đi sức sống. Hãy tìm 5 viên ngọc và đánh thức cây cổ thụ!</p>
<label>Tên nhà thám hiểm</label>
<input id="name" maxlength="18" placeholder="Nhập tên của em...">
<p>Chọn nhân vật</p>
<div class="choices">
<button id="boy" class="selected" onclick="choose('boy')">🧑 Nam</button>
<button id="girl" onclick="choose('girl')">👩 Nữ</button>
</div>
<button class="mainbtn" onclick="begin()">BẮT ĐẦU</button>
</div>
</div>

<div class="panel" id="win" style="display:none">
<div class="card">
<h1>🌳 THẾ GIỚI ĐƯỢC CỨU!</h1>
<p id="winText">BẠN ĐÃ GIẢI CỨU THẾ GIỚI THÀNH CÔNG!</p>
<button class="mainbtn" onclick="location.reload()">CHƠI LẠI</button>
</div>
</div>

<div id="joystick"><div id="stick"></div></div>

<script>
const c=document.getElementById('game'),x=c.getContext('2d');
let W,H,D=1;
function resize(){
D=Math.min(devicePixelRatio||1,2);
W=innerWidth;H=innerHeight;
c.width=W*D;c.height=H*D;
x.setTransform(D,0,0,D,0,0)
}
addEventListener('resize',resize);resize();

let gender='boy',started=false,won=false,keys={},joy={x:0,y:0};
let px=0,pz=0,cx=0,cz=0,gems=0;
const endZ=1450;

function choose(g){
gender=g;
document.getElementById('boy').classList.toggle('selected',g==='boy');
document.getElementById('girl').classList.toggle('selected',g==='girl')
}
function path(z){
return Math.sin(z/180)*115+Math.sin(z/82)*28
}
function rand(a,b){
return Math.abs(Math.sin(a*12.9898+b*78.233)*43758.5453)%1
}

let trees=[];
for(let z=25;z<1550;z+=38){
for(let s of [-1,1]){
let r=rand(z,s);
trees.push({
x:path(z)+s*(105+r*245),
z:z+(r-.5)*25,
k:r,size:.7+r*.8
})
}
}
for(let i=0;i<75;i++){
let z=40+(i*193)%1500;
trees.push({
x:path(z)+(i%2?1:-1)*(175+(i*41)%310),
z,k:(i*.31)%1,size:.7+(i%5)*.2
})
}

const gemsAt=[[-100,260],[115,480],[-120,720],[130,960],[0,1200]];
const taken=[false,false,false,false,false];

function proj(a,b){
let dz=b-cz;
if(dz< -10)return null;
let dep=1/(1+Math.max(0,dz)*.0027);
return {
x:W/2+(a-cx)*dep*1.05,
y:H*.68-dz*.48*dep,
dep
}
}

function tree(a,b,sc,k){
if(sc<.08)return;
let th=42*sc,w=23*sc;
x.fillStyle='#543b27';
x.fillRect(a-w*.22,b-th*.48,w*.44,th*.48);
let yy=b-th*.55,r=w*(1.25+k*.45);
for(let j=0;j<3;j++){
x.fillStyle=j===1?'#347d45':'#205b39';
x.beginPath();
x.arc(a+(j-1)*r*.4,yy-j*r*.3,r*(.72-j*.07),0,7);
x.fill()
}
x.fillStyle='#438c4e';
x.beginPath();x.arc(a-r*.25,yy-r*.22,r*.48,0,7);x.fill()
}

function draw(){
x.clearRect(0,0,W,H);
let sky=x.createLinearGradient(0,0,0,H);
sky.addColorStop(0,'#78b7c6');
sky.addColorStop(.45,'#c6dfae');
sky.addColorStop(1,'#426f39');
x.fillStyle=sky;x.fillRect(0,0,W,H);

for(let i=0;i<30;i++){
let a=i*W/29;
x.fillStyle=i%2?'#346c4b':'#28583f';
x.beginPath();
x.moveTo(a-35,H*.49);
x.lineTo(a+18,H*.22+(i%4)*13);
x.lineTo(a+70,H*.49);
x.fill()
}
x.fillStyle='#426f39';x.fillRect(0,H*.47,W,H*.53);

// Đường đất ngoằn ngoèo
for(let z=1550;z>Math.max(0,cz-10);z-=7){
let a=proj(path(z)-48,z),b=proj(path(z)+48,z);
let d=proj(path(z+7)-48,z+7),e=proj(path(z+7)+48,z+7);
if(!a||!b||!d||!e)continue;
x.fillStyle=Math.floor(z/25)%2?'#9a8865':'#ad9973';
x.beginPath();
x.moveTo(a.x,a.y);x.lineTo(b.x,b.y);
x.lineTo(e.x,e.y);x.lineTo(d.x,d.y);
x.closePath();x.fill();
x.strokeStyle='#d6c39a';
x.lineWidth=Math.max(.5,a.dep*2);
x.beginPath();x.moveTo(a.x,a.y);x.lineTo(d.x,d.y);x.stroke()
}

// Cây rừng
for(let t of [...trees].sort((a,b)=>b.z-a.z)){
let p=proj(t.x,t.z);
if(p&&p.y<H+100&&p.y>-150)
tree(p.x,p.y,p.dep*1.9*t.size,t.k)
}

// 5 viên ngọc
for(let i=0;i<gemsAt.length;i++){
if(taken[i])continue;
let p=proj(...gemsAt[i]);
if(p&&p.y>0&&p.y<H){
let r=Math.max(4,13*p.dep);
x.save();x.translate(p.x,p.y-18*p.dep);x.rotate(Math.PI/4);
x.fillStyle='#70f6ff';x.shadowColor='#a6ffff';
x.shadowBlur=18*p.dep;x.fillRect(-r/2,-r/2,r,r);
x.restore()
}
}

// Cây cổ thụ
let ap=proj(path(endZ),endZ);
if(ap){
let sc=Math.max(.4,ap.dep*4),tr=95*sc;
x.fillStyle='#594535';
x.fillRect(ap.x-14*sc,ap.y-tr*.65,28*sc,tr*.65);
for(let k=0;k<7;k++){
x.fillStyle=gems>=5?(k%2?'#26864a':'#36a85b'):'#66513f';
x.beginPath();
x.arc(ap.x+Math.cos(k)*24*sc,ap.y-tr+Math.sin(k)*22*sc,35*sc,0,7);
x.fill()
}
if(gems>=5){
x.fillStyle='#d9ffb0';
x.fillRect(ap.x-3*sc,ap.y-tr-130*sc,6*sc,130*sc);
x.globalAlpha=.45;x.fillStyle='#efffbd';
x.beginPath();
x.moveTo(ap.x,ap.y-tr-250*sc);
x.lineTo(ap.x-30*sc,ap.y-tr-100*sc);
x.lineTo(ap.x+30*sc,ap.y-tr-100*sc);
x.fill();x.globalAlpha=1
}
}

// Nhân vật nhìn từ phía sau
let a=W*.5,b=H*.76,s=Math.min(W,H)/700;
x.fillStyle='#14251a88';
x.beginPath();x.ellipse(a,b+24*s,25*s,8*s,0,0,7);x.fill();
x.fillStyle=gender==='boy'?'#3e78d8':'#d65b9d';
x.beginPath();x.roundRect(a-15*s,b-43*s,30*s,42*s,8*s);x.fill();
x.fillStyle='#d7a77e';x.beginPath();x.arc(a,b-56*s,13*s,0,7);x.fill();
x.fillStyle='#352a24';x.beginPath();x.arc(a,b-61*s,14*s,Math.PI,7);x.fill();
x.fillStyle='#253d2a';
x.fillRect(a-14*s,b-5*s,11*s,27*s);
x.fillRect(a+3*s,b-5*s,11*s,27*s);

if(gems===5&&cz>endZ-100&&!won){
won=true;
document.getElementById('win').style.display='flex';
document.getElementById('winText').textContent=
'BẠN ĐÃ GIẢI CỨU THẾ GIỚI THÀNH CÔNG, '+
(document.getElementById('name').value.trim()||'NHÀ THÁM HIỂM').toUpperCase()+'!'
}
}

function begin(){
started=true;
document.getElementById('start').style.display='none';
document.getElementById('playerName').textContent=
document.getElementById('name').value.trim()||'Nhà thám hiểm'
}

function tick(){
if(started&&!won){
let dx=joy.x,dy=joy.y;
if(keys.ArrowLeft||keys.a)dx--;
if(keys.ArrowRight||keys.d)dx++;
if(keys.ArrowUp||keys.w)dy--;
if(keys.ArrowDown||keys.s)dy++;
let m=Math.hypot(dx,dy);
if(m>1){dx/=m;dy/=m}
px+=dx*3.2;pz+=-dy*3.2;
pz=Math.max(0,Math.min(endZ+60,pz));
cx+=(px-cx)*.12;cz+=(pz-cz)*.12;
for(let i=0;i<gemsAt.length;i++){
if(!taken[i]&&Math.hypot(px-gemsAt[i][0],pz-gemsAt[i][1])<35){
taken[i]=true;gems++;
document.getElementById('gems').textContent=gems
}
}
}
draw();requestAnimationFrame(tick)
}

addEventListener('keydown',e=>{
keys[e.key]=true;
if(e.key.startsWith('Arrow'))e.preventDefault()
});
addEventListener('keyup',e=>keys[e.key]=false);

const base=document.getElementById('joystick');
const stick=document.getElementById('stick');
let active=false,pid=null;

function move(e){
let r=base.getBoundingClientRect();
let dx=e.clientX-(r.left+r.width/2);
let dy=e.clientY-(r.top+r.height/2);
let lim=r.width*.31,l=Math.hypot(dx,dy);
if(l>lim){dx=dx/l*lim;dy=dy/l*lim}
joy.x=dx/lim;joy.y=dy/lim;
stick.style.left=(r.width/2-stick.offsetWidth/2+dx)+'px';
stick.style.top=(r.height/2-stick.offsetHeight/2+dy)+'px'
}
base.addEventListener('pointerdown',e=>{
active=true;pid=e.pointerId;base.setPointerCapture(pid);move(e)
});
base.addEventListener('pointermove',e=>{
if(active&&e.pointerId===pid)move(e)
});
function reset(){
active=false;pid=null;joy.x=joy.y=0;
stick.style.left=(base.clientWidth-stick.offsetWidth)/2+'px';
stick.style.top=(base.clientHeight-stick.offsetHeight)/2+'px'
}
base.addEventListener('pointerup',reset);
base.addEventListener('pointercancel',reset);
tick();
</script>
</body>
</html>
