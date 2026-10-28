from pathlib import Path
import json
import streamlit as st
import streamlit.components.v1 as components

BASE=Path(__file__).resolve().parent
CONFIG={
 'rock':{'title':'화성 암석 집기','duration':180,'description':'암석에 그리퍼를 접근시켜 집은 뒤 위쪽 목표 구역에 놓으세요.'},
 'battery':{'title':'배터리 분리하기','duration':300,'description':'배터리 중앙을 집은 후 오른쪽으로 잡아당겨 게이지를 채우세요.'},
 'satellite':{'title':'위성 수리','duration':420,'description':'장애물을 집어 치운 뒤 버튼을 누르고 스위치를 잡아 오른쪽으로 당기세요.'}
}
def run(mission):
 st.set_page_config(page_title='MECHA LAB',page_icon='🦾',layout='wide',initial_sidebar_state='collapsed')
 st.markdown('''<style>[data-testid="stSidebar"],[data-testid="stSidebarNav"],[data-testid="stSidebarCollapsedControl"]{display:none!important}.block-container{max-width:1180px;padding-top:1rem}.stApp{background:#131a24;color:#f1e6d8}</style>''',unsafe_allow_html=True)
 cfg=CONFIG[mission]
 st.title('🦾 '+cfg['title'])
 st.caption(cfg['description'])
 template=(BASE/'assets'/'game.html').read_text(encoding='utf-8')
 html=template.replace('__GAME_CONFIG__',json.dumps({'mission':mission,**cfg},ensure_ascii=False))
 components.html(html,height=685,scrolling=False)
 if st.button('← 미션 선택 화면으로 돌아가기',use_container_width=True):st.switch_page('main.py')
 st.caption('조작법: 빨간 관절을 드래그해서 회전 → 그리퍼를 대상에 접근 → [잡기/놓기] 버튼. 관절마다 감도가 다릅니다. 물리 판정은 교육용 간이 모델입니다.')
