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

# iframe의 "처음으로"가 실제 Streamlit 페이지 1로 돌아오기 위한 URL 상태 처리
try:
    requested_page = st.query_params.get("page")
    if requested_page is not None:
        requested_page = int(requested_page)
        if requested_page in (1, 2, 3):
            st.session_state.page = requested_page
            if requested_page == 1:
                st.session_state.mission = None
                st.session_state.ship = None
            elif requested_page == 2:
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
# GLOBAL NAVIGATION
# ============================================================

nav1, nav2, nav3 = st.columns([1, 1, 1])
with nav1:
    if st.button("🪐 1. 임무 선택", key="global_home"):
        st.session_state.page = 1
        st.session_state.mission = None
        st.session_state.ship = None
        st.rerun()
with nav2:
    if st.button("🚀 2. 우주선 선택", key="global_ship"):
        if st.session_state.mission is not None:
            st.session_state.page = 2
            st.rerun()
with nav3:
    if st.button("⚡ 3. 스윙바이 게임", key="global_game"):
        if st.session_state.mission is not None and st.session_state.ship is not None:
            st.session_state.page = 3
            st.rerun()

if st.session_state.page == 2 and st.session_state.mission is None:
    st.session_state.page = 1
    st.rerun()

if st.session_state.page == 3 and (
    st.session_state.mission is None or st.session_state.ship is None
):
    st.session_state.page = 1
    st.rerun()


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
# PAGE 3 : 게임 — 스윙바이 궤도 시뮬레이션
# ============================================================

elif st.session_state.page == 3:

    mission = st.session_state.mission
    ship = st.session_state.ship

    mission_data = {
        "화성": {"emoji": "🔴", "target_radius": 46, "color": "#d84a3a"},
        "금성": {"emoji": "🟡", "target_radius": 48, "color": "#e8b84a"},
        "목성": {"emoji": "🟠", "target_radius": 62, "color": "#d89a62"},
        "해왕성": {"emoji": "🔵", "target_radius": 52, "color": "#3b82f6"}
    }

    ship_data = {
        "노즈형 탐사선": {"base_speed": 7.0, "power": 1.00},
        "캡슐형 탐사선": {"base_speed": 5.5, "power": 0.90},
        "장거리 탐사선": {"base_speed": 4.5, "power": 0.82}
    }

    GAME_DATA = {
        "mission": mission,
        "ship": ship,
        "target": mission_data[mission],
        "shipData": ship_data[ship]
    }

    game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
