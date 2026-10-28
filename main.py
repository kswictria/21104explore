import streamlit as st
st.set_page_config(page_title='MECHA LAB',page_icon='🦾',layout='wide',initial_sidebar_state='collapsed')
st.markdown('''<style>[data-testid="stSidebar"],[data-testid="stSidebarNav"],[data-testid="collapsedControl"],[data-testid="stSidebarCollapsedControl"]{display:none!important}.block-container{max-width:1200px;padding-top:2rem}.stApp{background:#f6f1e7;color:#28303c}h1,h2,h3,p{color:#28303c!important}div.stButton>button{background:#fff9ed;color:#28303c;border:2px solid #293442;border-radius:14px;padding:1rem;height:auto;min-height:64px}div.stButton>button:hover{border-color:#c76e44;background:#ffecdc;color:#28303c}</style>''',unsafe_allow_html=True)
st.caption('SPACE ROBOTICS · INDIE MECHANICAL PUZZLE')
st.title('🦾 MECHA LAB')
st.write('관절을 마우스로 돌려 우주 로봇팔을 조종하는 기계공학 퍼즐 게임. 세 가지 임무 중 하나를 선택하세요.')
cols=st.columns(3,gap='large')
missions=[('🪨','MISSION 01','화성 암석 집기','3분','암석을 집어 지정된 수거 지점으로 옮기기','pages/1_화성_암석_집기.py'),('🔋','MISSION 02','배터리 분리하기','5분','배터리를 잡은 채 뒤로 당겨 고정 장치 분리','pages/2_배터리_분리.py'),('🛰️','MISSION 03','위성 수리','7분','장애물 당기기 → 버튼 누르기 → 스위치 당기기','pages/3_위성_수리.py')]
for col,(emoji,n,title,limit,desc,path) in zip(cols,missions):
    with col:
        st.markdown(f'### {emoji} {n}')
        st.subheader(title)
        st.write(desc)
        st.caption('제한시간 '+limit)
        if st.button('미션 시작 →',key=path,use_container_width=True):st.switch_page(path)
