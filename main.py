
import streamlit as st

st.set_page_config(
    page_title="MECHA LAB | Space Arcade",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

MISSIONS = [
    {
        "n": "01",
        "icon": "🪨",
        "name": "화성 암석 집기",
        "sub": "MARS SAMPLE COLLECTION",
        "desc": "암석을 집어 멀리 떨어진 샘플 보관함으로 운반",
        "time": "01:30",
        "path": "pages/1_화성_암석_집기.py"
    },
    {
        "n": "02",
        "icon": "🔋",
        "name": "배터리 분리",
        "sub": "BATTERY EXTRACTION",
        "desc": "잠금장치를 해제하고 배터리를 오른쪽으로 추출",
        "time": "02:00",
        "path": "pages/2_배터리_분리.py"
    },
    {
        "n": "03",
        "icon": "🛰️",
        "name": "위성 수리",
        "sub": "SATELLITE REPAIR",
        "desc": "버튼 두 개, 스위치, 4색 전선과 안테나 정비",
        "time": "04:00",
        "path": "pages/3_위성_수리.py"
    }
]

if "mecha_screen" not in st.session_state:
    st.session_state.mecha_screen = "title"

st.markdown("""
<style>
[data-testid="stSidebar"],
[data-testid="stSidebarNav"],
[data-testid="stSidebarCollapsedControl"],
#MainMenu,
header[data-testid="stHeader"] {
    display: none !important;
}

html, body,
[data-testid="stAppViewContainer"],
.stApp {
    background: #100b29 !important;
    color: #f4eaff;
}

[data-testid="stAppViewBlockContainer"],
.block-container {
    max-width: none !important;
    width: 100% !important;
    padding: 20px clamp(22px,4vw,86px) 35px !important;
}

[data-testid="stMain"] {
    width: 100%;
    max-width: none !important;
}

[data-testid="stVerticalBlock"] {
    gap: 0.7rem;
}

/* 전체 화면을 사용하는 표지 */
.arcade {
    position: relative;
    overflow: hidden;
    width: 100%;
    min-height: calc(100vh - 215px);
    border: 5px solid #584091;
    outline: 2px solid #8b68c5;
    border-radius: 8px;
    background:
        radial-gradient(
            ellipse at 50% 75%,
            #302062 0%,
            #1a1240 55%,
            #100b29 100%
        );
    box-shadow: 8px 8px 0 #080719;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
    isolation: isolate;
}

.arcade:before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        radial-gradient(
            circle,
            #f9eaf9 1.4px,
            transparent 2px
        ),
        radial-gradient(
            circle,
            #76f3e1 1.2px,
            transparent 2px
        );
    background-size: 110px 98px, 157px 133px;
    background-position: 15px 5px, 70px 42px;
    opacity: .8;
    animation: drift 17s linear infinite;
    z-index: -1;
}

@keyframes drift {
    to {
        background-position:
            125px 103px,
            227px 175px;
    }
}

.arcade-top {
    padding: clamp(24px,4vh,44px) 12px 0;
    color: #88f6d1;
    font: 800 clamp(12px,1.2vw,16px) monospace;
    letter-spacing: 5px;
}

.orbit {
    display: flex;
    align-items: center;
    justify-content: space-evenly;
    font-size: clamp(50px,7vw,112px);
    margin: 0 8%;
    animation: float 3.8s ease-in-out infinite;
}

@keyframes float {
    50% {
        transform: translateY(-12px);
    }
}

.hero-title {
    font:
        900 clamp(74px,10vw,176px)/1.05
        monospace;
    letter-spacing: clamp(2px,.8vw,12px);
    color: #7fc6ff;
    text-shadow:
        5px 5px 0 #3e57b5,
        10px 10px 0 #14153a;
    white-space: nowrap;
}

.hero-sub {
    font: 800 clamp(16px,2vw,31px) monospace;
    letter-spacing: clamp(1px,.5vw,8px);
    color: #ffb9ed;
    text-shadow: 3px 3px #54358e;
    margin: 22px 0 12px;
}

.hero-meta {
    font: 700 clamp(12px,1.2vw,18px) monospace;
    letter-spacing: 3px;
    color: #8beedc;
}

/* 픽셀 스타일 하단 지형 */
.pixel-hills {
    height: 66px;
    margin-top: 18px;
    background:
        repeating-linear-gradient(
            90deg,
            #5799ec 0 24px,
            #377dd4 24px 48px
        );
    clip-path: polygon(
        0 20%,3% 8%,7% 27%,11% 9%,
        15% 27%,19% 8%,23% 25%,
        27% 9%,31% 22%,35% 8%,
        39% 25%,43% 8%,47% 22%,
        51% 8%,55% 26%,59% 8%,
        63% 27%,67% 8%,71% 25%,
        75% 8%,79% 26%,83% 8%,
        87% 26%,91% 8%,95% 24%,
        100% 8%,100% 100%,0 100%
    );
}

/* 미션 선택 화면 */
.menu-title {
    text-align: center;
    color: #f5e7ff;
    font: 900 clamp(30px,3.6vw,56px) monospace;
    text-shadow: 3px 3px #6546a1;
    margin: 0 0 18px;
}

.menu-sub {
    text-align: center;
    color: #a8e5dc;
    font: 700 clamp(12px,1.3vw,17px) monospace;
    letter-spacing: 3px;
    margin-bottom: 25px;
}

.mission-card {
    background: #211744;
    border: 3px solid #7a5abb;
    box-shadow: 6px 6px #0a0923;
    padding: clamp(20px,2vw,34px);
    min-height: clamp(330px,51vh,570px);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.card-number {
    color: #89f4dc;
    font: 800 clamp(13px,1.15vw,19px) monospace;
    letter-spacing: 2px;
}

.card-icon {
    font-size: clamp(68px,7vw,125px);
    text-align: center;
    margin: 20px 0;
}

.card-name {
    color: #fff0ff;
    font-size: clamp(24px,2.1vw,39px);
    font-weight: 900;
    line-height: 1.3;
}

.card-sub {
    color: #8ee8ed;
    font: 700 clamp(11px,1.05vw,17px) monospace;
    letter-spacing: 1px;
    margin-top: 10px;
}

.card-desc {
    color: #c9bfe6;
    font-size: clamp(14px,1.1vw,19px);
    line-height: 1.7;
    margin: 24px 0;
}

.card-time {
    color: #ffda83;
    font: 900 clamp(24px,2.3vw,39px) monospace;
}

/* 픽셀 스타일 버튼 */
.stButton > button {
    width: 100%;
    border-radius: 0 !important;
    min-height: clamp(55px,7vh,74px) !important;
    background: #5437a1 !important;
    border: 3px solid #9cc8ff !important;
    color: #fff !important;
    box-shadow: 5px 5px #0a0924 !important;
    font: 900 clamp(15px,1.25vw,20px)
          monospace !important;
    letter-spacing: 1px;
}

.stButton > button:hover {
    background: #7254c5 !important;
    border-color: #d5e6ff !important;
}

.how {
    margin: 0 auto;
    max-width: 1100px;
    background: #241949;
    border: 3px solid #7961b8;
    padding: clamp(20px,4vw,60px);
    font-size: clamp(16px,1.3vw,22px);
    line-height: 2;
    color: #e9defb;
}

@media(max-width:750px) {
    .arcade {
        min-height: 60vh;
    }

    .hero-title {
        font-size: clamp(42px,11vw,76px);
    }

    .orbit {
        font-size: 45px;
    }

    .mission-card {
        min-height: 290px;
    }
}
</style>
""", unsafe_allow_html=True)


def html(content):
    # HTML 들여쓰기 때문에 코드로 표시되는 문제 방지
    st.markdown(
        "".join(line.strip() for line in content.splitlines()),
        unsafe_allow_html=True
    )


# ===========================
# 첫 번째 화면: 표지
# ===========================

if st.session_state.mecha_screen == "title":

    html("""
    <div class="arcade">
        <div class="arcade-top">
            ✦ SPACE ROBOTICS ARCADE ✦
        </div>

        <div class="orbit">
            <span>🚀</span>
            <span>🛰️</span>
            <span>🌎</span>
        </div>

        <div>
            <div class="hero-title">MECHA LAB</div>
            <div class="hero-sub">
                ★ START YOUR SPACE MISSION ★
            </div>
            <div class="hero-meta">
                1 PLAYER · 3 MISSIONS · ROBOT ARM
            </div>
        </div>

        <div class="pixel-hills"></div>
    </div>
    """)

    left, mid, right = st.columns([1, 2, 1])

    with mid:
        if st.button("▶ START GAME", key="start"):
            st.session_state.mecha_screen = "select"
            st.rerun()

        if st.button("ⓘ HOW TO PLAY", key="how"):
            st.session_state.mecha_screen = "how"
            st.rerun()


# ===========================
# 두 번째 화면: 조작법
# ===========================

elif st.session_state.mecha_screen == "how":

    html("""
    <div class="menu-title">HOW TO PLAY</div>

    <div class="how">
        🦾 빨간 관절을 마우스로 드래그해 회전하세요.
        <br>
        🎮 집게 끝을 목표에 맞추고
        Space 키 또는 버튼으로 잡거나 놓으세요.
        <br>
        🪨 암석은 놓으면 중력에 따라 떨어지고 굴러갑니다.
        <br>
        ⏱ 제한시간 내에 미션을 완료하세요.
        <br>
        🛰️ 위성은 단계별 정비 작업을 모두 완료해야 합니다.
    </div>
    """)

    if st.button("◀ BACK TO TITLE"):
        st.session_state.mecha_screen = "title"
        st.rerun()


# ===========================
# 세 번째 화면: 미션 선택
# ===========================

else:

    html("""
    <div class="menu-title">✦ SELECT MISSION ✦</div>

    <div class="menu-sub">
        ONE PLAYER · THREE SPACE OPERATIONS
    </div>
    """)

    cols = st.columns(3, gap="large")

    for col, m in zip(cols, MISSIONS):

        with col:

            html(f"""
            <div class="mission-card">

                <div class="card-number">
                    MISSION {m['n']} / {m['sub']}
                </div>

                <div class="card-icon">
                    {m['icon']}
                </div>

                <div>
                    <div class="card-name">
                        {m['name']}
                    </div>

                    <div class="card-sub">
                        {m['sub']}
                    </div>

                    <div class="card-desc">
                        {m['desc']}
                    </div>

                    <div class="card-time">
                        ⏱ {m['time']}
                    </div>
                </div>

            </div>
            """)

            if st.button(
                f"▶ MISSION {m['n']}",
                key=m["n"]
            ):
                st.switch_page(m["path"])

    if st.button("◀ BACK TO TITLE"):
        st.session_state.mecha_screen = "title"
        st.rerun()
