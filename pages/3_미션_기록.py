import streamlit as st
import runpy
from pathlib import Path
if st.session_state.get("stage") not in (3, 4):
    st.session_state.stage = 3
runpy.run_path(str(Path(__file__).resolve().parents[1] / "engine.py"), run_name="__main__")
