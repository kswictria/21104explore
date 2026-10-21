import streamlit as st
import pandas as pd
from core import init, heading, params

init()
heading('MISSION LOG','테스트 기록 · 설계 비교 · CSV 출력')
history=st.session_state.history
if not history:
    st.info('아직 기록이 없습니다. 지형 테스트에서 「결과 기록하기」를 누르면 여기 표시됩니다.')
    if st.button('테스트하러 가기',type='primary'): st.switch_page('pages/2_지형_테스트.py')
else:
    df=pd.DataFrame(history)
    a,b,c=st.columns(3)
    a.metric('테스트 횟수',len(history))
    b.metric('통과 횟수',sum(x['판정']=='통과' for x in history))
    c.metric('최고 통과 경사',f"{max((x['경사(°)'] for x in history if x['판정']=='통과'),default=0)}°")
    st.dataframe(df,use_container_width=True,hide_index=True)
    st.download_button('CSV 다운로드',df.to_csv(index=False).encode('utf-8-sig'),file_name='rover_forge_mission_log.csv',mime='text/csv')
    if st.button('현재 세션 기록 초기화'):
        st.session_state.history=[]
        st.rerun()
st.divider()
st.subheader('현재 설계값')
st.json(params(),expanded=False)
st.caption('기록은 현재 Streamlit 접속 세션의 메모리에 저장됩니다. 새로고침이나 서버 재시작 후 영구 보존은 보장되지 않습니다.')
