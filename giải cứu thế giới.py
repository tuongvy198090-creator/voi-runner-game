
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="GIẢI CỨU THẾ GIỚI",
    page_icon="🌳",
    layout="wide"
)

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: #071d13;
}
header, footer, [data-testid="stToolbar"] {
    visibility: hidden;
}
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

game_code = r'''
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    overflow: hidden;
    font-family: Arial, sans-serif;
    background: #173b25;
}
canvas {
    display: block;
    width: 100%;
    height: 100%;
}
#game { position: relative; width: 100%; height: 790px; overflow: hidden; }
#hud {
    position: absolute; top: 12px; left: 12px;
    color: white; background: #102d20dd;
    border: 1px solid #a9d89a; border-radius: 12px;
    padding: 10px 14px; line-height: 1.7;
    z-index: 3;
}
#menu, #question, #win {
    position: absolute; z-index: 5;
    inset: 0; display: flex; align-items: center;
    justify-content: center; background: #071a12b8;
}
.panel {
    width: min(430px, 92%); padding: 24px;
    background: #f4f0d7; color: #173b25;
    border: 4px solid #7ab65d; border-radius: 20px;
    text-align: center; box-shadow: 0 10px 35px #0008;
}
h1 { font-size: 28px; margin: 4px 0 12px; }
p { line-height: 1.5; }
input {
    width: 100%; padding: 12px; border-radius: 9px;
    border: 2px solid #76a45d; font-size: 16px;
    margin: 8px 0;
}
button {
    cursor: pointer; border: 0; border-radius: 10px;
    padding: 11px 15px; margin: 5px;
    font-weight: bold; font-size: 15px;
    background: #2d824b; color: white;
}
button:hover { filter: brightness(1.12); }
button:disabled { opacity: .55; cursor: default; }
.choice { display:block; width:100%; text-align:left;
    background:#fffdf0; color:#173b25; border:2px solid #a7c78d; }
.choice.correct { background:#6ee7a0; border-color:#087b38; }
.choice.wrong { background:#ff9e9e; border-color:#b51e1e; }
#message { font-weight:bold; min-height:25px; }
#controls {
    position:absolute; bottom:18px; left:18px;
    width:142px; height:142px; z-index:4;
}
.pad {
    position:absolute; width:46px; height:46px;
    border-radius:50%; background:#173c2bcc;
    border:2px solid #d8efc4; color:white;
    font-size:22px; padding:0; margin:0;
}
#up {left:48px;top:0}
#down {left:48px;bottom:0}
#left {left:0;top:48px}
#right {right:0;top:48px}
#hint {
    position:absolute; bottom:18px; right:12px;
    color:white; background:#102d20cc;
    padding:9px 12px; border-radius:10px; z-index:3;
    font-size:13px;
}
#question, #win { display:none; }
@media(max-width:600px) {
    #game { height: 720px; }
    #hud { font-size:13px; }
    h1 { font-size:23px; }
    #hint { max-width:145px; font-size:11px; }
}
</style>
</head>
<body>
<div id="game">
    <div id="hud">
        <b>🌿 GIẢI CỨU THẾ GIỚI</b><br>
        Người chơi: <span id="playerName">Nhà thám hiểm</span><br>
        💎 Ngọc: <span id="score">0</span>/5
        <div id="task">Hãy tìm ngọc trong khu rừng!</div>
    </div>

    <div id="menu">
      <div class="panel">
        <h1>🌳 GIẢI CỨU THẾ GIỚI</h1>
        <p>Khu rừng đang cần em giúp đỡ! Thu thập 5 viên ngọc để hồi sinh Cây Cổ Thụ.</p>
        <input id="nameInput" maxlength="18" placeholder="Nhập tên nhân vật">
        <p>Chọn nhân vật:</p>
        <button onclick="choose('male')" id="maleBtn">🧑 Nam</button>
        <button onclick="choose('female')" id="femaleBtn">👩 Nữ</button>
        <p id="selectedText">Đã chọn: Nam</p>
        <button onclick="startGame()">BẮT ĐẦU PHIÊU LƯU</button>
      </div>
    </div>

    <div id="question">
      <div class="panel">
        <h1>🗝️ Thử thách rương báu</h1>
        <p id="qText"></p>
        <div id="answers"></div>
        <div id="message"></div>
        <button id="continueBtn" style="display:none" onclick="closeQuestion()">Tiếp tục</button>
      </div>
    </div>

    <div id="win">
      <div class="panel">
        <h1>🌟 BẠN ĐÃ GIẢI CỨU THẾ GIỚI THÀNH CÔNG!</h1>
        <p>Cây Cổ Thụ đã hồi sinh. Khu rừng lại xanh tươi nhờ em!</p>
        <button onclick="location.reload()">Chơi lại</button>
      </div>
    </div>

    <div id="controls">
      <button class="pad" id="up">▲</button>
      <button class="pad" id="down">▼</button>
      <button class="pad" id="left">◀</button>
      <button class="pad" id="right">▶</button>
    </div>
    <div id="hint">Dùng WASD hoặc phím mũi tên để di chuyển.</div>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
const game = document.getElementById("game");
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x9bd4a0);
scene.fog = new THREE.Fog(0x9bd4a0, 30, 125);

const camera = new THREE.PerspectiveCamera(65, game.clientWidth/game.clientHeight, .1, 250);
camera.position.set(0, 5, 9);

const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(game.clientWidth, game.clientHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.7));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
game.prepend(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xdfffea, 0x37532a, 2.0));
const sun = new THREE.DirectionalLight(0xfff1cf, 2.2);
sun.position.set(-15, 30, 12);
sun.castShadow = true;
sun.shadow.mapSize.set(1024,1024);
scene.add(sun);

const mat = (color, roughness=.85, metalness=0) =>
    new THREE.MeshStandardMaterial({color, roughness, metalness});

const grassMat = mat(0x477e3a);
const pathMat = mat(0x9a8b67);
const woodMat = mat(0x765035);
const leafMat = mat(0x267744);
const leafLight = mat(0x3b9650);
const goldMat = mat(0xf0c34d, .35, .45);

function box(parent, x,y,z, sx,sy,sz, material, cast=true) {
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(sx,sy,sz), material);
    mesh.position.set(x,y,z);
    mesh.castShadow = cast;
    mesh.receiveShadow = true;
    parent.add(mesh);
    return mesh;
}
function sphere(parent,x,y,z,sx,sy,sz,material) {
    const mesh = new THREE.Mesh(new THREE.SphereGeometry(1,12,10),material);
    mesh.position.set(x,y,z);
    mesh.scale.set(sx,sy,sz);
    mesh.castShadow=true;
    parent.add(mesh);
    return mesh;
}
function cylinder(parent,x,y,z,rt,rb,h,material,segments=10) {
    const mesh = new THREE.Mesh(
        new THREE.CylinderGeometry(rt,rb,h,segments),material
    );
    mesh.position.set(x,y,z);
    mesh.castShadow=true;
    mesh.receiveShadow=true;
    parent.add(mesh);
    return mesh;
}

// Ground
const ground = new THREE.Mesh(new THREE.PlaneGeometry(180,220),grassMat);
ground.rotation.x=-Math.PI/2;
ground.position.set(0,-.08,-40);
ground.receiveShadow=true;
scene.add(ground);

// A narrow winding path, fixed in the forest
const pathPoints = [];
for(let i=0;i<=36;i++){
    const z=18-i*3.1;
    const x=Math.sin(i*.25)*4.2;
    pathPoints.push(new THREE.Vector3(x,.015,z));
}
const pathCurve = new THREE.CatmullRomCurve3(pathPoints);
const pathShape = new THREE.Shape();
pathShape.moveTo(-1.8,0);
pathShape.lineTo(1.8,0);
pathShape.lineTo(1.8,-1);
pathShape.lineTo(-1.8,-1);
const pathGeo = new THREE.BufferGeometry();
const verts=[];
for(let i=0;i<pathPoints.length-1;i++){
    const a=pathPoints[i], b=pathPoints[i+1];
    const dx=b.x-a.x, dz=b.z-a.z;
    const len=Math.hypot(dx,dz);
    const nx=-dz/len*1.8, nz=dx/len*1.8;
    verts.push(a.x+nx,.012,a.z+nz, a.x-nx,.012,a.z-nz,
               b.x+nx,.012,b.z+nz,
               a.x-nx,.012,a.z-nz, b.x-nx,.012,b.z-nz,
               b.x+nx,.012,b.z+nz);
}
pathGeo.setAttribute('position',new THREE.Float32BufferAttribute(verts,3));
pathGeo.computeVertexNormals();
const pathMesh = new THREE.Mesh(pathGeo,new THREE.MeshStandardMaterial({
    color:0x9c8c69, side:THREE.DoubleSide, roughness:1
}));
pathMesh.receiveShadow=true;
scene.add(pathMesh);

// Trees: simple but layered shapes
function tree(x,z,scale=1,ancient=false){
    const g=new THREE.Group();
    g.position.set(x,0,z);
    g.scale.setScalar(scale);
    scene.add(g);
    cylinder(g,0,1.6,0,.42,.58,3.2,woodMat,9);

    const leafA=ancient?mat(0x51452d):leafMat;
    const leafB=ancient?mat(0x665537):leafLight;
    sphere(g,0,3.4,0,1.65,1.55,1.5,leafA);
    sphere(g,-.85,3.05,.05,.95,1.05,1.0,leafB);
    sphere(g,.8,3.15,-.12,1.05,1.0,1.0,leafA);
    sphere(g,.05,4.15,-.15,1.1,1.05,1.05,leafB);

    if(ancient){
        // Bare branches make the ancient tree look withered
        for(let i=0;i<4;i++){
            const branch=cylinder(g,0,0,0,.10,.16,2.0,woodMat,7);
            branch.position.set((i-1.5)*.42,2.8,-.1);
            branch.rotation.z=(i-1.5)*-.38;
        }
    }
    return g;
}

let seed=7831;
function rand(){seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;}

for(let i=0;i<300;i++){
    const x=(rand()-.5)*100;
    const z=rand()*-120+18;
    if(Math.abs(x)<7 && z<18 && z>-90) continue;
    tree(x,z,.75+rand()*.75);
}

// Ancient tree stays fixed
const ancientTree=tree(0,-91,2.6,true);

// A soft upward beam appears when the tree is restored
const beamMat=new THREE.MeshBasicMaterial({
    color:0xc8ffb5, transparent:true, opacity:.0,
    side:THREE.DoubleSide, depthWrite:false
});
const beam=new THREE.Mesh(new THREE.CylinderGeometry(.2,2.2,17,20,1,true),beamMat);
beam.position.set(0,12,-91);
scene.add(beam);

// Character model: improved details, still low-poly and lightweight
let gender='male';
let player, bodyParts={};
let playerX=0, playerZ=13;
let moving=false, gameStarted=false, gameWon=false;
const keys={};
let score=0;
let chestOpen=[false,false];
let questionOpen=false;
let activeChest=-1;
let usedQuestions=[];
let restored=false;

function makeCharacter(type){
    const root=new THREE.Group();
    const skin=mat(type==='female'?0xe9b88e:0xd9a579);
    const hair=mat(type==='female'?0x4a2c20:0x493020);
    const shirt=mat(type==='female'?0xe45f78:0x367fc0);
    const pants=mat(type==='female'?0x394c76:0x34455b);
    const boots=mat(0x513624);
    const dark=mat(0x33251e);
    const eye=mat(0x211a15,.5);
    const white=mat(0xffffff,.35);

    // Legs and boots
    const leftLeg=box(root,-.19,.55,0,.22,.72,.25,pants);
    const rightLeg=box(root,.19,.55,0,.22,.72,.25,pants);
    box(root,-.19,.17,.07,.25,.18,.38,boots);
    box(root,.19,.17,.07,.25,.18,.38,boots);

    // Body and simple clothing details
    box(root,0,1.28,0,.72,.88,.4,shirt);
    box(root,0,.88,0,.73,.12,.42,mat(0x533b2a));
    box(root,0,.87,.02,.12,.15,.44,goldMat);

    // Arms, sleeves and hands
    const leftArm=box(root,-.48,1.35,0,.22,.66,.25,shirt);
    const rightArm=box(root,.48,1.35,0,.22,.66,.25,shirt);
    sphere(root,-.48,1.0,0,.13,.14,.13,skin);
    sphere(root,.48,1.0,0,.13,.14,.13,skin);

    // Neck and head
    cylinder(root,0,1.77,0,.12,.13,.22,skin,10);
    sphere(root,0,2.08,0,.36,.4,.32,skin);

    // Hair cap
    sphere(root,0,2.30,-.015,.375,.25,.35,hair);
    if(type==='male'){
        sphere(root,-.20,2.25,.22,.16,.12,.12,hair);
        sphere(root,.12,2.34,.20,.18,.11,.12,hair);
    }else{
        // Long hair down the back and sides
        sphere(root,0,2.04,-.24,.39,.48,.22,hair);
        sphere(root,-.32,2.02,.01,.13,.42,.16,hair);
        sphere(root,.32,2.02,.01,.13,.42,.16,hair);
        sphere(root,-.17,2.32,.08,.20,.14,.20,hair);
    }

    // Eyes and eyebrows visible from the front
    sphere(root,-.13,2.10,.294,.045,.055,.025,white);
    sphere(root,.13,2.10,.294,.045,.055,.025,white);
    sphere(root,-.13,2.10,.315,.021,.032,.014,eye);
    sphere(root,.13,2.10,.315,.021,.032,.014,eye);
    box(root,-.13,2.19,.29,.10,.025,.035,dark);
    box(root,.13,2.19,.29,.10,.025,.035,dark);
    sphere(root,0,2.00,.32,.07,.035,.03,skin);

    // Small backpack
    box(root,0,1.35,-.27,.42,.52,.18,mat(0x98613b));
    box(root,0,1.49,-.37,.28,.17,.04,goldMat);

    root.position.set(playerX,0,playerZ);
    scene.add(root);
    bodyParts={leftLeg,rightLeg,leftArm,rightArm};
    return root;
}

function choose(type){
    gender=type;
    document.getElementById('selectedText').textContent=
        'Đã chọn: '+(type==='male'?'Nam':'Nữ');
    document.getElementById('maleBtn').style.outline=
        type==='male'?'3px solid #d9a844':'none';
    document.getElementById('femaleBtn').style.outline=
        type==='female'?'3px solid #d9a844':'none';
}

function startGame(){
    const name=document.getElementById('nameInput').value.trim()||'Nhà thám hiểm';
    document.getElementById('playerName').textContent=name;
    document.getElementById('menu').style.display='none';
    if(player) scene.remove(player);
    player=makeCharacter(gender);
    gameStarted=true;
}

// Three collectible gems
const gems=[];
function makeGem(x,z,color){
    const group=new THREE.Group();
    group.position.set(x,.85,z);
    const gemMat=new THREE.MeshStandardMaterial({
        color, emissive:color, emissiveIntensity:.45,
        metalness:.25, roughness:.25
    });
    const crystal=new THREE.Mesh(new THREE.OctahedronGeometry(.42,0),gemMat);
    crystal.scale.set(.8,1.25,.8);
    crystal.castShadow=true;
    group.add(crystal);
    const ring=new THREE.Mesh(
        new THREE.TorusGeometry(.58,.025,6,24),
        new THREE.MeshBasicMaterial({color:0xd9ffe4})
    );
    ring.rotation.x=Math.PI/2;
    group.add(ring);
    scene.add(group);
    gems.push({group,x,z,got:false});
}
makeGem(-12,-12,0x43ff99);
makeGem(13,-34,0x4da8ff);
makeGem(-10,-60,0xff5c91);

// Two detailed treasure chests
const chests=[];
function makeChest(x,z,index){
    const g=new THREE.Group();
    g.position.set(x,0,z);

    const wood=mat(0x754525);
    const woodLight=mat(0x9a6136);
    const darkMetal=mat(0x493d2d,.4,.35);

    // Base and layered front boards
    box(g,0,.42,0,1.25,.72,.82,wood);
    box(g,0,.25,.425,1.20,.10,.055,woodLight);
    box(g,0,.48,.425,1.20,.10,.055,woodLight);
    box(g,0,.70,.425,1.20,.10,.055,woodLight);

    // Gold corner strips and bands
    for(const xSide of [-.55,.55]){
        box(g,xSide,.43,.46,.09,.76,.08,goldMat);
        box(g,xSide,.43,-.42,.09,.76,.08,goldMat);
    }
    box(g,0,.10,.46,1.20,.09,.08,goldMat);
    box(g,0,.77,.46,1.20,.09,.08,goldMat);

    // Curved-looking lid made from layered segments
    const lid=box(g,0,.89,-.02,1.24,.32,.84,woodLight);
    lid.rotation.x=-.12;
    box(g,0,.93,.405,1.14,.09,.07,goldMat);

    // Front lock
    box(g,0,.49,.50,.22,.27,.09,goldMat);
    const lockRing=new THREE.Mesh(
        new THREE.TorusGeometry(.065,.018,7,14),
        goldMat
    );
    lockRing.position.set(0,.49,.56);
    g.add(lockRing);

    // Small glowing jewel on the lid
    sphere(g,0,1.12,0,.12,.13,.12,mat(0x79fff0,.25,.3));

    g.position.set(x,0,z);
    scene.add(g);
    chests.push({group:g,x,z,index,lid,opened:false});
}
makeChest(12,-70,0);
makeChest(5,4,1);

// Six school questions
const questions=[
 {q:"Dấu hiệu nào sau đây không phải là dấu hiệu nhận biết hình bình hành?",
  a:["Tứ giác có hai đường chéo vuông góc.","Tứ giác có các cạnh đối bằng nhau.","Tứ giác có các góc đối bằng nhau.","Tứ giác có hai đường chéo cắt nhau tại trung điểm mỗi đường."],c:0},
 {q:"Khối lượng nguyên tử của nguyên tố Sulfur (lưu huỳnh) xấp xỉ bằng bao nhiêu amu?",
  a:["40 amu.","90 amu.","32 amu.","Không có đáp án đúng."],c:2},
 {q:"Công thức tính khối lượng riêng là gì?",
  a:["D = V/m","D = m/V","D = m × V","D = m + V"],c:1},
 {q:"Kết quả phân tích đa thức x² − 9 thành nhân tử là gì?",
  a:["(x − 3)²","(x − 9)(x + 1)","x(x − 9)","(x − 3)(x + 3)"],c:3},
 {q:"Đặc điểm nổi bật của khí hậu môi trường nhiệt đới là gì?",
  a:["Nhiệt độ thấp quanh năm.","Băng tuyết quanh năm.","Mưa nhiều quanh năm, không có mùa khô.","Nhiệt độ cao, có sự thay đổi theo mùa."],c:3},
 {q:"Hệ cơ quan nào có chức năng vận chuyển oxygen và các chất dinh dưỡng đến tế bào?",
  a:["Hệ tiêu hóa.","Hệ tuần hoàn.","Hệ hô hấp.","Hệ bài tiết."],c:1}
];

function openQuestion(chest){
    if(questionOpen||chest.opened) return;
    questionOpen=true;
    activeChest=chest.index;
    chest.opened=true;

    // Lift the lid a little
    chest.lid.rotation.x=-.95;
    chest.lid.position.y=1.04;

    let choices=questions.map((q,i)=>i).filter(i=>!usedQuestions.includes(i));
    if(choices.length===0) choices=questions.map((q,i)=>i);
    const qi=choices[Math.floor(Math.random()*choices.length)];
    usedQuestions.push(qi);
    const q=questions[qi];

    document.getElementById('qText').textContent=q.q;
    document.getElementById('message').textContent='';
    document.getElementById('continueBtn').style.display='none';
    const holder=document.getElementById('answers');
    holder.innerHTML='';

    q.a.forEach((answer,i)=>{
        const btn=document.createElement('button');
        btn.className='choice';
        btn.textContent=String.fromCharCode(65+i)+'. '+answer;
        btn.onclick=()=>{
            if(btn.dataset.done) return;
            if(i===q.c){
                btn.classList.add('correct');
                document.getElementById('message').textContent='Chính xác! Em nhận được 1 viên ngọc! 💎';
                document.getElementById('message').style.color='#087b38';
                score++;
                updateScore();
                holder.querySelectorAll('button').forEach(b=>b.disabled=true);
                document.getElementById('continueBtn').style.display='inline-block';
                btn.dataset.done='yes';
            }else{
                btn.classList.add('wrong');
                document.getElementById('message').textContent='Chưa đúng rồi, em thử lại nhé!';
                document.getElementById('message').style.color='#b51e1e';
            }
        };
        holder.appendChild(btn);
    });
    document.getElementById('question').style.display='flex';
}
function closeQuestion(){
    document.getElementById('question').style.display='none';
    questionOpen=false;
    activeChest=-1;
    updateScore();
}
function updateScore(){
    document.getElementById('score').textContent=score;
    document.getElementById('task').textContent=
        score>=5?'Hãy tìm Cây Cổ Thụ!':'Tìm ngọc và mở rương báu.';
}

// Movement controls
function setKey(k,on){keys[k]=on;}
window.addEventListener('keydown',e=>{
    const k=e.key.toLowerCase();
    if(['arrowup','arrowdown','arrowleft','arrowright',' '].includes(k)) e.preventDefault();
    keys[k]=true;
    if(questionOpen && ['a','b','c','d'].includes(k)){
        const index=k.charCodeAt(0)-97;
        const btn=document.querySelectorAll('#answers button')[index];
        if(btn) btn.click();
    }
});
window.addEventListener('keyup',e=>keys[e.key.toLowerCase()]=false);

function bindPad(id,key){
    const el=document.getElementById(id);
    el.addEventListener('pointerdown',e=>{e.preventDefault();keys[key]=true;el.setPointerCapture(e.pointerId);});
    el.addEventListener('pointerup',()=>keys[key]=false);
    el.addEventListener('pointercancel',()=>keys[key]=false);
    el.addEventListener('lostpointercapture',()=>keys[key]=false);
}
bindPad('up','arrowup');bindPad('down','arrowdown');
bindPad('left','arrowleft');bindPad('right','arrowright');

function dist(x1,z1,x2,z2){return Math.hypot(x1-x2,z1-z2);}

const clock=new THREE.Clock();
function animate(){
    requestAnimationFrame(animate);
    const dt=Math.min(clock.getDelta(),.05);
    const t=clock.elapsedTime;

    if(gameStarted && player && !questionOpen && !gameWon){
        let dx=0,dz=0;
        if(keys['w']||keys['arrowup']) dz-=1;
        if(keys['s']||keys['arrowdown']) dz+=1;
        if(keys['a']||keys['arrowleft']) dx-=1;
        if(keys['d']||keys['arrowright']) dx+=1;
        moving=dx!==0||dz!==0;

        if(moving){
            const len=Math.hypot(dx,dz);
            dx/=len;dz/=len;
            playerX+=dx*7*dt;
            playerZ+=dz*7*dt;
            playerX=Math.max(-34,Math.min(34,playerX));
            playerZ=Math.max(-102,Math.min(17,playerZ));
            player.rotation.y=Math.atan2(dx,dz);
            if(bodyParts.leftLeg){
                bodyParts.leftLeg.rotation.x=Math.sin(t*10)*.45;
                bodyParts.rightLeg.rotation.x=-Math.sin(t*10)*.45;
                bodyParts.leftArm.rotation.x=-Math.sin(t*10)*.28;
                bodyParts.rightArm.rotation.x=Math.sin(t*10)*.28;
            }
        }else if(bodyParts.leftLeg){
            bodyParts.leftLeg.rotation.x=0;
            bodyParts.rightLeg.rotation.x=0;
            bodyParts.leftArm.rotation.x=0;
            bodyParts.rightArm.rotation.x=0;
        }
        player.position.set(playerX,0,playerZ);

        // Camera follows behind the character
        const camTarget=new THREE.Vector3(playerX,3.8,playerZ+7.5);
        camera.position.lerp(camTarget,1-Math.exp(-dt*4));
        camera.lookAt(playerX,1.5,playerZ-4);

        for(const gem of gems){
            if(!gem.got && dist(playerX,playerZ,gem.x,gem.z)<1.8){
                gem.got=true;
                scene.remove(gem.group);
                score++;
                updateScore();
            }
            if(!gem.got){
                gem.group.rotation.y+=dt*.8;
                gem.group.position.y=.85+Math.sin(t*2+gem.x)*.12;
            }
        }

        for(const chest of chests){
            if(!chest.opened && dist(playerX,playerZ,chest.x,chest.z)<2.1){
                openQuestion(chest);
            }
        }

        if(score>=5){
            document.getElementById('task').textContent='Đi đến Cây Cổ Thụ ở cuối rừng!';
            if(dist(playerX,playerZ,0,-91)<7){
                restored=true;
                gameWon=true;
                beamMat.opacity=.48;
                ancientTree.traverse(obj=>{
                    if(obj.material && obj.material.color &&
                       obj.material.color.getHex()!==woodMat.color.getHex()){
                        obj.material.color.lerp(new THREE.Color(0x4caf50),.75);
                    }
                });
                document.getElementById('win').style.display='flex';
            }
        }
    }

    if(restored){
        beamMat.opacity=.3+.15*Math.sin(t*2);
    }
    renderer.render(scene,camera);
}
animate();

window.addEventListener('resize',()=>{
    camera.aspect=game.clientWidth/game.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(game.clientWidth,game.clientHeight);
});
</script>
</div>
</body>
</html>
'''

components.html(game_code, height=800, scrolling=False)
