import streamlit as st
from core import init
init()
st.markdown('### ROVER FORGE  /  MARS ENGINEERING LAB')
st.title('설계하고. 시험하고. 살아남아라.')
st.markdown('#### 화성 로버 공학 설계 게임')
st.write('바퀴·차체·현가장치를 설계하고 실제 화성 고도 데이터 위에서 지형 시험을 시작하세요. 최종 결과에는 구동력과 안정성 분석이 표시됩니다.')
st.info('플레이 순서: ① 로버 설계 → ② 화성 지형 테스트 → ③ 임무 결과')
st.caption('시뮬레이션은 학습용 단순 모델입니다. NASA 로버의 실제 인증이나 정밀한 접지/동역학 해석을 대체하지 않습니다.')
if st.button('로버 설계 시작 →',type='primary',use_container_width=True):
    st.switch_page('pages/1_설계실.py')
