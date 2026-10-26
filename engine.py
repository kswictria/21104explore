
from pathlib import Path
import math
import json
import base64

import streamlit as st
import streamlit.components.v1 as components

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
    max-width: 1350px;
    padding-top: 1.25rem;
}
.stApp {
    background: #0d1018;
    color: #e7e9ec;
}
.stButton > button[kind="primary"] {
    background: #c76e48;
    border: none;
}
</style>
""", unsafe_allow_html=True)

ROOT = Path(__file__).resolve().parent

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

SITES = {
    "Jezero": {
        "name": "예제로 크레이터",
        "lat": 18.45,
        "lon": 77.45,
        "slope": 12.0,
        "mu": 0.63,
        "obstacle": 0.15,
        "description": "고대 삼각주와 퇴적암이 존재하는 크레이터입니다. 암석 지형을 중심으로 탐사합니다."
    },
    "Gale": {
        "name": "게일 크레이터",
        "lat": -5.4,
        "lon": 137.8,
        "slope": 19.0,
        "mu": 0.58,
        "obstacle": 0.22,
        "description": "샤프산이 위치한 크레이터입니다. 경사면과 암석 장애물에 대응해야 합니다."
    },
    "Elysium": {
        "name": "엘리시움 평원",
        "lat": 4.5,
        "lon": 135.6,
        "slope": 6.0,
        "mu": 0.39,
        "obstacle": 0.07,
        "description": "화산 활동으로 형성된 평원입니다. 느슨한 표층을 가정한 접지력 시험을 진행합니다."
    },
    "Olympus": {
        "name": "올림푸스산 주변",
        "lat": 18.65,
        "lon": 226.2,
        "slope": 24.0,
        "mu": 0.56,
        "obstacle": 0.19,
        "description": "거대한 화산 주변 지형입니다. 높은 경사와 안정성 조건에 대응해야 합니다."
    }
}

for key, value in {
    "stage": 0,
    "site": "Jezero",
    "design": DEFAULT.copy(),
    "result": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = value


def go(stage):
    st.session_state.stage = stage

    paths = {
        0: "main.py",
        1: "pages/1_화성_지도.py",
        2: "pages/2_로버_설계.py",
        3: "pages/3_주행_및_결과.py",
        4: "pages/3_주행_및_결과.py"
    }

    st.switch_page(paths[stage])


def calculate(design, site):
    gravity = 3.71
    mass = design["mass"]
    radius = design["radius"]
    theta = math.radians(site["slope"])

    demand = mass * gravity * (
        math.sin(theta) + 0.07 * math.cos(theta)
    )

    motor_force = 6 * design["torque"] / radius

    traction = (
        site["mu"] * mass * gravity * math.cos(theta)
    )

    available = min(motor_force, traction)

    pitch_limit = math.degrees(
        math.atan(
            design["body_length"] * 0.38 / design["cg"]
        )
    )

    obstacle_ok = (
        radius * 0.72 >= site["obstacle"]
    )

    clearance_ok = (
        design["clearance"] >= site["obstacle"] * 0.85
    )

    success = (
        available >= demand
        and site["slope"] < pitch_limit
        and obstacle_ok
        and clearance_ok
    )

    reasons = []

    if available < demand:
        reasons.append("구동력 또는 접지력 부족")

    if site["slope"] >= pitch_limit:
        reasons.append("정적 전복 위험")

    if not obstacle_ok:
        reasons.append("바퀴 크기 부족")

    if not clearance_ok:
        reasons.append("지상고 부족")

    return {
        "success": success,
        "demand": round(demand, 2),
        "available": round(available, 2),
        "pitch_limit": round(pitch_limit, 2),
        "reasons": reasons
    }


def rover_viewer(design, site, mode="design", success=True):
    js_path = ROOT / "viewer.js"

    if not js_path.exists():
        st.error("viewer.js 파일이 없습니다.")
        return

    js = js_path.read_text(encoding="utf-8")

    payload = json.dumps({
        "design": design,
        "site": site,
        "mode": mode,
        "success": success
    }, ensure_ascii=False)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
    body {{
        margin: 0;
        background: #151a21;
        overflow: hidden;
    }}
    #scene {{
        width: 100%;
        height: 100vh;
    }}
    #status {{
        position: absolute;
        top: 14px;
        left: 18px;
        color: white;
        background: #121821cc;
        padding: 10px;
        border-radius: 8px;
        font: 13px Arial;
    }}
    </style>
    </head>
    <body>
    <div id="scene"></div>
    <div id="status">ROVER FORGE · 3D VIEW</div>

    <script>
    window.ROVER_DATA = {payload};
    </script>

    <script type="importmap">
    {{
        "imports": {{
            "three": "https://cdn.jsdelivr.net/npm/three@0.165.0/build/three.module.js",
            "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.165.0/examples/jsm/"
        }}
    }}
    </script>

    <script type="module">
    {js}
    </script>
    </body>
    </html>
    """

    components.html(html, height=550, scrolling=False)


