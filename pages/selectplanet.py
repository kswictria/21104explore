import streamlit as st

st.set_page_config(
    page_title="행성 선택 | SWINGBY OVER",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "selected_planet" not in st.session_state:
    st.session_state.selected_planet = None

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Noto+Sans+KR:wght@400;600;800&display=swap');
.stApp {
    background: radial-gradient(ellipse at 50% 40%, #101b3a, #050814 68%, #03040b);
    color: #eef5ff;
}
#MainMenu, footer, header {visibility:hidden;}
[data-testid="stSidebar"] {display:none;}
.block-container {max-width:1450px;padding-top:1rem;}
.title {
    text-align:center; font-size:clamp(1.5rem,3vw,2.3rem);
    font-weight:800; letter-spacing:.04em; margin:12px 0 8px;
    text-shadow:0 0 16px rgba(69,205,255,.4);
}
.subtitle {text-align:center;color:#8298bf;font-size:.85rem;margin-bottom:26px;}
.orbit-scene {
    position:relative; height:310px; overflow:hidden;
    border:1px solid rgba(93,177,255,.18); border-radius:16px;
    background:radial-gradient(ellipse at center,rgba(30,52,105,.28),rgba(2,6,18,.8));
}
.orbit-line {
    position:absolute; left:-5%; width:110%; height:190px;
    border-top:1px solid rgba(179,195,216,.27); border-radius:50%;
    transform:rotate(-5deg);
}
.orbit-a {top:40px;}
.orbit-b {top:95px;transform:rotate(4deg);}
.orbit-c {top:145px;transform:rotate(-3deg);}
.planet-row {
    position:absolute; inset:0; display:flex; align-items:center;
    justify-content:space-around; gap:8px; padding:12px;
}
.planet-wrap {display:flex;flex-direction:column;align-items:center;justify-content:center;flex:1;min-width:0;z-index:2;}
.planet {
    border-radius:50%; position:relative; flex-shrink:0;
    transition:transform .25s ease, filter .25s ease;
}
.planet-wrap:hover .planet {transform:scale(1.16);filter:brightness(1.25);}
.planet:after {
    content:"";position:absolute;inset:-5px;border-radius:50%;
    border:1px solid transparent;transition:all .25s ease;
}
.planet-wrap:hover .planet:after {border-color:#a4eeff;box-shadow:0 0 18px #43cfff;}
.mercury {width:43px;height:43px;background:radial-gradient(circle at 32% 25%,#d8d4cc,#858891 55%,#393e4b);box-shadow:0 0 17px #9ca3b4;}
.venus {width:61px;height:61px;background:radial-gradient(circle at 32% 25%,#ffe6a4,#c98745 58%,#653f2e);box-shadow:0 0 18px #ffbd64;}
.earth {width:70px;height:70px;background:radial-gradient(circle at 35% 25%,#a5f4ff,#2878d7 50%,#132451);box-shadow:0 0 20px #4aafff;overflow:hidden;}
.earth:before {content:"";position:absolute;inset:8px 18px 18px 6px;border-radius:45% 30% 50% 40%;background:#56c58a;transform:rotate(-28deg);}
.mars {width:53px;height:53px;background:radial-gradient(circle at 32% 24%,#ffc09a,#c34c36 55%,#57202d);box-shadow:0 0 17px #ff7359;}
.jupiter {width:104px;height:104px;background:repeating-linear-gradient(0deg,#b8875e 0 9px,#e9d0a4 10px 17px,#956448 18px 23px);box-shadow:0 0 24px #ffca86;overflow:hidden;}
.jupiter:before {content:"";position:absolute;width:24px;height:13px;right:18px;top:55px;border-radius:50%;background:#a9573b;transform:rotate(-12deg);}
.planet-name {font-family:'Orbitron','Noto Sans KR',sans-serif;font-weight:700;margin-top:13px;font-size:.8rem;}
.planet-meta {color:#91a6c8;font-size:.68rem;margin-top:3px;}
.locked {filter:grayscale(.85);opacity:.55;}
.info-card {
    border:1px solid rgba(92,177,255,.28); border-radius:12px;
    padding:17px 18px; min-height:185px;
    background:linear-gradient(145deg,rgba(16,31,61,.75),rgba(6,10,26,.8));
    transition:all .22s ease;
}
.info-card:hover {border-color:#61dfff;box-shadow:0 0 20px rgba(61,185,255,.13);}
.card-head {font-size:1.05rem;font-weight:800;margin-bottom:10px;color:#c7f5ff;}
.stat {color:#aabbd8;font-size:.85rem;line-height:1.9;}
.note {color:#7589ae;font-size:.78rem;}
.stButton > button {border:1px solid #3dcaef;background:#0a2344;color:#e6faff;border-radius:8px;}
.stButton > button:hover {box-shadow:0 0 16px #2b9bd9;border-color:#a1f1ff;}
</style>

<div class="title">탐사할 행성을 선택하세요.</div>
<div class="subtitle">SELECT YOUR DESTINATION · GRAVITY WILL SHAPE YOUR JOURNEY</div>

<div class="orbit-scene">
  <div class="orbit-line orbit-a"></div>
  <div class="orbit-line orbit-b"></div>
  <div class="orbit-line orbit-c"></div>
  <div class="planet-row">
    <div class="planet-wrap">
      <div class="planet mercury"></div>
      <div class="planet-name">수성</div><div class="planet-meta">MERCURY</div>
    </div>
    <div class="planet-wrap">
      <div class="planet venus"></div>
      <div class="planet-name">금성</div><div class="planet-meta">VENUS</div>
    </div>
    <div class="planet-wrap">
      <div class="planet earth"></div>
      <div class="planet-name">지구</div><div class="planet-meta">HOME · LOCKED</div>
    </div>
    <div class="planet-wrap">
      <div class="planet mars"></div>
      <div class="planet-name">화성</div><div class="planet-meta">MARS</div>
    </div>
    <div class="planet-wrap">
      <div class="planet jupiter"></div>
      <div class="planet-name">목성</div><div class="planet-meta">JUPITER</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.write("")

planets = {
    "수성": {
        "g": "0.38 G", "escape": "4.25 km/s",
        "count": 6, "difficulty": "★★☆☆☆",
        "color": "#b9c0cc",
        "description": "태양 가까이에서 빠르게 공전하는 작은 암석 행성. 짧은 항로와 작은 중력장을 활용해 정밀한 스윙바이를 연습합니다."
    },
    "금성": {
        "g": "0.91 G", "escape": "10.36 km/s",
        "count": 9, "difficulty": "★★★☆☆",
        "color": "#ffbd72",
        "description": "두꺼운 대기와 높은 표면 온도를 가진 행성. 게임에서는 항로 오차와 중력 영향에 주의해야 합니다."
    },
    "화성": {
        "g": "0.38 G", "escape": "5.03 km/s",
        "count": 11, "difficulty": "★★★☆☆",
        "color": "#ff8067",
        "description": "얇은 대기와 낮은 표면 중력을 가진 암석 행성. 소행성 지대를 통과하면서 속도와 접근 방향을 조절합니다."
    },
    "목성": {
        "g": "2.53 G", "escape": "약 59.5 km/s",
        "count": 15, "difficulty": "★★★★★",
        "color": "#ffd08c",
        "description": "강력한 중력장을 가진 거대 가스 행성. 중력 도움을 크게 받을 수 있지만 궤도 계산이 까다로운 고난도 임무입니다."
    }
}

cols = st.columns(5)

for i, name in enumerate(["수성", "금성", "지구", "화성", "목성"]):
    with cols[i]:
        if name == "지구":
            st.markdown("""
            <div class="info-card locked">
                <div class="card-head">🔒 지구</div>
                <div class="stat">중력: 1.00 G<br>역할: 출발 행성<br>탐사 경로: 0개</div>
                <p class="note">출발 지점으로 지정되어 선택할 수 없습니다.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            p = planets[name]
            st.markdown(f"""
            <div class="info-card">
                <div class="card-head" style="color:{p['color']}">{name}</div>
                <div class="stat">
                    표면 중력: {p['g']}<br>
                    탈출 속도: {p['escape']}<br>
                    탐사 소행성: {p['count']}개<br>
                    난이도: {p['difficulty']}
                </div>
                <p class="note">{p['description']}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"선택: {name}", key=f"planet_{name}", use_container_width=True):
                st.session_state.selected_planet = name

st.write("")

selected = st.session_state.selected_planet

if selected:
    st.success(f"선택한 목적지: {selected}")
    if st.button("다음 단계 → 우주선 선택", type="primary", use_container_width=True):
        st.switch_page("pages/2_우주선_선택.py")
else:
    st.info("수성, 금성, 화성, 목성 중 하나를 선택하세요. 지구는 출발 행성으로 잠겨 있습니다.")

if st.button("← 메인 화면", use_container_width=False):
    st.switch_page("main.py")