* { box-sizing:border-box; }
html,body {
    margin:0; padding:0; width:100%; height:100%;
    overflow:hidden; background:#02030a;
    font-family:Arial,"Malgun Gothic",sans-serif;
}
#wrap {
    position:relative; width:100vw; height:100vh;
    min-height:700px; background:
      radial-gradient(circle at 50% 50%,#101936 0%,#03050d 65%,#010207 100%);
    color:white; overflow:hidden;
}
#canvas { position:absolute; inset:0; width:100%; height:100%; cursor:crosshair; }
#top {
    position:absolute; top:18px; left:24px; right:24px;
    display:flex; justify-content:space-between; align-items:center;
    pointer-events:none; z-index:5;
}
.title {
    font-size:25px; font-weight:900; letter-spacing:3px;
    text-shadow:0 0 15px #38bdf8;
}
.badge {
    background:rgba(7,12,30,.78); border:1px solid #334b7a;
    border-radius:12px; padding:9px 14px; backdrop-filter:blur(8px);
}
#hud {
    position:absolute; left:24px; top:70px; width:255px;
    padding:16px; border-radius:15px;
    background:rgba(5,10,25,.78); border:1px solid #293d68;
    backdrop-filter:blur(10px); z-index:4;
}
.row { display:flex; justify-content:space-between; margin:8px 0; color:#cbd5e1; }
.value { color:#fff; font-weight:800; }
#physics {
    position:absolute; left:24px; bottom:25px; width:350px;
    background:rgba(5,10,25,.84); border:1px solid #293d68;
    border-radius:15px; padding:14px 16px; z-index:4;
}
#physics b { color:#7dd3fc; }
#guide {
    position:absolute; right:24px; top:70px; width:315px;
    background:rgba(5,10,25,.82); border:1px solid #293d68;
    border-radius:15px; padding:15px; z-index:4;
    line-height:1.6; color:#cbd5e1;
}
#launch {
    position:absolute; right:24px; bottom:25px; z-index:7;
    padding:14px 24px; border:0; border-radius:13px;
    background:linear-gradient(135deg,#ef4444,#991b1b);
    color:white; font-weight:900; font-size:17px; cursor:pointer;
    box-shadow:0 0 25px rgba(239,68,68,.35);
}
#restart,#home,#full {
    position:absolute; z-index:8; top:115px;
    border:1px solid #3b82f6; background:rgba(10,20,50,.9);
    color:white; padding:9px 13px; border-radius:10px; cursor:pointer;
}
#restart { right:24px; }
#home { right:125px; }
#full { right:24px; top:160px; }
#message {
    display:none; position:absolute; inset:0; z-index:10;
    align-items:center; justify-content:center;
    background:rgba(1,3,10,.72); backdrop-filter:blur(5px);
}
.card {
    width:min(520px,90vw); padding:30px; text-align:center;
    border-radius:22px; background:rgba(8,15,38,.96);
    border:1px solid #42649e; box-shadow:0 20px 80px #000;
}
.card h1 { margin-top:0; font-size:35px; }
.card button {
    margin:7px; padding:12px 18px; border-radius:10px;
    border:1px solid #4771b5; background:#122550; color:white;
    cursor:pointer; font-weight:700;
}
#toast {
    position:absolute; left:50%; top:50%; transform:translate(-50%,-50%);
    z-index:9; display:none; padding:18px 30px; border-radius:18px;
    background:rgba(5,15,40,.92); border:2px solid #facc15;
    color:#fde68a; font-size:27px; font-weight:900;
    box-shadow:0 0 45px rgba(250,204,21,.3);
}
</style>
</head>
<body>
<div id="wrap">
<canvas id="canvas"></canvas>

<div id="top">
  <div class="title">🚀 ORBIT : SWING-BY</div>
  <div class="badge">목표 : __MISSION__　|　우주선 : __SHIP__</div>
</div>

<div id="hud">
  <div class="row"><span>발사 속도</span><span class="value" id="v0">0</span></div>
  <div class="row"><span>현재 속도</span><span class="value" id="vnow">0</span></div>
  <div class="row"><span>예상 힘</span><span class="value" id="force">0</span></div>
  <div class="row"><span>탈출속도 비율</span><span class="value" id="escapeRatio">0</span></div>
  <div class="row"><span>스윙바이</span><span class="value" id="swings">0 회</span></div>
</div>

<div id="guide">
  <b>🎯 발사 준비</b><br>
  우주선 뒤의 <span style="color:#f87171">빨간 화살표</span>를
  마우스로 잡고 뒤로 당기세요.<br><br>
  멀리 당길수록 초기 속도가 커집니다.<br>
  <span style="color:#ef4444">붉은 점선</span>은 현재 예상 궤도입니다.
  <hr style="border-color:#263653">
  <b>⚡ 스윙바이</b><br>
  소행성의 중력 범위 안으로 들어가면
  속도에 따라 궤도가 다르게 휘어집니다.
  충돌하지 않고 옆으로 지나가세요.
</div>

<div id="physics">
  <b>PHYSICS</b><br>
  중력장: <span id="gravityInfo">준비 중</span><br>
  탈출속도: <span id="vesc">0</span><br>
  궤도 굽힘: <span id="bend">0</span>°
</div>

<button id="home" onclick="goHome()">🏠 처음으로</button>
<button id="restart" onclick="restartGame()">🔄 다시하기</button>
<button id="full" onclick="fullscreenGame()">⛶ 전체화면</button>
<button id="launch">🚀 발사</button>
<div id="toast">⚡ SWING-BY!</div>

<div id="message">
  <div class="card">
    <h1 id="msgTitle"></h1>
    <p id="msgText"></p>
    <button onclick="restartGame()">🔄 다시하기</button>
    <button onclick="goHome()">🏠 처음으로</button>
  </div>
</div>
</div>

