
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="행성 선택 | SWINGBY OVER",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Noto+Sans+KR:wght@400;600;800&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 50% 15%, #14244b, transparent 55%),
        linear-gradient(145deg, #050916, #0a1025 55%, #050611);
    color: #edf5ff;
}

#MainMenu, footer, header,
[data-testid="stSidebar"] {
    display: none !important;
}

.block-container {
    max-width: 1500px !important;
    padding: 1.2rem 2rem 2rem !important;
}

h1 {
    text-align: center;
    font-family: 'Noto Sans KR', sans-serif;
    font-size: clamp(1.6rem, 3vw, 2.4rem) !important;
    text-shadow: 0 0 18px rgba(73, 204, 255, .45);
}

.intro {
    text-align: center;
    color: #91a8d2;
    font-size: .82rem;
    letter-spacing: .13em;
    margin-bottom: 1.3rem;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: rgba(94, 171, 255, .25) !important;
    background: linear-gradient(155deg, rgba(16, 29, 57, .8), rgba(5, 9, 23, .94));
    border-radius: 14px !important;
}

.planet-label {
    font-weight: 800;
    font-size: 1.15rem;
}

.planet-sub {
    color: #91a8d2;
    font-size: .75rem;
    letter-spacing: .08em;
}

.planet-info {
    color: #c6d4ec;
    font-size: .86rem;
    line-height: 1.8;
}

button[kind="secondary"], .stButton button {
    border: 1px solid #42cfff !important;
    background: #0b2140 !important;
    color: #e9faff !important;
    border-radius: 9px !important;
    transition: .2s ease;
}

.stButton button:hover {
    border-color: #b3f5ff !important;
    box-shadow: 0 0 18px rgba(66, 207, 255, .35) !important;
    transform: translateY(-1px);
}

button:disabled {
    opacity: .35 !important;
}

</style>
""", unsafe_allow_html=True)

st.title("탐사할 행성을 선택하세요.")
st.markdown(
    '<div class="intro">SELECT YOUR DESTINATION · GRAVITY WILL SHAPE YOUR JOURNEY</div>',
    unsafe_allow_html=True
)

# 행성 그림은 별도 HTML 영역에서 렌더링합니다.
# 이렇게 하면 Streamlit Markdown이 HTML을 코드 블록으로 오해하지 않습니다.
components.html("""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    background: transparent;
    color: #edf5ff;
    font-family: Arial, sans-serif;
}

.scene {
    position: relative;
    height: 300px;
    overflow: hidden;
    border: 1px solid rgba(93,177,255,.20);
    border-radius: 18px;
    background:
        radial-gradient(ellipse at center, rgba(35,65,125,.30), transparent 70%),
        rgba(3,8,22,.72);
}

.orbit {
    position: absolute;
    left: -8%;
    width: 116%;
    height: 200px;
    border: 1px solid rgba(179,195,216,.24);
    border-radius: 50%;
    pointer-events: none;
}
.o1 { top: 25px; transform: rotate(-5deg); }
.o2 { top: 75px; transform: rotate(4deg); }
.o3 { top: 120px; transform: rotate(-3deg); }

.planets {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: space-evenly;
    gap: 8px;
    padding: 10px 12px;
}

.planet-wrap {
    position: relative;
    z-index: 2;
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: default;
}

.planet {
    position: relative;
    flex-shrink: 0;
    border-radius: 50%;
    transition: transform .25s ease, filter .25s ease;
}

.planet-wrap:hover .planet {
    transform: scale(1.13);
    filter: brightness(1.2);
}

.planet-wrap:hover .planet:after {
    content: "";
    position: absolute;
    inset: -6px;
    border: 1px solid #a4eeff;
    border-radius: 50%;
    box-shadow: 0 0 18px #43cfff;
}

