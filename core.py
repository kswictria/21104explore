from pathlib import Path
import json, math, struct, urllib.request
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

ROOT=Path(__file__).resolve().parent
DEFAULT={'radius':0.32,'width':0.20,'grousers':12,'grouser_height':0.025,'body_length':1.6,'body_width':1.05,'clearance':0.42,'mass':95,'torque':38,'cg':0.68,'suspension':'Rocker-bogie'}

# Data: MGS MOLA MEGDR, 4 pixels per degree, global int16 big-endian topography in metres.
# PDS archive (NASA/Washington University). Note: this global grid is ~15 km resolution at equator.
MOLA_URL='https://pds-geosciences.wustl.edu/mgs/urn-nasa-pds-mgs_mola_topography_derived/meg004/megt90n000cb.img'


def init():
    st.set_page_config(page_title='ROVER FORGE',page_icon='🪐',layout='wide',initial_sidebar_state='collapsed')
    st.markdown('''<style>
    [data-testid="stSidebar"], [data-testid="stSidebarNav"], [data-testid="collapsedControl"], [data-testid="stSidebarCollapsedControl"] {display:none!important;}
    .block-container{padding-top:1.3rem;max-width:1440px}
    .stApp{background:linear-gradient(135deg,#0b101b 0%,#151b27 58%,#211b1c 100%);color:#ecedf2}
    h1,h2,h3{letter-spacing:.02em} div.stButton>button{background:#c56741;color:white;border:0;border-radius:9px}
    div.stButton>button:hover{background:#e08056;color:white}
    </style>''',unsafe_allow_html=True)
    if 'design' not in st.session_state: st.session_state.design=DEFAULT.copy()
    if 'result' not in st.session_state: st.session_state.result=None


def rover_html(height=570,terrain=None):
    js=(ROOT/'assets'/'viewer.js').read_text(encoding='utf8')
    css=(ROOT/'assets'/'viewer.css').read_text(encoding='utf8')
    payload={'design':st.session_state.design,'terrain':terrain}
    page=f'''<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div id="app"></div>
    <script>window.ROVER_STATE={json.dumps(payload,ensure_ascii=False)};</script>
    <script type="importmap">{{"imports":{{"three":"https://cdn.jsdelivr.net/npm/three@0.165.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.165.0/examples/jsm/"}}}}</script><script type="module">{js}</script></body></html>'''
    components.html(page,height=height,scrolling=False)


def engineering(d,angle=15,mu=.65):
    g=3.71
    m=float(d['mass']);r=float(d['radius']);n=6
    slope=math.radians(angle)
    # simplified six-wheel, 6 driven wheels, motor torque at each wheel
    required=m*g*(math.sin(slope)+.06*math.cos(slope))
    drive=n*d['torque']/r
    grip=mu*m*g*math.cos(slope)
    available=min(drive,grip)
    track=float(d['body_width'])+.65*float(d['width'])
    roll_limit=math.degrees(math.atan((track/2)/float(d['cg'])))
    pitch_limit=math.degrees(math.atan((float(d['body_length'])*.38)/float(d['cg'])))
    return {'required':round(required,1),'drive':round(drive,1),'traction':round(grip,1),
            'available':round(available,1),'margin':round(available-required,1),
            'roll_limit':round(roll_limit,1),'pitch_limit':round(pitch_limit,1),
            'pass':available>=required and angle < pitch_limit,
            'angle':angle,'mu':mu}


@st.cache_data(show_spinner=False,ttl=86400)
def load_mola():
    # May fail when remote server unavailable; caller must label demo fallback honestly.
    with urllib.request.urlopen(urllib.request.Request(MOLA_URL,headers={'User-Agent':'ROVER-FORGE-educational/1.0'}),timeout=22) as r:
        raw=r.read()
    if len(raw)!=1440*720*2: raise ValueError(f'Unexpected MOLA file size: {len(raw)}')
    arr=np.frombuffer(raw,dtype='>i2').reshape(720,1440).astype(np.float32)
    return arr


def terrain_patch(lat=18.5,lon=77.5,span=8.0,size=65):
    """Latitude/longitude centred gridded heights. Source explicitly included."""
    try:
        grid=load_mola()
        # DEM longitudes east, row 0 near +90 latitude. Sample rectangular region.
        lats=np.linspace(lat+span/2,lat-span/2,size)
        lons=np.linspace(lon-span/2,lon+span/2,size)
        rr=np.clip(np.rint((90-lats)*4).astype(int),0,719)
        cc=(np.rint(lons*4).astype(int))%1440
        z=grid[np.ix_(rr,cc)]
        if not np.isfinite(z).all() or z.min()<-20000: raise ValueError('Invalid MOLA values')
        source='NASA MGS/MOLA 관측 고도 (MEGDR 4ppd)'
        real=True
    except Exception:
        # explicit visual fallback: never claim it to be observed elevation
        x=np.linspace(-1,1,size); X,Y=np.meshgrid(x,x)
        z=170*np.sin(2.4*X)*np.cos(2.9*Y)+270*np.exp(-((X-.25)**2+(Y+.20)**2)/.13)-200*np.exp(-((X+.35)**2+(Y-.15)**2)/.09)
        source='시범용 생성 지형 (실제 NASA 데이터 다운로드 실패)'
        real=False
    return {'heights':np.round(z-z.mean(),2).tolist(),'source':source,'real':real,
            'lat':lat,'lon':lon,'span_deg':span,'sample_count':size}
