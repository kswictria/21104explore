import streamlit as st
from core import init,rover_html
init()
st.caption('ROVER FORGE  /  PHASE 01 OF 03')
st.title('01 · 로버 설계실')
st.write('설계값을 바꾸면 3D 로버 형상이 업데이트됩니다. 오른쪽 패널은 마우스로 회전·확대할 수 있어요.')
left,right=st.columns([.34,.66],gap='large')
with left:
    d=st.session_state.design
    with st.container(height=580,border=True):
        st.markdown('**WHEELS / 바퀴 설계**')
        d['radius']=st.slider('바퀴 반지름 (m)',.18,.50,float(d['radius']),.01)
        d['width']=st.slider('바퀴 폭 (m)',.10,.36,float(d['width']),.01)
        d['grousers']=st.slider('바퀴 돌기 개수',6,26,int(d['grousers']),2)
        d['grouser_height']=st.slider('돌기 높이 (m)',.005,.055,float(d['grouser_height']),.005)
        st.markdown('**CHASSIS / 차체 설계**')
        d['body_length']=st.slider('차체 길이 (m)',1.1,2.4,float(d['body_length']),.05)
        d['body_width']=st.slider('차체 폭 (m)',.75,1.5,float(d['body_width']),.05)
        d['clearance']=st.slider('지상고 (m)',.25,.75,float(d['clearance']),.01)
        d['cg']=st.slider('무게중심 높이 (m)',.40,1.05,float(d['cg']),.01)
        st.markdown('**POWER / 구동계**')
        d['mass']=st.slider('로버 질량 (kg)',50,170,int(d['mass']),5)
        d['torque']=st.slider('바퀴당 최대 토크 (N·m)',10,65,int(d['torque']),1)
        d['suspension']=st.selectbox('현가장치 유형',['Rocker-bogie','Rigid'],index=0 if d['suspension']=='Rocker-bogie' else 1)
with right:
    rover_html(580)
    st.caption('Three.js 파라메트릭 모델 · 실제 NASA CAD 모델은 아님 · 현가장치는 형상 표현이며 움직임 해석은 미구현')
if st.button('설계 확정 → 화성 지형 테스트',type='primary',use_container_width=True):
    st.session_state.result=None
    st.switch_page('pages/2_지형_테스트.py')