<script>
const GAME = __GAME_DATA__;
const canvas=document.getElementById("canvas");
const ctx=canvas.getContext("2d");
let W=0,H=0,dpr=1;
const TAU=Math.PI*2;
const world={w:3200,h:1900};
let ship, target, asteroids=[], stars=[];
let dragging=false, launched=false, over=false, success=false;
let dragX=0,dragY=0, swingCount=0, activeGravity=-1, lastTime=0;
let trail=[], predicted=[];
let toastTimer=null;

function resize(){
  W=window.innerWidth; H=window.innerHeight; dpr=window.devicePixelRatio||1;
  canvas.width=W*dpr; canvas.height=H*dpr;
  canvas.style.width=W+"px"; canvas.style.height=H+"px";
  ctx.setTransform(dpr,0,0,dpr,0,0);
  makeStars();
  if(ship) ship.x=W/2, ship.y=H/2;
  if(!launched) buildAsteroids();
}
window.addEventListener("resize",resize);

function rand(a,b){return Math.random()*(b-a)+a;}
function dist(a,b,c,d){return Math.hypot(a-c,b-d);}
function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
function fmt(v){return Number(v).toFixed(2);}

function makeStars(){
  stars=[];
  for(let i=0;i<180;i++) stars.push({x:rand(0,W),y:rand(0,H),r:rand(.4,1.7),a:rand(.25,.9)});
}

function makeAsteroid(i){
  const types=[
    {name:"암석형",color:"#8b7355",shape:"rock",mass:55},
    {name:"크레이터형",color:"#a18b72",shape:"crater",mass:90},
    {name:"결정형",color:"#60a5fa",shape:"crystal",mass:35},
    {name:"철질형",color:"#94a3b8",shape:"metal",mass:130},
    {name:"얼음형",color:"#67e8f9",shape:"ice",mass:70},
    {name:"붉은 암석형",color:"#ef6c55",shape:"red",mass:180},
    {name:"작은 위성형",color:"#c4b5fd",shape:"moon",mass:45}
  ];
  const t=types[i%types.length];
  let x,y;
  for(let tries=0;tries<100;tries++){
    x=rand(300,W-300); y=rand(220,H-220);
    if(dist(x,y,W/2,H/2)>190 && (!target || dist(x,y,target.x,target.y)>150)) break;
  }
  const radius=rand(18,34);
  // 질량마다 중력 세기가 크게 다르지만, 시각적 범위는 물리적 영향과 분리
  const mu=t.mass*12.0;
  const influence=clamp(95+Math.sqrt(mu)*9,115,250);
  return {x,y,radius,mass:t.mass,mu,influence,type:t.name,shape:t.shape,color:t.color,inside:false};
}

function buildAsteroids(){
  asteroids=[];
  const n=Math.floor(rand(5,8));
  for(let i=0;i<n;i++) asteroids.push(makeAsteroid(i));
  target={
    x:rand(W*0.72,W*0.9),
    y:rand(H*0.18,H*0.82),
    radius:GAME.target.target_radius,
    color:GAME.target.color
  };
  // 목표와 시작점을 너무 가깝게 두지 않음
  if(dist(target.x,target.y,W/2,H/2)<W*.25){
    target.x=W*.82;
  }
}

function reset(){
  over=false; success=false; launched=false; dragging=false;
  swingCount=0; activeGravity=-1; trail=[]; predicted=[];
  ship={x:W/2,y:H/2,vx:0,vy:0,angle:0};
  buildAsteroids();
  computePrediction();
  updateHUD();
  document.getElementById("message").style.display="none";
}
function initialVector(){
  let dx=ship.x-dragX, dy=ship.y-dragY;
  const len=Math.hypot(dx,dy);
  if(len<2) return {vx:0,vy:0,len:0};
  const maxDrag=Math.min(W,H)*.32;
  const power=clamp(len/maxDrag,0,1);
  const maxSpeed=13*GAME.shipData.power;
  const speed=1.1+power*maxSpeed;
  return {vx:dx/len*speed,vy:dy/len*speed,len};
}

