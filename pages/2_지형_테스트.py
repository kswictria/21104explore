import streamlit as st
from core import init,rover_html,engineering,terrain_patch
init()
st.caption('ROVER FORGE  /  PHASE 02 OF 03')
st.title('02 · 화성 지형 테스트')
st.write('실제 MOLA 관측 고도를 불러오며, 연결에 실패하면 시범용 지형을 명확히 표시합니다. 관측 지형의 해상도는 로버 바퀴보다 훨씬 커서 작은 암석은 모델링하지 않습니다.')
a,b,c=st.columns(3)
with a: lat=st.number_input('중심 위도 (°N)',-70.0,70.0,18.5,.5)
with b: lon=st.number_input('중심 경도 (°E)',0.0,359.0,77.5,.5)
with c: angle=st.slider('별도 주행 시험 경사각 (°)',0,35,15)
surface=st.selectbox('접지 조건 (가정값)', ['암반 (μ=0.70)','혼합 지반 (μ=0.55)','느슨한 모래 (μ=0.35)'])
mu={'암반 (μ=0.70)':.70,'혼합 지반 (μ=0.55)':.55,'느슨한 모래 (μ=0.35)':.35}[surface]
with st.spinner('화성 고도 데이터를 준비 중...'):
    terrain=terrain_patch(float(lat),float(lon))
st.info('지형 출처: '+terrain['source'])
rover_html(535,terrain)
st.caption('MOLA 고도 지형은 관측 기반이며 시각화를 위해 수직 축이 강조됩니다. 화면의 바위, 로버 크기와 충돌은 별도 게임 표현입니다. 아래 경사 시험은 지도 픽셀을 따라 실제로 주행한 결과가 아닙니다.')
res=engineering(st.session_state.design,angle,mu)
a,b,c=st.columns(3)
a.metric('필요 구동력',f"{res['required']} N")
b.metric('사용 가능 구동력',f"{res['available']} N")
c.metric('여유 구동력',f"{res['margin']} N")
st.write('시험 판정:', '✅ 기본 등판 조건 충족' if res['pass'] else '⚠️ 구동력·안정성 조건 부족')
left,right=st.columns(2)
with left:
    if st.button('← 설계 수정',use_container_width=True): st.switch_page('pages/1_설계실.py')
with right:
    if st.button('테스트 종료 → 결과 확인',type='primary',use_container_width=True):
        st.session_state.result={'analysis':res,'terrain_source':terrain['source'],'terrain_real':terrain['real'],'lat':lat,'lon':lon,'design':st.session_state.design.copy(),'surface':surface}
        st.switch_page('pages/3_미션_결과.py')
