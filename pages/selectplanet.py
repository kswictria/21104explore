
import streamlit as st

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
        radial-gradient(ellipse at 50% 15%, #17244b, transparent 55%),
        linear-gradient(145deg, #050916, #0a1025 55%, #030611);
    color: #edf5ff;
}

#MainMenu, footer, header, [data-testid="stSidebar"] {
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

.subtitle {
    text-align: center;
    color: #91a8d2;
    font-size: .78rem;
    letter-spacing: .12em;
    margin-bottom: 24px;
}

/* 행성 자체가 클릭 가능한 요소 */
[data-testid="stHorizontalBlock"] [data-testid="stColumn"] [data-testid="stButton"] button {
    width: 100%;
    height: 180px;
    min-height: 180px;
    white-space: pre-line;
    border-radius: 18px;
    border: 1px solid rgba(95, 170, 255, .3);
    background: rgba(7, 14, 34, .72);
    color: #eef6ff;
    font-family: 'Orbitron', 'Noto Sans KR', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease;
}

[data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(1) [data-testid="stButton"] button {
    background: radial-gradient(circle at 35% 30%, #c9c9c4 0%, #858b99 30%, #222b40 65%, #080d1b 100%);
}

[data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(2) [data-testid="stButton"] button {
    background: radial-gradient(circle at 35% 30%, #ffe2a0 0%, #c98745 35%, #603e38 68%, #0b1020 100%);
}

[data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(3) [data-testid="stButton"] button {
    background: radial-gradient(circle at 35% 30%, #a6efff 0%, #2878d7 35%, #164c48 65%, #081126 100%);
}

[data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(4) [data-testid="stButton"] button {
    background: radial-gradient(circle at 35% 30%, #ffbd98 0%, #c34c36 38%, #57202d 70%, #0b1020 100%);
}

[data-testid="stHorizontalBlock"] [data-testid="stColumn"]:nth-child(5) [data-testid="stButton"] button {
    background: repeating-linear-gradient(0deg, #9b6c50 0 12px, #e2c69a 13px 23px, #9b6c50 24px 30px);
}

[data-testid="stHorizontalBlock"] [data-testid="stColumn"] [data-testid="stButton"] button:hover {
    transform: scale(1.045);
    border-color: #b1f3ff;
    box-shadow: 0 0 25px rgba(70, 204, 255, .4);
    color: white;
}

.planet-info {
    margin-top: 12px;
    padding: 16px;
    min-height: 235px;
    border: 1px solid rgba(95, 170, 255, .22);
    border-radius: 13px;
    background: linear-gradient(155deg, rgba(16, 29, 57, .8), rgba(5, 9, 23, .94));
}

.planet-name {
    font-family: 'Orbitron', 'Noto Sans KR', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
    margin-bottom: 8px;
}

.stat {
    color: #c6d4ec;
    font-size: .85rem;
    line-height: 1.9;
}

.description {
    color: #91a4c4;
    font-size: .78rem;
    line-height: 1.6;
    margin-top: 8px;
}

.locked-card {
    opacity: .5;
}

.stButton button {
    border-radius: 8px;
}

@media (max-width: 800px) {
    .block-container {
        padding-left: .6rem !important;
        padding-right: .6rem !important;
    }

    [data-testid="stHorizontalBlock"] [data-testid="stColumn"] [data-testid="stButton"] button {
        height: 125px;
        min-height: 125px;
        font-size: .75rem;
    }

    .planet-info {
        padding: 9px;
        min-height: 260px;
    }

    .stat {
        font-size: .72rem;
    }
}
</style>
""", unsafe_allow_html=True)

st.title("탐사할 행성을 선택하세요.")
st.markdown(
    '<div class="subtitle">SELECT YOUR DESTINATION · GRAVITY WILL SHAPE YOUR JOURNEY</div>',
    unsafe_allow_html=True
)

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
        "description": "강력한 중력을 가진 거대 가스 행성입니다. 중력 도움을 크게 받을 수 있지만 난도가 높습니다."
    }
}

# 행성 버튼을 누르면 별도 탐사 버튼 없이 바로 이동
cols = st.columns(5, gap="small")
order = ["수성", "금성", "지구", "화성", "목성"]

for col, name in zip(cols, order):
    with col:
        if name == "지구":
            st.button(
                "🔒\n지구\n출발 행성",
                key="planet_earth",
                disabled=True,
                use_container_width=True
            )
        else:
            if st.button(
                name,
                key=f"planet_{name}",
                use_container_width=True
            ):
                st.session_state.selected_planet = name
                st.session_state.pop("selected_ship", None)
                st.session_state.pop("selected_ship_name", None)
                st.session_state.pop("selected_ship_stats", None)
                st.switch_page("pages/selectspaceship.py")

# 행성 정보는 각 행성 아래에 항상 표시
st.write("")
info_cols = st.columns(5, gap="small")

for col, name in zip(info_cols, order):
    with col:
        if name == "지구":
            st.markdown("""
            <div class="planet-info locked-card">
                <div class="planet-name">지구</div>
                <div class="stat">
                    표면 중력: 1.00 G<br>
                    역할: 출발 행성<br>
                    선택: 불가능
                </div>
                <div class="description">
                    출발 지점으로 지정되어 목적지로 선택할 수 없습니다.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            p = planets[name]
            st.markdown(f"""
            <div class="planet-info">
                <div class="planet-name" style="color:{p['color']}">{name}</div>
                <div class="stat">
                    표면 중력: {p['gravity']}<br>
                    탈출 속도: {p['escape']}<br>
                    탐사 소행성: {p['count']}개<br>
                    난이도: {p['difficulty']}
                </div>
                <div class="description">{p['description']}</div>
            </div>
            """, unsafe_allow_html=True)

st.write("")
st.caption(
    "행성 자체를 클릭해 목적지를 선택하세요. "
    "지구는 출발 행성이므로 선택할 수 없습니다. "
    "소행성 개수와 난이도는 게임용 설정입니다."
)

if st.button("← 메인 화면으로"):
    st.switch_page("main.py")
