from pathlib import Path
import math, json, time, io, urllib.request
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title='ROVER FORGE | Mars Engineering',page_icon='🪐',layout='wide',initial_sidebar_state='collapsed')
st.markdown('''<style>[data-testid="stSidebar"],[data-testid="stSidebarNav"],[data-testid="collapsedControl"],[data-testid="stSidebarCollapsedControl"]{display:none!important} .block-container{max-width:1350px;padding-top:1.25rem} .stApp{background:#0d1018;color:#e7e9ec} .stButton>button[kind="primary"]{background:#c76e48;border:0} h1,h2,h3{letter-spacing:.02em}</style>''',unsafe_allow_html=True)
ROOT=Path(__file__).parent
DEFAULT={'radius':0.28,'width':0.18,'grousers':14,'clearance':0.36,'body_length':1.5,'body_width':1.0,'mass':100.0,'torque':18.0,'cg':0.62,'suspension':'Rocker-bogie'}
SITES={
 'Jezero':{'name':'예제로 크레이터','lat':18.45,'lon':77.45,'slope':12.,'mu':.63,'roughness':.11,'obstacle':.15,'description':'고대 삼각주가 있는 충돌 크레이터. 퇴적층과 암석이 혼재하는 임무 환경을 모사합니다.'},
 'Gale':{'name':'게일 크레이터','lat':-5.4,'lon':137.8,'slope':19.,'mu':.58,'roughness':.15,'obstacle':.22,'description':'샤프산이 있는 크레이터. 상대적으로 급한 경사와 바위 장애물을 가정합니다.'},
 'Elysium':{'name':'엘리시움 평원','lat':4.5,'lon':135.6,'slope':6.,'mu':.39,'roughness':.04,'obstacle':.07,'description':'평탄한 용암 평원. 모래와 느슨한 표층에 의한 접지력 저하를 가정합니다.'},
 'Olympus':{'name':'올림푸스산 주변','lat':18.65,'lon':226.2,'slope':24.,'mu':.56,'roughness':.13,'obstacle':.19,'description':'화산 주변의 경사 환경. 큰 추진력과 안정성이 필요하도록 구성한 도전 구역입니다.'}
}
if 'stage' not in st.session_state: st.session_state.stage=0
if 'site' not in st.session_state: st.session_state.site='Jezero'
if 'design' not in st.session_state: st.session_state.design=DEFAULT.copy()
if 'result' not in st.session_state: st.session_state.result=None
if 'run_id' not in st.session_state: st.session_state.run_id=0

# NASA PDS MOLA global MEGDR, 4 samples per degree. This is regional, not rover-scale DEM.
MOLA_URL='https://pds-geosciences.wustl.edu/mgs/urn-nasa-pds-mgs_mola_topography_derived/meg004/megt90n000cb.img'
@st.cache_data(ttl=86400,show_spinner=False)
def mola_grid():
    # File can be placed locally by the user to avoid network dependency.
    p=ROOT/'data'/'megt90n000cb.img'
    if p.exists(): raw=p.read_bytes()
    else:
        req=urllib.request.Request(MOLA_URL,headers={'User-Agent':'RoverForgeEducational/1.0'})
        with urllib.request.urlopen(req,timeout=18) as f: raw=f.read()
    if len(raw)!=1440*720*2: raise ValueError('MOLA 파일 크기 불일치')
    return np.frombuffer(raw,dtype='>i2').reshape(720,1440).astype(float)

@st.cache_data(ttl=86400,show_spinner=False)
def heights_for(site):
    cfg=SITES[site];n=71; lat=cfg['lat'];lon=cfg['lon'];span=3.0
    lats=np.linspace(lat+span/2,lat-span/2,n);lons=np.linspace(lon-span/2,lon+span/2,n)
    try:
        g=mola_grid(); rr=np.clip(np.rint((90-lats)*4).astype(int),0,719);cc=np.rint(lons*4).astype(int)%1440
        z=g[np.ix_(rr,cc)]
        if np.any(z<-20000): raise ValueError('고도 결측')
        return z,True,'NASA MGS/MOLA MEGDR (4 pixels/degree)'
    except Exception:
        # Explicitly synthetic; never described as actual elevation.
        a=np.linspace(-1,1,n);X,Y=np.meshgrid(a,a)
        seed=list(SITES).index(site)
        z=210*np.exp(-((X-.38)**2+(Y+.1)**2)/(.20+seed*.02))-140*np.exp(-((X+.2)**2+(Y-.1)**2)/.12)+55*np.sin((X+seed)*4)*np.cos(Y*3)
        return z,False,'대체용 합성 지형 (NASA MOLA 데이터 미확보)'

