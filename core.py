from pathlib import Path
import math
import streamlit as st

ROOT = Path(__file__).parent
DEFAULTS = {
    'wheel_radius': .29, 'wheel_width': .17, 'wheel_style': '그라우저 휠',
    'grouser_count': 16, 'grouser_height': 16, 'body_length': 1.6,
    'body_width': 1.05, 'clearance': .48, 'suspension': '6륜 로커-보기 (개념 모형)',
    'mass': 130, 'motor_torque': 27., 'cg_extra': .10,
}

def init():
    st.set_page_config(page_title='ROVER FORGE', page_icon='🛞', layout='wide')
    st.markdown('''<style>
      .block-container{max-width:1550px;padding-top:1.6rem}
      [data-testid="stMetricValue"]{font-size:1.5rem}
      .stApp{background:linear-gradient(180deg,#141b26 0%,#111722 60%,#181c25 100%)}
      h1,h2,h3{letter-spacing:.015em}
    </style>''',unsafe_allow_html=True)
    for key,val in DEFAULTS.items():
        if key not in st.session_state: st.session_state[key]=val
    if 'history' not in st.session_state: st.session_state.history=[]

def params():
    p={k:st.session_state[k] for k in DEFAULTS}
    p['grouser_height']=p['grouser_height']/1000
    return p

def controls():
    st.subheader('바퀴 설계')
    st.slider('바퀴 반지름 (m)', .16,.50,step=.01,key='wheel_radius')
    st.slider('바퀴 폭 (m)',.08,.35,step=.01,key='wheel_width')
    st.selectbox('바퀴 형태',['그라우저 휠','평활 휠','격자형 휠'],key='wheel_style')
    st.slider('돌기 수',8,28,step=2,key='grouser_count',disabled=st.session_state.wheel_style=='평활 휠')
    st.slider('돌기 높이 (mm)',0,35,key='grouser_height',disabled=st.session_state.wheel_style=='평활 휠')
    st.subheader('차체와 현가장치')
    st.slider('차체 길이 (m)',1.,2.3,step=.05,key='body_length')
    st.slider('차체 폭 (m)',.65,1.5,step=.05,key='body_width')
    st.slider('차체 지상고 (m)',.25,.95,step=.01,key='clearance')
    st.selectbox('현가장치',['6륜 로커-보기 (개념 모형)','6륜 고정 링크'],key='suspension')
    st.subheader('질량·구동계')
    st.slider('로버 총질량 (kg)',40,300,step=5,key='mass')
    st.slider('바퀴당 최대 토크 (N·m)',2.,90.,step=1.,key='motor_torque')
    st.slider('무게중심 추가 높이 (m)',0.,.35,step=.01,key='cg_extra')

def physics(angle_deg=16., mu=.65, cr=.08):
    p=params(); g=3.71; a=math.radians(angle_deg)
    force=6*p['motor_torque']/p['wheel_radius']
    required=p['mass']*g*(math.sin(a)+cr*math.cos(a))
    grip=mu*p['mass']*g*math.cos(a)
    cg=p['clearance']+.20+p['cg_extra']
    track=p['body_width']+p['wheel_width']
    tip=math.degrees(math.atan(track/2/cg))
    # Rear-facing slope stability is omitted; static lateral tip only.
    return {'force':force,'required':required,'grip':grip,'tip':tip,'ok':force>=required and grip>=required,
            'margin':min(force,grip)-required,'angle':angle_deg,'mu':mu,'cr':cr}

def viewer(height=580):
    comp=st.components.v2.component(
        name='rover_forge_threejs',
        html='<div id="rover-viewport"><div class="viewport-loading">3D 모델 로딩 중…</div></div>',
        css=(ROOT/'assets'/'viewer.css').read_text(encoding='utf-8'),
        js=(ROOT/'assets'/'viewer.js').read_text(encoding='utf-8'))
    comp(key='threejs_rover',data={'params':params()},height=height)

def heading(page,subtitle):
    st.title('🛞 ROVER FORGE')
    st.caption(f'MARS ENGINEERING LAB  /  {page}  ·  {subtitle}')

def caveat():
    st.caption('교육용 정적 근사 모델: 화성 중력 3.71 m/s², 6륜 균일 구동. 실제 지면 접촉, 침하, 현가장치 동역학, 구조 강도는 아직 해석하지 않습니다.')
