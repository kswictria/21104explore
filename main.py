
import streamlit as st
from textwrap import dedent

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
        "description": "화성 표면의 암석을 집어 샘플 보관함으로 운반하세요.",
        "time": "01:30",
        "path": "pages/1_화성_암석_집기.py"
    },
    {
        "number": "02",
        "icon": "🔋",
        "title": "배터리 분리하기",
        "english": "BATTERY EXTRACTION",
        "description": "잠금장치를 해제한 뒤 배터리를 안전하게 추출하세요.",
        "time": "02:00",
        "path": "pages/2_배터리_분리.py"
    },
    {
        "number": "03",
        "icon": "🛰️",
        "title": "위성 수리",
        "english": "SATELLITE REPAIR",
        "description": "제어 버튼, 전선 연결, 안테나 정렬을 완료하세요.",
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
            ellipse at 50% 15%,
            #24374d 0%,
            #111d2d 43%,
            #090f19 100%
        );
    color: #f3eee7;
}

.block-container {
    max-width: 1120px;
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #f4efe8 !important;
}

.hero {
    position: relative;
    overflow: hidden;
    text-align: center;
    padding: 75px 24px 65px;
    border: 1px solid #41576b;
    border-radius: 24px;
    background:
        radial-gradient(
            ellipse at 50% 28%,
            #34485b 0%,
            #18283a 48%,
            #101927 100%
        );
}

.hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(#ffffff06 1px, transparent 1px),
        linear-gradient(90deg, #ffffff06 1px, transparent 1px);
    background-size: 44px 44px;
    pointer-events: none;
}

.system {
    position: relative;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #86e5bf;
}

.robot-icon {
    position: relative;
    margin-top: 35px;
    font-size: 88px;
    animation: floating 4s ease-in-out infinite;
}

@keyframes floating {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-12px);
    }
}

.hero-title {
    position: relative;
    margin-top: 15px;
    font-size: clamp(52px, 9vw, 105px);
    font-weight: 900;
    letter-spacing: 7px;
    line-height: 1.2;
    color: #f6efe6;
    text-shadow: 5px 5px 0 #a66b55;
}

.hero-sub {
    position: relative;
    margin-top: 18px;
    font-size: 14px;
    letter-spacing: 5px;
    color: #8acdd3;
}

.hero-desc {
    position: relative;
    margin-top: 28px;
    color: #c6d4de;
    font-size: 17px;
    line-height: 2;
}

.hero-bottom {
    position: relative;
    margin-top: 36px;
    color: #8fa9ba;
    font-size: 11px;
    letter-spacing: 2px;
}

.section-label {
    color: #e8ac85;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 3px;
}

.mission-card {
    background: linear-gradient(135deg, #213447, #152333);
    border: 1px solid #456074;
    border-radius: 16px;
    padding: 24px;
    min-height: 305px;
    margin-bottom: 12px;
}

.mission-number {
    color: #f0b08b;
    font-size: 12px;
    letter-spacing: 2px;
    font-weight: 800;
}

.mission-icon {
    margin-top: 24px;
    font-size: 51px;
}

.mission-title {
    margin-top: 14px;
    color: #f5eee7;
    font-size: 23px;
    font-weight: 850;
}

.mission-en {
    margin-top: 7px;
    color: #89c9ce;
    font-size: 11px;
    letter-spacing: 1px;
}

.mission-desc {
    margin-top: 19px;
    color: #bdcbd6;
    line-height: 1.7;
    font-size: 13px;
    min-height: 44px;
}

.mission-time {
    margin-top: 16px;
    color: #f3ca8d;
    font-size: 19px;
    font-weight: 800;
}

.stButton > button {
    background: #d98d63;
    border: 1px solid #eab794;
    color: #172333;
    font-weight: 800;
    border-radius: 11px;
    min-height: 50px;
}

.stButton > button:hover {
    background: #f1b78f;
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

    # dedent를 이용해 HTML 들여쓰기를 제거
    hero_html = dedent("""
    <div class="hero">
        <div class="system">
            ● SYSTEM ONLINE / ALL MODULES READY
        </div>

        <div class="robot-icon">🦾</div>

        <div class="hero-title">MECHA LAB</div>

        <div class="hero-sub">
            SPACE ROBOTICS DIVISION
        </div>

        <div class="hero-desc">
            우주에서 기계를 다루는 가장 정밀한 방법.<br>
            당신의 손끝에서 세 가지 임무가 시작됩니다.
        </div>

        <div class="hero-bottom">
            ENGINEERING · CONTROL · PRECISION
        </div>
    </div>
    """).strip()

    st.markdown(hero_html, unsafe_allow_html=True)

    st.write("")

    st.button(
        "▶  INITIALIZE MISSION",
        key="start",
        use_container_width=True,
        on_click=start_game
    )

    st.markdown(
        '<p style="text-align:center;color:#8299aa;'
        'font-size:12px;margin-top:25px">'
        '3 MISSIONS AVAILABLE · MECHA LAB</p>',
        unsafe_allow_html=True
    )

else:

    st.markdown(
        '<div class="section-label">'
        'MISSION CONTROL / SELECT OPERATION'
        '</div>',
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

            # HTML을 한 줄 문자열로 결합해 렌더링 오류 방지
            card_html = (
                '<div class="mission-card">'
                f'<div class="mission-number">MISSION {mission["number"]}</div>'
                f'<div class="mission-icon">{mission["icon"]}</div>'
                f'<div class="mission-title">{mission["title"]}</div>'
                f'<div class="mission-en">{mission["english"]}</div>'
                f'<div class="mission-desc">{mission["description"]}</div>'
                f'<div class="mission-time">⏱ {mission["time"]}</div>'
                '</div>'
            )

            st.markdown(
                card_html,
                unsafe_allow_html=True
            )

            if st.button(
                f'MISSION {mission["number"]} 시작 →',
                key=f'mission_{mission["number"]}',
                use_container_width=True
            ):
                st.switch_page(mission["path"])

    st.write("")

    st.button(
        "← 타이틀 화면으로 돌아가기",
        use_container_width=True,
        on_click=back_to_cover
    )