.mercury {
    width: 43px; height: 43px;
    background: radial-gradient(circle at 32% 25%, #dedbd5, #858891 55%, #393e4b);
    box-shadow: 0 0 17px #9ca3b4;
}

.venus {
    width: 61px; height: 61px;
    background: radial-gradient(circle at 32% 25%, #ffe6a4, #c98745 58%, #653f2e);
    box-shadow: 0 0 18px #ffbd64;
}

.earth {
    width: 70px; height: 70px;
    overflow: hidden;
    background: radial-gradient(circle at 35% 25%, #a5f4ff, #2878d7 50%, #132451);
    box-shadow: 0 0 20px #4aafff;
}

.earth:before {
    content: "";
    position: absolute;
    inset: 8px 18px 18px 6px;
    border-radius: 45% 30% 50% 40%;
    background: #56c58a;
    transform: rotate(-28deg);
}

.mars {
    width: 53px; height: 53px;
    background: radial-gradient(circle at 32% 24%, #ffc09a, #c34c36 55%, #57202d);
    box-shadow: 0 0 17px #ff7359;
}

.jupiter {
    width: 104px; height: 104px;
    overflow: hidden;
    background: repeating-linear-gradient(
        0deg, #b8875e 0 9px, #e9d0a4 10px 17px, #956448 18px 23px
    );
    box-shadow: 0 0 24px #ffca86;
}

.jupiter:before {
    content: "";
    position: absolute;
    width: 24px;
    height: 13px;
    right: 18px;
    top: 55px;
    border-radius: 50%;
    background: #a9573b;
    transform: rotate(-12deg);
}

.name {
    margin-top: 13px;
    color: #eef6ff;
    font-size: 14px;
    font-weight: bold;
}

.en {
    margin-top: 4px;
    color: #92a7c9;
    font-size: 10px;
    letter-spacing: .09em;
}

.locked .name, .locked .en {
    color: #78849a;
}

@media (max-width: 650px) {
    .scene { height: 240px; }
    .mercury { width: 28px; height: 28px; }
    .venus { width: 40px; height: 40px; }
    .earth { width: 46px; height: 46px; }
    .mars { width: 35px; height: 35px; }
    .jupiter { width: 59px; height: 59px; }
    .name { font-size: 11px; }
    .en { font-size: 8px; }
}
</style>
</head>
<body>
<div class="scene">
    <div class="orbit o1"></div>
    <div class="orbit o2"></div>
    <div class="orbit o3"></div>

    <div class="planets">
        <div class="planet-wrap">
            <div class="planet mercury"></div>
            <div class="name">수성</div>
            <div class="en">MERCURY</div>
        </div>
        <div class="planet-wrap">
            <div class="planet venus"></div>
            <div class="name">금성</div>
            <div class="en">VENUS</div>
        </div>
        <div class="planet-wrap locked">
            <div class="planet earth"></div>
            <div class="name">🔒 지구</div>
            <div class="en">HOME · LOCKED</div>
        </div>
        <div class="planet-wrap">
            <div class="planet mars"></div>
            <div class="name">화성</div>
            <div class="en">MARS</div>
        </div>
        <div class="planet-wrap">
            <div class="planet jupiter"></div>
            <div class="name">목성</div>
            <div class="en">JUPITER</div>
        </div>
    </div>
</div>
</body>
</html>
""", height=310, scrolling=False)

st.write("")

planets = {
    "수성": {
        "english": "MERCURY",
        "gravity": "0.38 G",
        "escape": "4.25 km/s",
        "count": 6,
        "difficulty": "★★☆☆☆",
        "color": "#c1c9d6",
        "description": "작은 암석 행성입니다. 짧은 항로에서 중력 도움을 연습하기 좋습니다."
    },
    "금성": {
        "english": "VENUS",
        "gravity": "0.90 G",
        "escape": "10.36 km/s",
        "count": 9,
        "difficulty": "★★★☆☆",
        "color": "#ffbd72",
        "description": "두꺼운 대기와 높은 표면 온도를 가진 행성입니다. 정밀한 궤도 조절이 필요합니다."
    },
    "화성": {
        "english": "MARS",
        "gravity": "0.38 G",
        "escape": "5.03 km/s",
        "count": 11,
        "difficulty": "★★★☆☆",
        "color": "#ff8067",
        "description": "얇은 대기를 가진 암석 행성입니다. 소행성 지대를 통과하며 속도와 방향을 조절합니다."
    },
    "목성": {
        "english": "JUPITER",
        "gravity": "2.53 G",
        "escape": "약 59.5 km/s",
        "count": 15,
        "difficulty": "★★★★★",
        "color": "#ffd08c",
        "description": "강력한 중력을 가진 거대 가스 행성입니다. 큰 중력 도움을 기대할 수 있지만 난도가 높습니다."
    }
}

st.subheader("목적지를 선택하세요")
st.caption("행성을 선택하면 우주선 선택 화면으로 바로 이동합니다. 지구는 출발 행성이라 선택할 수 없습니다.")

order = ["수성", "금성", "지구", "화성", "목성"]
cols = st.columns(5, gap="small")

for col, name in zip(cols, order):
    with col:
        if name == "지구":
            with st.container(border=True):
                st.markdown("### 🔒 지구")
                st.caption("EARTH · 출발 행성")
                st.markdown("**표면 중력:** 1.00 G")
                st.markdown("**역할:** 출발 지점")
                st.markdown("**선택:** 불가능")
                st.caption("탐사 목적지로 선택할 수 없습니다.")
        else:
            p = planets[name]
            with st.container(border=True):
                st.markdown(
                    f"<div class='planet-label' style='color:{p['color']}'>{name}</div>"
                    f"<div class='planet-sub'>{p['english']}</div>",
                    unsafe_allow_html=True
                )
                st.write("")
                st.markdown(
                    f"<div class='planet-info'>"
                    f"표면 중력: {p['gravity']}<br>"
                    f"탈출 속도: {p['escape']}<br>"
                    f"탐사 소행성: {p['count']}개<br>"
                    f"난이도: {p['difficulty']}"
                    f"</div>",
                    unsafe_allow_html=True
                )
                st.write("")
                st.caption(p["description"])

            if st.button(
                f"🚀 {name} 탐사",
                key=f"select_{name}",
                use_container_width=True
            ):
                st.session_state.selected_planet = name
                st.session_state.selected_ship = None
                st.session_state.pop("selected_ship_name", None)
                st.session_state.pop("selected_ship_stats", None)
                st.switch_page("pages/selectspaceship.py")

st.write("")
st.caption("※ 표면 중력은 지구를 1 G로 둔 상대값입니다. 소행성 개수와 난이도는 실제 천체의 개수가 아니라 게임용 설정입니다.")

if st.button("← 메인 화면으로"):
    st.switch_page("main.py")