// 물리 모델:
// μ=GM에 해당하는 유효 중력상수, a=μ/r².
// 탈출속도 v_escape=sqrt(2μ/r).
// 같은 근접거리라면 초기 속도가 높을수록 v_escape/v가 작아져
// 궤도 굽힘이 작아지도록 수치 적분과 함께 표현한다.
function acceleration(x,y,vx,vy){
  let ax=0,ay=0, strongest=-1,maxA=0;
  asteroids.forEach((p,i)=>{
    const dx=p.x-x,dy=p.y-y;
    const r=Math.hypot(dx,dy);
    const safe=Math.max(r,p.radius*1.05);
    const a=p.mu/(safe*safe);
    if(a>maxA){maxA=a;strongest=i;}
    ax+=a*dx/safe;
    ay+=a*dy/safe;
  });
  return {ax,ay,strongest,maxA};
}

function integratePoint(x,y,vx,vy,dt){
  const a1=acceleration(x,y,vx,vy);
  // RK4로 궤도를 부드럽게 계산
  const k1x=vx,k1y=vy,k1vx=a1.ax,k1vy=a1.ay;
  const a2=acceleration(x+k1x*dt/2,y+k1y*dt/2,vx+k1vx*dt/2,vy+k1vy*dt/2);
  const k2x=vx+k1vx*dt/2,k2y=vy+k1vy*dt/2,k2vx=a2.ax,k2vy=a2.ay;
  const a3=acceleration(x+k2x*dt/2,y+k2y*dt/2,vx+k2vx*dt/2,vy+k2vy*dt/2);
  const k3x=vx+k2vx*dt/2,k3y=vy+k2vy*dt/2,k3vx=a3.ax,k3vy=a3.ay;
  const a4=acceleration(x+k3x*dt,y+k3y*dt, vx+k3vx*dt,vy+k3vy*dt);
  const k4x=vx+k3vx*dt,k4y=vy+k3vy*dt,k4vx=a4.ax,k4vy=a4.ay;
  return {
    x:x+(k1x+2*k2x+2*k3x+k4x)*dt/6,
    y:y+(k1y+2*k2y+2*k3y+k4y)*dt/6,
    vx:vx+(k1vx+2*k2vx+2*k3vx+k4vx)*dt/6,
    vy:vy+(k1vy+2*k2vy+2*k3vy+k4vy)*dt/6
  };
}

function computePrediction(){
  if(launched)return;
  const iv=initialVector();
  predicted=[];
  if(iv.len<3)return;
  let x=ship.x,y=ship.y,vx=iv.vx,vy=iv.vy;
  for(let i=0;i<260;i++){
    predicted.push({x,y});
    const q=integratePoint(x,y,vx,vy,.18);
    x=q.x;y=q.y;vx=q.vx;vy=q.vy;
    if(x<-100||x>W+100||y<-100||y>H+100)break;
  }
}

function getClosestAsteroid(){
  let best=-1,bd=Infinity;
  asteroids.forEach((p,i)=>{
    const d=dist(ship.x,ship.y,p.x,p.y);
    if(d<bd){bd=d;best=i;}
  });
  return {i:best,d:bd};
}

function updatePhysics(dt){
  const q=integratePoint(ship.x,ship.y,ship.vx,ship.vy,dt);
  ship.x=q.x;ship.y=q.y;ship.vx=q.vx;ship.vy=q.vy;
  const speed=Math.hypot(ship.vx,ship.vy);

  asteroids.forEach((p,i)=>{
    const d=dist(ship.x,ship.y,p.x,p.y);
    const inside=d<p.influence;
    if(inside && !p.inside){
      p.inside=true;
      // 근접 순간의 속도와 탈출속도를 비교해 굽힘 가능성을 표시
      const vesc=Math.sqrt(2*p.mu/Math.max(d,p.radius));
      const vratio=vesc/Math.max(speed,.01);
      if(d>p.radius*1.35){
        swingCount++;
        showSwing(p,vratio);
      }
    }
    if(!inside)p.inside=false;
    if(d<p.radius+10){
      end(false,"💥 소행성과 충돌","소행성의 표면에 충돌했습니다.<br>조금 더 바깥쪽으로 스쳐 지나가 보세요.");
    }
  });

  const td=dist(ship.x,ship.y,target.x,target.y);
  if(td<target.radius+22){
    end(true,"🎯 탐사 성공!",`목표 행성에 도착했습니다.<br><b>스윙바이 ${swingCount}회</b>를 이용했습니다.`);
  }
  if(ship.x<-80||ship.x>W+80||ship.y<-80||ship.y>H+80){
    end(false,"🌌 우주 공간 이탈","화면 밖으로 벗어났습니다.");
  }
  trail.push({x:ship.x,y:ship.y});
  if(trail.length>700)trail.shift();
}

