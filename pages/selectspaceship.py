```python
import streamlit as st

st.set_page_config(
    page_title="우주선 선택 | SWINGBY OVER",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# 세션 상태 초기화
# -----------------------------
defaults = {
    "selected_planet": None,
    "selected_ship": None,
    "selected_ship_name": None,
    "selected_ship_stats": None,
    "mission_ready": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Noto+Sans+KR:wght@400;600;800&display=swap');

.stApp {
    background: radial-gradient(ellipse at 50% 15%, #16163e, #070916 60%, #03040a);
    color: #eef5ff;
}
#MainMenu, footer, header, [data-testid="stSidebar"] {
    display: none !important;
}
.block-container {
    max-width: 1400px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}
.title {
    text-align: center;
    font-family: 'Noto Sans KR', sans-serif;
    font-size: clamp(1.5rem, 3vw, 2.3rem);
    font-weight: 800;
    letter-spacing: .04em;
    margin: 12px 0 8px;
    text-shadow: 0 0 16px rgba(69, 205, 255, .4);
}
.subtitle {
    text-align: center;
    color: #8298bf;
    font-family: 'Orbitron', sans-serif;
    font-size: .75rem;
    margin-bottom: 20px;
    letter-spacing: .08em;
}

/* 우주선 카드 */
.ship-card {
    box-sizing: border-box;
    min-height: 365px;
    padding: 22px 18px;
    border: 1px solid var(--ship-color);
    border-radius: 16px;
    background: linear-gradient(160deg, rgba(22,30,58,.92), rgba(5,8,21,.97));
    text-align: center;
    transition: transform .25s ease, box-shadow .25s ease;
}
.ship-card:hover {
    transform: translateY(-6px) scale(1.025);
    box-shadow: 0 0 25px var(--ship-glow);
}
.ship-visual {
    width: 125px;
    height: 150px;
    margin: 12px auto 20px;
    position: relative;
    filter: drop-shadow(0 0 15px var(--ship-color));
    transition: transform .25s ease;
}
.ship-card:hover .ship-visual {
    transform: scale(1.08);
}
.ship-body {
    position: absolute;
    left: 40px;
    top: 5px;
    width: 45px;
    height: 135px;
    background: linear-gradient(90deg,#566c86,#effaff 38%,#7186a2 72%,#283449);
    clip-path: polygon(50% 0,78% 27%,100% 76%,74% 90%,70% 100%,30% 100%,26% 90%,0 76%,22% 27%);
}
.wing {
    position: absolute;
    top: 58px;
    width: 57px;
    height: 66px;
    background: linear-gradient(135deg,#d8f4ff,#526e93 55%,#1c2c4a);
}
.wing.left {
    left: 0;
    clip-path: polygon(100% 0,90% 100%,0 72%);
}
.wing.right {
    right: 0;
    clip-path: polygon(0 0,100% 72%,10% 100%);
}
.engine {
    position: absolute;
    bottom: 0;
    width: 14px;
    height: 24px;
    background: linear-gradient(#fff,#57dfff,#297aff,transparent);
    border-radius: 50%;
    filter: blur(2px);
}
.engine.e1 { left: 43px; }
.engine.e2 { left: 68px; }

/* 벌컨 */
.vulcan .ship-body {
    width: 53px;
    left: 36px;
    background: linear-gradient(90deg,#3e4652,#e5d8c3 30%,#8a7866 70%,#353b46);
}
.vulcan .wing {
    background: linear-gradient(135deg,#f8d3a2,#6f5c4d 55%,#262b35);
}
.vulcan .engine {
    background: linear-gradient(#fff,#ffb25c,#ff552c,transparent);
}

/* 노바 */
.nova .ship-body {
    background: linear-gradient(90deg,#453a72,#e3d7ff 35%,#8c67c7 72%,#30224d);
}
.nova .wing {
    background: linear-gradient(135deg,#e6d5ff,#8a65d7 55%,#281d4b);
}
.nova .engine {
    background: linear-gradient(#fff,#d9a0ff,#9b43ff,transparent);
}

/* 이클립스 */
.eclipse .wing {
    width: 61px;
    height: 74px;
    top: 54px;
}

.ship-name {
    font-family: 'Orbitron','Noto Sans KR',sans-serif;
    font-size: 1.2rem;
    font-weight: 800;
    margin: 10px 0;
    color: var(--ship-color);
}
.ship-stats {
    text-align: left;
    line-height: 2;
    color: #c4d1e8;
    font-size: .83rem;
    margin: 18px auto;
    max-width: 230px;
}
.ship-desc {
    color: #a0b0cd;
    font-size: .82rem;
    line-height: 1.7;
    min-height: 68px;
}
.ship-feature {
    font-weight: 800;
    margin: 10px 0;
}
.stButton > button {
    border: 1px solid #49cfff;
    background: #0a2040;
    color: #e6faff;
    border-radius: 8px;
    transition: all .2s ease;
}
.stButton > button:hover {
    box-shadow: 0 0 16px #2b9bd9;
    border-color: #a1f1ff;
}
.ready-panel {
    padding: 20px;
    margin-top: 15px;
    border: 1px solid rgba(73,207,255,.4);
    border-radius: 14px;
    background: rgba(8,26,52,.75);
    text-align: center;
}
@media (max-width: 700px) {
    .ship-card { min-height: auto; }
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# 제목
# -----------------------------
st.markdown("""
<div class="title">탐사할 우주선의 모양을 고르세요.</div>
<div class="subtitle">
CHOOSE YOUR CRAFT · EVERY DESIGN CHANGES YOUR FLIGHT
</div>
""", unsafe_allow_html=True)


# -----------------------------
# 목적지 확인
# -----------------------------
selected_planet = st.session_state.get("selected_planet")

if not selected_planet:
    st.warning("먼저 행성 선택 화면에서 탐사할 목적지를 선택해 주세요.")
    if st.button("← 행성 선택으로 돌아가기"):
        st.switch_page("pages/selectplanet.py")
    st.stop()

st.markdown(
    f"""
    <div style="text-align:center;color:#9cb4d9;margin:12px 0 24px;font-size:1rem;">
        DESTINATION / <b style="color:#d7f5ff;">{selected_planet}</b>
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# 우주선 데이터
# -----------------------------
ships = [
    {
        "id": "ECLIPSE",
        "name": "이클립스",
        "color": "#62dcff",
        "efficiency": 5,
        "maneuver": 5,
        "stability": 3,
        "desc": "날렵한 삼각 날개와 경량 선체. 빠른 방향 전환으로 행성의 중력장을 정밀하게 통과합니다.",
        "feature": "기동성 특화",
        "class": "eclipse"
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
        "class": "vulcan"
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
        "class": "nova"
    }
]

def stars(value):
    return "★" * value + "☆" * (5 - value)


# -----------------------------
# 우주선 카드 렌더링
# -----------------------------
cols = st.columns(3, gap="large")

for i, ship in enumerate(ships):
    with cols[i]:
        st.markdown(
            f"""
            <div class="ship-card"
                 style="--ship-color:{ship['color']};--ship-glow:0 0 25px {ship['color']}66;">
                <div class="ship-visual {ship['class']}">
                    <div class="ship-body"></div>
                    <div class="wing left"></div>
                    <div class="wing right"></div>
                    <div class="engine e1"></div>
                    <div class="engine e2"></div>
                </div>
                <div class="ship-name">{ship['name']}</div>
                <div style="color:{ship['color']};font-size:.72rem;letter-spacing:.15em;">{ship['id']}</div>
                <div class="ship-stats">
                    추진 효율　{stars(ship['efficiency'])}<br>
                    기동성　　{stars(ship['maneuver'])}<br>
                    안정성　　{stars(ship['stability'])}
                </div>
                <div class="ship-feature" style="color:{ship['color']};">{ship['feature']}</div>
                <div class="ship-desc">{ship['desc']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        is_selected = st.session_state.selected_ship == ship["id"]
        label = f"✓ {ship['name']} 선택됨" if is_selected else f"{ship['name']} 선택"

        if st.button(
            label,
            key=f"ship_{ship['id']}",
            use_container_width=True,
            type="primary" if is_selected else "secondary"
        ):
            st.session_state.selected_ship = ship["id"]
            st.session_state.selected_ship_name = ship["name"]
            st.session_state.selected_ship_stats = {
                "efficiency": ship["efficiency"],
                "maneuver": ship["maneuver"],
                "stability": ship["stability"]
            }
            st.session_state.mission_ready = False
            st.rerun()


# -----------------------------
# 선택 결과
# -----------------------------
st.write("")

if st.session_state.selected_ship:
    ship_name = st.session_state.selected_ship_name
    stats = st.session_state.selected_ship_stats or {}

    st.markdown(
        f"""
        <div class="ready-panel">
            <div style="color:#72e5ff;font-size:.78rem;letter-spacing:.16em;">
                SPACECRAFT CONFIGURATION
            </div>
            <h3 style="color:#f0f8ff;margin:12px 0;">{ship_name}</h3>
            <p style="color:#a9bddc;margin:0;">
                목적지: {selected_planet}
                &nbsp; | &nbsp; 기동성: {stats.get('maneuver', '-')} / 5
                &nbsp; | &nbsp; 안정성: {stats.get('stability', '-')} / 5
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if st.button("🚀 탐사 준비 완료", type="primary", use_container_width=True):
        st.session_state.mission_ready = True

    if st.session_state.mission_ready:
        st.success(
            f"탐사 준비 완료! {selected_planet} 탐사에 {ship_name} 우주선을 선택했습니다."
        )
        st.info("스윙바이 게임 페이지를 연결하면 이 단계에서 게임으로 이동할 수 있습니다.")
else:
    st.info("우주선을 선택하세요. 우주선마다 추진 효율, 기동성, 안정성이 다릅니다.")


st.divider()

if st.button("← 행성 선택으로 돌아가기"):
    st.switch_page("pages/selectplanet.py")
```
