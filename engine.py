    if c['slope']>=pitch_lim:reasons.append('전후방 정적 전복 한계 초과')
    if not obstacle_ok:reasons.append('장애물 높이에 비해 바퀴가 작음 (게임 단순 기준)')
    if not clearance_ok:reasons.append('차체 지상고 부족')
    return {'success':ok,'demand':round(demand,1),'available':round(available,1),'motor_force':round(drive,1),'traction':round(grip,1),'pitch_limit':round(pitch_lim,1),'roll_limit':round(roll_lim,1),'reasons':reasons,'distance':60 if ok else round(60*min(.88,max(.12,available/max(demand,1)))*(.58 if not obstacle_ok or not clearance_ok else 1),1)}

def go(step):
    st.session_state.stage = step
    target = {0: 'main.py', 1: 'pages/1_화성_지도.py', 2: 'pages/2_로버_설계.py', 3: 'pages/3_주행_및_결과.py', 4: 'pages/3_주행_및_결과.py'}[step]
    st.switch_page(target)

def viewer(d,site,mode='design',success=True,height=520):
    js=(ROOT/'viewer.js').read_text(encoding='utf8')
    payload=json.dumps({'design':d,'site':site,'mode':mode,'success':success},ensure_ascii=False)
    html=f'''<!doctype html><html><head><meta charset="UTF-8"><style>html,body{{margin:0;background:#151a21;overflow:hidden}}#scene{{width:100%;height:100vh}}#status{{position:absolute;left:18px;top:14px;font:600 12px Arial;color:#e5d1bb;background:#121821bb;padding:9px 12px;border-radius:8px}}</style></head><body><div id="scene"></div><div id="status">{('● DRIVE TEST · AUTOPILOT' if mode=='drive' else '● DESIGN VIEW · DRAG TO ROTATE')}</div><script>window.ROVER_DATA={payload};</script><script type="importmap">{{"imports":{{"three":"https://cdn.jsdelivr.net/npm/three@0.165.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.165.0/examples/jsm/"}}}}</script><script type="module">{js}</script></body></html>'''
    components.html(html,height=height,scrolling=False)

names=['시작','화성 지도','로버 설계','지형 주행','임무 결과']
st.caption('ROVER FORGE / MARS SYSTEMS ENGINEERING')
st.progress(st.session_state.stage/4,text=f'{st.session_state.stage+1}/5  ·  {names[st.session_state.stage]}')
site=st.session_state.site;c=SITES[site];d=st.session_state.design

if st.session_state.stage==0:
    st.title('ROVER FORGE')
    st.subheader('설계한 기계가 화성에서 살아남을 수 있을까?')
    st.write('착륙 지역을 선택하고, 바퀴·차체·모터를 설계한 뒤 로버를 실제로 움직여 보세요. 마지막에 실패 원인까지 분석합니다.')
    viewer(d,c,'design',height=470)
    if st.button('임무 시작 →',type='primary',use_container_width=True):go(1)

elif st.session_state.stage==1:
    st.title('01 / 실제 화성 지도에서 탐사 지역 선택')
    st.write('NASA Mars Global Surveyor의 MOLA 고도 관측으로 만든 **실제 화성 전역 지도**입니다. 지도를 확인하고 아래에서 지역을 선택하세요.')
    # Actual NASA-hosted MOLA cylindrical map; no long download and no Plotly dependency.
    mars_image = 'https://marsoweb.nas.nasa.gov/globalData/images/fullscale/MOLA_cylin.jpg'
    st.markdown('**NASA MOLA — 화성 전역 지형 지도**')
    st.markdown(
        f'<div style="border:1px solid #705347;border-radius:13px;overflow:hidden;background:#332a27">'
        f'<img src="{mars_image}" alt="NASA MOLA 화성 전역 고도 지도" '
        f'style="display:block;width:100%;height:auto;min-height:180px;object-fit:contain" '
        f'loading="eager"/></div>',
        unsafe_allow_html=True,
    )
    st.caption('출처: NASA Ames Marsoweb, MOLA Science Team. 색은 지형의 고도 차이를 나타냅니다. 전역 지도는 개별 바위나 바퀴 주행 수준의 해상도가 아닙니다.')
    st.markdown(f'[NASA에서 실제 지도 열기]({mars_image})')
    st.subheader('탐사 지역 선택')
    selected=st.radio('어느 지역에서 로버를 시험할까요?',list(SITES),
        index=list(SITES).index(site),format_func=lambda k:SITES[k]['name'],horizontal=True)
    if selected!=site:
        st.session_state.site=selected
        st.rerun()
    c=SITES[selected]
    st.info(f'**{c["name"]}** | 위도 {c["lat"]}° · 동경 {c["lon"]}°\n\n{c["description"]}')
    st.caption('지역별 경사·마찰·장애물 조건은 실제 지도에서 추출한 측정값이 아니라 게임용 가정입니다.')
    left,right=st.columns(2)
    with left:
        if st.button('← 시작 화면',use_container_width=True):go(0)
    with right:
        if st.button('이 지역 선택 → 3D 로버 설계',type='primary',use_container_width=True):go(2)

