import streamlit as st
from core import init
import json
init()
st.caption('ROVER FORGE  /  PHASE 03 OF 03')
st.title('03 · 임무 결과')
r=st.session_state.result
if not r:
    st.warning('아직 완료된 테스트가 없어. 설계실부터 시작해 줘.')
    if st.button('설계실로 이동'): st.switch_page('pages/1_설계실.py')
    st.stop()
a=r['analysis']
st.header('MISSION PASSED ✓' if a['pass'] else 'REDESIGN REQUIRED')
st.write('시험 대상 위치:',f"{r['lat']}°N, {r['lon']}°E")
st.caption(r['terrain_source']+' · '+r['surface'])
cols=st.columns(4)
for col,name,key,unit in zip(cols,['필요 구동력','가용 구동력','횡방향 정적 전복 한계','종방향 정적 전복 한계'],['required','available','roll_limit','pitch_limit'],['N','N','°','°']):
    col.metric(name,f"{a[key]} {unit}")
if a['pass']:
    st.success('단순화된 등판 조건을 만족했어. 다음 설계에서는 질량과 안정성도 비교해 보자.')
else:
    st.error('요구 구동력을 확보하지 못했거나 정적 전복 한계에 도달했어. 바퀴당 토크, 무게중심, 지반 조건을 다시 확인해 봐.')
st.markdown('### 엔지니어링 리포트')
st.write(f"총 질량 {r['design']['mass']} kg / 바퀴 반지름 {r['design']['radius']:.2f} m / 바퀴당 토크 {r['design']['torque']} N·m")
st.info('물리 모델 범위: 6륜 구동, 정적 경사, 구름저항 계수 0.06, 가정한 마찰계수. 동적 충격·침하·타이어 변형·현가장치 하중 분배는 미포함.')
st.download_button('결과 JSON 다운로드',json.dumps(r,ensure_ascii=False,indent=2),file_name='rover_forge_result.json',mime='application/json',use_container_width=True)
if st.button('← 다시 설계해서 도전',type='primary',use_container_width=True): st.switch_page('pages/1_설계실.py')
