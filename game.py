
from pathlib import Path
import json
import streamlit as st
import streamlit.components.v1 as components

BASE = Path(__file__).resolve().parent

CONFIG = {
    "rock": {
        "title": "화성 암석 집기",
        "duration": 90,
        "description": "제한시간 1분 30초 | 화성 암석을 집어 샘플 보관함으로 이동하세요."
    },
    "battery": {
        "title": "배터리 분리하기",
        "duration": 120,
        "description": "제한시간 2분 | 잠금장치를 해제한 후 배터리를 오른쪽으로 추출하세요."
    },
    "satellite": {
        "title": "위성 수리",
        "duration": 240,
        "description": "제한시간 4분 | 덮개 제거, 버튼 A·B, 스위치, 4색 전선 연결, 안테나 고정을 완료하세요."
    }
}


def run(mission):

    st.set_page_config(
        page_title="MECHA LAB",
        page_icon="🦾",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.markdown("""
    <style>
    [data-testid="stSidebar"],
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 1rem;
    }

    .stApp {
        background: #131a24;
        color: #f1e6d8;
    }
    </style>
    """, unsafe_allow_html=True)

    cfg = CONFIG[mission]

    st.title("🦾 " + cfg["title"])
    st.caption(cfg["description"])

    template_path = BASE / "assets" / "game.html"

    if not template_path.exists():
        st.error("assets/game.html 파일을 찾을 수 없습니다.")
        return

    template = template_path.read_text(encoding="utf-8")

    html = template.replace(
        "__GAME_CONFIG__",
        json.dumps(
            {"mission": mission, **cfg},
            ensure_ascii=False
        )
    )

    components.html(
        html,
        height=685,
        scrolling=False
    )

    if st.button(
        "← 미션 선택 화면으로 돌아가기",
        use_container_width=True
    ):
        st.session_state.mecha_started = True
        st.switch_page("main.py")

    st.caption(
        "조작법: 빨간 관절 드래그 → 집게를 목표에 접근 "
        "→ [잡기/놓기] 버튼 또는 Space 키"
    )
