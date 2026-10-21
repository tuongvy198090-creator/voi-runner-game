
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Gia đình chim cánh cụt",
    page_icon="🐧",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(#e8f8ff, #b9e8f8);
}
.block-container {
    padding-top: 1rem;
    max-width: 1100px;
}
h1 {
    color: #155574;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("🐧 GIA ĐÌNH CHIM CÁNH CỤT VƯỢT SÔNG BĂNG")
st.markdown(
    "<p style='text-align:center;color:#155574'>"
    "Trả lời 9 câu hỏi, vượt sông lấy cá rồi trở về với gia đình!</p>",
    unsafe_allow_html=True
)

game_html = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    font-family: Arial, sans-serif;
    color: #123d53;
    background: linear-gradient(#dff6ff, #9bdcf2);
}
#game { max-width: 850px; margin: auto; padding: 12px; }
.panel {
    background: rgba(255,255,255,.93);
    padding: 14px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 4px 12px #5aa8c433;
    margin-bottom: 12px;
}
h2 { margin: 4px 0 8px; font-size: 21px; }
.small { font-size: 13px; color: #47758a; }
#question { font-size: 19px; font-weight: bold; line-height: 1.4; }
#status { font-weight: bold; min-height: 44px; line-height: 1.5; }
#progress {
    height: 10px; border-radius: 8px;
    background: #d3e9f2; overflow: hidden; margin-top: 10px;
}
#bar { height: 100%; width: 0%; background: #27a7c9; transition: width .3s; }
.bank {
    padding: 14px 8px;
    border: 3px solid #fff;
    border-radius: 20px;
    text-align: center;
    background: linear-gradient(#f7fdff, #d9f4ff);
    margin: 10px 0;
    box-shadow: 0 5px 0 #83c9df;
}
.family { font-size: 38px; letter-spacing: 3px; }
.fish { font-size: 36px; }
#river {
    background: linear-gradient(90deg,#64cce9,#b0edfa,#53bfe1);
    border-radius: 18px;
    padding: 9px;
    border: 3px solid #eafcff;
}
.rowice {
    display: grid;
    grid-template-columns: repeat(3, minmax(0,1fr));
    gap: 7px;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px dashed #ffffff99;
}
.rowlabel {
    grid-column: 1 / -1;
    text-align: center;
    font-size: 11px;
    color: #135d77;
    font-weight: bold;
    margin-bottom: -2px;
}
.ice {
    min-height: 67px;
    border: 2px solid #fff;
    border-radius: 13px;
    background: linear-gradient(145deg,#ffffff,#bceeff);
    color: #15516c;
    font-size: 14px;
    font-weight: bold;
    padding: 7px 3px;
    cursor: pointer;
    box-shadow: 0 5px 0 #72bad4;
    transition: transform .15s, opacity .2s;
    overflow-wrap: anywhere;
}
.ice:active { transform: translateY(4px); box-shadow: none; }
.ice .emoji { display:block; font-size: 23px; margin-bottom: 3px; }
.ice:disabled { cursor: default; opacity: .72; }
.ice.cracked {
    background: linear-gradient(145deg,#e3faff,#a2ddec);
    border-color: #5a9eb9;
}
.ice.sunk {
    background: #368eae;
    color: #e1f8ff;
    opacity: .8;
    box-shadow: none;
    transform: translateY(7px);
}
.ice .sub { display:block; font-size:10px; margin-top:3px; }
button.action {
    border: 0; border-radius: 13px;
    background: #087fa7; color: white;
    font-size: 16px; font-weight: bold;
    padding: 13px 18px; cursor: pointer;
    margin: 5px;
}
button.action:hover { background: #086888; }
#controls { text-align:center; padding: 10px 0; }
#startscreen { text-align:center; padding: 8px; }
.hidden { display:none !important; }
.note { font-size: 12px; color: #356a80; line-height:1.5; }
@media(max-width:480px) {
    #game { padding: 5px; }
    .ice { font-size:12px; min-height:65px; }
    #question { font-size:17px; }
    .family { font-size:32px; }
}
</style>
</head>
<body>
<div id="game">

  <div class="panel" id="startscreen">
    <div style="font-size:58px">🐧 ❄️ 🐧</div>
    <h2>Cuộc phiêu lưu Bắc Cực</h2>
    <p>Mẹ chim cánh cụt và 4 con đang đói bụng!</p>
    <p>Nhiệm vụ của em là vượt 9 hàng băng, lấy thùng cá
    và mang cá trở về cho gia đình.</p>
    <button class="action" onclick="startGame()">▶ BẮT ĐẦU CHƠI</button>
  </div>

  <div id="playarea" class="hidden">
    <div class="panel">
      <div id="phase" class="small">LƯỢT ĐI · CÂU 1/9</div>
      <div id="question">Câu hỏi sẽ hiện ở đây</div>
      <div id="answershint" class="small">
        Nhảy lên tảng băng mang đáp án đúng!
      </div>
      <div id="progress"><div id="bar"></div></div>
      <p id="status">Chọn một tảng băng để bắt đầu.</p>
    </div>

    <div class="bank">
      <div class="family">🐧 🐧 🐧 🐧 🐧</div>
      <b>🏠 BỜ GIA ĐÌNH</b>
      <div class="small">Mẹ và 4 chim cánh cụt con</div>
    </div>

    <div id="river"></div>

    <div class="bank">
      <div class="fish">📦 🐟 🐟</div>
      <b>🐟 BỜ KHO CÁ</b>
      <div class="small">Đích đến lấy cá!</div>
    </div>

    <div id="controls" class="panel">
      <div id="instruction">Chọn đáp án ở hàng đang được đánh dấu.</div>
      <button id="continue" class="action hidden" onclick="beginReturn()">
        🐟 LẤY CÁ, QUAY VỀ
      </button>
      <button id="restart" class="action" onclick="startGame()">
        🔄 Chơi lượt mới
      </button>
      <p class="note">
        Băng yếu: lần đầu nứt nhẹ, lần thứ hai chìm sâu hơn,
        lần thứ ba chìm hẳn. Mỗi lượt mới, băng được hồi phục.
      </p>
    </div>
  </div>
</div>

<script>
const questions = [
  {
    q:"Toán: 3/4 + 1/4 bằng bao nhiêu?",
    a:["1","1/2","2"], c:0
  },
  {
    q:"Địa lí: Bắc Cực nằm chủ yếu ở đâu?",
    a:["Nam Cực","Vùng quanh Bắc Băng Dương","Sa mạc Sahara"], c:1
  },
  {
    q:"Tiếng Anh: Từ nào có nghĩa là 'chim cánh cụt'?",
    a:["Penguin","Dolphin","Eagle"], c:0
  },
  {
    q:"Khoa học: Nước đóng băng khi nhiệt độ khoảng bao nhiêu ở điều kiện thường?",
    a:["100°C","50°C","0°C"], c:2
  },
  {
    q:"Ngữ văn: Từ nào là từ láy?",
    a:["Long lanh","Học sinh","Bàn ghế"], c:0
  },
  {
    q:"Toán: 7 × 8 bằng bao nhiêu?",
    a:["54","56","64"], c:1
  },
  {
    q:"Sinh học: Động vật nào là thú?",
    a:["Cá mập","Ếch","Cá voi"], c:2
  },
  {
    q:"Địa lí: Nước biển đóng băng tạo thành gì?",
    a:["Băng biển","Đất đỏ","Cát nóng"], c:0
  },
  {
    q:"Tiếng Anh: 'Fish' có nghĩa là gì?",
    a:["Chim","Cá","Băng"], c:1
  }
];

let order = [];
let weak = [];
let hits = [];
let rowOptions = [];
let row = 0;
let phase = "out";
let started = false;
let finished = false;
let carryingFish = false;

function shuffle(arr) {
  let a = arr.slice();
  for (let i=a.length-1;i>0;i--) {
    let j=Math.floor(Math.random()*(i+1));
    [a[i],a[j]]=[a[j],a[i]];
  }
  return a;
}

function startGame() {
  order = shuffle(questions.map((q,i)=>i));
  weak = Array.from({length:9},()=>Math.floor(Math.random()*3));
  hits = Array(9).fill(0);
  rowOptions = [];
  for(let i=0;i<9;i++) {
    let q=questions[order[i]];
    let opts=shuffle([0,1,2]);
    rowOptions.push(opts);
  }
  row=0;
  phase="out";
  started=true;
  finished=false;
  carryingFish=false;
  document.getElementById("startscreen").classList.add("hidden");
  document.getElementById("playarea").classList.remove("hidden");
  document.getElementById("continue").classList.add("hidden");
  document.getElementById("restart").classList.remove("hidden");
  document.getElementById("status").textContent =
    "🐧 Hãy giúp gia đình tìm thùng cá nhé!";
  render();
}

function render() {
  const river=document.getElementById("river");
  river.innerHTML="";
  for(let i=8;i>=0;i--) {
    let r=document.createElement("div");
    r.className="rowice";
    let label=document.createElement("div");
    label.className="rowlabel";
    let current = phase==="out" ? row===i : row===i;
    label.textContent="HÀNG "+(i+1)+(current?" · 🐧 ĐANG Ở ĐÂY":"");
    r.appendChild(label);

    for(let j=0;j<3;j++) {
      let b=document.createElement("button");
      b.className="ice";
      let isWeak=weak[i]===j;
      if(isWeak && hits[i]===1) b.classList.add("cracked");
      if(isWeak && hits[i]>=2) b.classList.add("sunk");

      let labelText="";
      if(phase==="out") {
        let original=rowOptions[i][j];
        labelText=questions[order[i]].a[original];
      } else {
        labelText=["Nhảy sang đây","Nhảy sang đây","Nhảy sang đây"][j];
      }

      let emoji="🧊";
      if(isWeak && hits[i]===1) emoji="🧊";
      if(isWeak && hits[i]>=2) emoji="🌊";
      b.innerHTML='<span class="emoji">'+emoji+'</span>'+
        labelText+
        (isWeak && hits[i]===1?'<span class="sub">Có vết nứt</span>':
        (isWeak && hits[i]>=2?'<span class="sub">Băng đã chìm</span>':''));

      b.disabled = !current || finished ||
        (phase==="out" && i!==row) ||
        (phase==="back" && i!==row) ||
        (phase==="out" && isWeak && hits[i]>=2);

      b.onclick=()=>choose(i,j);
      r.appendChild(b);
    }
    river.appendChild(r);
  }

  if(phase==="out") {
    let q=questions[order[row]];
    document.getElementById("phase").textContent =
      "LƯỢT ĐI · CÂU "+(row+1)+"/9";
    document.getElementById("question").textContent=q.q;
    document.getElementById("answershint").textContent =
      "Chọn A, B hoặc C bằng cách nhảy lên tảng băng!";
    document.getElementById("bar").style.width=(row/18*100)+"%";
    document.getElementById("instruction").textContent=
      "Đang ở hàng "+(row+1)+". Hãy chọn đáp án.";
  } else if(phase==="back") {
    document.getElementById("phase").textContent=
      "LƯỢT VỀ · HÀNG "+(row+1)+"/9";
    document.getElementById("question").textContent=
      "Đã lấy cá! Chọn một tảng băng để nhảy về nhà.";
    document.getElementById("answershint").textContent=
      "Cẩn thận những tảng băng yếu nhé!";
    document.getElementById("bar").style.width=
      ((9+(8-row))/18*100)+"%";
    document.getElementById("instruction").textContent=
      "Đưa thùng cá về với mẹ và 4 chim con!";
  }
}

function choose(i,j) {
  if(finished || i!==row) return;

  const isWeak=(weak[i]===j);
  if(isWeak) {
    hits[i]++;
    if(hits[i]===1) {
      document.getElementById("status").textContent=
        "⚠️ Rắc! Tảng băng yếu chìm một nửa! Em vẫn có thể đi tiếp.";
    } else if(hits[i]===2) {
      document.getElementById("status").textContent=
        "⚠️ Băng chìm sâu hơn rồi! Hãy thật cẩn thận.";
    } else {
      document.getElementById("status").textContent=
        "💦 BĂNG CHÌM HẲN! Chim cánh cụt rơi xuống nước. Quay lại bờ!";
      setTimeout(startGame,1800);
      return;
    }
  } else {
    document.getElementById("status").textContent=
      "🧊 Tảng băng chắc chắn! Nhảy tốt lắm!";
  }

  if(phase==="out") {
    let q=questions[order[i]];
    let selected=rowOptions[i][j];
    if(selected!==q.c) {
      document.getElementById("status").textContent=
        "❄️ Chưa đúng rồi! Hãy thử đáp án khác ở hàng này nhé.";
      render();
      return;
    }

    document.getElementById("status").textContent=
      "🎉 Chính xác! Chim cánh cụt nhảy sang hàng tiếp theo.";
    row++;
    if(row>=9) {
      phase="fish";
      document.getElementById("phase").textContent="ĐÃ ĐẾN BỜ KHO CÁ!";
      document.getElementById("question").textContent=
        "Giỏi quá! Em đã trả lời xong 9 câu hỏi.";
      document.getElementById("answershint").textContent=
        "Nhấn nút bên dưới để lấy cá và quay về.";
      document.getElementById("bar").style.width="50%";
      document.getElementById("instruction").textContent=
        "Thùng cá đã ở ngay trước mặt em!";
      document.getElementById("continue").classList.remove("hidden");
      renderRiverOnly();
      return;
    }
  } else if(phase==="back") {
    row--;
    if(row<0) {
      finished=true;
      phase="win";
      carryingFish=true;
      document.getElementById("phase").textContent="CHIẾN THẮNG!";
      document.getElementById("question").textContent=
        "🐧🐧🐧🐧🐧 CẢ GIA ĐÌNH ĐÃ ĐOÀN TỤ!";
      document.getElementById("answershint").textContent=
        "Em đã mang cá về an toàn!";
      document.getElementById("bar").style.width="100%";
      document.getElementById("status").textContent=
        "🏆 TUYỆT VỜI! Gia đình chim cánh cụt có bữa ăn ngon!";
      document.getElementById("instruction").textContent=
        "Em đã hoàn thành trò chơi!";
      document.getElementById("continue").classList.add("hidden");
      renderRiverOnly();
      return;
    }
  }
  render();
}

function renderRiverOnly() {
  const river=document.getElementById("river");
  river.innerHTML=
    '<div class="panel" style="background:#e8faff">'+
    '<div style="font-size:42px">'+
    (phase==="win"?"🐧🐧🐧🐧🐧":"📦🐟🐟")+
    '</div><b>'+
    (phase==="win"?"Gia đình đã đoàn tụ!":"Em đã lấy được thùng cá!")+
    '</b></div>';
}

function beginReturn() {
  phase="back";
  row=8;
  carryingFish=true;
  document.getElementById("continue").classList.add("hidden");
  document.getElementById("status").textContent=
    "🐟 Đã lấy cá! Bây giờ hãy vượt sông trở về.";
  render();
}
</script>
</body>
</html>
"""

components.html(game_html, height=1500, scrolling=True)

st.caption(
    "Mẹo: Khi bắt đầu lượt mới, các tảng băng và bộ đếm băng yếu "
    "được đặt lại. Đây là bản đầu tiên để em thử cách chơi."
)
