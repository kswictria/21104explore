
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
    background:
        radial-gradient(ellipse at 50% 48%, rgba(28,48,99,.35), transparent 48%),
        radial-gradient(ellipse at 85% 10%, rgba(70,30,110,.16), transparent 38%),
        linear-gradient(145deg,#030611,#080b1d 58%,#10071d);
    color: #eef5ff;
}
#MainMenu, footer, header, [data-testid="stSidebar"] {
    display:none !important;
}
.block-container {
    max-width:1500px !important;
    padding:1.1rem 2rem 2rem !important;
}
.title {
    text-align:center;
    font-family:'Noto Sans KR',sans-serif;
    font-size:clamp(1.5rem,3vw,2.3rem);
    font-weight:800;
    letter-spacing:.04em;
    margin:12px 0 8px;
    text-shadow:0 0 16px rgba(69,205,255,.4);
}
.subtitle {
    text-align:center;
    color:#8298bf;
    font-size:.78rem;
    letter-spacing:.12em;
    margin-bottom:25px;
}

/* 궤도 장면 */
.orbit-scene {
    position:relative;
    height:350px;
    overflow:hidden;
    border:1px solid rgba(93,177,255,.15);
    border-radius:16px;
    background:
        radial-gradient(ellipse at 50% 48%,rgba(30,52,105,.25),transparent 60%),
        rgba(2,6,18,.5);
    margin-bottom:12px;
}
.orbit-scene:before {
    content:"";
    position:absolute;
    inset:0;
    background-image:
        radial-gradient(1px 1px at 8% 20%,#fff 99%,transparent),
        radial-gradient(2px 2px at 24% 76%,#6ddfff 99%,transparent),
        radial-gradient(1px 1px at 45% 25%,#fff 99%,transparent),
        radial-gradient(2px 2px at 70% 68%,#9d8cff 99%,transparent),
        radial-gradient(1px 1px at 91% 33%,#fff 99%,transparent);
    background-size:180px 140px;
    pointer-events:none;
}
.orbit {
    position:absolute;
    left:50%;
    top:50%;
    width:125%;
    height:190px;
    border:1px solid rgba(185,199,218,.26);
    border-radius:50%;
    transform:translate(-50%,-50%) rotate(-5deg);
    pointer-events:none;
}
.orbit.o2 {
    width:108%;
    height:260px;
    transform:translate(-50%,-50%) rotate(7deg);
    border-color:rgba(185,199,218,.22);
}
.orbit.o3 {
    width:91%;
    height:320px;
    transform:translate(-50%,-50%) rotate(-9deg);
    border-color:rgba(185,199,218,.18);
}
.scene-label {
    position:absolute;
    top:14px;
    left:18px;
    color:#7f9dc8;
    font-size:10px;
    letter-spacing:.16em;
    z-index:2;
}

/* 실제 행성 표면 */
.planet-row {
    position:absolute;
    inset:0;
    display:flex;
    align-items:center;
    justify-content:space-around;
    padding:10px 16px;
    gap:10px;
    z-index:2;
}
.planet-slot {
    flex:1;
    min-width:0;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
}
.planet {
    position:relative;
    flex-shrink:0;
    border-radius:50%;
    cursor:pointer;
    transition:transform .25s ease,filter .25s ease,box-shadow .25s ease;
}
.planet:hover {
    transform:scale(1.15);
    filter:brightness(1.2);
}
.mercury {
    width:47px;height:47px;
    background:
      radial-gradient(circle at 30% 25%,#e5e0d8 0%,#b2b0ad 20%,#777b83 53%,#343945 82%);
    box-shadow:0 0 15px rgba(174,190,214,.3);
}
.venus {
    width:65px;height:65px;
    background:
      radial-gradient(circle at 30% 24%,#fff0c2 0%,#e7bd79 24%,#bb794b 57%,#633d35 85%);
    box-shadow:0 0 19px rgba(255,181,101,.22);
}
.earth {
    width:73px;height:73px;
    overflow:hidden;
    background:
      radial-gradient(circle at 32% 24%,#a7efff 0%,#388ee0 35%,#1851a0 72%,#091c4a 100%);
    box-shadow:0 0 20px rgba(70,165,255,.35);
}
.earth:before {
    content:"";
    position:absolute;
    left:8px;top:17px;
    width:32px;height:28px;
    background:#4bc58b;
    border-radius:48% 32% 45% 38%;
    transform:rotate(-27deg);
}
.earth:after {
    content:"";
    position:absolute;
    right:10px;bottom:12px;
    width:19px;height:13px;
    background:#54c68b;
    border-radius:50% 40% 55% 30%;
    transform:rotate(30deg);
}
.mars {
    width:55px;height:55px;
    background:
      radial-gradient(circle at 30% 24%,#ffd0ad 0%,#e77a56 30%,#b83f35 60%,#57202d 88%);
    box-shadow:0 0 17px rgba(255,104,86,.25);
}
.jupiter {
    width:108px;height:108px;
    overflow:hidden;
    background:
      repeating-linear-gradient(
        0deg,
        #9d704f 0px,#c99b70 8px,#ead1a8 15px,
        #b9845e 23px,#e1bd8e 31px
      );
    box-shadow:0 0 24px rgba(255,192,123,.3);
}
.jupiter:after {
    content:"";
    position:absolute;
    right:17px;top:55px;
    width:25px;height:14px;
    border-radius:50%;
    background:#a9573b;
    transform:rotate(-13deg);
}
.planet-name {
    margin-top:15px;
    font-family:'Orbitron','Noto Sans KR',sans-serif;
    font-weight:800;
    font-size:.84rem;
    color:#e5f0ff;
    text-shadow:0 0 12px rgba(100,190,255,.25);
}
.planet-en {
    margin-top:3px;
    color:#8097bc;
    font-size:.62rem;
    letter-spacing:.12em;
}
.locked-label {color:#747f96;}

/* 선택 이벤트용 클릭 영역 */
.planet-hit {
    width:100%;
    display:flex;
    justify-content:center;
}
.planet-hit [data-testid="stButton"] {
    width:100%;
}
.planet-hit [data-testid="stButton"] button {
    background:transparent !important;
    border:1px solid transparent !important;
    box-shadow:none !important;
    color:transparent !important;
    height:1px !important;
    min-height:1px !important;
    padding:0 !important;
    margin:0 !important;
}
.planet-hit [data-testid="stButton"] button p {
    color:transparent !important;
    font-size:1px !important;
}

/* 정보卡 */
.info-card {
    border:1px solid rgba(92,177,255,.25);
    border-radius:12px;
    padding:15px;
    min-height:205px;
    background:linear-gradient(145deg,rgba(16,31,61,.75),rgba(6,10,26,.8));
}
.card-head {
    font-size:1.02rem;
    font-weight:800;
    margin-bottom:9px;
}
.stat {
    color:#b9c9e2;
    font-size:.79rem;
    line-height:1.9;
}
.note {
    color:#8397b8;
    font-size:.73rem;
    line-height:1.6;
    margin-top:8px;
}
.locked-card {opacity:.48;}
.stButton>button {
    border:1px solid #3dcaef;
    background:#0a2344;
    color:#e6faff;
    border-radius:8px;
}
.stButton>button:hover {
    box-shadow:0 0 16px #2b9bd9;
    border-color:#a1f1ff;
}
@media(max-width:800px) {
    .block-container {padding-left:.5rem !important;padding-right:.5rem !important;}
    .orbit-scene {height:290px;}
    .mercury {width:30px;height:30px;}
    .venus {width:43px;height:43px;}
    .earth {width:48px;height:48px;}
    .mars {width:36px;height:36px;}
    .jupiter {width:66px;height:66px;}
    .planet-name {font-size:.68rem;}
    .planet-en {font-size:.5rem;}
    .info-card {padding:8px;min-height:250px;}
    .stat {font-size:.67rem;}
    .note {font-size:.65rem;}
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">탐사할 행성을 선택하세요.</div>'
    '<div class="subtitle">SELECT YOUR DESTINATION · GRAVITY WILL SHAPE YOUR JOURNEY</div>',
    unsafe_allow_html=True
)

planets = {
    "수성": {
        "gravity": "0.38 G", "escape": "4.25 km/s",
        "count": 6, "difficulty": "★★☆☆☆",
        "color": "#c1c9d6",
        "description": "작은 암석 행성입니다. 짧은 항로에서 중력 도움을 연습하기 좋습니다."
    },
    "금성": {
        "gravity": "0.90 G", "escape": "10.36 km/s",
        "count": 9, "difficulty": "★★★☆☆",
        "color": "#ffbd72",
        "description": "두꺼운 대기와 높은 표면 온도를 가진 행성입니다. 정밀한 궤도 조절이 필요합니다."
    },
    "화성": {
        "gravity": "0.38 G", "escape": "5.03 km/s",
        "count": 11, "difficulty": "★★★☆☆",
        "color": "#ff8067",
        "description": "얇은 대기를 가진 암석 행성입니다. 소행성 지대를 통과하며 속도와 방향을 조절합니다."
    },
    "목성": {
        "gravity": "2.53 G", "escape": "약 59.5 km/s",
        "count": 15, "difficulty": "★★★★★",
        "color": "#ffd08c",
        "description": "강력한 중력을 가진 거대 가스 행성입니다. 중력 도움을 크게 받을 수 있지만 난도가 높습니다."
    }
}

# 궤도와 행성 장면
st.markdown("""
<div class="orbit-scene">
  <div class="scene-label">SOLAR SYSTEM / DESTINATION SELECT</div>
  <div class="orbit"></div>
  <div class="orbit o2"></div>
  <div class="orbit o3"></div>
  <div class="planet-row">
    <div class="planet-slot">
      <div class="planet mercury"></div>
      <div class="planet-name">수성</div>
      <div class="planet-en">MERCURY</div>
    </div>
    <div class="planet-slot">
      <div class="planet venus"></div>
      <div class="planet-name">금성</div>
      <div class="planet-en">VENUS</div>
    </div>
    <div class="planet-slot">
      <div class="planet earth"></div>
      <div class="planet-name locked-label">지구</div>
      <div class="planet-en">HOME · LOCKED</div>
    </div>
    <div class="planet-slot">
      <div class="planet mars"></div>
      <div class="planet-name">화성</div>
      <div class="planet-en">MARS</div>
    </div>
    <div class="planet-slot">
      <div class="planet jupiter"></div>
      <div class="planet-name">목성</div>
      <div class="planet-en">JUPITER</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# 클릭 이벤트는 Streamlit 위젯으로 처리
# 각 행성 이름을 누르면 즉시 다음 페이지로 이동
st.markdown("### 목적지 정보")

cols = st.columns(5, gap="small")
order = ["수성", "금성", "지구", "화성", "목성"]

for col, name in zip(cols, order):
    with col:
        if name == "지구":
            st.markdown("""
            <div class="info-card locked-card">
              <div class="card-head">🔒 지구</div>
              <div class="stat">
                표면 중력: 1.00 G<br>
                역할: 출발 행성<br>
                선택: 불가능
              </div>
              <div class="note">출발 지점으로 지정되어 목적지로 선택할 수 없습니다.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            p = planets[name]
            st.markdown(f"""
            <div class="info-card">
              <div class="card-head" style="color:{p['color']}">{name}</div>
              <div class="stat">
                표면 중력: {p['gravity']}<br>
                탈출 속도: {p['escape']}<br>
                탐사 소행성: {p['count']}개<br>
                난이도: {p['difficulty']}
              </div>
              <div class="note">{p['description']}</div>
            </div>
            """, unsafe_allow_html=True)

st.write("")
st.markdown(
    "<p style='text-align:center;color:#8096bb;font-size:.78rem'>"
    "목적지 선택은 아래 행성 이름을 클릭하세요 · 지구는 출발 행성으로 잠겨 있습니다."
    "</p>",
    unsafe_allow_html=True
)

# 행성별 선택 동작
select_cols = st.columns(5, gap="small")
for col, name in zip(select_cols, order):
    with col:
        if name == "지구":
            st.button("지구 · 선택 불가", key="earth_locked", disabled=True,
                      use_container_width=True)
        else:
            if st.button(f"{name} 선택", key=f"select_{name}",
                         use_container_width=True):
                st.session_state.selected_planet = name
                st.session_state.pop("selected_ship", None)
                st.session_state.pop("selected_ship_name", None)
                st.session_state.pop("selected_ship_stats", None)
                st.switch_page("pages/selectspaceship.py")

if st.button("← 메인 화면으로"):
    st.switch_page("main.py")