function showSwing(p,ratio){
  const t=document.getElementById("toast");
  t.innerHTML=`⚡ SWING-BY!<div style="font-size:14px;margin-top:5px">접근 속도 대비 탈출속도 ${fmt(ratio)}×</div>`;
  t.style.display="block";
  clearTimeout(toastTimer);
  toastTimer=setTimeout(()=>t.style.display="none",1100);
}

function end(ok,title,text){
  if(over)return;
  over=true;success=ok;
  document.getElementById("msgTitle").textContent=title;
  document.getElementById("msgText").innerHTML=text;
  document.getElementById("message").style.display="flex";
}

function updateHUD(){
  const iv=initialVector();
  const speed=launched?Math.hypot(ship.vx,ship.vy):iv.len?Math.hypot(iv.vx,iv.vy):0;
  document.getElementById("v0").textContent=fmt(iv.len);
  document.getElementById("vnow").textContent=fmt(speed);
  document.getElementById("force").textContent=fmt(iv.len*2.0);
  document.getElementById("swings").textContent=swingCount+" 회";
  const c=getClosestAsteroid();
  if(c.i>=0){
    const p=asteroids[c.i];
    const vesc=Math.sqrt(2*p.mu/Math.max(c.d,p.radius));
    document.getElementById("vesc").textContent=fmt(vesc);
    document.getElementById("escapeRatio").textContent=fmt(vesc/Math.max(speed,.01))+"×";
    document.getElementById("gravityInfo").textContent=p.type+" / 거리 "+fmt(c.d);
    document.getElementById("bend").textContent=fmt(Math.min(180,(vesc/Math.max(speed,.01))*35));
  }
}

function drawBackground(){
  ctx.fillStyle="#02030a";ctx.fillRect(0,0,W,H);
  stars.forEach(s=>{ctx.globalAlpha=s.a;ctx.fillStyle="#fff";ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,TAU);ctx.fill();});
  ctx.globalAlpha=1;
}

function drawTarget(){
  const pulse=1+Math.sin(Date.now()*.004)*.06;
  ctx.beginPath();ctx.arc(target.x,target.y,target.radius*1.5*pulse,0,TAU);
  ctx.strokeStyle="rgba(250,204,21,.35)";ctx.lineWidth=3;ctx.stroke();
  const g=ctx.createRadialGradient(target.x-10,target.y-10,2,target.x,target.y,target.radius);
  g.addColorStop(0,"#fff");g.addColorStop(.2,target.color);g.addColorStop(1,"#171717");
  ctx.beginPath();ctx.arc(target.x,target.y,target.radius,0,TAU);ctx.fillStyle=g;ctx.fill();
  ctx.fillStyle="#fde68a";ctx.font="bold 15px Arial";ctx.textAlign="center";
  ctx.fillText("TARGET "+GAME.mission,target.x,target.y+target.radius+25);
}

