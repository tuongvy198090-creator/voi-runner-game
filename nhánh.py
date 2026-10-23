reachShore();
}else{
penguin.position.z=iceRows[row][0].position.z+2.7;
showQuestion();
}
},600);
}else{
breakTile(iceRows[row][lane]);
msg("Sai đáp án! Băng vỡ!",1300);
setTimeout(()=>fall(resetStart),300);
}
}else if(phase==="return"){
const tile=penguin.userData.returnTile;
if(tile&&tile.userData.weak){
breakTile(tile);
msg("Băng yếu vỡ rồi! Chim rơi xuống nước!",1300);
setTimeout(()=>fall(resetBucket),300);
}else{
/* Đã đáp xuống đúng tâm tảng băng.
   Không dịch chuyển chim sang vị trí khác. */
step++;
if(step>=RETURN_ROW_COUNT){
msg("Về tới bờ an toàn!",1000);
setTimeout(win,1000);
}else{
$("progress").textContent="Hàng băng "+(step+1)+"/"+RETURN_ROW_COUNT;
msg("Đã đáp xuống! Nhảy tiếp về phía trước!",900);
setTimeout(()=>{busy=false;},500);
}
}
}
}
}
if(falling){
const t=Math.min(1,(performance.now()-fallStart)/650);
penguin.position.y=.15-t*2.8;
penguin.rotation.x=t*1.2;
if(t>=1){
falling=false;
if(fallCallback){
const cb=fallCallback;
fallCallback=null;
setTimeout(cb,450);
}
}
}
/* Camera luôn đặt phía sau chim theo đúng hướng đang đi. */
let desiredCam,lookAt;
if(phase==="return"){
desiredCam=new THREE.Vector3(
penguin.position.x*.35,
5.8,
penguin.position.z-8.5
);
lookAt=new THREE.Vector3(
penguin.position.x*.35,
1.0,
penguin.position.z+4.5
);
}else{
desiredCam=new THREE.Vector3(
penguin.position.x*.55,
4.8,
penguin.position.z+8.5
);
lookAt=new THREE.Vector3(
penguin.position.x*.55,
1.1,
penguin.position.z-3.2
);
}
camera.position.lerp(desiredCam,.09);
camera.lookAt(lookAt);
if(fishBucket.visible)fishBucket.rotation.y+=dt*.7;
renderer.render(scene,camera);
}
$("start").addEventListener("click",startGame);
$("left").addEventListener("click",()=>move(-1));
$("right").addEventListener("click",()=>move(1));
$("up").addEventListener("click",()=>{
if(phase==="outbound"||phase==="return")jump();
});
$("down").addEventListener("click",()=>move(0));
$("jump").addEventListener("click",jump);
window.addEventListener("keydown",e=>{
if(["ArrowLeft","ArrowRight","ArrowUp","ArrowDown"," ","a","d","w","s","A","D","W","S"].includes(e.key)){
e.preventDefault();
}
if(e.key==="ArrowLeft"||e.key==="a"||e.key==="A")move(-1);
if(e.key==="ArrowRight"||e.key==="d"||e.key==="D")move(1);
if(e.key===" "||e.key==="Enter"||e.key==="ArrowUp"||e.key==="w"||e.key==="W")jump();
if(e.key==="ArrowDown"||e.key==="s"||e.key==="S"){
if(phase==="outbound")move(0);
}
});
init();
})();
</script>
</body>
</html>
"""
components.html(GAME, height=760, scrolling=False)
