import streamlit as st

st.set_page_config(
    page_title="우주선 선택 | SWINGBY OVER",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "selected_planet" not in st.session_state:
    st.session_state.selected_planet = None

if "selected_ship" not in st.session_state:
    st.session_state.selected_ship = None

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Noto+Sans+KR:wght@400;600;800&display=swap');

.stApp {
    background:radial-gradient(ellipse at 50% 15%,#16163e,#070916 60%,#03040a);
    color:#eef5ff;
}
#MainMenu,footer,header {visibility:hidden;}
[data-testid="stSidebar"] {display:none;}
.block-container {max-width:1400px;padding-top:1rem;}
.title {
    text-align:center;font-size:clamp(1.5rem,3vw,2.3rem);
    font-weight:800;letter-spacing:.04em;margin:12px 0 8px;
    text-shadow:0 0 16px rgba(69,205,255,.4);
}
.subtitle {text-align:center;color:#8298bf;font-size:.85rem;margin-bottom:30px;}
.ship-card {
    height:100%;min-height:350px;padding:24px 20px;
    border:1px solid var(--ship-color);border-radius:16px;
    background:linear-gradient(160deg,rgba(22,30,58,.88),rgba(5,8,21,.96));
    text-align:center;transition:transform .25s ease,box-shadow .25s ease;
}
.ship-card:hover {
    transform:translateY(-6px) scale(1.025);
    box-shadow:0 0 25px color-mix(in srgb,var(--ship-color) 50%,transparent);
}
.ship-visual {
    width:125px;height:150px;margin:12px auto 20px;position:relative;
    filter:drop-shadow(0 0 15px var(--ship-color));
}
.ship-body {
    position:absolute;left:40px;top:5px;width:45px;height:135px;
    background:linear-gradient(90deg,#566c86,#effaff 38%,#7186a2 72%,#283449);
    clip-path:polygon(50% 0,78% 27%,100% 76%,74% 90%,70% 100%,30% 100%,26% 90%,0 76%,22% 27%);
}
.wing {
    position:absolute;top:58px;width:57px;height:66px;
    background:linear-gradient(135deg,#d8f4ff,#526e93 55%,#1c2c4a);
}
.wing.left {left:0;clip-path:polygon(100% 0,90% 100%,0 72%);}
.wing.right {right:0;clip-path:polygon(0 0,100% 72%,10% 100%);}
.engine {
    position:absolute;bottom:0;width:14px;height:24px;
    background:linear-gradient(#fff,#57dfff,#297aff,transparent);
    border-radius:50%;filter:blur(2px);
}
.engine.e1 {left:43px;}
.engine.e2 {left:68px;}
.vulcan .ship-body {width:53px;left:36px;background:linear-gradient(90deg,#3e4652,#e5d8c3 30%,#8a7866 70%,#353b46);}
.vulcan .wing {background:linear-gradient(135deg,#f8d3a2,#6f5c4d 55%,#262b35);}
.vulcan .engine {background:linear-gradient(#fff,#ffb25c,#ff552c,transparent);}
.nova .ship-body {background:linear-gradient(90deg,#453a72,#e3d7ff 35%,#8c67c7 72%,#30224d);}
.nova .wing {background:linear-gradient(135deg,#e6d5ff,#8a65d7 55%,#281d4b);}
.nova .engine {background:linear-gradient(#fff,#d9a0ff,#9b43ff,transparent);}
.ship-name {font-family:'Orbitron','Noto Sans KR',sans-serif;font-size:1.25rem;font-weight:800;margin:10px 0;color:var(--ship-color);}
.ship-stats {text-align:left;line-height:2;color:#c4d1e8;font-size:.86rem;margin:18px auto;max-width:230px;}
.ship-desc {color:#8e9fbe;font-size:.82rem;line-height:1.7;min-height:60px;}
.stButton>button {border:1px solid #49cfff;background:#0a2040;color:#e6faff;border-radius:8px;}
.stButton>button:hover {box-shadow:0 0 16px #2b9bd9;border-color:#a1f1ff;}
</style>
<div class="title">탐사할 우주선의 모양을 고르세요.</div>
<div class="subtitle">CHOOSE YOUR CRAFT · EVERY DESIGN CHANGES YOUR FLIGHT</div>
""", unsafe_allow_html=True)

if not st.session_state.selected_planet:
    st.warning("먼저 탐사 행성을 선택해야 합니다.")
    if st.button("행성 선택으로 돌아가기"):
        st.switch_page("pages/1_행성_선택.py")
    st.stop()

st.markdown(
    f"<p style='text-align:center;color:#9cb4d9;'>"
    f"목적지: <b>{st.session_state.selected_planet}</b>"
    f"</p>",
    unsafe_allow_html=True
)

ships = [
    {
        "id": "ECLIPSE",
        "name": "이클립스",
        "color": "#62dcff",
        "visual": "",
        "efficiency": 5,
        "maneuver": 5,
        "stability": 3,
        "desc": "날렵한 삼각 날개와 경량 선체. 빠른 방향 전환으로 행성의 중력장을 정밀하게 통과합니다.",
        "feature": "기동성 특화",
        "class": ""
    },
    {
        "id": "VULCAN",
        "name": "벌컨",
        "color": "#ffb76b",
        "visual": "",
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
        "visual": "",
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

cols = st.columns(3)

for i, ship in enumerate(ships):
    with cols[i]:
        st.markdown(f"""
        <div class="ship-card" style="--ship-color:{ship['color']}">
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
          <div style="color:{ship['color']};font-weight:700;margin-bottom:10px;">{ship['feature']}</div>
          <div class="ship-desc">{ship['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"{ship['name']} 선택", key=f"ship_{ship['id']}", use_container_width=True):
            st.session_state.selected_ship = ship["id"]
            st.session_state.selected_ship_name = ship["name"]
            st.session_state.selected_ship_stats = {
                "efficiency": ship["efficiency"],
                "maneuver": ship["maneuver"],
                "stability": ship["stability"]
            }

st.write("")

if st.session_state.selected_ship:
    st.success(
        f"선택한 우주선: {st.session_state.selected_ship_name}"
    )
    if st.button("🚀 탐사 준비 완료", type="primary", use_container_width=True):
        st.switch_page("pages/3_스윙바이_게임.py")
else:
    st.info("우주선에 마우스를 올려 설명을 확인하고, 원하는 우주선을 선택하세요.")

if st.button("← 행성 선택으로 돌아가기"):
    st.switch_page("pages/1_행성_선택.py")