function drawAsteroid(p){
  // 중력장
  ctx.beginPath();ctx.arc(p.x,p.y,p.influence,0,TAU);
  ctx.strokeStyle="rgba(96,165,250,.30)";ctx.lineWidth=1.5;
  ctx.setLineDash([5,7]);ctx.stroke();ctx.setLineDash([]);
  ctx.fillStyle="rgba(96,165,250,.035)";ctx.fill();

  ctx.save();ctx.translate(p.x,p.y);
  const r=p.radius;
  ctx.fillStyle=p.color;ctx.strokeStyle="#dbeafe";ctx.lineWidth=1;

  ctx.beginPath();
  if(p.shape==="crystal"){
    ctx.moveTo(0,-r*1.15);ctx.lineTo(r*.8,-r*.3);ctx.lineTo(r*.5,r);ctx.lineTo(-r*.65,r*.75);ctx.lineTo(-r,-.1*r);ctx.closePath();
  } else if(p.shape==="metal"){
    for(let i=0;i<10;i++){let a=i*TAU/10;let rr=i%2?r*.8:r*1.1;let x=Math.cos(a)*rr,y=Math.sin(a)*rr;i?ctx.lineTo(x,y):ctx.moveTo(x,y);}ctx.closePath();
  } else if(p.shape==="red"){
    ctx.moveTo(-r*.9,-r*.2);ctx.lineTo(-r*.25,-r);ctx.lineTo(r*.7,-r*.75);ctx.lineTo(r,r*.1);ctx.lineTo(r*.35,r);ctx.lineTo(-r*.8,r*.65);ctx.closePath();
  } else {
    for(let i=0;i<12;i++){let a=i*TAU/12;let rr=r*(.78+((i*37)%23)/100);let x=Math.cos(a)*rr,y=Math.sin(a)*rr;i?ctx.lineTo(x,y):ctx.moveTo(x,y);}ctx.closePath();
  }
  ctx.fill();ctx.stroke();

  // 개별 표면 디테일
  if(p.shape==="crater"||p.shape==="moon"){
    for(let i=0;i<4;i++){ctx.beginPath();ctx.arc(rand(-r*.45,r*.45),rand(-r*.45,r*.45),rand(2,5),0,TAU);ctx.fillStyle="rgba(30,41,59,.45)";ctx.fill();}
  }
  if(p.shape==="ice"){ctx.strokeStyle="rgba(255,255,255,.7)";ctx.beginPath();ctx.moveTo(-r*.7,-r*.4);ctx.lineTo(r*.4,r*.5);ctx.stroke();}
  if(p.shape==="metal"){ctx.strokeStyle="rgba(15,23,42,.55)";ctx.beginPath();ctx.moveTo(-r*.7,0);ctx.lineTo(r*.7,0);ctx.moveTo(0,-r*.7);ctx.lineTo(0,r*.7);ctx.stroke();}
  ctx.restore();

  ctx.fillStyle="#cbd5e1";ctx.font="11px Arial";ctx.textAlign="center";
  ctx.fillText(p.type+"  μ="+p.mass,p.x,p.y-p.radius-10);
}

function drawPrediction(){
  if(launched||predicted.length<2)return;
  ctx.beginPath();ctx.moveTo(predicted[0].x,predicted[0].y);
  for(let i=1;i<predicted.length;i++)ctx.lineTo(predicted[i].x,predicted[i].y);
  ctx.strokeStyle="rgba(248,113,113,.78)";ctx.lineWidth=2;
  ctx.setLineDash([7,8]);ctx.stroke();ctx.setLineDash([]);
}

function drawTrail(){
  if(trail.length<2)return;
  ctx.beginPath();ctx.moveTo(trail[0].x,trail[0].y);
  for(let i=1;i<trail.length;i++)ctx.lineTo(trail[i].x,trail[i].y);
  ctx.strokeStyle="rgba(125,211,252,.55)";ctx.lineWidth=2.2;ctx.stroke();
}

function drawArrow(){
  if(launched)return;
  const iv=initialVector();
  const dx=ship.x-dragX,dy=ship.y-dragY,len=Math.hypot(dx,dy);
  if(len<2)return;
  const ux=dx/len,uy=dy/len;
  const L=clamp(len,35,Math.min(W,H)*.32);
  const sx=ship.x-ux*L,sy=ship.y-uy*L;
  ctx.save();
  ctx.strokeStyle="#ef4444";ctx.fillStyle="#ef4444";ctx.lineWidth=7;
  ctx.shadowColor="#ef4444";ctx.shadowBlur=15;
  ctx.beginPath();ctx.moveTo(ship.x,ship.y);ctx.lineTo(sx,sy);ctx.stroke();
  ctx.beginPath();ctx.moveTo(sx,sy);
  ctx.lineTo(sx+ux*20+uy*14,sy+uy*20-ux*14);
  ctx.lineTo(sx+ux*20-uy*14,sy+uy*20+ux*14);ctx.closePath();ctx.fill();
  ctx.restore();
  ctx.fillStyle="#fecaca";ctx.font="bold 14px Arial";ctx.textAlign="center";
  ctx.fillText("드래그해서 발사 방향·힘 설정",ship.x,ship.y+65);
}

