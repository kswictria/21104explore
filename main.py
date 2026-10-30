
import streamlit as st

st.set_page_config(
    page_title="MECHA LAB | Space Robotics",
    page_icon="🦾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

MISSIONS = [
    {
        "number": "01",
        "icon": "🪨",
        "title": "화성 암석 집기",
        "english": "MARS SAMPLE COLLECTION",
        "description": "화성 표면의 암석 시료를 집어 샘플 보관함으로 운반하세요.",
        "time": "01:30",
        "path": "pages/1_화성_암석_집기.py"
    },
    {
        "number": "02",
        "icon": "🔋",
        "title": "배터리 분리하기",
        "english": "ORBITAL BATTERY EXTRACTION",
        "description": "잠금장치를 해제하고 배터리를 안전하게 분리하세요.",
        "time": "02:00",
        "path": "pages/2_배터리_분리.py"
    },
    {
        "number": "03",
        "icon": "🛰️",
        "title": "위성 수리",
        "english": "SATELLITE REPAIR OPERATION",
        "description": "버튼, 스위치, 전선, 안테나를 정비해 위성을 복구하세요.",
        "time": "04:00",
        "path": "pages/3_위성_수리.py"
    }
]

if "mecha_started" not in st.session_state:
    st.session_state.mecha_started = False

st.markdown("""
<style>
[data-testid="stSidebar"],
[data-testid="stSidebarNav"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

.stApp {
    background:
        radial-gradient(
            ellipse at 55% 10%,
            #23354b 0%,
            #111c2b 40%,
            #090f19 100%
        );
    color: #f3eee7;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
}

#MainMenu, footer {
    visibility: hidden;
}

h1, h2, h3 {
    color: #f4efe8 !important;
}

.hero {
    text-align: center;
    padding: 65px 20px 48px;
    border: 1px solid #34495c;
    border-radius: 22px;
    background:
        radial-gradient(
            circle at 50% 25%,
            #33465a 0%,
            #172637 40%,
            #101927 85%
        );
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(#ffffff06 1px,transparent 1px),
        linear-gradient(90deg,#ffffff06 1px,transparent 1px);
    background-size: 44px 44px;
    pointer-events: none;
}

.robot-icon {
    font-size: 78px;
    margin-bottom: 18px;
    animation: floatRobot 4s ease-in-out infinite;
}

@keyframes floatRobot {
    0%,100% {transform:translateY(0)}
    50% {transform:translateY(-12px)}
}

.hero-title {
    font-size: clamp(52px,9vw,105px);
    font-weight: 900;
    letter-spacing: 6px;
    line-height: 1.12;
    color: #f5eee4;
    text-shadow: 5px 5px 0px #a46b56;
}

.hero-sub {
    font-size: 14px;
    letter-spacing: 5px;
    color: #83c9cd;
    margin-top: 18px;
}

.hero-desc {
    margin-top: 28px;
    font-size: 17px;
    color: #c0cfda;
    line-height: 1.9;
}

.system {
    color: #81d9b7;
    font-size: 12px;
    letter-spacing: 2px;
    font-weight: bold;
    margin-bottom: 20px;
}

.section-label {
    color: #e8ac85;
    letter-spacing: 3px;
    font-size: 13px;
    font-weight: bold;
}

.mission-card {
    background: linear-gradient(
        135deg,
        #1c3042,
        #172535
    );
    border: 1px solid #455d6f;
    border-radius: 15px;
    padding: 22px;
    min-height: 160px;
    margin-top: 10px;
    transition: all .2s ease;
}

.mission-card:hover {
    border-color: #edaf85;
    transform: translateY(-2px);
}

.mission-icon {
    font-size: 42px;
    margin-bottom: 12px;
}

.mission-number {
    color: #f1b08c;
    font-size: 12px;
    letter-spacing: 2px;
    font-weight: bold;
}

.mission-title {
    font-size: 23px;
    font-weight: 800;
    margin-top: 7px;
    color: #f3ede7;
}

.mission-en {
    color: #8dc9cc;
    font-size: 11px;
    letter-spacing: 1.5px;
    margin-top: 6px;
}

.mission-desc {
    color: #b9c7d1;
    font-size: 13px;
    margin-top: 13px;
    line-height: 1.7;
}

.mission-time {
    color: #f4c68e;
    font-size: 17px;
    font-weight: 800;
    margin-top: 18px;
}

.stButton > button {
    background: #d98d63;
    border: 1px solid #e9b391;
    color: #172333;
    border-radius: 10px;
    font-weight: 800;
    min-height: 48px;
}

.stButton > button:hover {
    background: #f1b48b;
    color: #172333;
    border-color: #ffcfab;
}
</style>
""", unsafe_allow_html=True)


def start_game():
    st.session_state.mecha_started = True


def back_to_cover():
    st.session_state.mecha_started = False


if not st.session_state.mecha_started:

    st.markdown("""
    <div class="hero">
        <div class="system">
            ● SYSTEM ONLINE / ALL MODULES READY
        </div>

        <div class="robot-icon">🦾</div>

        <div class="hero-title">
            MECHA LAB
        </div>

        <div class="hero-sub">
            SPACE ROBOTICS DIVISION
        </div>

        <div class="hero-desc">
            우주에서 기계를 다루는 가장 정밀한 방법.<br>
            당신의 손끝에서 세 가지 임무가 시작됩니다.
        </div>

        <div style="
            margin-top:38px;
            color:#8fa9ba;
            font-size:12px;
            letter-spacing:2px;
        ">
            ENGINEERING · CONTROL · PRECISION
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if st.button(
        "▶  INITIALIZE MISSION",
        key="start",
        use_container_width=True,
        type="primary",
        on_click=start_game
    ):
        pass

    st.markdown(
        """
        <p style="
            text-align:center;
            color:#7f96a7;
            font-size:12px;
            margin-top:25px;
        ">
            3 MISSIONS AVAILABLE · MECHA LAB
        </p>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        '<div class="section-label">MISSION CONTROL / 001</div>',
        unsafe_allow_html=True
    )

    st.title("SELECT YOUR MISSION")

    st.caption(
        "세 가지 우주 정비 임무 중 하나를 선택하세요. "
        "제한시간 안에 로봇팔을 조작해 목표를 완료해야 합니다."
    )

    st.write("")

    columns = st.columns(3, gap="medium")

    for col, mission in zip(columns, MISSIONS):

        with col:

            st.markdown(
                f"""
                <div class="mission-card">
                    <div class="mission-number">
                        MISSION {mission['number']}
                    </div>

                    <div class="mission-icon">
                        {mission['icon']}
                    </div>

                    <div class="mission-title">
                        {mission['title']}
                    </div>

                    <div class="mission-en">
                        {mission['english']}
                    </div>

                    <div class="mission-desc">
                        {mission['description']}
                    </div>

                    <div class="mission-time">
                        ⏱ {mission['time']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                f"MISSION {mission['number']} 시작 →",
                key=f"mission_{mission['number']}",
                use_container_width=True
            ):
                st.switch_page(mission["path"])

    st.write("")

    if st.button(
        "← 타이틀 화면으로 돌아가기",
        on_click=back_to_cover
    ):
        pass
