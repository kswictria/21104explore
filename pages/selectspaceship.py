
import streamlit as st

st.set_page_config(
    page_title="SWINGBY OVER | 우주선 선택",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------
# 기본 설정
# ----------------------------------------
if "selected_planet" not in st.session_state:
    st.session_state.selected_planet = "지구"

if "selected_ship" not in st.session_state:
    st.session_state.selected_ship = None

if "selected_ship_name" not in st.session_state:
    st.session_state.selected_ship_name = None

if "selected_ship_stats" not in st.session_state:
    st.session_state.selected_ship_stats = None

if "mission_ready" not in st.session_state:
    st.session_state.mission_ready = False


# ----------------------------------------
# 우주선 데이터
# 능력치는 1~5
# ----------------------------------------
SHIPS = {
    "ECLIPSE": {
        "emoji": "◈",
        "subtitle": "DEEP SPACE EXPLORER",
        "description": "균형 잡힌 성능으로 다양한 중력장에서 안정적인 비행을 수행합니다.",
        "speed": 4,
        "control": 4,
        "defense": 3,
        "color": "#6ee7ff",
        "shape": "diamond",
    },
    "VULCAN": {
        "emoji": "▲",
        "subtitle": "HIGH-THRUST INTERCEPTOR",
        "description": "강력한 추진력으로 빠르게 가속합니다. 초기 속도를 적극적으로 활용하세요.",
        "speed": 5,
        "control": 2,
        "defense": 3,
        "color": "#ff735f",
        "shape": "triangle",
    },
    "NOVA": {
        "emoji": "✦",
        "subtitle": "PRECISION NAVIGATOR",
        "description": "정밀한 조종에 특화되어 있습니다. 행성의 중력을 이용한 궤도 설계에 유리합니다.",
        "speed": 3,
        "control": 5,
        "defense": 4,
        "color": "#c69aff",
        "shape": "star",
    },
}


def stars(value):
    """5단계 능력치를 별로 표시합니다."""
    return "★" * value + "☆" * (5 - value)


def go_to_planets():
    """행성 선택 페이지로 이동합니다."""
    st.switch_page("pages/selectplanet.py")


def select_ship(ship_name):
    """선택한 우주선 정보를 저장합니다."""
    ship = SHIPS[ship_name]

    st.session_state.selected_ship = ship_name
    st.session_state.selected_ship_name = ship_name
    st.session_state.selected_ship_stats = {
        "speed": ship["speed"],
        "control": ship["control"],
        "defense": ship["defense"],
    }
    st.session_state.mission_ready = False


# ----------------------------------------
# CSS 디자인
# ----------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Noto+Sans+KR:wght@400;600;800&display=swap');

    .stApp {
        background:
            radial-gradient(ellipse at 50% 10%, #171a43 0%, #090c20 48%, #03040a 100%);
        color: #eef5ff;
        font-family: 'Noto Sans KR', sans-serif;
    }

    #MainMenu,
    footer,
    header,
    [data-testid="stSidebar"] {
        display: none !important;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    .eyebrow {
        text-align: center;
        color: #7ceaff;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.78rem;
        letter-spacing: 0.3rem;
        margin-bottom: 0.8rem;
    }

    .main-title {
        text-align: center;
        color: #f5f7ff;
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(2rem, 5vw, 3.6rem);
        font-weight: 800;
        letter-spacing: 0.08em;
        margin: 0;
        text-shadow: 0 0 25px rgba(110, 231, 255, 0.28);
    }

    .subtitle {
        text-align: center;
        color: #a9b5d8;
        font-size: 0.95rem;
        margin-top: 0.8rem;
        margin-bottom: 2rem;
    }

    .mission-bar {
        max-width: 900px;
        margin: 0 auto 2rem auto;
        padding: 1rem 1.4rem;
        border: 1px solid rgba(124, 234, 255, 0.25);
        border-radius: 14px;
        background: rgba(16, 25, 55, 0.65);
        text-align: center;
        color: #dbe8ff;
    }

    .mission-label {
        color: #7ceaff;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.7rem;
        letter-spacing: 0.18rem;
    }

    .section-label {
        color: #7ceaff;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.8rem;
        letter-spacing: 0.2rem;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }

    .ship-card {
        min-height: 330px;
        padding: 1.5rem 1.2rem;
        border: 1px solid rgba(142, 165, 255, 0.23);
        border-radius: 20px;
        background: linear-gradient(
            150deg,
            rgba(25, 34, 72, 0.9),
            rgba(7, 11, 28, 0.92)
        );
        text-align: center;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }

    .ship-symbol {
        font-size: 4rem;
        line-height: 1.5;
        margin: 0.5rem 0;
        text-shadow: 0 0 25px currentColor;
    }

    .ship-name {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.4rem;
        font-weight: 800;
        letter-spacing: 0.12rem;
        margin-bottom: 0.35rem;
    }

    .ship-subtitle {
        color: #9baad1;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.65rem;
        letter-spacing: 0.08rem;
        margin-bottom: 1rem;
    }

    .ship-description {
        color: #c4cee8;
        font-size: 0.88rem;
        line-height: 1.8;
        min-height: 78px;
        margin-bottom: 1rem;
    }

    .stat-line {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0.45rem 0;
        font-size: 0.85rem;
    }

    .stat-name {
        color: #b6c2e2;
    }

    .selected-tag {
        color: #7ceaff;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.7rem;
        letter-spacing: 0.15rem;
        margin-top: 0.7rem;
    }

    div.stButton > button {
        width: 100%;
        min-height: 2.8rem;
        border: 1px solid rgba(124, 234, 255, 0.5);
        border-radius: 10px;
        background: rgba(24, 39, 75, 0.85);
        color: #eafaff;
        font-weight: 700;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        border-color: #7ceaff;
        background: rgba(35, 65, 105, 0.95);
        color: white;
        box-shadow: 0 0 18px rgba(124, 234, 255, 0.15);
    }

    div.stButton > button:focus {
        box-shadow: 0 0 0 2px rgba(124, 234, 255, 0.3);
    }

    .footer-note {
        text-align: center;
        color: #7180a8;
        font-size: 0.78rem;
        margin-top: 2rem;
        line-height: 1.8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------
# 상단 제목
# ----------------------------------------
st.markdown(
    '<div class="eyebrow">SWINGBY OVER / FLIGHT SYSTEM</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<h1 class="main-title">SELECT YOUR SPACECRAFT</h1>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">당신의 비행 전략에 맞는 탐사선을 선택하세요.</div>',
    unsafe_allow_html=True,
)

selected_planet = st.session_state.get("selected_planet", "지구")

st.markdown(
    f"""
    <div class="mission-bar">
        <div class="mission-label">CURRENT DESTINATION</div>
        <div style="font-size: 1.35rem; font-weight: 800; margin-top: 0.5rem;">
            {selected_planet}
        </div>
        <div style="font-size: 0.82rem; color: #9baad1; margin-top: 0.3rem;">
            우주선을 선택한 뒤 임무 준비를 완료하세요.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-label">CHOOSE YOUR FLIGHT SYSTEM</div>',
    unsafe_allow_html=True,
)

st.write("")


# ----------------------------------------
# 우주선 선택 카드
# ----------------------------------------
columns = st.columns(3, gap="large")

for column, (ship_name, ship) in zip(columns, SHIPS.items()):
    with column:
        is_selected = st.session_state.selected_ship == ship_name
        color = ship["color"]

        if ship_name == "ECLIPSE":
            symbol = "◇"
        elif ship_name == "VULCAN":
            symbol = "▲"
        else:
            symbol = "✦"

        selected_border = (
            "2px solid " + color
            if is_selected
            else "1px solid rgba(142, 165, 255, 0.23)"
        )

        st.markdown(
            f"""
            <div class="ship-card" style="border: {selected_border};">
                <div class="ship-symbol" style="color: {color};">
                    {symbol}
                </div>
                <div class="ship-name" style="color: {color};">
                    {ship_name}
                </div>
                <div class="ship-subtitle">{ship["subtitle"]}</div>
                <div class="ship-description">{ship["description"]}</div>
                <div class="stat-line">
                    <span class="stat-name">추진 속도</span>
                    <span style="color:{color};">{stars(ship["speed"])}</span>
                </div>
                <div class="stat-line">
                    <span class="stat-name">조종 정밀도</span>
                    <span style="color:{color};">{stars(ship["control"])}</span>
                </div>
                <div class="stat-line">
                    <span class="stat-name">기체 안정성</span>
                    <span style="color:{color};">{stars(ship["defense"])}</span>
                </div>
                {"<div class='selected-tag'>✓ SELECTED</div>" if is_selected else ""}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        button_label = (
            "✓ 선택됨"
            if is_selected
            else f"{ship_name} 선택"
        )

        if st.button(
            button_label,
            key=f"select_{ship_name}",
            use_container_width=True,
        ):
            select_ship(ship_name)
            st.rerun()


# ----------------------------------------
# 선택 결과 및 임무 준비
# ----------------------------------------
st.write("")
st.markdown("---")

selected_name = st.session_state.selected_ship

if selected_name:
    selected = SHIPS[selected_name]

    st.markdown(
        f"""
        <div style="
            text-align:center;
            padding:1.2rem;
            border:1px solid {selected["color"]};
            border-radius:14px;
            background:rgba(12,20,45,0.7);
        ">
            <div style="
                color:{selected["color"]};
                font-family:'Orbitron',sans-serif;
                font-size:0.72rem;
                letter-spacing:0.2rem;
            ">SPACECRAFT CONFIRMED</div>
            <div style="
                color:#f3f7ff;
                font-size:1.35rem;
                font-weight:800;
                margin-top:0.5rem;
            ">{selected_name}</div>
            <div style="color:#b9c6e6;margin-top:0.4rem;">
                목적지: {selected_planet}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    left, right = st.columns(2)

    with left:
        if st.button(
            "← 행성 다시 선택",
            key="back_to_planets",
            use_container_width=True,
        ):
            go_to_planets()

    with right:
        if st.button(
            "임무 준비 완료 ✓",
            key="mission_ready_button",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.mission_ready = True

    if st.session_state.mission_ready:
        st.success(
            f"{selected_name} 탐사선이 {selected_planet} 임무를 위해 준비되었습니다."
        )
        st.info(
            "우주선 선택 정보가 저장되었습니다. "
            "게임 화면과 연결하려면 실제 게임 페이지의 파일 경로에 맞춰 "
            "페이지 이동 코드를 연결해야 합니다."
        )

else:
    st.markdown(
        """
        <div style="
            text-align:center;
            color:#9baad1;
            padding:1rem;
        ">
            먼저 탐사선을 선택하세요.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "← 행성 다시 선택",
        key="back_to_planets_empty",
        use_container_width=True,
    ):
        go_to_planets()


# ----------------------------------------
# 하단 안내
# ----------------------------------------
st.markdown(
    """
    <div class="footer-note">
        SWINGBY OVER · GRAVITY IS YOUR ENGINE<br>
        중력을 이해하고, 궤도를 설계하고, 우주를 탐사하세요.
    </div>
    """,
    unsafe_allow_html=True,
)
