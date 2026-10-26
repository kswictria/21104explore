
from pathlib import Path
import json
import math
import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="ROVER FORGE",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
[data-testid="stSidebar"],
[data-testid="stSidebarNav"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.3rem;
}

.stApp {
    background: #10131c;
    color: #f1eae4;
}
</style>
""", unsafe_allow_html=True)


SITES = {
    "Jezero": {
        "name": "예제로 크레이터",
        "lat": 18.45,
        "lon": 77.45,
        "slope": 12.0,
        "mu": 0.63,
        "obstacle": 0.15,
        "description": "고대 하천 삼각주와 퇴적암이 있는 탐사 지역입니다. 암석과 모래가 혼재합니다."
    },
    "Gale": {
        "name": "게일 크레이터",
        "lat": -5.4,
        "lon": 137.8,
        "slope": 19.0,
        "mu": 0.58,
        "obstacle": 0.22,
        "description": "샤프산이 있는 크레이터입니다. 퇴적층과 다양한 경사면을 탐사합니다."
    },
    "Elysium": {
        "name": "엘리시움 평원",
        "lat": 4.5,
        "lon": 135.6,
        "slope": 6.0,
        "mu": 0.39,
        "obstacle": 0.07,
        "description": "비교적 평탄한 화산성 평원으로 InSight 착륙지가 있는 지역입니다."
    },
    "Olympus": {
        "name": "올림푸스산 주변",
        "lat": 18.65,
        "lon": 226.2,
        "slope": 24.0,
        "mu": 0.56,
        "obstacle": 0.19,
        "description": "거대한 순상화산과 그 주변의 복잡한 화산 지형입니다."
    }
}

DEFAULT = {
    "radius": 0.28,
    "width": 0.18,
    "grousers": 14,
    "clearance": 0.36,
    "body_length": 1.5,
    "body_width": 1.0,
    "mass": 100.0,
    "torque": 18.0,
    "cg": 0.62,
    "suspension": "Rocker-bogie"
}

for name, val in [
    ("stage", 0),
    ("site", "Jezero"),
    ("design", DEFAULT.copy()),
    ("result", None)
]:
    if name not in st.session_state:
        st.session_state[name] = val


def move(stage):
    st.session_state.stage = stage

    paths = {
        0: "main.py",
        1: "pages/1_화성_지도.py",
        2: "pages/2_로버_설계.py",
        3: "pages/3_주행_및_결과.py",
        4: "pages/3_주행_및_결과.py"
    }

    st.switch_page(paths[stage])


def test_rover(d, s):
    gravity = 3.71
    angle = math.radians(s["slope"])
    weight = d["mass"] * gravity

    needed = weight * (
        math.sin(angle)
        + 0.07 * math.cos(angle)
    )

    motor = 6 * d["torque"] / d["radius"]

    traction = (
        s["mu"] * weight * math.cos(angle)
    )

    usable = min(motor, traction)

    pitch = math.degrees(
        math.atan(
            0.38 * d["body_length"] / d["cg"]
        )
    )

    problems = []

    if usable < needed:
        problems.append("등판 구동력 또는 접지력 부족")

    if s["slope"] >= pitch:
        problems.append("전후방 전복 안정성 부족")

    if d["radius"] * 0.72 < s["obstacle"]:
        problems.append("바퀴 크기에 비해 장애물이 높음")

    if d["clearance"] < s["obstacle"] * 0.85:
        problems.append("차체 지상고 부족")

    return {
        "success": not problems,
        "demand": round(needed, 1),
        "available": round(usable, 1),
        "pitch_limit": round(pitch, 1),
        "reasons": problems,
        "distance": 60 if not problems else 10
    }


def rover_view(d, s, drive=False, passed=True):
    fp = ROOT / "viewer.js"

    if not fp.exists():
        st.error(
            "저장소 루트에 viewer.js 파일이 없습니다."
        )
        return

    payload = json.dumps(
        {
            "design": d,
            "site": s,
            "mode": "drive" if drive else "design",
            "success": passed
        },
        ensure_ascii=False
    )

    js = fp.read_text(encoding="utf-8")

    html = """
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            html, body {
                margin: 0;
                background: #151a21;
            }

            #scene {
                width: 100%;
                height: 520px;
            }

            #status {
                position: absolute;
                left: 16px;
                top: 12px;
                color: #fff;
                background: #151a21bb;
                padding: 10px;
                font: 14px Arial;
            }
        </style>
    </head>

    <body>
        <div id="scene"></div>
        <div id="status">
            ROVER FORGE · 3D VIEW
        </div>

        <script>
            window.ROVER_DATA = __PAYLOAD__;
        </script>

        <script type="importmap">
        {
            "imports": {
                "three": "https://cdn.jsdelivr.net/npm/three@0.165.0/build/three.module.js",
                "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.165.0/examples/jsm/"
            }
        }
        </script>

        <script type="module">
        __SCRIPT__
        </script>
    </body>
    </html>
    """

    html = html.replace(
        "__PAYLOAD__", payload
    ).replace(
        "__SCRIPT__", js
    )

    components.html(
        html,
        height=530,
        scrolling=False
    )


def mars_map():

    places = [
        {"id": k, **v}
        for k, v in SITES.items()
    ]

    html = r"""
