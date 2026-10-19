import streamlit as st

st.set_page_config(
    page_title="우주선 선택 | SWINGBY OVER",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------
# 세션 상태 초기화
# ----------------------------------------
DEFAULTS = {
    "selected_planet": None,
    "selected_ship": None,
    "selected_ship_name": None,
    "selected_ship_stats": None,
    "mission_ready": False,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ----------------------------------------
# 우주선 데이터
# ----------------------------------------
SHIPS = [
    {
        "id": "ECLIPSE",
        "name": "이클립스",
        "color": "#62dcff",
        "efficiency": 5,
        "maneuver": 5,
        "stability": 3,
        "desc": "날렵한 삼각 날개와 경량 선체. 빠른 방향 전환으로 행성의 중력장을 정밀하게 통과합니다.",
        "feature": "기동성 특화",
        "class": "eclipse",
    },
    {
        "id": "VULCAN",
        "name": "벌컨",
        "color": "#ffb76b",
        "efficiency": 3,
        "maneuver": 3,
        "stability": 5,
        "desc": "넓은 선체와 견고한 구조. 궤도 오차에 비교적 안정적이지만 추진 효율은 낮습니다.",
        "feature": "안정성 특화",
        "class": "vulcan",
    },
    {
        "id": "NOVA",
        "name": "노바",
        "color": "#c39aff",
        "efficiency": 5,
        "maneuver": 4,
        "stability": 2,
        "desc": "가벼운 미래형 선체와 고효율 추진 장치. 속도를 확보하기 좋지만 정밀한 접근이 필요합니다.",
        "feature": "추진 효율 특화",
        "class": "nova",
    },
]


def stars(value):
    """5단계 능력치를 별로 표시합니다."""
    return "★" * value + "☆" * (5 - value)


def go_to_planets():
    """행성 선택 페이지로 이동합니다."""
    st.switch_page("pages/selectplanet.py")


# ----------------------------------------
# CSS 디자인
# ----------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Noto+Sans+KR:wght@400;600;800&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 50% 15%, #16163e, #070916 60%, #03040a);
    color: #eef5ff;
}

#MainMenu,
footer,
header,
[data-testid="stSidebar"] {
    display: none !important;
}

.block-container {
    max-width: 1400px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

.title {
    text-align: center;
    font-family: 'Noto Sans
