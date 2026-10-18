import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="GIẢI CỨU THẾ GIỚI",
    page_icon="🌲",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background: #071b12;
    }
    header, footer, #MainMenu {
        visibility: hidden;
    }
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

game_code = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;font-family:Arial,sans-serif}
body{background:#071b12}
canvas{display:block;width:100%;height:100%;touch-action:none}
#menu{
 position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
 background:linear-gradient(#06170bc9,#071b12ee),radial-gradient(#376d37,#071b12);
 color:white;z-index:5
}
.panel{
 width:min(92%,480px);padding:28px;border:2px solid #79c86a;
 border-radius:24px;background:#0a261eee;text-align:center;
 box-shadow:0 0 35px #38c85b55
}
h1{font-size:clamp(30px,6vw,48px);color:#a5ff91;margin:0 0 8px}
.sub{color:#d0e9c8;line-height:1.6}
input{
 width:100%;padding:13px;border-radius:10px;border:1px solid #8ebc7e;
 font-size:17px;margin:12px 0;background:#f2fff0;color:#17351b
}
button{
 cursor:pointer;border:0;border-radius:12px;padding:12px 20px;
 font-size:17px;font-weight:bold
}
.choice{background:#24482d;color:white;border:1px solid #80bb77;margin:5px}
.choice.active{background:#a1e88b;color:#15331b}
#start{width:100%;margin-top:14px;background:#9bea82;color:#103518}
#hud{
 position:absolute;top:12px;left:12px;right:12px;display:none;
 color:white;justify-content:space-between;gap:8px;align-items:flex-start;
 pointer-events:none;text-shadow:0 2px 4px black;font-weight:bold
}
.pill{background:#092417d9;border:1px solid #8bd37c;padding:10px 13px;border-radius:14px}
#hint{position:absolute;top:67px;left:50%;transform:translateX(-50%);
 background:#071b12c9;color:white;border-radius:10px;padding:8px 12px;
 font-size:13px;white-space:nowrap;pointer-events:none}
#joystick{
 position:absolute;left:20px;bottom:20px;width:126px;height:126px;
 border-radius:50%;border:3px solid #ffffff90;background:#ffffff28;
 display:none;touch-action:none
}
#stick{
 position:absolute;left:39px;top:39px;width:42px;height:42px;border-radius:50%;
 background:#d5ffd5d9;border:2px solid white;box-shadow:0 0 12px #fff7
}
#win{
 position:absolute;inset:0;display:none;align-items:center;justify-content:center;
 background:#031609c9;color:white;text-align:center;padding:20px;z-index:4
}
#win h2{font-size:clamp(27px,5vw,52px);color:#baff9e;text-shadow:0 0 22px #7cff63}
#win button{background:#a4f28c;color:#103518}
@media(max-width:600px){
 .panel{padding:20px}
 #joystick{width:112px;height:112px}
 #stick{left:34px;top:34px}
 #hint{top:74px;font-size:11px}
}
</style>
</head>
<body>
<canvas id="game"></canvas>

<div id="menu">
 <div class="panel">
  <h1>GIẢI CỨU<br>THẾ GIỚI</h1>
  <div class="sub">
   🌲 Khám phá khu rừng bí ẩn
