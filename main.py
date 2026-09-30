import streamlit as st
import streamlit.components.v1 as components
import json

# ============================================================
# ORBIT : 행성 탐사 임무
# ============================================================

st.set_page_config(
    page_title="ORBIT - 행성 탐사 임무",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = 1

if "mission" not in st.session_state:
    st.session_state.mission = None

if "ship" not in st.session_state:
    st.session_state.ship = None


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 20% 20%,
            #18254a 0%,
            transparent 25%
        ),
        radial-gradient(
            circle at 80% 80%,
            #151a3d 0%,
            transparent 25%
        ),
        #050713;
    color: white;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

.title {
    text-align: center;
    font-size: 58px;
    font-weight: 900;
    letter-spacing: 8px;
    color: #ffffff;
    text-shadow:
        0 0 10px #4cc9ff,
        0 0 25px #4cc9ff;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #9ca9d8;
    font-size: 18px;
    margin-bottom: 40px;
}

.mission-card {
    background: rgba(17, 25, 52, 0.88);
    border: 1px solid rgba(96, 165, 250, 0.35);
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 15px;
    min-height: 230px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}

.mission-card h2 {
    color: white;
    margin-top: 0;
}

.mission-card p {
    color: #c4cbea;
    line-height: 1.7;
}

.stat {
    display: inline-block;
    background: rgba(76, 201, 240, 0.12);
    border: 1px solid rgba(76, 201, 240, 0.3);
    border-radius: 8px;
    padding: 5px 9px;
    margin: 3px;
    font-size: 13px;
    color: #bdeeff;
}

.section-title {
    text-align: center;
    color: white;
    font-size: 28px;
    font-weight: 800;
    margin: 15px 0 25px 0;
}

div.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid #3b82f6;
    background: linear-gradient(
        135deg,
        #172554,
        #1e3a8a
    );
    color: white;
    font-weight: 700;
    padding: 12px;
    transition: 0.2s;
}

div.stButton > button:hover {
    border-color: #67e8f9;
    box-shadow:
        0 0 18px rgba(56,189,248,0.35);
    transform: translateY(-2px);
}

.info-box {
    background: rgba(15,23,42,0.8);
    border-left: 4px solid #38bdf8;
    border-radius: 10px;
    padding: 15px 20px;
    color: #cbd5e1;
    line-height: 1.7;
    margin: 20px 0;
}


#swingbyBanner {
    display:none;
    position:absolute;
    left:50%;
    top:24%;
    transform:translateX(-50%);
    padding:14px 24px;
    border:2px solid rgba(34,211,238,0.85);
    border-radius:999px;
    background:rgba(3,15,30,0.88);
    color:#67e8f9;
    font-size:20px;
    font-weight:900;
    letter-spacing:1px;
    box-shadow:0 0 30px rgba(34,211,238,0.35);
    z-index:30;
}

#swingbyGuide {
    position:absolute;
    left:50%;
    bottom:42px;
    transform:translateX(-50%);
    padding:8px 14px;
    border-radius:10px;
    background:rgba(2,8,23,0.72);
    color:#c7d2fe;
    font-size:12px;
    z-index:12;
    pointer-events:none;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# PAGE 1 : 임무 선택
# ============================================================