<!doctype html>
<html lang="ko">

<head>
<meta charset="utf-8">

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #141925;
    color: #fff;
    font: 14px Arial, sans-serif;
}

#map {
    height: 535px;
    width: 100%;
    position: relative;
    overflow: hidden;
    background: #262533;
    cursor: grab;
    touch-action: none;
    border-radius: 14px;
}

#map:active {
    cursor: grabbing;
}

.tile {
    position: absolute;
    width: 256px;
    height: 256px;
    pointer-events: none;
}

.pin {
    position: absolute;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #f8a368;
    border: 3px solid white;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 0 6px #df824c55;
    z-index: 4;
    cursor: pointer;
}

.pin:hover {
    background: #f06750;
}

.tip {
    display: none;
    position: absolute;
    z-index: 8;
    max-width: 305px;
    background: #101923f5;
    border: 1px solid #c98158;
    padding: 14px;
    border-radius: 10px;
    pointer-events: none;
    line-height: 1.5;
}

#ctrl {
    position: absolute;
    right: 12px;
    top: 12px;
    z-index: 10;
    display: grid;
    gap: 6px;
}

button {
    background: #1e293b;
    border: 1px solid #627084;
    color: white;
    padding: 10px;
    border-radius: 6px;
    cursor: pointer;
}

#info {
    padding: 11px;
    background: #222834;
    margin-top: 8px;
    border-radius: 8px;
    color: #ddd;
    font-size: 12px;
}
</style>
</head>

<body>

<div id="map">
    <div id="tiles"></div>
    <div id="pins"></div>
    <div id="tip" class="tip"></div>

    <div id="ctrl">
        <button id="plus">+</button>
        <button id="minus">−</button>
        <button id="home">초기화</button>
    </div>
</div>

<div id="info">
    NASA Mars Trek WMTS 지도 타일 연결 중...
</div>

<script>
const places = __PLACES__;

const base =
    'https://trek.nasa.gov/tiles/Mars/EQ/' +
    'Mars_MGS_MOLA_ClrShade_merge_global_463m/' +
    '1.0.0/default/default028mm/';

const holder = document.getElementById('map');
const tiles = document.getElementById('tiles');
const pins = document.getElementById('pins');
const tip = document.getElementById('tip');
const info = document.getElementById('info');

let zoom = 1;
let ox = 0;
let oy = 0;

let dragging = false;
let lastX = 0;
let lastY = 0;

let ok = 0;
let err = 0;

function size() {
    return {
        w: holder.clientWidth,
        h: holder.clientHeight
    };
}

function reset() {
    let {w, h} = size();

    zoom = 1;
    ox = (w - 1024) / 2;
    oy = (h - 512) / 2;

    paint();
}

