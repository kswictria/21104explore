from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
ROOT=Path(__file__).resolve().parent
STYLE='''<style>[data-testid="stSidebar"],[data-testid="stSidebarNav"],[data-testid="collapsedControl"],[data-testid="stSidebarCollapsedControl"]{display:none!important}.block-container{max-width:1250px;padding-top:1.2rem}.stApp{background:#f6f1e7;color:#29323f}h1,p{color:#29323f!important}div.stButton>button{border:2px solid #29323f;border-radius:12px;color:#29323f}</style>'''
CONFIG={1:('🪨 화성 암석 집기',180),2:('🔋 배터리 분리하기',300),3:('🛰️ 위성 수리',420)}
def show(num):
    st.set_page_config(page_title='MECHA LAB | '+CONFIG[num][0],page_icon='🦾',layout='wide',initial_sidebar_state='collapsed')
    st.markdown(STYLE,unsafe_allow_html=True)
    st.caption(f'MECHA LAB / MISSION {num:02d}')
    st.title(CONFIG[num][0])
    st.caption('빨간 관절을 클릭한 뒤 마우스를 원형으로 움직여 회전시키세요. 관절별 감도가 다릅니다. 그리퍼로 잡거나 놓으세요.')
    html=(ROOT/'assets'/'game.html').read_text(encoding='utf-8').replace('__MISSION__',str(num)).replace('__LIMIT__',str(CONFIG[num][1]))
    components.html(html,height=660,scrolling=False)
    if st.button('← 미션 선택 화면으로 돌아가기',use_container_width=True):st.switch_page('main.py')