def mars_map():
    local_map = ROOT / "assets" / "mars_map.jpg"

    if local_map.exists():
        encoded = base64.b64encode(
            local_map.read_bytes()
        ).decode("ascii")

        image_url = "data:image/jpeg;base64," + encoded
        map_source = "로컬 화성 지도"

    else:
        image_url = (
            "https://marsoweb.nas.nasa.gov/"
            "globalData/images/fullscale/MOLA_cylin.jpg"
        )
        map_source = "NASA 외부 지도 서버"

    locations = [
        {
            "key": key,
            "name": site["name"],
            "lat": site["lat"],
            "lon": site["lon"],
            "description": site["description"]
        }
        for key, site in SITES.items()
    ]

    html = """
    <!doctype html>
    <html lang="ko">
    <head>
    <meta charset="utf-8">
    <style>
    * {box-sizing:border-box}

    body {
        margin:0;
        background:#131821;
        color:#fff;
        font-family:Arial,sans-serif;
    }

    #viewport {
        height:510px;
        position:relative;
        overflow:hidden;
        border-radius:12px;
        background:#191e27;
        cursor:grab;
        touch-action:none;
    }

    #viewport:active {cursor:grabbing}

    #map {
        position:absolute;
        inset:0;
        width:100%;
        height:100%;
        pointer-events:none;
        user-select:none;
        transform-origin:0 0;
    }

    #markers {
        position:absolute;
        inset:0;
        pointer-events:none;
    }

    .marker {
        position:absolute;
        width:18px;
        height:18px;
        border-radius:50%;
        background:#ffad69;
        border:3px solid white;
        transform:translate(-50%,-50%);
        box-shadow:0 0 0 5px #ffad6950;
        pointer-events:auto;
        cursor:pointer;
    }

    .marker:hover {background:#ff593c}

    #tooltip {
        position:absolute;
        display:none;
        z-index:20;
        max-width:300px;
        background:#111827f2;
        border:1px solid #cb855a;
        border-radius:9px;
        padding:13px;
        pointer-events:none;
        line-height:1.6;
    }

    #controls {
        position:absolute;
        right:15px;
        top:15px;
        z-index:15;
        display:grid;
        gap:6px;
    }

    button {
        background:#172330;
        color:white;
        border:1px solid #777;
        border-radius:7px;
        padding:9px 13px;
        cursor:pointer;
    }

    #error {
        display:none;
        padding:14px;
        margin-top:8px;
        background:#59362c;
        border-radius:8px;
    }

    #status {
        color:#cabbb0;
        font-size:12px;
        padding:8px 0;
    }
    </style>
    </head>

    <body>
    <div id="viewport">
        <img id="map" draggable="false">
        <div id="markers"></div>
        <div id="tooltip"></div>

        <div id="controls">
            <button id="zoomIn">+</button>
            <button id="zoomOut">−</button>
            <button id="reset">초기화</button>
        </div>
    </div>

    <div id="error"></div>
    <div id="status">화성 지도 불러오는 중...</div>

    <script>
    const imageURL = __IMAGE__;
    const sites = __SITES__;
    const source = __SOURCE__;

    const viewport = document.getElementById("viewport");
    const map = document.getElementById("map");
    const markers = document.getElementById("markers");
    const tooltip = document.getElementById("tooltip");
    const error = document.getElementById("error");
    const status = document.getElementById("status");

    let zoom = 1;
    let offsetX = 0;
    let offsetY = 0;
    let dragging = false;
    let lastX = 0;
    let lastY = 0;
    let loaded = false;

    function position(lon, lat) {
        return {
            x: (((lon % 360) + 360) % 360) / 360,
            y: (90 - lat) / 180
        };
    }

    function render() {
        const w = viewport.clientWidth;
        const h = viewport.clientHeight;

        map.style.transform =
            `translate(${offsetX}px, ${offsetY}px) scale(${zoom})`;

        markers.innerHTML = "";

        sites.forEach(site => {
            const p = position(site.lon, site.lat);

            const x = offsetX + p.x * w * zoom;
            const y = offsetY + p.y * h * zoom;

            if (x < 0 || x > w || y < 0 || y > h) return;

            const marker = document.createElement("div");

            marker.className = "marker";
            marker.style.left = x + "px";
            marker.style.top = y + "px";
            marker.title = site.name;

            marker.addEventListener("mouseenter", () => {
                tooltip.style.display = "block";
                tooltip.innerHTML =
                    "<b>" + site.name + "</b>" +
                    "<p>위도: " + site.lat + "°</p>" +
                    "<p>동경: " + site.lon + "°</p>" +
                    "<p>" + site.description + "</p>";
            });

            marker.addEventListener("mousemove", () => {
                tooltip.style.left =
                    Math.max(10, Math.min(x + 20, w - 310)) + "px";
                tooltip.style.top =
                    Math.max(10, Math.min(y + 15, h - 165)) + "px";
            });

            marker.addEventListener("mouseleave", () => {
                tooltip.style.display = "none";
            });

            markers.appendChild(marker);
        });
    }

    function changeZoom(factor, x, y) {
        const next = Math.max(1, Math.min(8, zoom * factor));

        offsetX = x - (x - offsetX) * next / zoom;
        offsetY = y - (y - offsetY) * next / zoom;

        zoom = next;
        render();
    }

    viewport.addEventListener("wheel", e => {
        e.preventDefault();

        const rect = viewport.getBoundingClientRect();

        changeZoom(
            e.deltaY < 0 ? 1.25 : 0.8,
            e.clientX - rect.left,
            e.clientY - rect.top
        );
    }, {passive:false});

    viewport.addEventListener("pointerdown", e => {
        if (e.target.tagName === "BUTTON") return;
        if (e.target.classList.contains("marker")) return;

        dragging = true;
        lastX = e.clientX;
        lastY = e.clientY;

        viewport.setPointerCapture(e.pointerId);
    });

    viewport.addEventListener("pointermove", e => {
        if (!dragging) return;

        offsetX += e.clientX - lastX;
        offsetY += e.clientY - lastY;

        lastX = e.clientX;
        lastY = e.clientY;

        render();
    });

    viewport.addEventListener("pointerup", () => {
        dragging = false;
    });

    viewport.addEventListener("pointercancel", () => {
        dragging = false;
    });

    document.getElementById("zoomIn").onclick = () => {
        changeZoom(1.4,
            viewport.clientWidth / 2,
            viewport.clientHeight / 2);
    };

    document.getElementById("zoomOut").onclick = () => {
        changeZoom(1 / 1.4,
            viewport.clientWidth / 2,
            viewport.clientHeight / 2);
    };

    document.getElementById("reset").onclick = () => {
        zoom = 1;
        offsetX = 0;
        offsetY = 0;
        render();
    };

    map.onload = () => {
        loaded = true;
        status.textContent = "화성 지도 로드 완료 · " + source;
        render();
    };

    map.onerror = () => {
        error.style.display = "block";
        error.textContent =
            "지도 이미지 연결 실패: assets/mars_map.jpg를 추가하세요.";
        status.textContent = "화성 지도 로딩 실패";
    };

    map.src = imageURL;

    setTimeout(() => {
        if (!loaded) {
            error.style.display = "block";
            error.textContent =
                "지도 로딩 지연: 로컬 지도 파일을 추가하세요.";
        }
    }, 9000);

    window.addEventListener("resize", render);
    </script>
    </body>
    </html>
    """

    html = html.replace(
        "__IMAGE__", json.dumps(image_url)
    ).replace(
        "__SITES__", json.dumps(locations, ensure_ascii=False)
    ).replace(
        "__SOURCE__", json.dumps(map_source, ensure_ascii=False)
    )

    components.html(html, height=570, scrolling=False)

    if not local_map.exists():
        st.warning(
            "로컬 지도 파일이 없어 NASA 서버에 접속합니다. "
            "안정적으로 사용하려면 assets/mars_map.jpg를 추가하세요."
        )


