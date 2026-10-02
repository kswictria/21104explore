
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="SWINGBY OVER",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 전체 화면 클릭 후 다음 페이지로 이동
if st.query_params.get("start") == "1":
    st.query_params.clear()
    st.switch_page("pages/1_행성_선택.py")

# 불필요한 Streamlit UI 숨기기
st.markdown("""
<style>
#MainMenu, footer, header,
[data-testid="stSidebar"] {
    display: none !important;
}
.block-container {
    max-width: 100% !important;
    padding: 0 !important;
}
iframe {
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# HTML과 CSS를 별도의 프레임에서 렌더링
components.html("""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* {
    box-sizing: border-box;
}

html, body {
    margin: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    font-family: Arial, sans-serif;
    background: #030611;
}

.scene {
    position: relative;
    width: 100%;
    height: 100vh;
    min-height: 550px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    cursor: pointer;
    background:
        radial-gradient(ellipse at 50% 48%,
            rgba(38, 60, 135, .34), transparent 30%),
        radial-gradient(ellipse at 80% 25%,
            rgba(114, 35, 160, .20), transparent 35%),
        linear-gradient(145deg, #030611, #080a1d 55%, #10051d);
}

.scene::before {
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background-image:
        radial-gradient(2px 2px at 10% 20%, #ffffff 99%, transparent),
        radial-gradient(2px 2px at 30% 70%, #65e9ff 99%, transparent),
        radial-gradient(2px 2px at 75% 25%, #d6a0ff 99%, transparent),
        radial-gradient(1px 1px at 90% 60%, #ffffff 99%, transparent),
        radial-gradient(1px 1px at 45% 15%, #ffffff 99%, transparent),
        radial-gradient(2px 2px at 65% 85%, #72aaff 99%, transparent);
    background-size: 220px 190px;
    animation: stars 18s linear infinite;
}

@keyframes stars {
    from { background-position: 0 0; }
    to { background-position: 220px 190px; }
}

.orbit {
    position: absolute;
    width: min(42vw, 390px);
    aspect-ratio: 1;
    border: 1px solid rgba(81, 210, 255, .28);
    border-radius: 50%;
    box-shadow: 0 0 35px rgba(43, 118, 255, .08);
    pointer-events: none;
}

.orbit.outer {
    width: min(54vw, 500px);
    border-color: rgba(173, 91, 255, .19);
}

.sun {
    position: relative;
    width: clamp(75px, 10vw, 120px);
    aspect-ratio: 1;
    border-radius: 50%;
    background: radial-gradient(
        circle at 35% 28%,
        #ffffff 0%,
        #8ef2ff 20%,
        #4779e8 52%,
        #a02dff 82%
    );
    box-shadow:
        0 0 24px #49cfff,
        0 0 70px rgba(82, 71, 255, .65),
        0 0 120px rgba(167, 38, 255, .23);
    margin-bottom: 32px;
    animation: glow 4s ease-in-out infinite;
    z-index: 2;
}

@keyframes glow {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.06); }
}

.title {
    position: relative;
    z-index: 3;
    color: #e8fbff;
    font-size: clamp(45px, 8vw, 100px);
    font-weight: 900;
    letter-spacing: .08em;
    line-height: 1.05;
    text-align: center;
    text-shadow:
        0 0 8px #56e9ff,
        0 0 25px #168aff,
        0 0 55px #812dff;
    user-select: none;
}

.subtitle {
    position: relative;
    z-index: 3;
    margin-top: 24px;
    color: #a7bbdf;
    font-size: clamp(10px, 1.3vw, 15px);
    letter-spacing: .25em;
    text-align: center;
    user-select: none;
}

.hint {
    position: relative;
    z-index: 3;
    margin-top: 55px;
    color: #d9faff;
    font-size: 12px;
    letter-spacing: .22em;
    animation: pulse 1.7s ease-in-out infinite;
    user-select: none;
}

@keyframes pulse {
    0%, 100% { opacity: .45; }
    50% {
        opacity: 1;
        text-shadow: 0 0 12px #43dfff;
    }
}

.shooting {
    position: absolute;
    width: 120px;
    height: 2px;
    background: linear-gradient(
        90deg, transparent, #4ceaff, #ffffff
    );
    box-shadow: 0 0 12px #46dfff;
    transform: rotate(-38deg);
    opacity: 0;
    pointer-events: none;
    animation: shoot 4s linear infinite;
}

.s1 { top: 18%; left: 12%; animation-delay: 0s; }
.s2 { top: 30%; left: 76%; animation-delay: 1.1s; }
.s3 { top: 65%; left: 28%; animation-delay: 2.2s; }
.s4 { top: 12%; left: 88%; animation-delay: 2.9s; }

@keyframes shoot {
    0% {
        transform: translate(0, 0) rotate(-38deg);
        opacity: 0;
    }
    12% { opacity: 1; }
    65% { opacity: .8; }
    100% {
        transform: translate(-260px, 190px) rotate(-38deg);
        opacity: 0;
    }
}

.corner {
    position: absolute;
    z-index: 3;
    color: rgba(138, 177, 221, .55);
    font-size: 10px;
    letter-spacing: .15em;
    user-select: none;
}

.top-left { top: 22px; left: 25px; }
.top-right { top: 22px; right: 25px; }
.bottom-left { bottom: 22px; left: 25px; }
.bottom-right { bottom: 22px; right: 25px; }

@media (max-width: 600px) {
    .subtitle { letter-spacing: .12em; }
    .hint { letter-spacing: .12em; }
}
</style>
</head>
<body>
<div class="scene" id="scene">
    <div class="orbit"></div>
    <div class="orbit outer"></div>

    <div class="shooting s1"></div>
    <div class="shooting s2"></div>
    <div class="shooting s3"></div>
    <div class="shooting s4"></div>

    <div class="sun"></div>

    <div class="title">SWINGBY<br>OVER</div>

    <div class="subtitle">
        GRAVITY IS YOUR ENGINE
    </div>

    <div class="hint">
        CLICK ANYWHERE TO START
    </div>

    <div class="corner top-left">DEEP SPACE / 001</div>
    <div class="corner top-right">SWINGBY PROGRAM</div>
    <div class="corner bottom-left">GRAVITY ASSIST ADVENTURE</div>
    <div class="corner bottom-right">SYSTEM READY</div>
</div>

<script>
document.getElementById("scene").addEventListener("click", function() {
    window.parent.location.search = "?start=1";
});
</script>
</body>
</html>
""", height=850, scrolling=False)
