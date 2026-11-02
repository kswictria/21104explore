import streamlit as st

st.set_page_config(page_title="MECHA LAB | Pixel Space Arcade", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")

if 'mecha_started' not in st.session_state:
    st.session_state.mecha_started = False
if 'mecha_help' not in st.session_state:
    st.session_state.mecha_help = False

st.markdown('''<style>
[data-testid="stSidebar"],[data-testid="stSidebarNav"],[data-testid="stSidebarCollapsedControl"]{display:none!important}
.stApp{background:#100d2b;color:#f4ecff}
.block-container{max-width:980px;padding-top:1.4rem}
h1,h2,h3{color:#f8eaff!important}
.arcade{position:relative;isolation:isolate;min-height:515px;overflow:hidden;border:5px solid #4a327a;border-radius:8px;background:radial-gradient(circle at 48% 56%,#2a1b61,#100c2e 76%);box-shadow:0 0 0 5px #151232,0 16px 50px #05020c}
.arcade:before{content:"";position:absolute;inset:0;background-image:radial-gradient(#d9f7ff 1.8px,transparent 2px),radial-gradient(#e89fff 1.8px,transparent 2px);background-size:91px 83px,137px 107px;background-position:17px 22px,45px 54px;opacity:.83;animation:stars 23s linear infinite;z-index:-1}
@keyframes stars{to{background-position:108px 105px,182px 161px}}
.arcade .pixel-title{font:1000 clamp(35px,7.9vw,75px)/1.3 monospace;letter-spacing:5px;color:#7cc8ff;text-align:center;text-shadow:4px 0 #426cf2,0 5px #234aa7,5px 8px #090c34;white-space:nowrap}
.arcade .pixel-sub{color:#f5e4ff;text-align:center;letter-spacing:5px;font:bold 16px monospace;text-shadow:2px 2px #773fa7}
.arcade .tag{color:#79ffb4;text-align:center;font:bold 13px monospace;letter-spacing:3px}
.arcade .world{height:145px;position:relative}
.orbit-planet{position:absolute;right:10%;top:35px;width:78px;height:78px;border:6px solid #74b6fa;border-radius:45%;background:linear-gradient(155deg,#71d58a 20%,#4ccac9 21%,#4085f6 55%,#76dc8e 56%);box-shadow:8px 8px #232f89;animation:float 5s ease-in-out infinite}
.pixel-rocket{position:absolute;left:13%;top:33px;font-size:74px;filter:drop-shadow(6px 6px #572b88);animation:float 3.4s ease-in-out infinite}
.pixel-sat{position:absolute;right:33%;top:8px;font-size:48px;animation:float 4s ease-in-out infinite reverse}
.pixel-star{position:absolute;color:#f4c94d;font:bold 35px monospace;animation:twinkle 2s steps(2) infinite}
@keyframes float{50%{transform:translateY(15px)}}@keyframes twinkle{50%{opacity:.25}}
.arcade .floor{position:absolute;bottom:0;left:0;right:0;height:53px;background:repeating-linear-gradient(90deg,#61b8f7 0 18px,#4785e3 18px 34px);clip-path:polygon(0 23%,5% 5%,10% 35%,15% 8%,20% 35%,25% 8%,30% 24%,35% 7%,40% 30%,45% 6%,50% 22%,55% 6%,60% 36%,65% 6%,70% 26%,75% 5%,80% 33%,85% 8%,90% 28%,95% 7%,100% 26%,100% 100%,0 100%)}
.stButton>button{background:#482d85;color:#fff6d9;border:3px solid #a8d7ff;border-radius:2px;box-shadow:5px 5px #21144b;font:bold 16px monospace;min-height:51px}
.stButton>button:hover{background:#754cbd;color:#fff;border-color:#ffe08f}
.m-card{min-height:240px;background:#211742;border:3px solid #6c56aa;padding:19px;border-radius:4px;box-shadow:5px 5px #0a0820;color:#f4ebff;font-family:monospace}
.m-card .num{color:#73ecb8;font-size:13px}.m-card .icon{font-size:48px;margin:12px 0}.m-card .name{font-size:21px;font-weight:900}.m-card .info{color:#c1addf;line-height:1.7;margin-top:12px;min-height:55px}.m-card .time{color:#ffe292;font-size:20px;font-weight:900;margin-top:8px}
</style>''',unsafe_allow_html=True)

def html(*parts):
    st.markdown(''.join(x.strip() for x in parts),unsafe_allow_html=True)

if not st.session_state.mecha_started:
    html('<div class="arcade">',
         '<div style="padding-top:28px" class="tag">★ SPACE ROBOTICS ARCADE ★</div>',
         '<div class="world">',
         '<span class="pixel-rocket">🚀</span><span class="pixel-sat">🛰️</span><span class="orbit-planet"></span>',
         '<span class="pixel-star" style="left:34%;top:60px">✦</span>',
         '<span class="pixel-star" style="right:7%;top:5px">✧</span>',
         '<span class="pixel-star" style="left:64%;top:90px">+</span>',
         '</div>',
         '<div class="pixel-title">MECHA LAB</div>',
         '<div class="pixel-sub">★ START YOUR SPACE MISSION ★</div>',
         '<div style="margin-top:28px" class="tag">1 PLAYER · 3 MISSIONS · ROBOT ARM</div>',
         '<div class="floor"></div>',
         '</div>')
    st.write('')
    a,b,c=st.columns([1,2,1])
    with b:
        if st.button('▶ START GAME',use_container_width=True):
            st.session_state.mecha_started=True
            st.session_state.mecha_help=False
            st.rerun()
        if st.button('ⓘ HOW TO PLAY',use_container_width=True):
            st.session_state.mecha_help=not st.session_state.mecha_help
            st.rerun()
    if st.session_state.mecha_help:
        st.info('빨간 관절을 마우스로 원형 드래그해 집게를 이동시키세요. 목표에 닿으면 **집게 닫기/열기** 또는 Space를 눌러 조작하세요. 제한시간 안에 미션을 수행하면 성공합니다.')
else:
    st.markdown('### ✦ SELECT MISSION')
    st.caption('ONE PLAYER · THREE SPACE OPERATIONS')
    missions=[
        ('01','🪨','화성 암석 집기','MARS SAMPLE COLLECTION','암석을 집어 멀리 떨어진 샘플 통으로 이동','01:30','pages/1_화성_암석_집기.py'),
        ('02','🔋','배터리 분리','BATTERY EXTRACTION','잠금을 해제하고 배터리를 오른쪽으로 추출','02:00','pages/2_배터리_분리.py'),
        ('03','🛰️','위성 수리','SATELLITE REPAIR','버튼·스위치·4색 전선·안테나 정비','04:00','pages/3_위성_수리.py')]
    for col, (num,icon,name,en,desc,duration,path) in zip(st.columns(3),missions):
        with col:
            html('<div class="m-card">',f'<div class="num">MISSION {num} / {en}</div>',
                 f'<div class="icon">{icon}</div>',f'<div class="name">{name}</div>',
                 f'<div class="info">{desc}</div>',f'<div class="time">⏱ {duration}</div>','</div>')
            if st.button(f'▶ MISSION {num}',key=num,use_container_width=True):
                st.switch_page(path)
    st.write('')
    if st.button('◀ BACK TO TITLE'):
        st.session_state.mecha_started=False
        st.rerun()