stage = st.session_state.stage
site_key = st.session_state.site
site = SITES[site_key]
design = st.session_state.design

stage_names = [
    "시작",
    "화성 지도",
    "로버 설계",
    "주행 시험",
    "임무 결과"
]

st.caption("ROVER FORGE / MARS ENGINEERING")
st.progress(
    stage / 4,
    text=f"{stage + 1}/5 · {stage_names[stage]}"
)


if stage == 0:
    st.title("ROVER FORGE")
    st.subheader("당신의 로버는 화성에서 살아남을 수 있을까?")

    st.write(
        "실제 화성 지도에서 탐사 지역을 선택하고, "
        "로버를 직접 설계해 주행 시험에 도전하세요."
    )

    rover_viewer(design, site)

    if st.button(
        "임무 시작 →",
        type="primary",
        use_container_width=True
    ):
        go(1)


elif stage == 1:
    st.title("01 / 화성 탐사 지역 선택")

    mars_map()

    selected = st.selectbox(
        "탐사 지역",
        list(SITES),
        index=list(SITES).index(site_key),
        format_func=lambda x: SITES[x]["name"]
    )

    if selected != site_key:
        st.session_state.site = selected
        st.rerun()

    st.subheader(site["name"])
    st.write(site["description"])

    st.caption(
        "지도는 화성 관측 자료를 사용하지만, "
        "이후 시험의 경사·마찰·장애물 수치는 게임용 가정입니다."
    )

    if st.button(
        "이 지역 선택 → 3D 로버 설계",
        type="primary",
        use_container_width=True
    ):
        go(2)

    if st.button("← 처음으로"):
        go(0)