function paint() {
    let {w, h} = size();

    const step = 256;
    const worldW = 512 * 2 ** zoom;
    const worldH = 256 * 2 ** zoom;

    const startX = Math.max(
        0,
        Math.floor((-ox) / step)
    );

    const endX = Math.min(
        2 ** (zoom + 1) - 1,
        Math.floor((w - ox) / step)
    );

    const startY = Math.max(
        0,
        Math.floor((-oy) / step)
    );

    const endY = Math.min(
        2 ** zoom - 1,
        Math.floor((h - oy) / step)
    );

    tiles.replaceChildren();
    pins.replaceChildren();

    tip.style.display = 'none';

    for (let y = startY; y <= endY; y++) {
        for (let x = startX; x <= endX; x++) {

            const img = document.createElement('img');

            img.className = 'tile';

            img.style.left = (
                ox + x * step
            ) + 'px';

            img.style.top = (
                oy + y * step
            ) + 'px';

            img.src =
                base + zoom + '/' +
                y + '/' + x + '.jpg';

            img.onload = () => {
                ok++;

                info.textContent =
                    'NASA 화성 지도 · 드래그 및 휠 확대 가능';
            };

            img.onerror = () => {
                err++;

                if (!ok) {
                    info.textContent =
                        'NASA 지도 타일 서버 응답 없음 · 연결 상태를 확인하세요.';
                }
            };

            tiles.appendChild(img);
        }
    }

    for (const p of places) {

        const lon = (
            ((p.lon + 180) % 360 + 360) % 360
        ) / 360;

        const lat = (
            90 - p.lat
        ) / 180;

        const x = ox + lon * worldW;
        const y = oy + lat * worldH;

        if (
            x < 0 ||
            x > w ||
            y < 0 ||
            y > h
        ) {
            continue;
        }

        const dot = document.createElement('div');

        dot.className = 'pin';

        dot.style.left = x + 'px';
        dot.style.top = y + 'px';
        dot.title = p.name;

        dot.onmouseenter = () => {
            tip.style.display = 'block';

            tip.innerHTML =
                '<b>' + p.name + '</b>' +
                '<p>위도 ' + p.lat + '°, 동경 ' +
                p.lon + '°</p>' +
                '<p>' + p.description + '</p>';

            tip.style.left = Math.min(
                x + 14,
                w - 315
            ) + 'px';

            tip.style.top = Math.max(
                8,
                Math.min(y + 16, h - 140)
            ) + 'px';
        };

        dot.onmouseleave = () => {
            tip.style.display = 'none';
        };

        pins.appendChild(dot);
    }
}

function adjust(dir, px, py) {
    const nz = Math.max(
        0,
        Math.min(7, zoom + dir)
    );

    if (nz === zoom) {
        return;
    }

    const r = 2 ** (nz - zoom);

    ox = px + (ox - px) * r;
    oy = py + (oy - py) * r;

    zoom = nz;

    paint();
}

holder.addEventListener(
    'wheel',
    e => {
        e.preventDefault();

        const a = holder.getBoundingClientRect();

        adjust(
            e.deltaY < 0 ? 1 : -1,
            e.clientX - a.left,
            e.clientY - a.top
        );
    },
    {passive: false}
);

holder.addEventListener(
    'pointerdown',
    e => {
        if (
            e.target.tagName === 'BUTTON' ||
            e.target.classList.contains('pin')
        ) {
            return;
        }

        dragging = true;

        lastX = e.clientX;
        lastY = e.clientY;

        holder.setPointerCapture(e.pointerId);
    }
);

holder.addEventListener(
    'pointermove',
    e => {
        if (!dragging) {
            return;
        }

        ox += e.clientX - lastX;
        oy += e.clientY - lastY;

        lastX = e.clientX;
        lastY = e.clientY;

        paint();
    }
);

holder.addEventListener(
    'pointerup',
    () => {
        dragging = false;
    }
);

holder.addEventListener(
    'pointercancel',
    () => {
        dragging = false;
    }
);

document.getElementById('plus').onclick = () => {
    adjust(
        1,
        size().w / 2,
        size().h / 2
    );
};

document.getElementById('minus').onclick = () => {
    adjust(
        -1,
        size().w / 2,
        size().h / 2
    );
};

document.getElementById('home').onclick = reset;

window.addEventListener('resize', reset);

reset();
</script>

