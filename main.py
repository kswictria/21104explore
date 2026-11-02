
import streamlit as st

st.set_page_config(
    page_title="MECHA LAB | Space Arcade",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "mecha_screen" not in st.session_state:
    st.session_state.mecha_screen = "title"

st.markdown('''
<style>
[data-testid="stSidebar"],
[data-testid="stSidebarNav"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

.stApp {
    background: #100b29;
    color: #f4ecff;
}

.block-container,
[data-testid="stAppViewBlockContainer"] {
    max-width: none !important;
    width: 100% !important;
    padding: 18px clamp(22px,4vw,84px) 40px !important;
}

[data-testid="stMain"] {
    max-width: none !important;
}

.arcade {
    position: relative;
    isolation: isolate;
    height: clamp(420px,66vh,720px);
    overflow: hidden;
    border: 5px solid #584091;
    border-radius: 9px;
    background: radial-gradient(
        ellipse at 50% 72%,
        #33216c 0%,
        #19113b 55%,
        #110c30 100%
    );
    box-shadow:
        0 0 0 4px #20173e,
        0 14px 40px #06040c;
}

.arcade:before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        radial-gradient(#d9f7ff 1.8px,transparent 2px),
        radial-gradient(#e89fff 1.7px,transparent 2px);
    background-size: 91px 83px,137px 107px;
    background-position: 17px 22px,45px 54px;
    opacity: .8;
    animation: stars 25s linear infinite;
    z-index: -1;
}

@keyframes stars {
    to {
        background-position: 108px 105px,182px 161px;
    }
}

.arcade-top {
    text-align: center;
    padding: clamp(18px,3.7vh,35px) 0;
    color: #8fffd1;
    letter-spacing: 5px;
    font: bold clamp(12px,1.3vw,17px) monospace;
}

.space-art {
    position: absolute;
    inset: 15% 6% 22%;
    pointer-events: none;
}

.ship,.sat,.world {
    position: absolute;
    animation: float 4s ease-in-out infinite;
}

.ship {
    left: 11%;
    top: 15%;
    font-size: clamp(48px,6vw,100px);
}

.sat {
    right: 23%;
    top: 9%;
    font-size: clamp(42px,5vw,74px);
    animation-delay: -1.6s;
}

.world {
    right: 7%;
    top: 22%;
    font-size: clamp(57px,7vw,112px);
    animation-delay: -2.3s;
}

@keyframes float {
    50% {
        transform: translateY(-17px) rotate(5deg);
    }
}

.pixel-spark {
    position: absolute;
    color: #ffdc6d;
    font: 900 34px monospace;
    animation: twinkle 1.6s steps(2) infinite;
}

@keyframes twinkle {
    50% { opacity: .3; }
}

.hero-copy {
    position: absolute;
    left: 0;
    right: 0;
    top: 45%;
    transform: translateY(-24%);
    text-align: center;
    padding: 0 10px;
}

.hero-name {
    font: 900 clamp(54px,9vw,155px)/1 monospace;
    letter-spacing: clamp(2px,.65vw,12px);
    color: #85cfff;
    text-shadow:
        5px 5px 0 #3c61c1,
        9px 9px 0 #0d1041;
    white-space: nowrap;
}

.hero-sub {
    margin-top: 24px;
    color: #ffd1f7;
    letter-spacing: clamp(1px,.5vw,8px);
    font: 800 clamp(13px,2vw,29px) monospace;
}

.hero-meta {
    margin-top: 21px;
    color: #91f2d8;
    font: 700 clamp(11px,1.25vw,17px) monospace;
    letter-spacing: 3px;
}

.pixel-hills {
    height: clamp(46px,8vh,75px);
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: repeating-linear-gradient(
        90deg,
        #68bdff 0 24px,
        #3f83d9 24px 45px
    );
    clip-path: polygon(
        0 23%,5% 5%,10% 35%,15% 8%,
        20% 35%,25% 8%,30% 24%,35% 7%,
        40% 30%,45% 6%,50% 22%,55% 6%,
        60% 36%,65% 6%,70% 26%,75% 5%,
        80% 33%,85% 8%,90% 28%,95% 7%,
        100% 26%,100% 100%,0 100%
    );
}

.button-caption {
    text-align: center;
    color: #9b8ec8;
    font: 700 11px monospace;
    letter-spacing: 3px;
    margin-top: 10px;
}

.stButton > button {
    background: #57389d !important;
    color: #fff4da !important;
    border: 3px solid #99caff !important;
    border-radius: 2px !important;
    box-shadow: 5px 5px #211346 !important;
    font: 900 clamp(15px,1.2vw,20px) monospace !important;
    min-height: 56px !important;
}

.stButton > button:hover {
    background: #7855c6 !important;
    border-color: #ffdf9b !important;
}

.m-title {
    text-align: center;
    color: #f8e8ff;
    font: 900 clamp(30px,3.4vw,55px) monospace;
    text-shadow: 3px 3px #6e43b2;
    margin: 8px 0 14px;
}

.m-sub {
    text-align: center;
    color: #97eee3;
    font: 700 14px monospace;
    letter-spacing: 3px;
    margin-bottom: 28px;
}

.m-card {
    min-height: clamp(320px,50vh,530px);
    background: #211742;
    border: 3px solid #795ab7;
    padding: clamp(20px,2.1vw,36px);
    box-shadow: 6px 6px #09071d;
    color: #f5ecff;
}

.m-num {
    color: #81edc2;
    font: 700 clamp(12px,1vw,17px) monospace;
}

.m-icon {
    font-size: clamp(64px,7vw,115px);
    margin: clamp(24px,4vh,50px) 0;
}

.m-name {
    font-size: clamp(24px,2.3vw,38px);
    font-weight: 900;
}

.m-desc {
    color: #cfc2e5;
    font-size: clamp(14px,1.2vw,20px);
    line-height: 1.6;
    margin: 18px 0;
}

.m-time {
    color: #ffe394;
    font: 900 clamp(23px,2.3vw,36px) monospace;
}

.how {
    max-width: 1100px;
    margin: 20px auto;
    background: #251946;
    border: 3px solid #7456b4;
    padding: 32px;
    font-size: 19px;
    line-height: 2;
    color: #f4eaff;
}

@media(max-width:750px) {
    .hero-name { font-size: 11vw; }
    .hero-copy { top: 48%; }
    .arcade { height: 58vh; }
    .space-art { opacity: .73; }
    .m-card { min-height: 280px; }
}
</style>
''', unsafe_allow_html=True)


def html(s):
    # HTML이 코드 블록으로 표시되지 않게 한 줄로 결합
    st.markdown(
        ''.join(x.strip() for x in s.splitlines()),
        unsafe_allow_html=True
    )


# 화면 1: 타이틀
if st.session_state.mecha_screen == "title":

    html('''
    <div class="arcade">
      <div class="arcade-top">
        ★ SPACE ROBOTICS ARCADE ★
      </div>
      <div class="space-art">
        <span class="ship">🚀</span>
        <span class="sat">🛰️</span>
        <span class="world">🌎</span>
        <span class="pixel-spark" style="left:38%;top:15%">✦</span>
        <span class="pixel-spark" style="right:9%;top:3%">✧</span>
        <span class="pixel-spark" style="left:57%;top:58%">+</span>
      </div>
      <div class="hero-copy">
        <div class="hero-name">MECHA LAB</div>
        <div class="hero-sub">
          ★ START YOUR SPACE MISSION ★
        </div>
        <div class="hero-meta">
          1 PLAYER · 3 MISSIONS · ROBOT ARM
        </div>
      </div>
      <div class="pixel-hills"></div>
    </div>
    ''')

    st.write("")

    left, center, right = st.columns(
        [1.7, 1.1, 1.7],
        gap="medium"
    )

    with center:
        if st.button(
            "▶ START GAME",
            key="start",
            use_container_width=True
        ):
            st.session_state.mecha_screen = "select"
            st.rerun()

        if st.button(
            "ⓘ HOW TO PLAY",
            key="help",
            use_container_width=True
        ):
            st.session_state.mecha_screen = "how"
            st.rerun()

    html(
        '<div class="button-caption">'
        'PRESS START TO BEGIN / SINGLE PLAYER'
        '</div>'
    )


# 화면 2: 조작법
elif st.session_state.mecha_screen == "how":

    html('''
    <div class="m-title">HOW TO PLAY</div>
    <div class="how">
      🦾 빨간 관절을 마우스로 원형 드래그해 움직이세요.
      <br>
      🎮 집게를 목표에 맞춘 뒤 Space 또는 집게 버튼을
      눌러 잡거나 놓으세요.
      <br>
      🪨 암석을 놓으면 떨어지고 바닥에서 굴러갑니다.
      <br>
      ⏱ 제한시간 안에 세부 작업을 완료하세요.
    </div>
    ''')

    if st.button("◀ BACK TO TITLE"):
        st.session_state.mecha_screen = "title"
        st.rerun()


# 화면 3: 미션 선택
else:

    html(
        '<div class="m-title">✦ SELECT MISSION ✦</div>'
        '<div class="m-sub">'
        'ONE PLAYER · THREE SPACE OPERATIONS'
        '</div>'
    )

    missions = [
        (
            '01', '🪨', '화성 암석 집기',
            'MARS SAMPLE COLLECTION',
            '암석을 집어 멀리 떨어진 샘플 통으로 이동',
            '01:30',
            'pages/1_화성_암석_집기.py'
        ),
        (
            '02', '🔋', '배터리 분리',
            'BATTERY EXTRACTION',
            '잠금을 해제하고 배터리를 오른쪽으로 추출',
            '02:00',
            'pages/2_배터리_분리.py'
        ),
        (
            '03', '🛰️', '위성 수리',
            'SATELLITE REPAIR',
            '버튼 2개 · 스위치 · 4색 전선 · 신호 안테나',
            '04:00',
            'pages/3_위성_수리.py'
        )
    ]

    columns = st.columns(3, gap="large")

    for col, (n, icon, title, en, desc, time, path) in zip(
        columns, missions
    ):
        with col:

            html(f'''
            <div class="m-card">
                <div class="m-num">
                    MISSION {n} / {en}
                </div>
                <div class="m-icon">{icon}</div>
                <div class="m-name">{title}</div>
                <div class="m-desc">{desc}</div>
                <div class="m-time">⏱ {time}</div>
            </div>
            ''')

            if st.button(
                f"▶ MISSION {n}",
                key=f"mission_{n}",
                use_container_width=True
            ):
                st.switch_page(path)

    st.write("")

    if st.button("◀ BACK TO TITLE"):
        st.session_state.mecha_screen = "title"
        st.rerun()