def calc(d,c):
    g=3.71;m=d['mass'];r=d['radius'];theta=math.radians(c['slope'])
    demand=m*g*(math.sin(theta)+.07*math.cos(theta))
    drive=6*d['torque']/r
    grip=c['mu']*m*g*math.cos(theta)
    available=min(drive,grip)
    track=d['body_width']+d['width']*.8
    roll_lim=math.degrees(math.atan(track/(2*d['cg'])))
    pitch_lim=math.degrees(math.atan(d['body_length']*.38/d['cg']))
    obstacle_ok=d['radius']*.72>=c['obstacle']
    clearance_ok=d['clearance']>=c['obstacle']*.85
    ok=available>=demand and c['slope']<pitch_lim and obstacle_ok and clearance_ok
    reasons=[]
    if available<demand:reasons.append('구동력 또는 접지력이 등판 요구력을 충족하지 못함')
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
    st.title('01 / 화성 탐사 지역 선택')
    st.write('지도에서 후보 지역의 위치를 확인하고 시험할 탐사 지점을 선택하세요.')
    from plotly import graph_objects as go_plot
    # Geographical overview on the Mars longitude/latitude grid, not a false Earth basemap.
    try:
        z,real,source=heights_for(site)
    except Exception:z=np.zeros((71,71));real=False;source='합성 지형'
    col1,col2=st.columns([1.65,1])
    with col1:
        fig=go_plot.Figure()
        fig.add_trace(go_plot.Scatter(x=[v['lon'] if v['lon']<=180 else v['lon']-360 for v in SITES.values()],y=[v['lat'] for v in SITES.values()],mode='markers+text',text=[v['name'] for v in SITES.values()],textposition='top center',marker=dict(size=13,color='#ffb475'),hovertemplate='%{text}<extra></extra>'))
        fig.update_layout(title='화성 후보 지역 좌표도 (2D)',paper_bgcolor='#171c26',plot_bgcolor='#25232a',font_color='#f2e5d9',xaxis=dict(title='경도 (°)',range=[-180,180],gridcolor='#493b37'),yaxis=dict(title='위도 (°)',range=[-90,90],gridcolor='#493b37'),height=450,margin=dict(l=40,r=20,b=40,t=55))
        st.plotly_chart(fig,use_container_width=True)
        st.caption('위 그림은 좌표도이며 위성 영상 지도가 아닙니다. 선택 지역의 실제 고도 미리보기는 아래에서 확인할 수 있습니다.')
        z,real,source=heights_for(site)
        fig2=go_plot.Figure(data=go_plot.Heatmap(z=z,colorscale='Oryel',showscale=True,colorbar=dict(title='고도 m')))
        fig2.update_layout(title=f'{c["name"]} 주변 지역 고도 미리보기',height=260,margin=dict(l=20,r=20,t=40,b=20),paper_bgcolor='#171c26',font_color='#f2e5d9')
        st.plotly_chart(fig2,use_container_width=True)
        st.caption(('실제 자료: ' if real else '주의: ')+source+' / 광역 고도 자료이며 바위 규모 정밀 지형은 아님')
    with col2:
        selected=st.radio('탐사 지역',options=list(SITES),index=list(SITES).index(site),format_func=lambda k:SITES[k]['name'])
        if selected!=site:st.session_state.site=selected;st.rerun()
        st.markdown(f'### {c["name"]}')
        st.write(c['description'])
        st.metric('위도',f'{c["lat"]}°');st.metric('동경',f'{c["lon"]}°')
        st.info('주의: 아래 단계의 경사·마찰·장애물 수치는 실제 현장 측정치가 아닌 게임 시나리오 가정입니다.')
        if st.button('이 지형 선택 → 로버 설계',type='primary',use_container_width=True):go(2)
        if st.button('← 처음으로'):go(0)

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
