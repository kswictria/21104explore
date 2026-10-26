from pathlib import Path
import math, json, base64
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
        raise FileNotFoundError('data/megt90n000cb.img가 없습니다')
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

def mars_map():
    # Official NASA Mars Trek WMTS raster tile layer.
    # Tiles cover -180..180 longitude and -90..90 latitude at zoom 0 (2x1 tiles).
    # Each zoom doubles the number of tile columns and rows.
    locations = [
        {"key": key, "name": site["name"], "lat": site["lat"],
         "lon": site["lon"], "description": site["description"]}
        for key, site in SITES.items()
    ]
    html = r"""
<!doctype html><html lang="ko"><head><meta charset="utf-8">
<style>
* {box-sizing:border-box} html,body{margin:0;background:#101721;color:#eee;font-family:Arial,sans-serif}
#map{height:570px;position:relative;overflow:hidden;background:#101925;border:1px solid #34404e;border-radius:13px;touch-action:none;cursor:grab}
#map:active{cursor:grabbing} #tiles{position:absolute;inset:0;pointer-events:none}
.tile{position:absolute;width:256px;height:256px;user-select:none;image-rendering:auto}
