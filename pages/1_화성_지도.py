import streamlit as st
import runpy
from pathlib import Path
st.session_state.stage = 1
runpy.run_path(str(Path(__file__).resolve().parents[1] / "engine.py"), run_name="__main__")