elif stage == 2:
    st.title("02 / 3D 로버 설계")
    st.write(f"탐사 지역: {site['name']}")

    a, b, c = st.columns(3)

    a.metric("게임 경사 조건", f"{site['slope']}°")
    b.metric("가정 마찰계수", site["mu"])
    c.metric("가정 장애물 높이", f"{site['obstacle']} m")

    left, right = st.columns([1, 2])

    with left:
        design["radius"] = st.slider(
            "바퀴 반지름 (m)",
            0.14, 0.52, float(design["radius"]), 0.01
        )

        design["width"] = st.slider(
            "바퀴 폭 (m)",
            0.10, 0.38, float(design["width"]), 0.01
        )

        design["grousers"] = st.slider(
            "바퀴 돌기 수",
            6, 30, int(design["grousers"])
        )

        design["clearance"] = st.slider(
            "지상고 (m)",
            0.20, 0.75, float(design["clearance"]), 0.01
        )

        design["body_length"] = st.slider(
            "차체 길이 (m)",
            1.0, 2.4, float(design["body_length"]), 0.05
        )

        design["body_width"] = st.slider(
            "차체 폭 (m)",
            0.7, 1.7, float(design["body_width"]), 0.05
        )

        design["cg"] = st.slider(
            "무게중심 높이 (m)",
            0.32, 1.0, float(design["cg"]), 0.02
        )

        design["mass"] = st.slider(
            "로버 질량 (kg)",
            50.0, 190.0, float(design["mass"]), 5.0
        )

        design["torque"] = st.slider(
            "바퀴당 모터 토크 (N·m)",
            4.0, 55.0, float(design["torque"]), 1.0
        )

    with right:
        rover_viewer(design, site)

        result = calculate(design, site)

        st.metric(
            "필요 구동력",
            f"{result['demand']} N"
        )

        st.metric(
            "사용 가능 구동력",
            f"{result['available']} N"
        )

        if st.button(
            "설계 완료 → 주행 시뮬레이션",
            type="primary",
            use_container_width=True
        ):
            st.session_state.design = design.copy()
            go(3)

        if st.button("← 화성 지도"):
            go(1)


elif stage == 3:
    st.title("03 / 화성 지형 주행 시뮬레이션")

    result = calculate(design, site)

    rover_viewer(
        design,
        site,
        mode="drive",
        success=result["success"]
    )

    st.caption(
        "전진 주행은 Three.js 애니메이션이며, "
        "현재 판정은 단순 공학 모델을 사용합니다."
    )

    if st.button(
        "주행 종료 → 임무 결과",
        type="primary",
        use_container_width=True
    ):
        st.session_state.result = result
        go(4)

    if st.button("← 로버 재설계"):
        go(2)


else:
    st.title("04 / 임무 결과")

    result = st.session_state.result

    if result is None:
        result = calculate(design, site)

    if result["success"]:
        st.success("MISSION SUCCESS · 임무 성공")
    else:
        st.error("MISSION FAILED · 임무 실패")

    a, b, c = st.columns(3)

    a.metric("요구 구동력", f"{result['demand']} N")
    b.metric("사용 가능한 구동력", f"{result['available']} N")
    c.metric("정적 안정 한계", f"{result['pitch_limit']}°")

    st.subheader("공학적 분석")

    if result["reasons"]:
        for reason in result["reasons"]:
            st.warning(reason)
    else:
        st.info("간이 설계 기준을 모두 충족했습니다.")

    st.caption(
        "이 판정은 실제 화성 주행 실험 결과가 아니며, "
        "지반 침하와 바퀴 슬립 등을 생략한 단순 모델입니다."
    )

    report = {
        "site": site_key,
        "design": design,
        "result": result
    }

    st.download_button(
        "결과 JSON 다운로드",
        json.dumps(report, ensure_ascii=False, indent=2),
        file_name="rover_forge_result.json",
        mime="application/json"
    )

    if st.button(
        "로버 다시 설계하기",
        type="primary",
        use_container_width=True
    ):
        go(2)

    if st.button("새로운 탐사 임무"):
        st.session_state.result = None
        go(1)
