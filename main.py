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
*{box-sizing:border-box} html,body{margin:0;padding:0;background:#020617;color:white;font-family:Arial,'Malgun Gothic',sans-serif;overflow:hidden} 
#wrap{width:100%;height:860px;background:radial-gradient(circle at 50% 45%,#111c3b 0%,#050a19 48%,#01030b 100%);border:1px solid #26375f;border-radius:18px;overflow:hidden;position:relative;box-shadow:0 0 45px rgba(30,64,175,.25)}
#top{height:68px;padding:10px 18px;display:flex;align-items:center;justify-content:space-between;background:rgba(3,7,18,.86);border-bottom:1px solid #26375f;position:relative;z-index:5}
#title{font-size:24px;font-weight:900;letter-spacing:2px;color:#e0f2fe}.sub{font-size:12px;color:#93a4c7;margin-top:4px}.badge{padding:8px 13px;border-radius:10px;background:#111d3b;border:1px solid #36538e;color:#bdeeff;font-size:13px;font-weight:700}
#game{position:relative;height:792px}.layer{position:absolute;inset:0} canvas{width:100%;height:100%;display:block;cursor:crosshair}
#hud{position:absolute;left:15px;top:15px;width:245px;padding:13px 15px;background:rgba(4,10,25,.84);border:1px solid #29477d;border-radius:13px;backdrop-filter:blur(5px);pointer-events:none}.ht{font-weight:900;color:#67e8f9;margin-bottom:8px;font-size:13px;letter-spacing:1px}.row{display:flex;justify-content:space-between;padding:4px 0;font-size:12px;color:#b9c5df}.row b{color:white}.swing{color:#fbbf24!important;font-weight:900}
#help{position:absolute;left:15px;bottom:15px;padding:11px 14px;border-radius:12px;background:rgba(4,10,25,.86);border:1px solid #29477d;font-size:12px;color:#cbd5e1;line-height:1.55;pointer-events:none}.red{color:#f87171;font-weight:900}.cyan{color:#67e8f9;font-weight:900}
#launchPanel{position:absolute;left:50%;bottom:16px;transform:translateX(-50%);min-width:390px;padding:12px 16px;text-align:center;background:rgba(4,10,25,.9);border:1px solid #3c5f9f;border-radius:15px;box-shadow:0 8px 30px rgba(0,0,0,.35)}#launchPanel .power{font-size:12px;color:#aab8d4;margin-bottom:7px}#powerBar{height:8px;background:#17213d;border-radius:99px;overflow:hidden;border:1px solid #30436c}#powerFill{height:100%;width:0%;background:linear-gradient(90deg,#fca5a5,#ef4444,#b91c1c);transition:width .04s}#launchBtn{margin-top:10px;width:100%;padding:10px;border:1px solid #ef4444;border-radius:10px;background:linear-gradient(135deg,#7f1d1d,#dc2626);color:white;font-weight:900;cursor:pointer}#launchBtn:disabled{opacity:.35;cursor:not-allowed}
#message{display:none;position:absolute;inset:0;background:rgba(1,4,12,.82);z-index:20;align-items:center;justify-content:center}.box{width:min(560px,88%);padding:28px;border-radius:20px;background:#081127;border:1px solid #3b5c9d;text-align:center;box-shadow:0 20px 70px rgba(0,0,0,.6)}.box h1{margin:0 0 12px;font-size:30px}.box p{color:#cbd5e1;line-height:1.7}.btns{display:flex;gap:10px;margin-top:20px}.btn{flex:1;padding:12px;border-radius:10px;border:1px solid #3b82f6;background:#13254b;color:white;font-weight:800;cursor:pointer}.btn.primary{border-color:#ef4444;background:#991b1b}
#swingFlash{position:absolute;left:50%;top:45%;transform:translate(-50%,-50%);font-size:28px;font-weight:1000;color:#fbbf24;text-shadow:0 0 20px #f59e0b;opacity:0;pointer-events:none;z-index:10;transition:opacity .2s}
#legend{position:absolute;right:15px;top:15px;width:225px;padding:12px;background:rgba(4,10,25,.84);border:1px solid #29477d;border-radius:13px;font-size:11px;color:#cbd5e1;line-height:1.65;pointer-events:none}.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px}.dg{background:#60a5fa}.dr{background:#ef4444}.dy{background:#fbbf24}
</style>
</head>
<body>
<div id="wrap">
  <div id="top"><div><div id="title">🚀 ORBIT : SWING-BY</div><div class="sub">행성의 중력장을 이용해 우주선의 비행 궤도를 바꾸는 탐사 임무</div></div><div class="badge">__MISSION__ · __SHIP__</div></div>
  <div id="game">
    <canvas id="canvas"></canvas>
    <div id="hud"><div class="ht">FLIGHT DATA</div><div class="row"><span>발사 상태</span><b id="state">조준 중</b></div><div class="row"><span>발사 속도</span><b id="speed">0.00</b></div><div class="row"><span>목표 거리</span><b id="dist">-</b></div><div class="row"><span>중력 영향</span><b id="gravity">없음</b></div><div class="row"><span>스윙바이</span><b id="swing" class="swing">0 회</b></div></div>
    <div id="legend"><span class="dot dr"></span><b>붉은 점선</b> : 예상 비행 궤도<br><span class="dot dg"></span><b>파란 원</b> : 소행성 중력 범위<br><span class="dot dy"></span><b>노란색</b> : 목표 행성<br><br>💡 중력 범위 안으로 스쳐 지나가면 우주선의 궤도가 크게 휘어집니다.</div>
    <div id="help"><span class="red">마우스로 빨간 화살표를 뒤로 당기세요.</span><br>당긴 거리 = 발사 힘 · 당긴 방향의 반대 = 비행 방향<br>발사 후에는 중력에 의해 궤도가 자동으로 휘어집니다.</div>
    <div id="swingFlash">⚡ SWING-BY! ⚡</div>
    <div id="launchPanel"><div class="power">발사 힘 <b id="powerText">0%</b></div><div id="powerBar"><div id="powerFill"></div></div><button id="launchBtn" disabled>🚀 발사하기</button></div>
    <div id="message"><div class="box"><h1 id="msgTitle">🎯 임무 성공</h1><p id="msgText"></p><div class="btns"><button class="btn primary" onclick="restartGame()">🔄 다시하기</button><button class="btn" onclick="goHome()">🏠 처음으로</button></div></div></div>
  </div>
</div>
<script>
const GAME=__GAME_DATA__;
const canvas=document.getElementById('canvas'),ctx=canvas.getContext('2d');
let W=0,H=0,dpr=1,animationId=null,dragging=false,launched=false,ended=false,swings=0,stars=[],asteroids=[],target=null;
const world={w:5200,h:3000};
const ship={x:0,y:0,vx:0,vy:0,r:13,angle:0};
const aim={x:0,y:0,power:0};
const G=1150;
function resize(){const r=canvas.getBoundingClientRect();W=r.width;H=r.height;dpr=window.devicePixelRatio||1;canvas.width=W*dpr;canvas.height=H*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);if(!launched){ship.x=W/2;ship.y=H/2;aim.x=ship.x-100;aim.y=ship.y;}}
window.addEventListener('resize',resize);
function rand(a,b){return Math.random()*(b-a)+a}
function dist(a,b,c,d){return Math.hypot(a-c,b-d)}
function makeStars(){stars=[];for(let i=0;i<150;i++)stars.push({x:rand(0,W),y:rand(0,H),r:rand(.5,1.8),a:rand(.2,.9)});}
function makeAsteroids(){asteroids=[];const n=10;for(let i=0;i<n;i++){let x,y;do{x=rand(180,W-180);y=rand(150,H-150)}while(dist(x,y,ship.x,ship.y)<180);const mass=rand(75,190),range=105+mass*.48;asteroids.push({x,y,mass,r:rand(13,25),range,active:false});}}
function makeTarget(){let x,y;do{x=rand(120,W-100);y=rand(100,H-100)}while(dist(x,y,ship.x,ship.y)<Math.min(W*.38,330));target={x,y,r:GAME.targetRadius*.55,color:GAME.targetColor};}
function reset(){ended=false;launched=false;dragging=false;swings=0;ship.x=W/2;ship.y=H/2;ship.vx=ship.vy=0;ship.angle=0;aim.x=ship.x-110;aim.y=ship.y;makeStars();makeAsteroids();makeTarget();document.getElementById('message').style.display='none';document.getElementById('launchBtn').disabled=true;updateAimUI();cancelAnimationFrame(animationId);loop();}
function screenPoint(e){const r=canvas.getBoundingClientRect();return{x:e.clientX-r.left,y:e.clientY-r.top}}
function setAim(p){const dx=p.x-ship.x,dy=p.y-ship.y;const max=260,d=Math.min(Math.hypot(dx,dy),max);if(d<18){aim.x=ship.x-18;aim.y=ship.y;aim.power=0;return}const k=d/Math.hypot(dx,dy);aim.x=ship.x+dx*k;aim.y=ship.y+dy*k;aim.power=d/max;}
canvas.addEventListener('pointerdown',e=>{if(launched||ended)return;const p=screenPoint(e);if(dist(p.x,p.y,aim.x,aim.y)<55||dist(p.x,p.y,ship.x,ship.y)<70){dragging=true;canvas.setPointerCapture(e.pointerId);setAim(p);updateAimUI();}});
canvas.addEventListener('pointermove',e=>{if(!dragging||launched||ended)return;setAim(screenPoint(e));updateAimUI();});
canvas.addEventListener('pointerup',e=>{if(!dragging)return;dragging=false;updateAimUI();});
canvas.addEventListener('pointercancel',()=>dragging=false);
document.getElementById('launchBtn').onclick=launch;
function launch(){if(launched||ended||aim.power<.06)return;const dx=ship.x-aim.x,dy=ship.y-aim.y,L=Math.hypot(dx,dy);const dirX=dx/L,dirY=dy/L;const base=GAME.speed*.35;const max=GAME.speed*1.7;const v=base+(max-base)*aim.power;ship.vx=dirX*v;ship.vy=dirY*v;ship.angle=Math.atan2(ship.vy,ship.vx);launched=true;document.getElementById('launchBtn').disabled=true;document.getElementById('state').textContent='비행 중';document.getElementById('powerText').textContent=Math.round(aim.power*100)+'%';}
function gravity(){let total=0,nearest=99999;for(const a of asteroids){const dx=a.x-ship.x,dy=a.y-ship.y,r=Math.hypot(dx,dy);if(r<nearest)nearest=r;if(r<a.range&&r>a.r+8){const strength=G*a.mass/(r*r);ship.vx+=(dx/r)*strength;ship.vy+=(dy/r)*strength;total+=strength;a.active=true;}else a.active=false;if(r<a.r+ship.r){end(false,'💥 충돌!','소행성에 너무 가까이 접근했습니다. 다음에는 중력 범위 안으로 들어가되 행성을 스쳐 지나가도록 발사 방향을 조절해 보세요.');return false;}}document.getElementById('gravity').textContent=total>0?total.toFixed(2):'없음';return true;}
function update(){if(!launched||ended)return;for(const a of asteroids)a.active=false;if(!gravity())return;ship.x+=ship.vx;ship.y+=ship.vy;const sp=Math.hypot(ship.vx,ship.vy);ship.angle=Math.atan2(ship.vy,ship.vx);if(ship.x<0||ship.x>W||ship.y<0||ship.y>H){end(false,'🌌 우주 공간 이탈','우주선이 화면 밖으로 이탈했습니다. 발사 방향과 힘을 조금 조절해 보세요.');return;}for(const a of asteroids){const r=dist(ship.x,ship.y,a.x,a.y);if(r<a.range){if(!a.wasInside){swings++;flashSwing();}a.wasInside=true;}else a.wasInside=false;}const td=dist(ship.x,ship.y,target.x,target.y);document.getElementById('dist').textContent=Math.round(td);if(td<target.r+ship.r+8)end(true,'🎯 스윙바이 탐사 성공!',`목표 행성에 도착했습니다.<br><br>총 <b>${swings}회</b>의 중력장 진입을 이용했습니다.<br>행성의 중력에 의해 우주선의 비행 궤도가 휘어지는 스윙바이 효과를 확인했습니다.`);document.getElementById('speed').textContent=sp.toFixed(2);}
function flashSwing(){const el=document.getElementById('swingFlash');el.style.opacity='1';setTimeout(()=>el.style.opacity='0',650);document.getElementById('swing').textContent=swings+' 회';}
function predicted(){if(launched||aim.power<.04)return[];const dx=ship.x-aim.x,dy=ship.y-aim.y,L=Math.hypot(dx,dy);if(!L)return[];const dirX=dx/L,dirY=dy/L;let x=ship.x,y=ship.y;const base=GAME.speed*.35,max=GAME.speed*1.7,v=base+(max-base)*aim.power;let vx=dirX*v,vy=dirY*v;const pts=[];for(let i=0;i<180;i++){for(const a of asteroids){const gx=a.x-x,gy=a.y-y,r=Math.hypot(gx,gy);if(r<a.range&&r>20){const f=G*a.mass/(r*r);vx+=(gx/r)*f;vy+=(gy/r)*f;}}x+=vx;y+=vy;if(x<0||x>W||y<0||y>H)break;if(i%3===0)pts.push({x,y});}return pts;}
function draw(){ctx.clearRect(0,0,W,H);const grd=ctx.createRadialGradient(W*.5,H*.5,20,W*.5,H*.5,Math.max(W,H));grd.addColorStop(0,'#101b3a');grd.addColorStop(1,'#01030b');ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);for(const s of stars){ctx.globalAlpha=s.a;ctx.fillStyle='#dbeafe';ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill();}ctx.globalAlpha=1;for(const a of asteroids)drawAsteroid(a);drawTarget();if(!launched)drawPrediction();if(!launched)drawAim();drawShip();}
function drawAsteroid(a){ctx.beginPath();ctx.arc(a.x,a.y,a.range,0,Math.PI*2);ctx.fillStyle=a.active?'rgba(96,165,250,.12)':'rgba(96,165,250,.045)';ctx.fill();ctx.strokeStyle=a.active?'rgba(96,165,250,.65)':'rgba(96,165,250,.22)';ctx.setLineDash([5,7]);ctx.stroke();ctx.setLineDash([]);const g=ctx.createRadialGradient(a.x-5,a.y-5,2,a.x,a.y,a.r);g.addColorStop(0,'#e2e8f0');g.addColorStop(1,'#334155');ctx.fillStyle=g;ctx.beginPath();ctx.arc(a.x,a.y,a.r,0,Math.PI*2);ctx.fill();ctx.fillStyle='#94a3b8';ctx.font='10px Arial';ctx.textAlign='center';ctx.fillText('중력',a.x,a.y+a.r+14);}
function drawTarget(){const pulse=1+Math.sin(Date.now()*.004)*.08;ctx.beginPath();ctx.arc(target.x,target.y,target.r*1.7*pulse,0,Math.PI*2);ctx.strokeStyle='rgba(251,191,36,.28)';ctx.lineWidth=3;ctx.stroke();const g=ctx.createRadialGradient(target.x-8,target.y-8,2,target.x,target.y,target.r);g.addColorStop(0,'#fff');g.addColorStop(.2,target.color);g.addColorStop(1,'#111827');ctx.fillStyle=g;ctx.beginPath();ctx.arc(target.x,target.y,target.r,0,Math.PI*2);ctx.fill();ctx.fillStyle='#fde68a';ctx.font='bold 13px Arial';ctx.textAlign='center';ctx.fillText('🎯 목표',target.x,target.y+target.r+22);}
function drawPrediction(){const pts=predicted();if(!pts.length)return;ctx.strokeStyle='#ef4444';ctx.lineWidth=2;ctx.setLineDash([7,8]);ctx.beginPath();ctx.moveTo(ship.x,ship.y);for(const p of pts)ctx.lineTo(p.x,p.y);ctx.stroke();ctx.setLineDash([]);}
function drawAim(){const dx=ship.x-aim.x,dy=ship.y-aim.y,L=Math.hypot(dx,dy)||1;const nx=dx/L,ny=dy/L;ctx.strokeStyle='rgba(239,68,68,.35)';ctx.lineWidth=10;ctx.beginPath();ctx.moveTo(ship.x,ship.y);ctx.lineTo(aim.x,aim.y);ctx.stroke();ctx.strokeStyle='#ef4444';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(ship.x,ship.y);ctx.lineTo(aim.x,aim.y);ctx.stroke();const hx=aim.x,hy=aim.y;ctx.fillStyle='#ef4444';ctx.beginPath();ctx.arc(hx,hy,11,0,Math.PI*2);ctx.fill();ctx.beginPath();ctx.moveTo(ship.x+nx*95,ship.y+ny*95);ctx.lineTo(ship.x+nx*72-ny*12,ship.y+ny*72+nx*12);ctx.lineTo(ship.x+nx*72+ny*12,ship.y+ny*72-nx*12);ctx.closePath();ctx.fill();ctx.fillStyle='#fca5a5';ctx.font='bold 12px Arial';ctx.textAlign='center';ctx.fillText('← 드래그해서 힘 설정',aim.x,aim.y-18);}
function drawShip(){ctx.save();ctx.translate(ship.x,ship.y);ctx.rotate(ship.angle);ctx.shadowBlur=18;ctx.shadowColor='#38bdf8';ctx.fillStyle='#e2e8f0';ctx.beginPath();ctx.moveTo(20,0);ctx.lineTo(-12,-10);ctx.lineTo(-7,0);ctx.lineTo(-12,10);ctx.closePath();ctx.fill();ctx.fillStyle='#38bdf8';ctx.beginPath();ctx.arc(4,0,4,0,Math.PI*2);ctx.fill();ctx.restore();}
function updateAimUI(){const pct=Math.round(aim.power*100);document.getElementById('powerFill').style.width=pct+'%';document.getElementById('powerText').textContent=pct+'%';document.getElementById('launchBtn').disabled=launched||ended||pct<6;document.getElementById('state').textContent=launched?'비행 중':'조준 중';}
function end(success,title,text){if(ended)return;ended=true;launched=false;cancelAnimationFrame(animationId);document.getElementById('msgTitle').textContent=title;document.getElementById('msgText').innerHTML=text;document.getElementById('message').style.display='flex';}
function restartGame(){reset()}function goHome(){window.parent.postMessage({type:'ORBIT_HOME'},'*')}
function loop(){update();draw();animationId=requestAnimationFrame(loop)}
resize();reset();
</script>
</body>
</html>
"""

    game_html = game_html.replace("__MISSION__", mission)
    game_html = game_html.replace("__SHIP__", ship)
    game_html = game_html.replace("__GAME_DATA__", data_json)

    components.html(game_html, height=875, scrolling=False)


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
