
import streamlit as st

st.set_page_config(
    page_title="MECHA LAB",
    page_icon="🦾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
[data-testid="stSidebar"],
[data-testid="stSidebarNav"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
}
.stApp {
    background: #131a24;
    color: #f2eadc;
}
.stButton button {
    border-radius: 12px;
    min-height: 3rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style="text-align:center;letter-spacing:5px;color:#f6c38d">
MECHA LAB
</h1>
<p style="text-align:center;color:#bfc7d1">
SPACE ROBOTICS · MISSION SELECT
</p>
""", unsafe_allow_html=True)

st.write(
    "관절을 직접 움직여 우주 작업을 해결하는 "
    "기계공학 퍼즐 게임"
)

missions = [
    (
        "🪨",
        "MISSION 01",
        "화성 암석 집기",
        "3분 · 암석을 집어 목표 구역으로 옮기기",
        "pages/1_화성_암석_집기.py"
    ),
    (
        "🔋",
        "MISSION 02",
        "배터리 분리하기",
        "5분 · 배터리를 잡고 뒤쪽으로 당겨 분리하기",
        "pages/2_배터리_분리.py"
    ),
    (
        "🛰️",
        "MISSION 03",
        "위성 수리",
        "7분 · 장애물 제거 → 버튼 누르기 → 스위치 당기기",
        "pages/3_위성_수리.py"
    )
]

for emoji, number, name, description, path in missions:

    with st.container(border=True):

        icon_col, info_col = st.columns([1, 5])

        icon_col.markdown(
            f'<div style="font-size:55px;text-align:center">{emoji}</div>',
            unsafe_allow_html=True
        )

        info_col.markdown(
            f"**{number} — {name}**"
        )

        info_col.caption(description)

        if info_col.button(
            f"{name} 시작 →",
            key=number,
            use_container_width=True
        ):
            st.switch_page(path)
