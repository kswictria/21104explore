import streamlit as st
from core import init, heading, physics, viewer, params, caveat

init()
heading('TERRAIN TEST','가상 경사면·지면 접지 시험')
terrain=st.selectbox('시험 환경',['암반 경사면','먼지 덮인 경사면','매끄러운 지반'])
mu={'암반 경사면':.75,'먼지 덮인 경사면':.45,'매끄러운 지반':.25}[terrain]
cr={'암반 경사면':.08,'먼지 덮인 경사면':.15,'매끄러운 지반':.06}[terrain]
angle=st.slider('시험 경사각 (°)',0,35,16)
r=physics(angle,mu,cr)
left,right=st.columns([2,1],gap='large')
with left:
    viewer(470)
    st.caption('3D 화면은 평평한 설계 뷰어입니다. 선택한 경사가 화면 지형에 반영되거나 로버가 실제로 움직이는 것은 아닙니다.')
with right:
    st.metric('사용 가능한 구동력',f"{r['force']:.0f} N")
    st.metric('요구 주행 힘',f"{r['required']:.0f} N")
    st.metric('접지력 상한',f"{r['grip']:.0f} N")
    st.metric('힘 여유량',f"{r['margin']:+.0f} N")
    if r['ok']: st.success('기준 통과: 정적 모델에서 구동 및 접지 조건 충족')
    else: st.error('기준 실패: 구동력 또는 접지력 부족')
    if st.button('결과 기록하기',type='primary',use_container_width=True):
        st.session_state.history.append({'번호':len(st.session_state.history)+1,'지형':terrain,'경사(°)':angle,
            '질량(kg)':params()['mass'],'바퀴 반지름(m)':params()['wheel_radius'],
            '구동력(N)':round(r['force'],1),'요구 힘(N)':round(r['required'],1),
            '접지 한계(N)':round(r['grip'],1),'판정':'통과' if r['ok'] else '실패'})
        st.success('이번 세션의 미션 기록에 저장했습니다.')
        st.switch_page('pages/3_미션_기록.py')
st.info('이 페이지의 지형별 마찰·구름저항 값은 게임용 가정이며 실제 화성 지반 측정값이 아닙니다.')
with st.expander('적용된 계산식'):
    st.latex(r'F_{drive}=6\tau/r')
    st.latex(r'F_{required}=mg(\sin\theta+c_r\cos\theta)')
    st.latex(r'F_{grip}=\mu mg\cos\theta')
    st.write('구동력과 접지력 모두 요구 힘 이상이어야 통과로 표시합니다. 실차 검증에 사용할 수 없습니다.')
caveat()
