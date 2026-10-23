import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Vượt Băng Lấy Cá 3D",
    page_icon="🐧",
    layout="wide"
)

GAME = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
<div id="game"></div>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
(function(){
    // Phần đồ họa và cách chơi 3D đặt ở đây.
    // Không gọi buildDistantIcebergs();
})();
</script>
</body>
</html>
"""

components.html(GAME, height=760, scrolling=False)