elif st.session_state.stage==2:
    st.title('02 / 현장 환경에 맞춘 로버 설계')
    st.write(f'**임무 지역: {c["name"]}** — {c["description"]}')
    a,b,e=st.columns(3)
    a.metric('게임 경사 조건',f'{c["slope"]}°')
    b.metric('가정 마찰계수',f'{c["mu"]:.2f}')
    e.metric('가정 장애물 높이',f'{c["obstacle"]:.2f} m')
    st.caption('이 세 값은 DEM으로 측정한 실제 주행 지점 값이 아니라 설계 과제를 위한 가정입니다.')
    l,r=st.columns([1,2])
    with l:
        d['radius']=st.slider('바퀴 반지름 (m)',.14,.52,float(d['radius']),.01)
        d['width']=st.slider('바퀴 폭 (m)',.10,.38,float(d['width']),.01)
        d['grousers']=st.slider('바퀴 돌기 수',6,30,int(d['grousers']))
        d['clearance']=st.slider('지상고 (m)',.20,.75,float(d['clearance']),.01)
        d['body_length']=st.slider('차체 길이 (m)',1.0,2.4,float(d['body_length']),.05)
        d['body_width']=st.slider('차체 폭 (m)',.7,1.7,float(d['body_width']),.05)
        d['cg']=st.slider('무게중심 높이 (m)',.32,1.0,float(d['cg']),.02)
        d['mass']=st.slider('로버 질량 (kg)',50.,190.,float(d['mass']),5.)
        d['torque']=st.slider('바퀴당 모터 토크 (N·m)',4.,55.,float(d['torque']),1.)
    with r:
        viewer(d,c,'design',height=550)
        st.caption('3D 모델을 드래그해 회전하고 스크롤해 확대하세요. 매개변수를 바꾸면 즉시 갱신됩니다.')
        pred=calc(d,c)
        x,y,zcol=st.columns(3)
        x.metric('등판 요구력',f'{pred["demand"]} N')
        y.metric('사용 가능한 추진력',f'{pred["available"]} N')
        zcol.metric('전후방 정적 안정 한계',f'{pred["pitch_limit"]}°')
        if st.button('설계 완료 → 주행 시험',type='primary',use_container_width=True):st.session_state.design=d.copy();go(3)
        if st.button('← 다른 지형 선택'):go(1)

elif st.session_state.stage==3:
    st.title('03 / 화성 지형 전진 주행 테스트')
    st.write(f'{c["name"]} 시나리오의 경사와 장애물 조건에서 제작한 로버가 앞으로 이동하는 과정을 시각화합니다.')
    result=calc(d,c)
    viewer(d,c,'drive',success=result['success'],height=570)
    st.caption('주행 애니메이션은 Three.js 기반 시각화입니다. 성공/실패는 단순 구동력·정적 안정성·장애물 기준으로 판정하며, 연속적인 실제 접촉 물리 엔진은 아닙니다.')
    st.metric('목표 주행 거리','60 m')
    if st.button('주행 판정 완료 → 결과 보기',type='primary',use_container_width=True):
        st.session_state.result={'site':site,'design':d.copy(),'analysis':result};go(4)
    if st.button('← 로버 재설계'):go(2)

else:
    st.title('04 / 임무 결과')
    record=st.session_state.result or {'site':site,'design':d,'analysis':calc(d,c)}
    p=record['analysis']
    if p['success']:st.success('MISSION SUCCESS — 모든 간이 설계 통과 조건을 충족했습니다.')
    else:st.error('MISSION FAILED — 설계 개선이 필요합니다.')
    a,b,c1=st.columns(3)
    a.metric('판정 기반 주행 거리',f'{p["distance"]} / 60 m')
    b.metric('요구 구동력',f'{p["demand"]} N')
    c1.metric('사용 가능 구동력',f'{p["available"]} N')
    st.subheader('공학적 진단')
    if p['reasons']:
        for reason in p['reasons']:st.warning(reason)
    else:st.info('간이 모델에서 구동력, 안정성, 바퀴 크기와 지상고 조건을 충족했습니다.')
    st.write('실제 주행 검증을 위해서는 지반 침하, 바퀴 슬립, 현가장치의 동역학과 고해상도 DEM 기반 충돌 분석을 추가해야 합니다.')
    st.download_button('설계 및 결과 JSON 다운로드',data=json.dumps(record,ensure_ascii=False,indent=2),file_name='rover_forge_result.json',mime='application/json')
    if st.button('설계를 바꿔 다시 도전',type='primary',use_container_width=True):go(2)
    if st.button('새 임무 시작'):st.session_state.result=None;go(1)
