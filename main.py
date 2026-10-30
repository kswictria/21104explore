
import streamlit as st

st.set_page_config(
    page_title="MECHA LAB",
    page_icon="🦾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "mecha_started" not in st.session_state:
    st.session_state.mecha_started = False

MISSIONS = [
    {
        "number": "01",
        "icon": "🪨",
        "title": "화성 암석 집기",
        "english": "MARS SAMPLE COLLECTION",
        "description": "화성 암석을 집어 샘플 보관함으로 옮기세요.",
        "time": "01:30",
        "path": "pages/1_화성_암석_집기.py"
    },
    {
        "number": "02",
        "icon": "🔋",
        "title": "배터리 분리하기",
        "english": "BATTERY EXTRACTION",
        "description": "잠금장치를 해제하고 배터리를 추출하세요.",
        "time": "02:00",
        "path": "pages/2_배터리_분리.py"
    },
    {
        "number": "03",
        "icon": "🛰️",
        "title": "위성 수리",
        "english": "SATELLITE REPAIR",
        "description": "버튼, 스위치, 전선, 안테나를 정비하세요.",
        "time": "04:00",
        "path": "pages/3_위성_수리.py"
    }
]

st.markdown("""
<style>
[data-testid="stSidebar"],
[data-testid="stSidebarNav"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

.stApp {
    background: radial-gradient(
        ellipse at 50% 15%,
        #25394d 0%,
        #121f2e 45%,
        #09111d 100%
    );
    color: #f2ede5;
}

.block-container {
    max-width: 1130px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    position: relative;
    overflow: hidden;
    text-align: center;
    padding: 60px 20px;
    border: 1px solid #455e70;
    border-radius: 22px;
    background:
        radial-gradient(
            ellipse at 50% 30%,
            #334b61 0%,
            #1a2d40 48%,
            #101c2b 100%
        );
}

.hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(#ffffff07 1px, transparent 1px),
        linear-gradient(90deg, #ffffff07 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
}

.hero > div {
    position: relative;
    z-index: 1;
}

.system-status {
    color: #8ee6c3;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
}

.robot {
    font-size: 84px;
    margin-top: 30px;
    animation: floating 4s ease-in-out infinite;
}

@keyframes floating {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-12px); }
}

.game-title {
    font-size: clamp(48px, 8vw, 100px);
    font-weight: 900;
    letter-spacing: 6px;
    line-height: 1.25;
    color: #f6eee4;
    text-shadow: 5px 5px 0 #ac7359;
    margin-top: 14px;
}

.game-subtitle {
    font-size: 14px;
    letter-spacing: 4px;
    color: #93d0d6;
    margin-top: 15px;
}

.game-description {
    font-size: 17px;
    line-height: 1.9;
    color: #c8d5df;
    margin-top: 28px;
}

.game-footer {
    font-size: 11px;
    letter-spacing: 2px;
    color: #8eabba;
    margin-top: 32px;
}

.section-label {
    font-size: 12px;
    color: #e7ad88;
    letter-spacing: 3px;
    font-weight: 800;
}

.mission-card {
    min-height: 310px;
    padding: 22px;
    margin-bottom: 12px;
    border: 1px solid #476174;
    border-radius: 16px;
    background: linear-gradient(
        145deg,
        #22364a,
        #142334
    );
}

.mission-card:hover {
    border-color: #f1af84;
}

.mission-number {
    font-size: 12px;
    color: #edb18c;
    font-weight: bold;
    letter-spacing: 2px;
}

.mission-icon {
    font-size: 48px;
    margin-top: 24px;
}

.mission-title {
    font-size: 23px;
    font-weight: 800;
    color: #f5efe8;
    margin-top: 14px;
}

.mission-english {
    color: #8fcbd1;
    font-size: 11px;
    letter-spacing: 1px;
    margin-top: 8px;
}

.mission-description {
    color: #c1ced8;
    font-size: 13px;
    line-height: 1.8;
    min-height: 48px;
    margin-top: 18px;
}

.mission-time {
    color: #f2c78c;
    font-size: 20px;
    font-weight: 800;
    margin-top: 15px;
}

.stButton > button {
    background: #d99068;
    color: #182433;
    border: 1px solid #eab491;
    border-radius: 11px;
    font-weight: 800;
    min-height: 51px;
}

.stButton > button:hover {
    background: #f2b58c;
    color: #172333;
    border-color: #ffd4b1;
}
</style>
""", unsafe_allow_html=True)


def render_html(parts):
    # 모든 태그를 한 줄로 결합하여
    # Markdown의 들여쓰기 코드 블록 오류를 방지
    html = "".join(part.strip() for part in parts)
    st.markdown(html, unsafe_allow_html=True)


if not st.session_state.mecha_started:

    render_html([
        '<div class="hero">',
        '<div class="system-status">',
        '● SYSTEM ONLINE / ALL MODULES READY',
        '</div>',

        '<div class="robot">🦾</div>',

        '<div class="game-title">',
        'MECHA LAB',
        '</div>',

        '<div class="game-subtitle">',
        'SPACE ROBOTICS DIVISION',
        '</div>',

        '<div class="game-description">',
        '우주에서 기계를 다루는 가장 정밀한 방법.',
        '<br>',
        '당신의 손끝에서 세 가지 임무가 시작됩니다.',
        '</div>',

        '<div class="game-footer">',
        'ENGINEERING · CONTROL · PRECISION',
        '</div>',

        '</div>'
    ])

    st.write("")

    if st.button(
        "▶ INITIALIZE MISSION",
        key="start_mission",
        use_container_width=True
    ):
        st.session_state.mecha_started = True
        st.rerun()

    st.markdown(
        '<p style="text-align:center;color:#90aabc;'
        'font-size:12px;margin-top:25px;">'
        '3 MISSIONS AVAILABLE · MECHA LAB'
        '</p>',
        unsafe_allow_html=True
    )

else:

    render_html([
        '<div class="section-label">',
        'MISSION CONTROL / SELECT OPERATION',
        '</div>'
    ])

    st.title("SELECT YOUR MISSION")

    st.caption(
        "세 가지 우주 정비 임무 중 하나를 선택하세요. "
        "제한시간 안에 로봇팔을 조작해 임무를 완료해야 합니다."
    )

    st.write("")

    cols = st.columns(3, gap="medium")

    for col, mission in zip(cols, MISSIONS):
        with col:

            render_html([
                '<div class="mission-card">',

                '<div class="mission-number">',
                f'MISSION {mission["number"]}',
                '</div>',

                '<div class="mission-icon">',
                mission["icon"],
                '</div>',

                '<div class="mission-title">',
                mission["title"],
                '</div>',

                '<div class="mission-english">',
                mission["english"],
                '</div>',

                '<div class="mission-description">',
                mission["description"],
                '</div>',

                '<div class="mission-time">',
                f'⏱ {mission["time"]}',
                '</div>',

                '</div>'
            ])

            if st.button(
                f'MISSION {mission["number"]} 시작 →',
                key=f'open_{mission["number"]}',
                use_container_width=True
            ):
                st.switch_page(mission["path"])

    st.write("")

    if st.button(
        "← 타이틀 화면으로 돌아가기",
        use_container_width=True
    ):
        st.session_state.mecha_started = False
        st.rerun()
