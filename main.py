import streamlit as st
from core import init, heading

init()
heading('MISSION CONTROL','로버를 설계하고, 지형에서 시험하고, 결과를 기록하세요.')
st.markdown('### 화성에서 작동하는 탐사 로버를 직접 제작하세요')
st.write('바퀴 크기, 폭, 돌기, 차체 형상, 현가장치, 구동 토크를 변경하면 Three.js 3D 로버 모델이 갱신됩니다. 그다음 화성 중력 조건에서 설계를 비교해 보세요.')
a,b,c=st.columns(3,gap='large')
with a:
    st.subheader('01 · 🔧 3D 설계실')
    st.write('슬라이더를 움직여 바퀴·차체 형상을 실시간으로 변경합니다.')
    if st.button('설계실 열기',use_container_width=True,type='primary'): st.switch_page('pages/1_설계실.py')
with b:
    st.subheader('02 · 🪨 지형 테스트')
    st.write('경사와 지표면 마찰 조건을 바꿔 구동력·접지력 한계를 확인합니다.')
    if st.button('테스트 시작',use_container_width=True): st.switch_page('pages/2_지형_테스트.py')
with c:
    st.subheader('03 · 📋 미션 기록실')
    st.write('테스트 결과를 저장하고 이전 설계와 비교합니다.')
    if st.button('기록 보기',use_container_width=True): st.switch_page('pages/3_미션_기록.py')
st.divider()
st.info('이 게임은 실제 화성 지형 데이터와 접촉 물리 엔진을 아직 포함하지 않는 첫 버전입니다. Three.js는 CDN으로 불러오므로 인터넷 연결이 필요합니다.')