</body>
</html>
"""

    html = html.replace(
        "__PLACES__",
        json.dumps(places, ensure_ascii=False)
    )

    components.html(
        html,
        height=585,
        scrolling=False
    )


stage = int(st.session_state.stage)

site = SITES[st.session_state.site]

d = st.session_state.design

st.caption("ROVER FORGE · MARS ENGINEERING")

st.progress(
    stage / 4,
    text=f"{stage + 1}/5 · " + [
        "시작",
        "화성 지도",
        "로버 설계",
        "지형 주행",
        "결과"
    ][stage]
)


if stage == 0:

    st.title("ROVER FORGE")

    st.write(
        "화성에서 지역을 선택하고 로버를 설계해 "
        "주행 성능을 시험합니다."
    )

    rover_view(d, site)

    if st.button(
        "임무 시작 →",
        type="primary",
        use_container_width=True
    ):
        move(1)


elif stage == 1:

    st.title("01 / 화성 탐사 지역 선택")

    st.write(
        "NASA Mars Trek의 화성 고도 타일 지도입니다. "
        "지도를 드래그하거나 확대해 보세요."
    )

    mars_map()

    selected = st.selectbox(
        "탐사할 지역",
        list(SITES),
        index=list(SITES).index(
            st.session_state.site
        ),
        format_func=lambda x: SITES[x]["name"]
    )

    st.info(SITES[selected]["description"])

    st.caption(
        "지역별 주행 난이도 수치는 실제 관측값이 아닌 "
        "게임용 조건입니다."
    )

    if st.button(
        "이 지역으로 로버 설계 →",
        type="primary",
        use_container_width=True
    ):
        st.session_state.site = selected
        move(2)

    if st.button("← 시작 화면"):
        move(0)


elif stage == 2:

    st.title("02 / 3D 로버 설계")

    st.write("선택 지역: " + site["name"])

    a, b, c = st.columns(3)

    a.metric(
        "시험 경사",
        f"{site['slope']}°"
    )

    b.metric(
        "마찰계수 가정",
        site["mu"]
    )

    c.metric(
        "장애물 가정",
        f"{site['obstacle']}m"
    )

    left, right = st.columns([1, 2])

    with left:

        sliders = [
            (
                "radius",
                "바퀴 반지름 (m)",
                0.14, 0.52, 0.01
            ),
            (
                "width",
                "바퀴 폭 (m)",
                0.10, 0.38, 0.01
            ),
            (
                "clearance",
                "지상고 (m)",
                0.20, 0.75, 0.01
            ),
            (
                "body_length",
                "차체 길이 (m)",
                1.0, 2.4, 0.05
            ),
            (
                "body_width",
                "차체 폭 (m)",
                0.7, 1.7, 0.05
            ),
            (
                "cg",
                "무게중심 높이 (m)",
                0.32, 1.0, 0.02
            ),
            (
                "mass",
                "질량 (kg)",
                50.0, 190.0, 5.0
            ),
            (
                "torque",
                "바퀴당 토크 (N·m)",
                4.0, 55.0, 1.0
            )
        ]

        for key, label, lo, hi, step in sliders:

            d[key] = st.slider(
                label,
                float(lo),
                float(hi),
                float(d[key]),
                float(step),
                key="design_" + key
            )

        d["grousers"] = st.slider(
            "바퀴 돌기 수",
            6,
            30,
            int(d["grousers"]),
            key="design_grousers"
        )

    with right:

        rover_view(d, site)

        result = test_rover(d, site)

        st.metric(
            "필요 구동력",
            f"{result['demand']} N"
        )

        st.metric(
            "사용 가능 구동력",
            f"{result['available']} N"
        )

    if st.button(
        "설계 확정 → 주행 시작",
        type="primary",
        use_container_width=True
    ):
        st.session_state.design = d.copy()
        move(3)

    if st.button("← 지도"):
        move(1)


elif stage == 3:

    st.title("03 / 주행 시뮬레이션")

    result = test_rover(d, site)

    rover_view(
        d,
        site,
        drive=True,
        passed=result["success"]
    )

    st.caption(
        "3D 전진 주행은 시각적 애니메이션이며, "
        "주행 판정은 단순화한 공학 모델로 계산합니다."
    )

    if st.button(
        "주행 종료 → 결과",
        type="primary",
        use_container_width=True
    ):
        st.session_state.result = result
        move(4)

    if st.button("← 다시 설계"):
        move(2)


else:

    st.title("04 / 임무 결과")

    result = (
        st.session_state.result
        or test_rover(d, site)
    )

    if result["success"]:
        st.success(
            "MISSION SUCCESS · 임무 성공"
        )
    else:
        st.error(
            "MISSION FAILED · 임무 실패"
        )

    a, b, c = st.columns(3)

    a.metric(
        "요구 구동력",
        f"{result['demand']} N"
    )

    b.metric(
        "가용 구동력",
        f"{result['available']} N"
    )

    c.metric(
        "전복 임계각",
        f"{result['pitch_limit']}°"
    )

    for reason in result["reasons"]:
        st.warning(reason)

    st.caption(
        "실제 화성 지면 접촉의 정밀 물리 계산이 아닌 "
        "학습용 단순 모델입니다."
    )

    st.download_button(
        "결과 JSON 저장",
        json.dumps(
            {
                "site": st.session_state.site,
                "design": d,
                "result": result
            },
            ensure_ascii=False,
            indent=2
        ),
        file_name="mission_result.json"
    )

    if st.button(
        "다시 설계하기",
        type="primary",
        use_container_width=True
    ):
        move(2)

    if st.button("새 임무 선택"):
        move(1)