function drawShip(){
  ctx.save();ctx.translate(ship.x,ship.y);
  let a=Math.atan2(ship.vy,ship.vx);
  if(!launched)a=Math.atan2(ship.y-dragY,ship.x-dragX);
  ctx.rotate(a);
  ctx.fillStyle="#e2e8f0";ctx.strokeStyle="#38bdf8";ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(24,0);ctx.lineTo(-18,-12);ctx.lineTo(-10,0);ctx.lineTo(-18,12);ctx.closePath();ctx.fill();ctx.stroke();
  ctx.fillStyle="#38bdf8";ctx.beginPath();ctx.arc(2,0,5,0,TAU);ctx.fill();
  if(!launched){ctx.fillStyle="#f59e0b";ctx.beginPath();ctx.moveTo(-17,0);ctx.lineTo(-30,-7);ctx.lineTo(-26,0);ctx.lineTo(-30,7);ctx.closePath();ctx.fill();}
  ctx.restore();
}

function draw(){
  drawBackground();
  drawPrediction();
  asteroids.forEach(drawAsteroid);
  drawTarget();
  drawTrail();
  drawArrow();
  drawShip();
}

function loop(t){
  const dt=Math.min(.032,(t-lastTime)/1000||.016);lastTime=t;
  if(launched&&!over)updatePhysics(dt*2.2);
  draw();updateHUD();
  requestAnimationFrame(loop);
}

canvas.addEventListener("pointerdown",e=>{
  if(launched||over)return;
  dragging=true;dragX=e.clientX;dragY=e.clientY;computePrediction();
});
canvas.addEventListener("pointermove",e=>{
  if(!dragging||launched||over)return;
  dragX=e.clientX;dragY=e.clientY;computePrediction();
});
window.addEventListener("pointerup",e=>{
  if(!dragging||launched||over)return;
  dragging=false;dragX=e.clientX;dragY=e.clientY;computePrediction();
});
document.getElementById("launch").onclick=()=>{
  if(launched||over)return;
  const iv=initialVector();
  if(iv.len<10)return;
  ship.vx=iv.vx;ship.vy=iv.vy;launched=true;predicted=[];
};
function restartGame(){reset();}
function fullscreenGame(){
  const el=document.getElementById("wrap");
  if(!document.fullscreenElement) el.requestFullscreen?.();
  else document.exitFullscreen?.();
}
function goHome(){
  // iframe에서 부모 Streamlit의 query parameter를 직접 바꾸는 대신
  // 부모에게 명확한 메시지를 보내고, 부모가 수신해 1페이지로 이동한다.
  window.parent.location.href = window.parent.location.pathname + "?page=1";
}
window.addEventListener("message",e=>{
  if(e.data?.type==="ORBIT_HOME"){
    // 안전한 fallback: iframe 자체는 부모 페이지를 조작할 수 없으므로
    // Streamlit 외부 버튼도 제공한다.
  }
});

resize();reset();requestAnimationFrame(loop);
</script>
</body>
</html>
"""

    game_html = game_html.replace("__MISSION__", mission)
    game_html = game_html.replace("__SHIP__", ship)
    game_html = game_html.replace("__GAME_DATA__", json.dumps(GAME_DATA, ensure_ascii=False))

    components.html(game_html, height=900, scrolling=False)

    st.markdown(
        """
        <div style="
            text-align:center;
            margin-top:8px;
            color:#94a3b8;
            font-size:13px;
        ">
        💡 게임 내부의 <b>🏠 처음으로</b>가 브라우저 보안상 Streamlit 상태를 직접 변경할 수 있으므로,
        아래의 Streamlit 버튼도 제공합니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🏠 임무 선택(1페이지)으로 이동", key="bottom_home"):
        st.session_state.page = 1
        st.session_state.mission = None
        st.session_state.ship = None
        st.rerun()
