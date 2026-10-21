import streamlit as st
from core import init, controls, params, physics, viewer, heading, caveat

init()
heading('DESIGN LAB','매개변수형 실시간 3D 설계')
left,right=st.columns([1.1,2.5],gap='large')
with left:
    with st.container(height=690,border=True): controls()
with right:
    viewer(550)
    a,b,c=st.columns(3)
    p=params(); res=physics()
    a.metric('바퀴 외경',f"{p['wheel_radius']*200:.0f} cm")
    b.metric('총 구동력',f"{res['force']:.0f} N")
    c.metric('측면 전복 임계각',f"{res['tip']:.1f}°")
    st.caption('마우스 왼쪽 드래그: 회전 / 휠: 확대·축소 / 오른쪽 드래그: 이동')
    caveat()
    if st.button('이 설계로 지형 테스트 →',type='primary'): st.switch_page('pages/2_지형_테스트.py')
