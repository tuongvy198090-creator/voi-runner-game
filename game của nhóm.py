
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Heo Chủ Tịch",
    page_icon="🐷",
    layout="wide"
)

st.title("🐷 HEO CHỦ TỊCH")
st.caption("Chạy thật nhanh, vượt chướng ngại vật và chinh phục con đường!")

game = r"""
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
    background: #b9e8ff;
    font-family: Arial, sans-serif;
}
#game { width: 100%; height: 650px; position: relative; }
canvas { display: block; }
#hud {
    position: absolute;
    top: 12px; left: 12px; right: 12px;
    display: flex; justify-content: space-between;
    gap: 8px; pointer-events: none;
}
.panel {
    color: white; background: rgba(25,35,48,.82);
    padding: 10px 14px; border-radius: 12px;
    font-weight: bold; font-size: 15px;
}
#message {
    position: absolute; inset: 0;
    display: flex; align-items: center; justify-content: center;
    background: rgba(10,20,30,.48);
}
#card {
    background: white; color: #263238; padding: 24px;
    border-radius: 20px; text-align: center;
    width: min(90%, 420px); box-shadow: 0 8px 28px #0004;
}
#card h2 { margin-top: 0; color: #e65c76; }
#card p { line-height: 1.6; }
#start {
    border: 0; border-radius: 12px; padding: 13px 25px;
    background: #ff6680; color: white;
    font-weight: bold; font-size: 17px; cursor: pointer;
}
#help {
    position: absolute; bottom: 10px; left: 10px; right: 10px;
    text-align: center; color: white; font-size: 12px;
    text-shadow: 1px 1px 3px #000; pointer-events: none;
}
</style>
</head>
<body>
<div id="game">
    <div id="hud">
        <div class="panel">🐷 HEO CHỦ TỊCH</div>
        <div class="panel">⭐ Điểm: <span id="score">0</span></div>
        <div class="panel">🏆 Kỷ lục: <span id="best">0</span></div>
    </div>
    <div id="message">
        <div id="card">
            <h2>🐷 HEO CHỦ TỊCH</h2>
            <p>
                Heo tự động chạy ngay khi bắt đầu!<br>
                ⬅️ ➡️ Đổi làn đường<br>
                ⬆️ hoặc SPACE: Nhảy qua rơm thấp<br>
                ⬇️: Cúi xuống chui qua lỗ<br>
                🪜 Gặp bậc rơm: Heo tự leo lên rồi xuống
            </p>
            <button id="start">BẮT ĐẦU CHƠI!</button>
        </div>
    </div>
    <div id="help">
        Bấm vào màn hình game trước khi dùng bàn phím.
        Tránh rơm để không bị thua nhé!
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
(() => {
const root = document.getElementById("game");
const scoreText = document.getElementById("score");
const bestText = document.getElementById("best");
const message = document.getElementById("message");
const startButton = document.getElementById("start");

let scene, camera, renderer, pig;
let running = false;
let gameOver = false;
let score = 0;
let best = 0;
let speed = 17;
let spawnTimer = 0;
let jumpVelocity = 0;
let jumpHeight = 0;
let duckTimer = 0;
let elapsed = 0;
let lane = 1;
let targetX = 0;
let lastTime = 0;
let obstacles = [];
let trees = [];
let markings = [];
let legs = [];
let arms = [];
let rampHeight = 0;
let rampTarget = 0;

const lanes = [-2.35, 0, 2.35];
const playerZ = 4;
const clock = new THREE.Clock();

function mat(color, roughness=0.85) {
    return new THREE.MeshStandardMaterial({color, roughness});
}
const pink = mat(0xff91a9);
const lightPink = mat(0xffb4c4);
const darkPink = mat(0xd94f72);
const blue = mat(0x258bd2);
const darkBlue = mat(0x14548e);
const white = mat(0xffffff);
const black = mat(0x29232b);
const gold = mat(0xffd34e);
const straw = mat(0xd9a33e);
const strawLight = mat(0xf1c86b);
const roadMat = mat(0x555c65);
const grassMat = mat(0x63b85a);
const leafMat = mat(0x23864b);
const trunkMat = mat(0x79502e);

function box(parent, w,h,d, material, x,y,z) {
    const mesh = new THREE.Mesh(
        new THREE.BoxGeometry(w,h,d), material
    );
    mesh.position.set(x,y,z);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    parent.add(mesh);
    return mesh;
}

function sphere(parent, rx,ry,rz, material, x,y,z) {
    const mesh = new THREE.Mesh(
        new THREE.SphereGeometry(1,20,14), material
    );
    mesh.scale.set(rx,ry,rz);
    mesh.position.set(x,y,z);
    mesh.castShadow = true;
    parent.add(mesh);
    return mesh;
}

function cylinder(parent, r1,r2,h, material, x,y,z, sides=12) {
    const mesh = new THREE.Mesh(
        new THREE.CylinderGeometry(r1,r2,h,sides), material
    );
    mesh.position.set(x,y,z);
    mesh.castShadow = true;
    parent.add(mesh);
    return mesh;
}

function makePig() {
    pig = new THREE.Group();
    scene.add(pig);
    pig.position.set(0,0,playerZ);

    // Thân heo mặc vest xanh
    sphere(pig,0.58,0.69,0.72,pink,0,1.03,0.08);
    sphere(pig,0.55,0.52,0.48,blue,0,0.92,0.15);
    box(pig,0.13,0.48,0.12,gold,0,0.96,-0.31);

    // Hai chân sau làm trụ đứng
    for (const x of [-0.28,0.28]) {
        const leg = cylinder(pig,0.13,0.16,0.53,darkPink,x,0.31,0.28);
        legs.push(leg);
        sphere(pig,0.17,0.10,0.20,black,x,0.075,0.20);
    }

    // Đầu to để nhân vật nổi bật
    sphere(pig,0.53,0.49,0.48,pink,0,1.82,-0.30);

    // Tai
    for (const x of [-0.37,0.37]) {
        const ear = sphere(pig,0.17,0.24,0.11,pink,x,2.20,-0.27);
        ear.rotation.z = x < 0 ? 0.35 : -0.35;
        sphere(pig,0.09,0.14,0.045,darkPink,x,2.21,-0.365);
    }

    // Mõm hướng về phía trước
    sphere(pig,0.29,0.22,0.18,lightPink,0,1.69,-0.73);
    for (const x of [-0.10,0.10]) {
        sphere(pig,0.035,0.06,0.025,darkPink,x,1.70,-0.89);
    }

    // Mắt và lông mày
    for (const x of [-0.22,0.22]) {
        sphere(pig,0.075,0.09,0.045,white,x,1.93,-0.695);
        sphere(pig,0.033,0.052,0.025,black,x,1.93,-0.735);
        box(pig,0.13,0.035,0.035,black,x,2.055,-0.70);
    }

    // Hai chân trước giống cánh tay
    for (const side of [-1,1]) {
        const arm = new THREE.Group();
        arm.position.set(side*0.42,1.32,-0.23);
        arm.rotation.z = side * -0.45;
        pig.add(arm);
        cylinder(arm,0.115,0.13,0.47,pink,side*0.05,-0.17,-0.02);
        sphere(arm,0.14,0.13,0.14,lightPink,side*0.05,-0.39,-0.02);
        arms.push(arm);
    }

    // Nơ đỏ và huy hiệu vàng
    sphere(pig,0.14,0.11,0.07,darkPink,0,1.39,-0.47);
    sphere(pig,0.075,0.075,0.06,gold,0,1.39,-0.54);

    // Mũ chủ tịch
    cylinder(pig,0.32,0.34,0.09,darkBlue,0,2.27,-0.30);
    const hat = new THREE.Mesh(
        new THREE.ConeGeometry(0.23,0.43,12), gold
    );
    hat.position.set(0,2.51,-0.30);
    hat.castShadow = true;
    pig.add(hat);
    sphere(pig,0.07,0.07,0.07,white,0,2.72,-0.30);
}

function makeTree(x,z) {
    const group = new THREE.Group();
    group.position.set(x,0,z);
    scene.add(group);
    cylinder(group,0.22,0.30,2.0,trunkMat,0,1,0,8);
    sphere(group,0.92,1.05,0.82,leafMat,0,2.35,0);
    sphere(group,0.66,0.72,0.64,mat(0x319b50),-0.38,2.85,-0.12);
    sphere(group,0.65,0.75,0.65,mat(0x3ba653),0.38,2.80,0.08);
    trees.push(group);
}

function makeWorld() {
    scene.background = new THREE.Color(0x9bdbff);
    scene.fog = new THREE.Fog(0x9bdbff,45,115);

    const ambient = new THREE.HemisphereLight(0xffffff,0x64834d,2.0);
    scene.add(ambient);

    const sun = new THREE.DirectionalLight(0xffffff,2.2);
    sun.position.set(-7,14,5);
    sun.castShadow = true;
    scene.add(sun);

    // Mặt cỏ
    const grass = new THREE.Mesh(
        new THREE.PlaneGeometry(150,200),grassMat
    );
    grass.rotation.x = -Math.PI/2;
    grass.position.set(0,-0.13,-35);
    scene.add(grass);

    // Đường nhựa màu xám
    const road = box(scene,8,0.16,180,roadMat,0,-0.03,-35);
    road.receiveShadow = true;

    // Lề đường
    for (const x of [-4.15,4.15]) {
        box(scene,0.22,0.13,180,white,x,0.035,-35);
    }

    // Vạch đường di chuyển liên tục
    for (let z=-110; z<30; z+=8) {
        for (const x of [-1.28,1.28]) {
            markings.push(box(scene,0.10,0.025,3.2,white,x,0.065,z));
        }
    }

    // Cây to hai bên đường
    for (let z=-100; z<25; z+=10) {
        makeTree(-5.5,z);
        makeTree(5.5,z-4);
    }

    // Mây trang trí
    const cloudMat = mat(0xffffff);
    for (let i=0;i<8;i++) {
        const cloud = new THREE.Group();
        cloud.position.set((i%2?1:-1)*(8+Math.random()*8),
            8+Math.random()*5,-20-i*13);
        sphere(cloud,1.6,0.55,0.8,cloudMat,0,0,0);
        sphere(cloud,1.0,0.65,0.7,cloudMat,1,0.1,0);
        sphere(cloud,1.0,0.5,0.7,cloudMat,-1,0,0);
        scene.add(cloud);
    }
}

function makeHayBall(parent,x,y,z,r=0.48) {
    const bale = cylinder(parent,r,r,0.78,straw,x,y,z,12);
    bale.rotation.z = Math.PI/2;
    sphere(parent,r*0.95,r*0.95,0.10,strawLight,x,y,z+0.40);
    // Vòng dây trên rơm
    const ring = new THREE.Mesh(
        new THREE.TorusGeometry(r*0.78,0.025,6,16),darkPink
    );
    ring.position.set(x,y,z+0.43);
    parent.add(ring);
}

function makeObstacle(type, obstacleLane) {
    const group = new THREE.Group();
    group.position.set(lanes[obstacleLane],0,-75);
    scene.add(group);

    if (type===1) {
        // Cổng rơm cao, chừa khe thấp để cúi người
        // Hai trụ hai bên và thanh ngang phía trên
        for (const x of [-0.85,0.85]) {
            for (let y=0.48;y<2.3;y+=0.78) {
                makeHayBall(group,x,y,0,0.48);
            }
        }
        for (let x=-0.42;x<=0.42;x+=0.72) {
            makeHayBall(group,x,2.35,0,0.48);
        }
        group.userData.type=1;
    } else if (type===2) {
        // Rơm thấp chắn đường, phải nhảy qua
        makeHayBall(group,0,0.48,0,0.48);
        makeHayBall(group,0.72,0.48,0,0.48);
        group.userData.type=2;
    } else {
        // Bậc rơm đi lên rồi đi xuống
        // Heo tự động leo theo các bậc khi đi qua
        const steps = [
            {x:0,y:0.25,z:-1.15},
            {x:0,y:0.52,z:-0.60},
            {x:0,y:0.79,z:-0.05},
            {x:0,y:1.06,z:0.50},
            {x:0,y:0.79,z:1.05},
            {x:0,y:0.52,z:1.60},
            {x:0,y:0.25,z:2.15}
        ];
        for (const s of steps) {
            box(group,1.75,s.y*2,0.60,straw,s.x,s.y,s.z);
            for (let j=0;j<2;j++) {
                sphere(group,0.12,0.12,0.12,strawLight,
                    -0.48+j*0.96,s.y*2,s.z);
            }
        }
        group.userData.type=3;
    }

    group.userData.lane=obstacleLane;
    obstacles.push(group);
}

function resetGame() {
    for (const ob of obstacles) scene.remove(ob);
    obstacles=[];
    score=0;
    speed=17;
    spawnTimer=0.6;
    elapsed=0;
    lane=1;
    targetX=0;
    jumpHeight=0;
    jumpVelocity=0;
    duckTimer=0;
    rampHeight=0;
    rampTarget=0;
    gameOver=false;
    running=true;
    pig.position.set(0,0,playerZ);
    pig.rotation.set(0,0,0);
    message.style.display="none";
    clock.getDelta();
}

function endGame() {
    running=false;
    gameOver=true;
    best=Math.max(best,Math.floor(score));
    bestText.textContent=best;
    message.style.display="flex";
    document.getElementById("card").innerHTML=
        '<h2>Ôi! Heo vấp rơm rồi! 🐷</h2>'+
        '<p>Điểm của em: <b>'+Math.floor(score)+'</b><br>'+
        'Cố gắng thêm lần nữa nha!</p>'+
        '<button id="start">CHƠI LẠI</button>';
    document.getElementById("start").onclick=resetGame;
}

function moveLane(direction) {
    if (!running) return;
    lane=Math.max(0,Math.min(2,lane+direction));
    targetX=lanes[lane];
}

function jump() {
    if (running && jumpHeight<=0.02 && duckTimer<=0) {
        jumpVelocity=8.5;
    }
}

function duck() {
    if (running && jumpHeight<=0.05) duckTimer=0.85;
}

window.addEventListener("keydown",e=>{
    if (["ArrowLeft","ArrowRight","ArrowUp","ArrowDown"," "].includes(e.key)) {
        e.preventDefault();
    }
    if (e.repeat) return;
    if (e.key==="ArrowLeft" || e.key.toLowerCase()==="a") moveLane(-1);
    if (e.key==="ArrowRight" || e.key.toLowerCase()==="d") moveLane(1);
    if (e.key==="ArrowUp" || e.key===" ") jump();
    if (e.key==="ArrowDown" || e.key.toLowerCase()==="s") duck();
});

startButton.onclick=resetGame;

function animate(time) {
    requestAnimationFrame(animate);
    const dt=Math.min(clock.getDelta(),0.04);
    elapsed+=dt;

    if (running) {
        score+=dt*10;
        speed=Math.min(29,17+score/150);
        scoreText.textContent=Math.floor(score);

        // Heo tự chạy liên tục
        pig.position.x += (targetX-pig.position.x)*Math.min(1,dt*9);

        // Nhảy
        if (jumpVelocity!==0 || jumpHeight>0) {
            jumpVelocity-=21*dt;
            jumpHeight+=jumpVelocity*dt;
            if (jumpHeight<=0) {
                jumpHeight=0;
                jumpVelocity=0;
            }
        }

        if (duckTimer>0) duckTimer-=dt;

        // Bậc rơm: tự leo lên rồi xuống
        rampTarget=0;
        for (const ob of obstacles) {
            if (ob.userData.type===3 &&
                ob.userData.lane===lane &&
                Math.abs(ob.position.z-playerZ)<4.2) {
                const p=1-Math.abs(ob.position.z-playerZ)/4.2;
                rampTarget=Math.max(rampTarget,Math.sin(p*Math.PI)*1.05);
            }
        }
        rampHeight += (rampTarget-rampHeight)*Math.min(1,dt*6);

        // Chạy tại chỗ: hai chân sau và tay trước đung đưa
        for (let i=0;i<legs.length;i++) {
            legs[i].rotation.x=Math.sin(elapsed*13+i*Math.PI)*0.24;
        }
        for (let i=0;i<arms.length;i++) {
            arms[i].rotation.x=Math.sin(elapsed*13+i*Math.PI)*0.30;
        }

        const ducking=duckTimer>0;
        const scaleY=ducking?0.53:1;
        pig.scale.y += (scaleY-pig.scale.y)*Math.min(1,dt*14);
        pig.position.y=jumpHeight+rampHeight;
        pig.rotation.z += ((targetX-pig.position.x)*-0.12-pig.rotation.z)
            *Math.min(1,dt*7);

        // Cảnh vật chạy về phía người chơi
        for (const tree of trees) {
            tree.position.z+=speed*dt;
            if (tree.position.z>18) tree.position.z-=140;
        }
        for (const mark of markings) {
            mark.position.z+=speed*dt;
            if (mark.position.z>15) mark.position.z-=120;
        }

        // Sinh chướng ngại vật
        spawnTimer-=dt;
        if (spawnTimer<=0) {
            const type=1+Math.floor(Math.random()*3);
            const chosenLane=Math.floor(Math.random()*3);
            makeObstacle(type,chosenLane);
            spawnTimer=Math.max(1.25,2.0-score/900)+Math.random()*0.55;
        }

        // Kiểm tra va chạm
        for (let i=obstacles.length-1;i>=0;i--) {
            const ob=obstacles[i];
            ob.position.z+=speed*dt;
            const dz=Math.abs(ob.position.z-playerZ);
            if (dz<0.8 && ob.userData.lane===lane) {
                const type=ob.userData.type;
                if (type===1 && !ducking) {
                    endGame();
                    break;
                }
                if (type===2 && jumpHeight<0.65) {
                    endGame();
                    break;
                }
                // Bậc rơm loại 3 được thiết kế để tự động vượt qua
            }
            if (ob.position.z>15) {
                scene.remove(ob);
                obstacles.splice(i,1);
            }
        }
    }

    renderer.render(scene,camera);
}

function init() {
    scene=new THREE.Scene();
    camera=new THREE.PerspectiveCamera(
        58,root.clientWidth/650,0.1,180
    );
    camera.position.set(0,6.3,11.8);
    camera.lookAt(0,1.0,-8);

    renderer=new THREE.WebGLRenderer({antialias:true});
    renderer.setSize(root.clientWidth,650);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio,1.8));
    renderer.shadowMap.enabled=true;
    renderer.shadowMap.type=THREE.PCFSoftShadowMap;
    root.insertBefore(renderer.domElement,root.firstChild);
    renderer.domElement.style.position="absolute";
    renderer.domElement.style.inset="0";
    renderer.domElement.style.width="100%";
    renderer.domElement.style.height="100%";
    renderer.domElement.style.outline="none";
    renderer.domElement.tabIndex=0;

    makeWorld();
    makePig();

    window.addEventListener("resize",()=>{
        camera.aspect=root.clientWidth/650;
        camera.updateProjectionMatrix();
        renderer.setSize(root.clientWidth,650);
    });

    requestAnimationFrame(animate);
}
init();
})();
</script>
</body>
</html>
"""

components.html(game, height=660, scrolling=False)
