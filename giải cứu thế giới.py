
import streamlit as st

st.set_page_config(
    page_title="GIẢI CỨU THẾ GIỚI",
    page_icon="🌳",
    layout="centered"
)

st.title("🌍 GIẢI CỨU THẾ GIỚI")
st.write("🌳 Hãy thu thập 5 viên ngọc, giúp chú thỏ và cứu Cây Cổ Thụ!")

if "started" not in st.session_state:
    st.session_state.started = False
if "player" not in st.session_state:
    st.session_state.player = [3, 3]
if "gems" not in st.session_state:
    st.session_state.gems = set()
if "rabbit" not in st.session_state:
    st.session_state.rabbit = False
if "won" not in st.session_state:
    st.session_state.won = False

if not st.session_state.started:
    st.subheader("✨ Chọn nhân vật của em")

    name = st.text_input("Tên nhân vật", value="Voi")
    gender = st.radio(
        "Em muốn chọn nhân vật nào?",
        ["Nữ tiên rừng 🌿", "Nam phiêu lưu 🧭"]
    )

    if st.button("🌟 BẮT ĐẦU PHIÊU LƯU"):
        st.session_state.name = name.strip() or "Nhà thám hiểm"
        st.session_state.gender = gender
        st.session_state.started = True
        st.rerun()

else:
    name = st.session_state.name
    gender = st.session_state.gender
    player = st.session_state.player

    hero = "🧚" if gender == "Nữ tiên rừng 🌿" else "🧑‍🌾"

    st.subheader(f"Xin chào, {name}! {hero}")
    st.write("Di chuyển bằng các nút mũi tên để khám phá khu rừng.")

    crystals = {
        (0, 1), (1, 3), (2, 5), (4, 1), (5, 4)
    }

    st.write(f"💎 Ngọc đã thu thập: {len(st.session_state.gems)}/5")
    st.write(
        "🐰 Chú thỏ: " +
        ("Đã được giúp đỡ!" if st.session_state.rabbit
         else "Đang cần em giúp!")
    )

    st.markdown("### 🗺️ Bản đồ khu rừng")

    for y in range(7):
        cells = []
        for x in range(7):
            pos = (x, y)

            if pos == tuple(player):
                cell = hero
            elif pos == (6, 0):
                cell = "🌀"
            elif pos == (3, 0):
                cell = "🌳"
            elif pos == (1, 5):
                cell = "🐰"
            elif pos in crystals and pos not in st.session_state.gems:
                cell = "💎"
            elif pos in st.session_state.gems:
                cell = "🟩"
            else:
                cell = "🌲"

            cells.append(cell)

        st.markdown("　".join(cells))

    x, y = player
    current = (x, y)

    if current in crystals and current not in st.session_state.gems:
        st.session_state.gems.add(current)
        st.success("✨ Em đã tìm được một viên ngọc!")
        st.rerun()

    if current == (1, 5) and not st.session_state.rabbit:
        if st.button("🐰 Giúp chú thỏ"):
            st.session_state.rabbit = True
            st.success("Chú thỏ vui vẻ cảm ơn em!")
            st.rerun()

    st.markdown("### 🎮 Điều khiển")

    col1, col2, col3 = st.columns(3)

    with col2:
        if st.button("⬆️ Đi lên", use_container_width=True):
            st.session_state.player[1] = max(0, y - 1)
            st.rerun()

    with col1:
        if st.button("⬅️ Sang trái", use_container_width=True):
            st.session_state.player[0] = max(0, x - 1)
            st.rerun()

    with col2:
        if st.button("⬇️ Đi xuống", use_container_width=True):
            st.session_state.player[1] = min(6, y + 1)
            st.rerun()

    with col3:
        if st.button("➡️ Sang phải", use_container_width=True):
            st.session_state.player[0] = min(6, x + 1)
            st.rerun()

    if current == (6, 0):
        if len(st.session_state.gems) == 5 and st.session_state.rabbit:
            st.session_state.won = True
        else:
            st.info("🌀 Cổng phép thuật cần 5 viên ngọc và chú thỏ được giúp đỡ!")

    if st.session_state.won:
        st.balloons()
        st.success(
            "🎉 CHIẾN THẮNG! Em đã cứu được Cây Cổ Thụ "
            "và giải cứu thế giới!"
        )

    if st.button("🔄 Chơi lại từ đầu"):
        for key in ["started", "player", "gems", "rabbit", "won",
                    "name", "gender"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
