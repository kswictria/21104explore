
import streamlit as st

st.set_page_config(
    page_title="SWINGBY OVER",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Noto+Sans+KR:wght@400;600;800&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 20% 20%, #17244c 0%, transparent 35%),
        radial-gradient(ellipse at 80% 70%, #32104b 0%, transparent 35%),
        linear-gradient(145deg, #030611, #080a1d 55%, #10051d);
    color: #edf6ff;
    font-family: 'Noto Sans KR', sans-serif;
}

#MainMenu,
footer,
header {
    visibility: hidden;
}

[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    max-width: 100%;
    padding: 1rem 1rem 0;
}

.hero {
    position: relative;
    min-height: calc(100vh - 2rem);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    border: 1px solid rgba(91, 210, 255, .20);
    border-radius: 22px;
    background:
        radial-gradient(
            circle at 50% 48%,
            rgba(37, 58, 125, .28),
            transparent 30%
        ),
        radial-gradient(
            circle at 80% 30%,
            rgba(135, 33, 188, .18),
            transparent 25%
        ),
        linear-gradient(
            180deg,
            rgba(2, 5, 18, .7),
            rgba(4, 6, 22, .92)
        );
    box-shadow: inset 0 0 80px rgba(35, 106, 255, .08);
}

.hero:before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        radial-gradient(
            1px 1px at 10% 20%,
            white 99%,
            transparent
        ),
        radial-gradient(
            2px 2px at 20% 70%,
            #78eaff 99%,
            transparent
        ),
        radial-gradient(
            1px 1px at 35% 32%,
            white 99%,
            transparent
        ),
        radial-gradient(
            2px 2px at 70% 20%,
            #d5a2ff 99%,
            transparent
        ),
        radial-gradient(
            1px 1px at 90% 60%,
            white 99%,
            transparent
        ),
        radial-gradient(
            1px 1px at 55% 85%,
            white 99%,
            transparent
        ),
        radial-gradient(
            2px 2px at 45% 12%,
            #80aaff 99%,
            transparent
        );
    background-size: 300px 230px;
    opacity: .85;
    pointer-events: none;
}

.orbit {
    position: absolute;
    width: 310px;
    height: 310px;
    border: 1px solid rgba(83, 218, 255, .23);
    border-radius: 50%;
    box-shadow: 0 0 35px rgba(60, 119, 255, .08);
    pointer-events: none;
}

.orbit.two {
    width: 390px;
    height: 390px;
    border-color: rgba(195, 81, 255, .17);
}

.sun {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background:
        radial-gradient(
            circle at 35% 30%,
            #f7fcff,
            #71eaff 28%,
            #4a54d8 62%,
            #a327ff 85%
        );
    box-shadow:
        0 0 30px #3e9dff,
        0 0 90px rgba(123, 48, 255, .6);
    margin-bottom: 25px;
    pointer-events: none;
}

.game-title {
    z-index: 2;
    text-align: center;
    font-family: 'Orbitron', sans-serif;
    font-weight: 800;
    font-size: clamp(2.8rem, 7vw, 6.5rem);
    letter-spacing: .09em;
    line-height: 1.1;
    color: #e8fbff;
    text-shadow:
        0 0 8px #56e9ff,
        0 0 24px #168aff,
        0 0 55px #812dff;
    pointer-events: none;
}

.game-subtitle {
    z-index: 2;
    margin-top: 22px;
    color: #a7bbdf;
    letter-spacing: .28em;
    font-size: .85rem;
    text-align: center;
    pointer-events: none;
}

.shooting {
    position: absolute;
    width: 130px;
    height: 2px;
    background: linear-gradient(
        90deg,
        transparent,
        #4ceaff,
        white
    );
    box-shadow: 0 0 12px #46dfff;
    transform: rotate(-38deg);
    animation: shoot 3.6s linear infinite;
    opacity: 0;
    pointer-events: none;
}

.s1 {
    top: 18%;
    left: 8%;
    animation-delay: 0s;
}

.s2 {
    top: 35%;
    left: 72%;
    animation-delay: 1.2s;
}

.s3 {
    top: 65%;
    left: 20%;
    animation-delay: 2.1s;
}

.s4 {
    top: 12%;
    left: 85%;
    animation-delay: 2.7s;
}

@keyframes shoot {
    0% {
        transform: translate(0, 0) rotate(-38deg);
        opacity: 0;
    }

    10% {
        opacity: 1;
    }

    65% {
        opacity: .9;
    }

    100% {
        transform: translate(-240px, 180px) rotate(-38deg);
        opacity: 0;
    }
}

.hint {
    z-index: 2;
    margin-top: 48px;
    color: #d9faff;
    font-family: 'Orbitron', sans-serif;
    font-size: .9rem;
    letter-spacing: .22em;
    animation: pulse 1.7s ease-in-out infinite;
    pointer-events: none;
}

@keyframes pulse {
    0%, 100% {
        opacity: .5;
    }

    50% {
        opacity: 1;
        text-shadow: 0 0 12px #43dfff;
    }
}

/* 투명한 전체 화면 클릭 영역 */
div[data-testid="stButton"] {
    position: fixed !important;
    inset: 0 !important;
    z-index: 999999 !important;
    width: 100vw !important;
    height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
}

div[data-testid="stButton"] button {
    position: absolute !important;
    inset: 0 !important;
    width: 100% !important;
    height: 100% !important;
    min-height: 100vh !important;
    opacity: 0 !important;
    cursor: pointer !important;
    border: none !important;
    background: transparent !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

/* 클릭 영역의 텍스트를 화면에 표시하지 않음 */
div[data-testid="stButton"] button p {
    color: transparent !important;
}

/* 작은 화면 최적화 */
@media (max-width: 600px) {
    .hero {
        min-height: calc(100vh - 2rem);
    }

    .sun {
        width: 85px;
        height: 85px;
    }

    .orbit {
        width: 240px;
        height: 240px;
    }

    .orbit.two {
        width: 300px;
        height: 300px;
    }

    .game-subtitle {
        font-size: .65rem;
        letter-spacing: .12em;
    }

    .hint {
        font-size: .72rem;
        letter-spacing: .12em;
    }
}
</style>

<div class="hero">
    <div class="orbit"></div>
    <div class="orbit two"></div>

    <div class="sun"></div>

    <div class="shooting s1"></div>
    <div class="shooting s2"></div>
    <div class="shooting s3"></div>
    <div class="shooting s4"></div>

    <div class="game-title">
        SWINGBY<br>OVER
    </div>

    <div class="game-subtitle">
        GRAVITY IS YOUR ENGINE
    </div>

    <div class="hint">
        ▼ &nbsp; CLICK ANYWHERE TO START &nbsp; ▼
    </div>
</div>
""", unsafe_allow_html=True)

# 화면 전체를 덮는 투명한 클릭 영역
if st.button(
    "CLICK ANYWHERE TO START",
    key="start_anywhere"
):
    st.switch_page("pages/selectplanet.py")
