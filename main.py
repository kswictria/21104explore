import streamlit as st
import runpy
from pathlib import Path
st.session_state.stage = 0
runpy.run_path(str(Path(__file__).parent / "engine.py"), run_name="__main__")
