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

# iframe 안의 "처음으로" 버튼이 Streamlit의 1페이지로 돌아오도록 하는 연결
try:
    if "page" in st.query_params:
        requested_page = int(st.query_params.get("page", "1"))
        st.session_state.page = requested_page
        if requested_page == 1:
            st.session_state.mission = None
            st.session_state.ship = None
        st.query_params.clear()
        st.rerun()
except Exception:
    pass


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
            "speed": 6.5,
            "turn": 0.055,
            "stability": 0.75,
            "description":
                "앞부분이 뾰족한 형태입니다. "
                "고속 비행에 유리하지만 "
                "방향을 급격하게 변경하기 어렵습니다."
        },

        "캡슐형 탐사선": {
            "emoji": "🛸",
            "speed": 5.0,
            "turn": 0.085,
            "stability": 1.0,
            "description":
                "둥근 캡슐 형태입니다. "
                "속도는 조금 느리지만 방향 전환이 쉽고 "
                "안정적인 조종이 가능합니다."
        },

        "장거리 탐사선": {
            "emoji": "🛰️",
            "speed": 4.2,
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
# PAGE 3 : 게임 — 스윙바이 발사 시뮬레이션
# ============================================================

elif st.session_state.page == 3:

    mission = st.session_state.mission
    ship = st.session_state.ship

    mission_data = {
        "화성": {"emoji": "🔴", "mass": 250, "target_mass": 500, "target_radius": 42, "color": "#d84a3a"},
        "금성": {"emoji": "🟡", "mass": 500, "target_mass": 700, "target_radius": 45, "color": "#e8b84a"},
        "목성": {"emoji": "🟠", "mass": 1100, "target_mass": 1500, "target_radius": 65, "color": "#d89a62"},
        "해왕성": {"emoji": "🔵", "mass": 650, "target_mass": 900, "target_radius": 50, "color": "#3b82f6"}
    }

    ship_data = {
        "노즈형 탐사선": {"speed": 6.5, "turn": 0.055, "stability": 0.75, "symbol": "🚀"},
        "캡슐형 탐사선": {"speed": 5.0, "turn": 0.085, "stability": 1.0, "symbol": "🛸"},
        "장거리 탐사선": {"speed": 4.2, "turn": 0.045, "stability": 1.25, "symbol": "🛰️"}
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

    data_json = json.dumps(game_data, ensure_ascii=False)

    game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#01030a;color:white;font-family:Arial,'Malgun Gothic',sans-serif;overflow:hidden}
#wrap{width:100%;height:calc(100vh - 12px);min-height:760px;background:radial-gradient(circle at 50% 45%,#111c3b 0%,#050a19 50%,#01030b 100%);position:relative;overflow:hidden}
#game{position:absolute;inset:0}
#canvas{width:100%;height:100%;display:block;cursor:crosshair}
#top{position:absolute;left:0;right:0;top:0;height:72px;padding:12px 18px;display:flex;justify-content:space-between;align-items:center;background:linear-gradient(180deg,rgba(2,6,23,.92),rgba(2,6,23,.15));z-index:5;pointer-events:none}
#title{font-size:22px;font-weight:900;letter-spacing:1px} .sub{font-size:11px;color:#9fb0d1;margin-top:3px}.badge{padding:7px 11px;border:1px solid #334d82;border-radius:10px;background:rgba(7,15,36,.8);font-size:12px}
#hud{position:absolute;left:15px;top:88px;width:210px;padding:13px;background:rgba(3,8,22,.82);border:1px solid #29477d;border-radius:13px;z-index:5;pointer-events:none}.ht{font-weight:900;color:#7dd3fc;margin-bottom:9px}.row{display:flex;justify-content:space-between;font-size:11px;padding:5px 0;border-bottom:1px solid rgba(148,163,184,.08)}.row b{color:#fff}.swing{color:#fbbf24!important}
#legend{position:absolute;right:15px;top:88px;width:245px;padding:12px;background:rgba(3,8,22,.82);border:1px solid #29477d;border-radius:13px;font-size:11px;color:#cbd5e1;line-height:1.7;z-index:5;pointer-events:none}.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px}.dg{background:#60a5fa}.dr{background:#ef4444}.dy{background:#fbbf24}
#help{position:absolute;left:50%;top:88px;transform:translateX(-50%);padding:9px 15px;text-align:center;background:rgba(3,8,22,.78);border:1px solid #334d82;border-radius:11px;font-size:11px;color:#cbd5e1;z-index:5;pointer-events:none}.red{color:#fca5a5;font-weight:900}
#launchPanel{position:absolute;left:50%;bottom:20px;transform:translateX(-50%);width:min(430px,72vw);padding:12px 16px;text-align:center;background:rgba(3,8,22,.92);border:1px solid #3c5f9f;border-radius:15px;box-shadow:0 8px 30px rgba(0,0,0,.45);z-index:6}.power{font-size:12px;color:#aab8d4;margin-bottom:7px}#powerBar{height:9px;background:#17213d;border-radius:99px;overflow:hidden;border:1px solid #30436c}#powerFill{height:100%;width:0%;background:linear-gradient(90deg,#fca5a5,#ef4444,#b91c1c);transition:width .04s}#launchBtn{margin-top:10px;width:100%;padding:10px;border:1px solid #ef4444;border-radius:10px;background:linear-gradient(135deg,#7f1d1d,#dc2626);color:white;font-weight:900;cursor:pointer}#launchBtn:disabled{opacity:.35;cursor:not-allowed}
#fullscreenBtn{position:absolute;right:15px;bottom:20px;padding:10px 13px;border:1px solid #4b6291;border-radius:10px;background:rgba(3,8,22,.9);color:#dbeafe;font-weight:800;cursor:pointer;z-index:7}#fullscreenBtn:hover{border-color:#67e8f9}
#message{display:none;position:absolute;inset:0;background:rgba(1,4,12,.86);z-index:20;align-items:center;justify-content:center}.box{width:min(560px,88%);padding:28px;border-radius:20px;background:#081127;border:1px solid #3b5c9d;text-align:center;box-shadow:0 20px 70px rgba(0,0,0,.6)}.box h1{margin:0 0 12px;font-size:30px}.box p{color:#cbd5e1;line-height:1.7}.btns{display:flex;gap:10px;margin-top:20px}.btn{flex:1;padding:12px;border-radius:10px;border:1px solid #3b82f6;background:#13254b;color:white;font-weight:800;cursor:pointer}.btn.primary{border-color:#ef4444;background:#991b1b}
#swingFlash{position:absolute;left:50%;top:47%;transform:translate(-50%,-50%);font-size:32px;font-weight:1000;color:#fbbf24;text-shadow:0 0 20px #f59e0b;opacity:0;pointer-events:none;z-index:10;transition:opacity .2s}
@media (max-width:900px){#hud{width:180px}#legend{display:none}#help{font-size:10px;top:82px;width:300px}.badge{display:none}}
:fullscreen #wrap{height:100vh;min-height:0;border:0;border-radius:0}
</style>
</head>
<body>
<div id="wrap">
<div id="game">
<canvas id="canvas"></canvas>
<div id="top"><div><div id="title">🚀 ORBIT : SWING-BY</div><div class="sub">행성의 중력장을 이용해 우주선의 비행 궤도를 바꾸는 탐사 임무</div></div><div class="badge">__MISSION__ · __SHIP__</div></div>
<div id="hud"><div class="ht">FLIGHT DATA</div><div class="row"><span>상태</span><b id="state">조준 중</b></div><div class="row"><span>발사 속도</span><b id="speed">0.00</b></div><div class="row"><span>목표 거리</span><b id="dist">-</b></div><div class="row"><span>중력 영향</span><b id="gravity">없음</b></div><div class="row"><span>스윙바이</span><b id="swing" class="swing">0 회</b></div></div>
<div id="legend"><span class="dot dr"></span><b>붉은 점선</b> : 예상 비행 궤도<br><span class="dot dg"></span><b>파란 원</b> : 소행성 중력 범위<br><span class="dot dy"></span><b>노란색</b> : 목표 행성<br><br>💡 중력 범위 안으로 들어가면 우주선의 궤도가 휘어집니다.<br>소행성과 충돌하지 않고 스쳐 지나가 보세요.</div>
<div id="help"><span class="red">🚀 빨간 화살표를 마우스로 뒤로 당기세요.</span><br>당긴 거리 = 발사 힘 · 당긴 방향의 반대 = 비행 방향 · 점선 = 예상 궤도</div>
<div id="swingFlash">⚡ SWING-BY! ⚡</div>
<div id="launchPanel"><div class="power">발사 힘 <b id="powerText">0%</b></div><div id="powerBar"><div id="powerFill"></div></div><button id="launchBtn" disabled>🚀 발사하기</button></div>
<button id="fullscreenBtn" onclick="toggleFullscreen()">⛶ 전체화면</button>
<div id="message"><div class="box"><h1 id="msgTitle">🎯 임무 성공</h1><p id="msgText"></p><div class="btns"><button class="btn primary" onclick="restartGame()">🔄 다시하기</button><button class="btn" onclick="goHome()">🏠 처음으로</button></div></div></div>
</div></div>
<script>
const GAME=__GAME_DATA__;
const canvas=document.getElementById('canvas'),ctx=canvas.getContext('2d');
let W=0,H=0,dpr=1,animationId=null,dragging=false,launched=false,ended=false,swings=0,stars=[],asteroids=[],target=null;
const ship={x:0,y:0,vx:0,vy:0,r:13,angle:0};
const aim={x:0,y:0,power:0};
const G=1050;
function resize(){const r=canvas.getBoundingClientRect();W=r.width;H=r.height;dpr=window.devicePixelRatio||1;canvas.width=W*dpr;canvas.height=H*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);if(!launched){ship.x=W/2;ship.y=H/2;aim.x=ship.x-110;aim.y=ship.y;}}
window.addEventListener('resize',resize);
function rand(a,b){return Math.random()*(b-a)+a} function dist(a,b,c,d){return Math.hypot(a-c,b-d)}
function makeStars(){stars=[];for(let i=0;i<170;i++)stars.push({x:rand(0,W),y:rand(0,H),r:rand(.4,1.7),a:rand(.2,.9)});}
function makeAsteroids(){
 asteroids=[]; const n=Math.floor(rand(5,8)); const types=['rock','crater','crystal','ring','ice','iron','spiky'];
 for(let i=0;i<n;i++){let x,y;do{x=rand(260,W-260);y=rand(170,H-170)}while(dist(x,y,W/2,H/2)<190|| (target&&dist(x,y,target.x,target.y)<100));const mass=rand(80,190),range=125+mass*.48;asteroids.push({x,y,mass,r:rand(18,29),range,type:types[i%types.length],phase:rand(0,6.28),active:false,wasInside:false,rot:rand(0,6.28)});}
}
function makeTarget(){let x,y;do{x=rand(280,W-180);y=rand(150,H-150)}while(dist(x,y,W/2,H/2)<Math.min(W*.34,330));target={x,y,r:Math.max(34,Math.min(58,W*.045)),color:GAME.targetColor};}
function reset(){ended=false;launched=false;dragging=false;swings=0;ship.x=W/2;ship.y=H/2;ship.vx=ship.vy=0;ship.angle=0;aim.x=ship.x-110;aim.y=ship.y;makeStars();makeTarget();makeAsteroids();document.getElementById('message').style.display='none';document.getElementById('launchBtn').disabled=true;document.getElementById('swing').textContent='0 회';updateAimUI();cancelAnimationFrame(animationId);loop();}
function screenPoint(e){const r=canvas.getBoundingClientRect();return{x:e.clientX-r.left,y:e.clientY-r.top}}
function setAim(p){const dx=p.x-ship.x,dy=p.y-ship.y,max=Math.min(300,Math.max(180,W*.28)),d=Math.min(Math.hypot(dx,dy),max);if(d<18){aim.x=ship.x-18;aim.y=ship.y;aim.power=0;return}const k=d/Math.hypot(dx,dy);aim.x=ship.x+dx*k;aim.y=ship.y+dy*k;aim.power=d/max;}
canvas.addEventListener('pointerdown',e=>{if(launched||ended)return;const p=screenPoint(e);if(dist(p.x,p.y,aim.x,aim.y)<65||dist(p.x,p.y,ship.x,ship.y)<75){dragging=true;canvas.setPointerCapture(e.pointerId);setAim(p);updateAimUI();}});
canvas.addEventListener('pointermove',e=>{if(!dragging||launched||ended)return;setAim(screenPoint(e));updateAimUI();});
canvas.addEventListener('pointerup',()=>{dragging=false;updateAimUI()});canvas.addEventListener('pointercancel',()=>dragging=false);
document.getElementById('launchBtn').onclick=launch;
function launch(){if(launched||ended||aim.power<.06)return;const dx=ship.x-aim.x,dy=ship.y-aim.y,L=Math.hypot(dx,dy);const dirX=dx/L,dirY=dy/L;const base=Math.max(2.2,GAME.speed*.28),max=Math.max(4.5,GAME.speed*1.25),v=base+(max-base)*aim.power;ship.vx=dirX*v;ship.vy=dirY*v;ship.angle=Math.atan2(ship.vy,ship.vx);launched=true;document.getElementById('launchBtn').disabled=true;document.getElementById('state').textContent='비행 중';}
function gravity(){let total=0;for(const a of asteroids){const dx=a.x-ship.x,dy=a.y-ship.y,r=Math.hypot(dx,dy);if(r<a.range&&r>a.r+10){const f=G*a.mass/(r*r);ship.vx+=(dx/r)*f;ship.vy+=(dy/r)*f;total+=f;a.active=true;}else a.active=false;if(r<a.r+ship.r){end(false,'💥 소행성 충돌!','소행성의 중심에 너무 가까이 접근했습니다.<br>중력 범위 안으로 들어가되, 표면은 피해서 스쳐 지나가 보세요.');return false;}}document.getElementById('gravity').textContent=total>0?total.toFixed(2):'없음';return true;}
function update(){if(!launched||ended)return;if(!gravity())return;ship.x+=ship.vx;ship.y+=ship.vy;ship.angle=Math.atan2(ship.vy,ship.vx);const sp=Math.hypot(ship.vx,ship.vy);if(ship.x<0||ship.x>W||ship.y<0||ship.y>H){end(false,'🌌 비행 경로 이탈','화면 밖으로 날아갔습니다.<br>발사 힘과 방향을 조금 조절해 보세요.');return;}for(const a of asteroids){const r=dist(ship.x,ship.y,a.x,a.y);if(r<a.range){if(!a.wasInside){swings++;flashSwing();}a.wasInside=true;}else a.wasInside=false;}const td=dist(ship.x,ship.y,target.x,target.y);document.getElementById('dist').textContent=Math.round(td);document.getElementById('speed').textContent=sp.toFixed(2);if(td<target.r+ship.r+10)end(true,'🎯 스윙바이 탐사 성공!',`목표 행성에 도착했습니다.<br><br><b>${swings}회</b>의 스윙바이 구간을 통과했습니다.<br>소행성의 중력장이 우주선의 비행 방향을 변화시키는 효과를 확인했습니다.`);}
function flashSwing(){const el=document.getElementById('swingFlash');el.style.opacity='1';setTimeout(()=>el.style.opacity='0',650);document.getElementById('swing').textContent=swings+' 회';}
function predicted(){if(launched||aim.power<.04)return[];const dx=ship.x-aim.x,dy=ship.y-aim.y,L=Math.hypot(dx,dy);if(!L)return[];let x=ship.x,y=ship.y;const base=Math.max(2.2,GAME.speed*.28),max=Math.max(4.5,GAME.speed*1.25),v=base+(max-base)*aim.power;let vx=(dx/L)*v,vy=(dy/L)*v;const pts=[];for(let i=0;i<220;i++){for(const a of asteroids){const gx=a.x-x,gy=a.y-y,r=Math.hypot(gx,gy);if(r<a.range&&r>20){const f=G*a.mass/(r*r);vx+=(gx/r)*f;vy+=(gy/r)*f;}}x+=vx;y+=vy;if(x<0||x>W||y<0||y>H)break;if(i%3===0)pts.push({x,y});}return pts;}
function draw(){ctx.clearRect(0,0,W,H);const grd=ctx.createRadialGradient(W*.5,H*.5,20,W*.5,H*.5,Math.max(W,H));grd.addColorStop(0,'#101b3a');grd.addColorStop(1,'#01030b');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);for(const s of stars){ctx.globalAlpha=s.a;ctx.fillStyle='#dbeafe';ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill();}ctx.globalAlpha=1;for(const a of asteroids)drawAsteroid(a);drawTarget();if(!launched)drawPrediction();if(!launched)drawAim();drawShip();}
function drawAsteroid(a){ctx.save();ctx.translate(a.x,a.y);ctx.rotate(a.rot);ctx.beginPath();ctx.arc(0,0,a.range,0,Math.PI*2);ctx.fillStyle=a.active?'rgba(96,165,250,.14)':'rgba(96,165,250,.045)';ctx.fill();ctx.strokeStyle=a.active?'rgba(96,165,250,.72)':'rgba(96,165,250,.25)';ctx.setLineDash([5,7]);ctx.stroke();ctx.setLineDash([]);if(a.type==='crystal'){drawCrystal(a);}
 else if(a.type==='ring'){drawRock(a);ctx.strokeStyle='#cbd5e1';ctx.lineWidth=4;ctx.beginPath();ctx.ellipse(0,0,a.r*1.65,a.r*.45,0,0,Math.PI*2);ctx.stroke();}
 else if(a.type==='ice'){drawRock(a,'#bae6fd','#1e3a5f');ctx.strokeStyle='#e0f2fe';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(-a.r*.7,-a.r*.2);ctx.lineTo(a.r*.5,a.r*.55);ctx.stroke();}
 else if(a.type==='spiky'){ctx.beginPath();for(let i=0;i<14;i++){const ang=i*Math.PI*2/14,rr=i%2?a.r*.72:a.r*1.22;const px=Math.cos(ang)*rr,py=Math.sin(ang)*rr;i?ctx.lineTo(px,py):ctx.moveTo(px,py)}ctx.closePath();ctx.fillStyle='#78716c';ctx.fill();ctx.strokeStyle='#d6d3d1';ctx.stroke();}
 else {drawRock(a,a.type==='iron'?'#a8a29e':'#64748b','#1c1917');if(a.type==='crater'){for(let i=0;i<3;i++){ctx.beginPath();ctx.arc((i-1)*a.r*.35,((i%2)-.5)*a.r*.45,a.r*.16,0,Math.PI*2);ctx.fillStyle='#292524';ctx.fill();}}}
 ctx.restore();ctx.fillStyle='#94a3b8';ctx.font='10px Arial';ctx.textAlign='center';ctx.fillText('중력',a.x,a.y+a.r+16);}
function drawRock(a,light='#94a3b8',dark='#334155'){const g=ctx.createRadialGradient(-a.r*.3,-a.r*.35,2,0,0,a.r);g.addColorStop(0,light);g.addColorStop(1,dark);ctx.fillStyle=g;ctx.beginPath();for(let i=0;i<9;i++){const ang=i*Math.PI*2/9,rr=a.r*(.78+Math.sin(i*7.3+a.phase)*.16);const px=Math.cos(ang)*rr,py=Math.sin(ang)*rr;i?ctx.lineTo(px,py):ctx.moveTo(px,py)}ctx.closePath();ctx.fill();ctx.strokeStyle='rgba(226,232,240,.35)';ctx.stroke();}
function drawCrystal(a){ctx.fillStyle='#67e8f9';ctx.strokeStyle='#e0f2fe';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(-a.r*.65,a.r*.5);ctx.lineTo(-a.r*.25,-a.r*.9);ctx.lineTo(a.r*.05,-a.r*.25);ctx.lineTo(a.r*.45,-a.r*1.05);ctx.lineTo(a.r*.72,a.r*.55);ctx.closePath();ctx.fill();ctx.stroke();ctx.fillStyle='rgba(255,255,255,.35)';ctx.beginPath();ctx.moveTo(-a.r*.25,-a.r*.9);ctx.lineTo(a.r*.05,-a.r*.25);ctx.lineTo(-a.r*.05,a.r*.55);ctx.closePath();ctx.fill();}
function drawTarget(){const pulse=1+Math.sin(Date.now()*.004)*.08;ctx.beginPath();ctx.arc(target.x,target.y,target.r*1.7*pulse,0,Math.PI*2);ctx.strokeStyle='rgba(251,191,36,.3)';ctx.lineWidth=3;ctx.stroke();const g=ctx.createRadialGradient(target.x-8,target.y-8,2,target.x,target.y,target.r);g.addColorStop(0,'#fff');g.addColorStop(.2,target.color);g.addColorStop(1,'#111827');ctx.fillStyle=g;ctx.beginPath();ctx.arc(target.x,target.y,target.r,0,Math.PI*2);ctx.fill();ctx.fillStyle='#fde68a';ctx.font='bold 13px Arial';ctx.textAlign='center';ctx.fillText('🎯 목표',target.x,target.y+target.r+22);}
function drawPrediction(){const pts=predicted();if(!pts.length)return;ctx.strokeStyle='#ef4444';ctx.lineWidth=2;ctx.setLineDash([7,8]);ctx.beginPath();ctx.moveTo(ship.x,ship.y);for(const p of pts)ctx.lineTo(p.x,p.y);ctx.stroke();ctx.setLineDash([]);}
function drawAim(){const dx=ship.x-aim.x,dy=ship.y-aim.y,L=Math.hypot(dx,dy)||1,nx=dx/L,ny=dy/L;ctx.strokeStyle='rgba(239,68,68,.3)';ctx.lineWidth=10;ctx.beginPath();ctx.moveTo(ship.x,ship.y);ctx.lineTo(aim.x,aim.y);ctx.stroke();ctx.strokeStyle='#ef4444';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(ship.x,ship.y);ctx.lineTo(aim.x,aim.y);ctx.stroke();ctx.fillStyle='#ef4444';ctx.beginPath();ctx.arc(aim.x,aim.y,12,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.moveTo(ship.x+nx*98,ship.y+ny*98);ctx.lineTo(ship.x+nx*73-ny*13,ship.y+ny*73+nx*13);ctx.lineTo(ship.x+nx*73+ny*13,ship.y+ny*73-nx*13);ctx.closePath();ctx.fill();ctx.fillStyle='#fca5a5';ctx.font='bold 12px Arial';ctx.textAlign='center';ctx.fillText('← 드래그',aim.x,aim.y-20);}
function drawShip(){ctx.save();ctx.translate(ship.x,ship.y);ctx.rotate(ship.angle);ctx.shadowBlur=18;ctx.shadowColor='#38bdf8';ctx.fillStyle='#e2e8f0';ctx.beginPath();ctx.moveTo(21,0);ctx.lineTo(-13,-11);ctx.lineTo(-7,0);ctx.lineTo(-13,11);ctx.closePath();ctx.fill();ctx.fillStyle='#38bdf8';ctx.beginPath();ctx.arc(4,0,4,0,Math.PI*2);ctx.fill();ctx.restore();}
function updateAimUI(){const pct=Math.round(aim.power*100);document.getElementById('powerFill').style.width=pct+'%';document.getElementById('powerText').textContent=pct+'%';document.getElementById('launchBtn').disabled=launched||ended||pct<6;document.getElementById('state').textContent=launched?'비행 중':'조준 중';}
function end(success,title,text){if(ended)return;ended=true;launched=false;cancelAnimationFrame(animationId);document.getElementById('msgTitle').textContent=title;document.getElementById('msgText').innerHTML=text;document.getElementById('message').style.display='flex';}
function restartGame(){reset()}
function goHome(){window.parent.location.href=window.parent.location.pathname+'?page=1';}
async function toggleFullscreen(){try{if(!document.fullscreenElement){await document.documentElement.requestFullscreen();document.getElementById('fullscreenBtn').textContent='⛶ 전체화면 해제';}else{await document.exitFullscreen();document.getElementById('fullscreenBtn').textContent='⛶ 전체화면';}resize();}catch(e){alert('브라우저가 전체화면을 허용하지 않았습니다. 게임 화면을 한 번 클릭한 뒤 다시 눌러주세요.');}}
document.addEventListener('fullscreenchange',()=>{document.getElementById('fullscreenBtn').textContent=document.fullscreenElement?'⛶ 전체화면 해제':'⛶ 전체화면';setTimeout(resize,100);});
function loop(){update();draw();animationId=requestAnimationFrame(loop)}
resize();reset();
</script></body></html>
"""

    game_html = game_html.replace("__MISSION__", mission)
    game_html = game_html.replace("__SHIP__", ship)
    game_html = game_html.replace("__GAME_DATA__", data_json)

    components.html(game_html, height=950, scrolling=False)

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