if st.session_state.page == 1:

    st.markdown(
        '<div class="title">ORBIT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        '행성 탐사 임무를 선택하고 우주선을 출발시키세요.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">'
        '🪐 01. 탐사 임무 선택'
        '</div>',
        unsafe_allow_html=True
    )

    missions = {

        "화성": {
            "emoji": "🔴",
            "gravity": 0.38,
            "distance": 4200,
            "difficulty": "★★☆☆☆",
            "description":
                "지구보다 중력이 약한 행성입니다. "
                "목표 행성의 중력 영향이 비교적 작아 "
                "기본적인 조종을 연습하기 좋습니다."
        },

        "금성": {
            "emoji": "🟡",
            "gravity": 0.90,
            "distance": 3600,
            "difficulty": "★★★☆☆",
            "description":
                "지구와 비슷한 중력을 가진 행성입니다. "
                "목표에 가까워질수록 우주선의 경로가 "
                "크게 휘어질 수 있습니다."
        },

        "목성": {
            "emoji": "🟠",
            "gravity": 2.53,
            "distance": 5200,
            "difficulty": "★★★★★",
            "description":
                "매우 큰 질량을 가진 행성입니다. "
                "강한 중력 때문에 목표 주변에서 "
                "우주선의 진행 방향이 크게 변화할 수 있습니다."
        },

        "해왕성": {
            "emoji": "🔵",
            "gravity": 1.14,
            "distance": 6800,
            "difficulty": "★★★★☆",
            "description":
                "아주 먼 거리에 있는 행성입니다. "
                "긴 비행시간 동안 여러 작은 행성의 "
                "중력과 공전 운동을 피해야 합니다."
        }
    }

    cols = st.columns(2)

    for i, (name, data) in enumerate(missions.items()):

        with cols[i % 2]:

            st.markdown(
                f"""
                <div class="mission-card">
                    <h2>
                        {data["emoji"]} {name}
                    </h2>

                    <p>
                        {data["description"]}
                    </p>

                    <span class="stat">
                        중력: {data["gravity"]} g
                    </span>

                    <span class="stat">
                        거리: {data["distance"]} km
                    </span>

                    <span class="stat">
                        난이도: {data["difficulty"]}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                f"{data['emoji']} {name} 탐사 임무 선택",
                key=f"mission_{name}"
            ):

                st.session_state.mission = name
                st.session_state.page = 2

                st.rerun()


# ============================================================
# PAGE 2 : 우주선 선택
# ============================================================

elif st.session_state.page == 2:

    mission = st.session_state.mission

    st.markdown(
        '<div class="title">ORBIT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="subtitle">'
        f'목표 행성 : {mission}　|　02. 우주선 선택'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">'
        '🚀 탐사에 사용할 우주선을 선택하세요'
        '</div>',
        unsafe_allow_html=True
    )

    ships = {

        "노즈형 탐사선": {
            "emoji": "🚀",
            "speed": 3.2,
            "turn": 0.055,
            "stability": 0.75,
            "description":
                "앞부분이 뾰족한 형태입니다. "
                "고속 비행에 유리하지만 "
                "방향을 급격하게 변경하기 어렵습니다."
        },

        "캡슐형 탐사선": {
            "emoji": "🛸",
            "speed": 2.6,
            "turn": 0.085,
            "stability": 1.0,
            "description":
                "둥근 캡슐 형태입니다. "
                "속도는 조금 느리지만 방향 전환이 쉽고 "
                "안정적인 조종이 가능합니다."
        },

        "장거리 탐사선": {
            "emoji": "🛰️",
            "speed": 2.2,
            "turn": 0.045,
            "stability": 1.25,
            "description":
                "긴 탐사 장비를 탑재한 우주선입니다. "
                "속도와 조향 반응은 느리지만 안정성이 높습니다."
        }
    }

    cols = st.columns(3)

    for i, (name, data) in enumerate(ships.items()):

        with cols[i]:

            speed_stars = "★" * max(
                1,
                min(5, round(data["speed"] / 1.3))
            )

            turn_stars = "★" * max(
                1,
                min(5, round(data["turn"] * 60))
            )

            stability_stars = "★" * max(
                1,
                min(5, round(data["stability"] * 4))
            )

            st.markdown(
                f"""
                <div class="mission-card">

                    <h2>
                        {data["emoji"]} {name}
                    </h2>

                    <p>
                        {data["description"]}
                    </p>

                    <span class="stat">
                        속도 {speed_stars}
                    </span>

                    <span class="stat">
                        조향 {turn_stars}
                    </span>

                    <span class="stat">
                        안정성 {stability_stars}
                    </span>

                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                f"{data['emoji']} {name} 선택",
                key=f"ship_{name}"
            ):

                st.session_state.ship = name
                st.session_state.page = 3

                st.rerun()

    st.markdown(
        """
        <div class="info-box">

        💡 <b>공학적 설계 원리</b><br>

        우주선의 형태는 단순한 외관이 아니라
        속도, 방향 전환, 안정성에 영향을 줍니다.

        따라서 모든 우주선이 같은 성능을 가지지 않으며,
        플레이어는 탐사 환경에 맞는 우주선을 선택해야 합니다.

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "← 임무 선택으로 돌아가기"
    ):

        st.session_state.page = 1
        st.session_state.mission = None
        st.session_state.ship = None

        st.rerun()


# ============================================================
# PAGE 3 : 게임
# ============================================================

elif st.session_state.page == 3:

    mission = st.session_state.mission
    ship = st.session_state.ship

    mission_data = {

        "화성": {
            "emoji": "🔴",
            "mass": 250,
            "target_mass": 500,
            "target_radius": 42,
            "color": "#d84a3a"
        },

        "금성": {
            "emoji": "🟡",
            "mass": 500,
            "target_mass": 700,
            "target_radius": 45,
            "color": "#e8b84a"
        },

        "목성": {
            "emoji": "🟠",
            "mass": 1100,
            "target_mass": 1500,
            "target_radius": 65,
            "color": "#d89a62"
        },

        "해왕성": {
            "emoji": "🔵",
            "mass": 650,
            "target_mass": 900,
            "target_radius": 50,
            "color": "#3b82f6"
        }
    }

    ship_data = {

        "노즈형 탐사선": {
            "speed": 3.2,
            "turn": 0.055,
            "stability": 0.75,
            "symbol": "🚀"
        },

        "캡슐형 탐사선": {
            "speed": 2.6,
            "turn": 0.085,
            "stability": 1.0,
            "symbol": "🛸"
        },

        "장거리 탐사선": {
            "speed": 2.2,
            "turn": 0.045,
            "stability": 1.25,
            "symbol": "🛰️"
        }
    }

    md = mission_data[mission]
    sd = ship_data[ship]

    game_data = {

        "mission": mission,

        "ship": ship,

        "planetMass": md["mass"],

        "targetMass": md["target_mass"],

        "targetRadius": md["target_radius"],

        "targetColor": md["color"],

        "targetEmoji": md["emoji"],

        "speed": sd["speed"],

        "turnSpeed": sd["turn"],

        "stability": sd["stability"],

        "shipSymbol": sd["symbol"]
    }

    data_json = json.dumps(
        game_data,
        ensure_ascii=False
    )

    # ========================================================
    # 중요:
    # Python f-string과 JavaScript 충돌을 막기 위해
    # JavaScript 부분은 전부 format() 방식으로 삽입한다.
    # ========================================================

    game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
* { box-sizing: border-box; }

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background: #02040d;
    color: white;
    font-family: Arial, sans-serif;
    overflow: hidden;
}

#gameWrapper {
    width: 100%;
    margin: 0 auto;
}

#topBar {
    height: 68px;
    background: linear-gradient(90deg, rgba(8,15,38,0.98), rgba(12,25,60,0.95));
    border: 1px solid #26355f;
    border-radius: 14px 14px 0 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 22px;
}

#gameTitle {
    font-size: 23px;
    font-weight: bold;
    color: #8be9fd;
}

#missionInfo {
    font-size: 14px;
    color: #cbd5e1;
}

#gameContainer {
    position: relative;
    width: 100%;
    height: 790px;
    overflow: hidden;
    border: 1px solid #26355f;
    border-top: 0;
    background: #030617;
}

canvas {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
}

#hud {
    position: absolute;
    top: 15px;
    left: 15px;
    z-index: 5;
    background: rgba(3,7,22,0.82);
    border: 1px solid rgba(96,165,250,0.35);
    border-radius: 12px;
    padding: 12px 15px;
    min-width: 225px;
    backdrop-filter: blur(5px);
}

.hudTitle {
    font-weight: bold;
    color: #67e8f9;
    margin-bottom: 8px;
}

.hudRow {
    font-size: 13px;
    color: #dbeafe;
    margin: 5px 0;
}

#destination {
    position: absolute;
    right: 300px;
    top: 15px;
    z-index: 5;
    background: rgba(3,7,22,0.82);
    border: 1px solid rgba(251,191,36,0.4);
    border-radius: 12px;
    padding: 8px 14px;
    text-align: center;
}

#destination .big { font-size: 24px; }
#destination .small { font-size: 12px; color: #cbd5e1; }

#minimapPanel {
    position: absolute;
    right: 15px;
    top: 15px;
    z-index: 6;
    width: 255px;
    height: 190px;
    background: rgba(2,6,23,0.90);
    border: 1px solid rgba(96,165,250,0.55);
    border-radius: 14px;
    padding: 10px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
}

#minimapTitle {
    font-size: 12px;
    font-weight: bold;
    color: #93c5fd;
    margin-bottom: 5px;
    display: flex;
    justify-content: space-between;
}

#miniMap {
    width: 100%;
    height: 145px;
    display: block;
    border-radius: 8px;
    background: #050b1d;
}

#controls {
    position: absolute;
    bottom: 15px;
    left: 15px;
    z-index: 5;
    background: rgba(3,7,22,0.82);
    border: 1px solid rgba(96,165,250,0.35);
    border-radius: 12px;
    padding: 10px 15px;
    color: #cbd5e1;
    font-size: 13px;
}

.key {
    display: inline-block;
    background: #111827;
    border: 1px solid #64748b;
    border-radius: 5px;
    padding: 2px 7px;
    margin: 0 2px;
    color: white;
    font-weight: bold;
}

#cameraHint {
    position: absolute;
    bottom: 15px;
    right: 15px;
    z-index: 5;
    background: rgba(3,7,22,0.72);
    border: 1px solid rgba(148,163,184,0.25);
    border-radius: 10px;
    padding: 8px 12px;
    color: #94a3b8;
    font-size: 12px;
}

#message {
    display: none;
    position: absolute;
    z-index: 20;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: min(500px, 90%);
    text-align: center;
    background: rgba(3,7,22,0.97);
    border: 1px solid #38bdf8;
    border-radius: 20px;
    padding: 35px;
    box-shadow: 0 0 40px rgba(56,189,248,0.2);
}

#message h1 {
    font-size: 38px;
    margin: 0 0 12px 0;
}

#message p {
    color: #cbd5e1;
    line-height: 1.6;
}

.buttonRow {
    display: flex;
    gap: 12px;
    justify-content: center;
    margin-top: 20px;
}

.gameButton {
    border: 1px solid #38bdf8;
    background: linear-gradient(135deg, #0c4a6e, #172554);
    color: white;
    padding: 12px 20px;
    border-radius: 10px;
    cursor: pointer;
    font-weight: bold;
    font-size: 14px;
}

.gameButton:hover {
    background: #075985;
    box-shadow: 0 0 15px rgba(56,189,248,0.35);
}

@media (max-width: 900px) {
    #destination { display: none; }
    #minimapPanel { width: 210px; height: 165px; }
    #miniMap { height: 120px; }
    #gameContainer { height: 700px; }
}

</style>
</head>

<body>
<div id="gameWrapper">
    <div id="topBar">
        <div id="gameTitle">🚀 ORBIT</div>
        <div id="missionInfo">
            목표 : __MISSION__　|　우주선 : __SHIP__
        </div>
    </div>

    <div id="gameContainer">
        <canvas id="gameCanvas"></canvas>

        <div id="hud">
            <div class="hudTitle">FLIGHT DATA</div>
            <div class="hudRow">속도 : <span id="speedText">0</span></div>
            <div class="hudRow">방향 : <span id="angleText">0</span>°</div>
            <div class="hudRow">목표 거리 : <span id="distanceText">0</span></div>
            <div class="hudRow">중력 영향 : <span id="gravityText">0</span></div>
            <div class="hudRow">스윙바이 : <span id="swingbyText">0회</span></div>
            <div class="hudRow">우주 위치 : <span id="positionText">0, 0</span></div>
        </div>

        <div id="destination">
            <div class="big">__EMOJI__</div>
            <div class="small">TARGET : __MISSION__</div>
        </div>

        <div id="minimapPanel">
            <div id="minimapTitle">
                <span>🗺️ 탐사 미니맵</span>
                <span id="mapDistance">거리 0</span>
            </div>
            <canvas id="miniMap"></canvas>
        </div>

        <div id="controls">
            조종 :
            <span class="key">←</span>
            <span class="key">→</span>
            <span class="key">↑</span>
            <span class="key">↓</span>
        </div>

        <div id="cameraHint">
            🌌 우주선의 이동에 따라 화면이 이동합니다
        </div>

        <div id="swingbyBanner">🚀 SWING-BY</div>

        <div id="swingbyGuide">🪐 행성 가까이 접근 → 중력으로 궤도 변경 → 공전 속도를 이용해 가속/감속</div>

        <div id="message">
            <h1 id="messageTitle">💥 충돌</h1>
            <p id="messageText">우주선이 행성과 충돌했습니다.</p>
            <div class="buttonRow">
                <button class="gameButton" onclick="restartGame()">🔄 다시하기</button>
                <button class="gameButton" onclick="goHome()">🏠 처음으로</button>
            </div>
        </div>
    </div>
</div>

<script>
const GAME = __GAME_DATA__;

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const miniMap = document.getElementById("miniMap");
const mctx = miniMap.getContext("2d");

let W = 0;
let H = 0;
let MW = 0;
let MH = 0;

let animationId = null;
let gameOver = false;
let missionComplete = false;
let keys = {};
let stars = [];
let planets = [];
let swingbyCount = 0;
let swingbyBannerTimer = 0;
let lastSwingbyPlanet = null;

const WORLD_WIDTH = 5200;
const WORLD_HEIGHT = 2600;

let camera = {
    x: 0,
    y: 0
};

let target = {
    x: 0,
    y: 0,
    radius: GAME.targetRadius,
    mass: GAME.targetMass,
    color: GAME.targetColor
};

let ship = {
    x: 0,
    y: 0,
    vx: 0,
    vy: 0,
    angle: 0,
    radius: 12
};

function resizeCanvas() {
    const rect = canvas.getBoundingClientRect();
    W = Math.max(600, rect.width);
    H = Math.max(500, rect.height);

    const ratio = window.devicePixelRatio || 1;
    canvas.width = W * ratio;
    canvas.height = H * ratio;
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);

    const mrect = miniMap.getBoundingClientRect();
    MW = Math.max(100, mrect.width);
    MH = Math.max(80, mrect.height);

    miniMap.width = MW * ratio;
    miniMap.height = MH * ratio;
    mctx.setTransform(ratio, 0, 0, ratio, 0, 0);
}

window.addEventListener("resize", resizeCanvas);

function rand(min, max) {
    return Math.random() * (max - min) + min;
}

function clamp(v, min, max) {
    return Math.max(min, Math.min(max, v));
}

function createStars() {
    stars = [];

    for (let i = 0; i < 420; i++) {
        stars.push({
            x: rand(0, WORLD_WIDTH),
            y: rand(0, WORLD_HEIGHT),
            r: rand(0.5, 2.0),
            alpha: rand(0.2, 1)
        });
    }
}

function createPlanets() {
    planets = [];

    const count = 18;

    for (let i = 0; i < count; i++) {
        const radius = rand(10, 28);
        const orbitRadius = rand(70, 240);

        const centerX = rand(500, WORLD_WIDTH - 500);
        const centerY = rand(250, WORLD_HEIGHT - 250);

        planets.push({
            centerX: centerX,
            centerY: centerY,
            orbitRadius: orbitRadius,
            orbitAngle: rand(0, Math.PI * 2),
            orbitSpeed: rand(-0.0045, 0.0045),
            radius: radius,
            vx: 0,
            vy: 0,
            swingUsed: false,
            mass: rand(60, 190),
            color: [
                "#64748b",
                "#94a3b8",
                "#a78bfa",
                "#60a5fa",
                "#f59e0b",
                "#f87171",
                "#34d399"
            ][Math.floor(rand(0, 7))]
        });
    }
}

function initGame() {
    resizeCanvas();
    createStars();
    createPlanets();

    gameOver = false;
    missionComplete = false;
    swingbyCount = 0;
    swingbyBannerTimer = 0;
    lastSwingbyPlanet = null;

    document.getElementById("message").style.display = "none";
    document.getElementById("swingbyBanner").style.display = "none";

    // 출발 지점
    ship.x = 220;
    ship.y = WORLD_HEIGHT / 2;

    // 속도를 기존보다 크게 낮춤
    ship.angle = 0;
    ship.vx = Math.cos(ship.angle) * GAME.speed;
    ship.vy = Math.sin(ship.angle) * GAME.speed;

    // 목표 행성은 항상 출발 지점보다 훨씬 오른쪽.
    // 화면 밖에 있을 수 있으며 카메라 이동으로 발견하게 됨.
    target.x = rand(3500, 4650);
    target.y = rand(350, WORLD_HEIGHT - 350);

    // 목표 주변에 행성이 너무 겹치지 않도록 약간 정리
    planets = planets.filter(function(p) {
        const d = distance(p.centerX, p.centerY, target.x, target.y);
        return d > 230;
    });

    camera.x = clamp(ship.x - W * 0.35, 0, WORLD_WIDTH - W);
    camera.y = clamp(ship.y - H * 0.50, 0, WORLD_HEIGHT - H);

    cancelAnimationFrame(animationId);
    gameLoop();
}

function setArrowKey(e, pressed) {
    const code = e.code || "";
    const key = e.key || "";
    const isArrow =
        code === "ArrowUp" || code === "ArrowDown" ||
        code === "ArrowLeft" || code === "ArrowRight" ||
        key === "ArrowUp" || key === "ArrowDown" ||
        key === "ArrowLeft" || key === "ArrowRight";

    if (isArrow) {
        e.preventDefault();
        e.stopPropagation();
        keys[code || key] = pressed;
        keys[key] = pressed;
        return false;
    }
}

window.addEventListener("keydown", function(e) {
    setArrowKey(e, true);
}, { passive: false });

window.addEventListener("keyup", function(e) {
    setArrowKey(e, false);
}, { passive: false });

window.addEventListener("blur", function() {
    keys = {};
});

function updatePlanets() {
    planets.forEach(function(p) {
        p.orbitAngle += p.orbitSpeed;

        p.x = p.centerX +
            Math.cos(p.orbitAngle) * p.orbitRadius;

        p.y = p.centerY +
            Math.sin(p.orbitAngle) * p.orbitRadius;

        // 행성의 공전 속도: 스윙바이에서 이 속도가 우주선에 전달될 수 있음
        p.vx = -Math.sin(p.orbitAngle) * p.orbitRadius * p.orbitSpeed;
        p.vy =  Math.cos(p.orbitAngle) * p.orbitRadius * p.orbitSpeed;
    });
}

function distance(x1, y1, x2, y2) {
    return Math.sqrt(
        (x2 - x1) * (x2 - x1) +
        (y2 - y1) * (y2 - y1)
    );
}

function performSwingBy(p, dist) {
    // 행성 기준 상대속도를 구한다.
    const rvx = ship.vx - p.vx;
    const rvy = ship.vy - p.vy;
    const vInf = Math.max(Math.sqrt(rvx * rvx + rvy * rvy), 0.35);

    // 가장 가까운 접근거리(충돌 직전보다 조금 바깥)를 사용한 단순화된 편향각 계산
    const rp = Math.max(dist, p.radius + ship.radius + 8);
    const mu = p.mass * 45;
    const turnAngle = clamp(
        2 * Math.atan(mu / (rp * vInf * vInf)),
        0.12,
        1.05
    );

    // 어느 방향으로 휘어질지는 접근 방향과 행성-우주선 위치의 외적으로 결정
    const rx = ship.x - p.x;
    const ry = ship.y - p.y;
    const cross = rx * rvy - ry * rvx;
    const sign = cross >= 0 ? 1 : -1;
    const a = sign * turnAngle;

    const cosA = Math.cos(a);
    const sinA = Math.sin(a);
    const newRvx = rvx * cosA - rvy * sinA;
    const newRvy = rvx * sinA + rvy * cosA;

    // 행성 기준에서 방향을 바꾼 뒤, 행성의 공전 속도를 다시 더한다.
    ship.vx = newRvx + p.vx;
    ship.vy = newRvy + p.vy;

    // 지나치게 빠르거나 느려지지 않도록 게임용 범위에서 제한
    const v = Math.sqrt(ship.vx * ship.vx + ship.vy * ship.vy);
    const maxSwingSpeed = GAME.speed * 2.15;
    if (v > maxSwingSpeed) {
        ship.vx = ship.vx / v * maxSwingSpeed;
        ship.vy = ship.vy / v * maxSwingSpeed;
    }

    swingbyCount += 1;
    p.swingUsed = true;
    lastSwingbyPlanet = p;
    swingbyBannerTimer = 150;

    const banner = document.getElementById("swingbyBanner");
    banner.style.display = "block";
    banner.textContent = "🚀 SWING-BY 성공!  궤도 변경 + 공전 에너지 이용";

    const speedNow = Math.sqrt(ship.vx * ship.vx + ship.vy * ship.vy);
    document.getElementById("swingbyText").textContent = swingbyCount + "회";

    setTimeout(function() {
        if (swingbyBannerTimer <= 0) {
            banner.style.display = "none";
        }
    }, 1800);
}

function checkSwingBys() {
    planets.forEach(function(p) {
        const d = distance(ship.x, ship.y, p.x, p.y);

        // 행성과 충돌하지 않으면서 아주 가까이 지나갈 때 스윙바이 발생
        const swingRadius = p.radius + 95;
        if (!p.swingUsed && d < swingRadius && d > p.radius + ship.radius + 3) {
            performSwingBy(p, d);
        }
    });
}

function applyGravity() {
    let totalGravity = 0;

    planets.forEach(function(p) {
        const dx = p.x - ship.x;
        const dy = p.y - ship.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 330) {
            const safeDistance = Math.max(dist, 40);

            const force =
                p.mass /
                (safeDistance * safeDistance);

            const acceleration =
                force * 0.70 * GAME.stability;

            ship.vx +=
                (dx / safeDistance) * acceleration;

            ship.vy +=
                (dy / safeDistance) * acceleration;

            totalGravity += force;
        }
    });

    const dx = target.x - ship.x;
    const dy = target.y - ship.y;
    const dist = Math.sqrt(dx * dx + dy * dy);

    if (dist < 420) {
        const safeDistance = Math.max(dist, 50);

        const force =
            target.mass /
            (safeDistance * safeDistance);

        const acceleration =
            force * 0.42 * GAME.stability;

        ship.vx +=
            (dx / safeDistance) * acceleration;

        ship.vy +=
            (dy / safeDistance) * acceleration;

        totalGravity += force;
    }

    document.getElementById("gravityText").textContent =
        totalGravity.toFixed(3);
}

function controlShip() {
    if (keys["ArrowLeft"] || keys["ArrowLeft"]) {
        ship.angle -= GAME.turnSpeed;
    }

    if (keys["ArrowRight"]) {
        ship.angle += GAME.turnSpeed;
    }

    // 느린 게임을 위해 가속도도 감소
    if (keys["ArrowUp"]) {
        ship.vx += Math.cos(ship.angle) * 0.025;
        ship.vy += Math.sin(ship.angle) * 0.025;
    }

    if (keys["ArrowDown"]) {
        // ↓ : 역추진. 속도를 줄이거나 진행 방향을 반대로 바꿀 수 있음.
        ship.vx -= Math.cos(ship.angle) * 0.045;
        ship.vy -= Math.sin(ship.angle) * 0.045;
    }

    let velocity = Math.sqrt(
        ship.vx * ship.vx +
        ship.vy * ship.vy
    );

    const maxSpeed = GAME.speed * 1.35;
    const minSpeed = 0.35;

    if (velocity > maxSpeed) {
        ship.vx = ship.vx / velocity * maxSpeed;
        ship.vy = ship.vy / velocity * maxSpeed;
    }

    if (velocity < minSpeed && velocity > 0) {
        ship.vx = ship.vx / velocity * minSpeed;
        ship.vy = ship.vy / velocity * minSpeed;
    }
}

function moveShip() {
    ship.x += ship.vx;
    ship.y += ship.vy;

    // 우주 끝에 도달하면 튕겨내어 무한 루프가 되지 않게 함
    if (ship.x < 20) {
        ship.x = 20;
        ship.vx = Math.abs(ship.vx);
        ship.angle = Math.atan2(ship.vy, ship.vx);
    }

    if (ship.x > WORLD_WIDTH - 20) {
        ship.x = WORLD_WIDTH - 20;
        ship.vx = -Math.abs(ship.vx);
        ship.angle = Math.atan2(ship.vy, ship.vx);
    }

    if (ship.y < 20) {
        ship.y = 20;
        ship.vy = Math.abs(ship.vy);
        ship.angle = Math.atan2(ship.vy, ship.vx);
    }

    if (ship.y > WORLD_HEIGHT - 20) {
        ship.y = WORLD_HEIGHT - 20;
        ship.vy = -Math.abs(ship.vy);
        ship.angle = Math.atan2(ship.vy, ship.vx);
    }
}

function updateCamera() {
    // 우주선이 화면 중앙 부근에 오도록 카메라 이동
    const desiredX = ship.x - W * 0.38;
    const desiredY = ship.y - H * 0.50;

    camera.x += (desiredX - camera.x) * 0.08;
    camera.y += (desiredY - camera.y) * 0.08;

    camera.x = clamp(camera.x, 0, Math.max(0, WORLD_WIDTH - W));
    camera.y = clamp(camera.y, 0, Math.max(0, WORLD_HEIGHT - H));
}

function checkCollisions() {
    for (let p of planets) {
        const d = distance(
            ship.x,
            ship.y,
            p.x,
            p.y
        );

        if (d < ship.radius + p.radius) {
            endGame(
                false,
                "💥 충돌!",
                "작은 행성과 충돌했습니다.<br>다른 경로를 선택해 다시 도전하세요."
            );
            return;
        }
    }

    const targetDistance = distance(
        ship.x,
        ship.y,
        target.x,
        target.y
    );

    if (targetDistance < ship.radius + target.radius) {
        endGame(
            true,
            "🎉 스윙바이 탐사 성공!",
            "목표 행성에 성공적으로 도착했습니다!<br>이번 비행에서 <strong>" + swingbyCount + "회</strong>의 스윙바이를 수행했습니다."
        );
    }
}

function worldToScreen(x, y) {
    return {
        x: x - camera.x,
        y: y - camera.y
    };
}

function drawBackground() {
    ctx.fillStyle = "#030617";
    ctx.fillRect(0, 0, W, H);

    const gradient = ctx.createRadialGradient(
        W * 0.35,
        H * 0.45,
        10,
        W * 0.35,
        H * 0.45,
        500
    );

    gradient.addColorStop(0, "rgba(59,130,246,0.14)");
    gradient.addColorStop(1, "rgba(59,130,246,0)");

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, W, H);

    stars.forEach(function(s) {
        const sx = s.x - camera.x * 0.22;
        const sy = s.y - camera.y * 0.22;

        // 별이 화면 밖으로 나갔다가 다시 나타나도록 반복
        const px = ((sx % W) + W) % W;
        const py = ((sy % H) + H) % H;

        ctx.beginPath();
        ctx.arc(px, py, s.r, 0, Math.PI * 2);
        ctx.fillStyle =
            "rgba(255,255,255," + s.alpha + ")";
        ctx.fill();
    });

    // 우주 영역 경계감
    ctx.strokeStyle = "rgba(96,165,250,0.10)";
    ctx.strokeRect(
        -camera.x,
        -camera.y,
        WORLD_WIDTH,
        WORLD_HEIGHT
    );
}

function drawOrbit(p) {
    const s = worldToScreen(p.centerX, p.centerY);

    if (
        s.x < -300 ||
        s.x > W + 300 ||
        s.y < -300 ||
        s.y > H + 300
    ) return;

    ctx.beginPath();
    ctx.arc(
        s.x,
        s.y,
        p.orbitRadius,
        0,
        Math.PI * 2
    );

    ctx.strokeStyle =
        "rgba(148,163,184,0.13)";
    ctx.lineWidth = 1;
    ctx.stroke();
}

function drawPlanet(p) {
    const s = worldToScreen(p.x, p.y);

    drawOrbit(p);

    // 아직 스윙바이를 사용하지 않은 행성은 접근 가능 영역을 점선으로 표시
    if (!p.swingUsed) {
        ctx.beginPath();
        ctx.arc(
            s.x,
            s.y,
            p.radius + 95,
            0,
            Math.PI * 2
        );
        ctx.strokeStyle = "rgba(34,211,238,0.16)";
        ctx.lineWidth = 1.5;
        ctx.setLineDash([5, 7]);
        ctx.stroke();
        ctx.setLineDash([]);
    }

    if (
        s.x < -80 ||
        s.x > W + 80 ||
        s.y < -80 ||
        s.y > H + 80
    ) return;

    const gradient = ctx.createRadialGradient(
        s.x - p.radius * 0.3,
        s.y - p.radius * 0.3,
        2,
        s.x,
        s.y,
        p.radius
    );

    gradient.addColorStop(0, "#ffffff");
    gradient.addColorStop(0.15, p.color);
    gradient.addColorStop(1, "#111827");

    ctx.beginPath();
    ctx.arc(
        s.x,
        s.y,
        p.radius,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = gradient;
    ctx.fill();

    ctx.beginPath();
    ctx.arc(
        s.x,
        s.y,
        70,
        0,
        Math.PI * 2
    );

    ctx.strokeStyle =
        "rgba(96,165,250,0.05)";
    ctx.stroke();
}

function drawTarget() {
    const s = worldToScreen(target.x, target.y);

    if (
        s.x < -150 ||
        s.x > W + 150 ||
        s.y < -150 ||
        s.y > H + 150
    ) return;

    const pulse =
        1 +
        Math.sin(Date.now() * 0.004) * 0.05;

    ctx.beginPath();
    ctx.arc(
        s.x,
        s.y,
        target.radius * 1.6 * pulse,
        0,
        Math.PI * 2
    );

    ctx.strokeStyle =
        "rgba(251,191,36,0.25)";
    ctx.lineWidth = 3;
    ctx.stroke();

    const gradient = ctx.createRadialGradient(
        s.x - target.radius * 0.35,
        s.y - target.radius * 0.35,
        3,
        s.x,
        s.y,
        target.radius
    );

    gradient.addColorStop(0, "#ffffff");
    gradient.addColorStop(0.15, target.color);
    gradient.addColorStop(1, "#111827");

    ctx.beginPath();
    ctx.arc(
        s.x,
        s.y,
        target.radius,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = gradient;
    ctx.fill();

    ctx.fillStyle = "#fef3c7";
    ctx.font = "bold 14px Arial";
    ctx.textAlign = "center";

    ctx.fillText(
        GAME.mission,
        s.x,
        s.y + target.radius + 25
    );
}

function drawShip() {
    const s = worldToScreen(ship.x, ship.y);

    ctx.save();

    ctx.translate(s.x, s.y);
    ctx.rotate(ship.angle);

    // 엔진 불꽃
    ctx.beginPath();
    ctx.moveTo(-ship.radius - 5, 0);
    ctx.lineTo(-ship.radius - 17, -5);
    ctx.lineTo(-ship.radius - 12, 0);
    ctx.lineTo(-ship.radius - 17, 5);
    ctx.closePath();

    ctx.fillStyle = "#f59e0b";
    ctx.fill();

    // 우주선 본체
    ctx.beginPath();
    ctx.moveTo(ship.radius + 9, 0);
    ctx.lineTo(-ship.radius, -ship.radius * 0.7);
    ctx.lineTo(-ship.radius * 0.65, 0);
    ctx.lineTo(-ship.radius, ship.radius * 0.7);
    ctx.closePath();

    const gradient = ctx.createLinearGradient(
        -ship.radius,
        0,
        ship.radius,
        0
    );

    gradient.addColorStop(0, "#64748b");
    gradient.addColorStop(0.5, "#e2e8f0");
    gradient.addColorStop(1, "#38bdf8");

    ctx.fillStyle = gradient;
    ctx.fill();

    ctx.restore();
}

function drawRouteInWorld() {
    // 플레이어가 목표까지의 방향을 이해할 수 있도록
    // 현재 화면에 목표가 보이지 않아도 방향선을 표시
    const targetScreen = worldToScreen(
        target.x,
        target.y
    );

    const shipScreen = worldToScreen(
        ship.x,
        ship.y
    );

    if (
        targetScreen.x < -200 ||
        targetScreen.x > W + 200 ||
        targetScreen.y < -200 ||
        targetScreen.y > H + 200
    ) {
        const dx = target.x - ship.x;
        const dy = target.y - ship.y;
        const angle = Math.atan2(dy, dx);

        const edgeX =
            W / 2 +
            Math.cos(angle) * (W * 0.38);

        const edgeY =
            H / 2 +
            Math.sin(angle) * (H * 0.38);

        ctx.save();
        ctx.setLineDash([8, 8]);
        ctx.strokeStyle = "rgba(251,191,36,0.20)";
        ctx.lineWidth = 2;

        ctx.beginPath();
        ctx.moveTo(shipScreen.x, shipScreen.y);
        ctx.lineTo(edgeX, edgeY);
        ctx.stroke();

        ctx.restore();

        ctx.fillStyle = "#fbbf24";
        ctx.font = "bold 12px Arial";
        ctx.textAlign = "center";
        ctx.fillText(
            "목표 방향 →",
            edgeX,
            edgeY - 10
        );
    }
}

function drawMiniMap() {
    mctx.clearRect(0, 0, MW, MH);

    mctx.fillStyle = "#050b1d";
    mctx.fillRect(0, 0, MW, MH);

    const pad = 8;
    const scaleX = (MW - pad * 2) / WORLD_WIDTH;
    const scaleY = (MH - pad * 2) / WORLD_HEIGHT;

    function mx(x) {
        return pad + x * scaleX;
    }

    function my(y) {
        return pad + y * scaleY;
    }

    // 전체 우주 영역
    mctx.strokeStyle = "rgba(96,165,250,0.28)";
    mctx.strokeRect(
        pad,
        pad,
        MW - pad * 2,
        MH - pad * 2
    );

    // 출발지 → 목표까지의 전체 경로
    mctx.save();
    mctx.setLineDash([5, 4]);
    mctx.strokeStyle = "rgba(251,191,36,0.35)";
    mctx.lineWidth = 1.5;

    mctx.beginPath();
    mctx.moveTo(mx(220), my(WORLD_HEIGHT / 2));
    mctx.lineTo(mx(target.x), my(target.y));
    mctx.stroke();
    mctx.restore();

    // 지나온 경로
    mctx.strokeStyle = "rgba(56,189,248,0.55)";
    mctx.lineWidth = 2;
    mctx.beginPath();
    mctx.moveTo(
        mx(220),
        my(WORLD_HEIGHT / 2)
    );
    mctx.lineTo(
        mx(ship.x),
        my(ship.y)
    );
    mctx.stroke();

    // 행성
    planets.forEach(function(p) {
        const r = Math.max(1.5, p.radius * 0.16);

        mctx.beginPath();
        mctx.arc(
            mx(p.x),
            my(p.y),
            r,
            0,
            Math.PI * 2
        );

        mctx.fillStyle = p.color;
        mctx.fill();
    });

    // 목표 행성
    mctx.beginPath();
    mctx.arc(
        mx(target.x),
        my(target.y),
        5,
        0,
        Math.PI * 2
    );

    mctx.fillStyle = "#fbbf24";
    mctx.fill();

    mctx.strokeStyle = "#fde68a";
    mctx.stroke();

    // 우주선
    mctx.beginPath();
    mctx.arc(
        mx(ship.x),
        my(ship.y),
        4,
        0,
        Math.PI * 2
    );

    mctx.fillStyle = "#38bdf8";
    mctx.fill();

    // 현재 카메라 영역
    const viewX = mx(camera.x);
    const viewY = my(camera.y);
    const viewW = Math.min(
        MW - pad * 2,
        W * scaleX
    );
    const viewH = Math.min(
        MH - pad * 2,
        H * scaleY
    );

    mctx.strokeStyle = "rgba(255,255,255,0.18)";
    mctx.lineWidth = 1;
    mctx.strokeRect(
        viewX,
        viewY,
        viewW,
        viewH
    );

    const d = distance(
        ship.x,
        ship.y,
        target.x,
        target.y
    );

    document.getElementById("mapDistance").textContent =
        "거리 " + Math.round(d);
}

function updateHUD() {
    document.getElementById("swingbyText").textContent = swingbyCount + "회";
    document.getElementById("positionText").textContent = Math.round(ship.x) + ", " + Math.round(ship.y);
    const velocity = Math.sqrt(
        ship.vx * ship.vx +
        ship.vy * ship.vy
    );

    let angleDegrees =
        ship.angle * 180 / Math.PI;

    if (angleDegrees < 0) {
        angleDegrees += 360;
    }

    const d = distance(
        ship.x,
        ship.y,
        target.x,
        target.y
    );

    document.getElementById("speedText").textContent =
        velocity.toFixed(2);

    document.getElementById("angleText").textContent =
        angleDegrees.toFixed(0);

    document.getElementById("distanceText").textContent =
        Math.round(d);

    let nearest = null;
    let nearestD = Infinity;
    planets.forEach(function(p) {
        if (p.swingUsed) return;
        const pd = distance(ship.x, ship.y, p.x, p.y);
        if (pd < nearestD) {
            nearestD = pd;
            nearest = p;
        }
    });

    const guide = document.getElementById("swingbyGuide");
    if (nearest && nearestD < 260) {
        if (nearestD < nearest.radius + 110) {
            guide.textContent = "⚡ SWING-BY 접근! 행성에 충돌하지 않고 가까이 스쳐 지나가세요.";
            guide.style.color = "#67e8f9";
        } else {
            guide.textContent = "🪐 스윙바이 후보 접근 중 — 행성 옆을 스쳐 지나가세요.";
            guide.style.color = "#c7d2fe";
        }
    } else {
        guide.textContent = "🪐 행성 가까이 접근 → 중력으로 궤도 변경 → 공전 속도를 이용해 가속/감속";
        guide.style.color = "#c7d2fe";
    }

    document.getElementById("positionText").textContent =
        Math.round(ship.x) + ", " +
        Math.round(ship.y);
}

function endGame(success, title, text) {
    if (gameOver || missionComplete) {
        return;
    }

    if (success) {
        missionComplete = true;
    } else {
        gameOver = true;
    }

    cancelAnimationFrame(animationId);

    document.getElementById("messageTitle").textContent =
        title;

    document.getElementById("messageText").innerHTML =
        text;

    document.getElementById("message").style.display =
        "block";
}

function restartGame() {
    initGame();
}

function goHome() {
    window.parent.postMessage(
        { type: "ORBIT_HOME" },
        "*"
    );
}

function gameLoop() {
    if (gameOver || missionComplete) {
        return;
    }

    updatePlanets();
    controlShip();
    applyGravity();
    checkSwingBys();
    moveShip();
    updateCamera();
    checkCollisions();

    drawBackground();

    planets.forEach(function(p) {
        drawPlanet(p);
    });

    drawRouteInWorld();
    drawTarget();
    drawShip();

    drawMiniMap();
    updateHUD();

    animationId =
        requestAnimationFrame(gameLoop);
}

initGame();
</script>
</body>
</html>
"""

    game_html = game_html.replace("__MISSION__", mission)
    game_html = game_html.replace("__SHIP__", ship)
    game_html = game_html.replace("__EMOJI__", md["emoji"])
    game_html = game_html.replace("__GAME_DATA__", data_json)


    # --------------------------------------------------------
    # Python 값 삽입
    # --------------------------------------------------------

    game_html = game_html.replace(
        "__MISSION__",
        mission
    )

    game_html = game_html.replace(
        "__SHIP__",
        ship
    )

    game_html = game_html.replace(
        "__EMOJI__",
        md["emoji"]
    )

    game_html = game_html.replace(
        "__GAME_DATA__",
        data_json
    )

    # --------------------------------------------------------
    # 게임 표시
    # --------------------------------------------------------

    components.html(
        game_html,
        height=875,
        scrolling=False
    )

    # --------------------------------------------------------
    # Streamlit 바깥쪽 복귀 버튼
    # --------------------------------------------------------

    st.markdown("---")

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        if st.button(
            "🏠 임무 선택 화면으로 돌아가기",
            key="back_to_mission"
        ):

            st.session_state.page = 1

            st.session_state.mission = None

            st.session_state.ship = None

            st.rerun()
