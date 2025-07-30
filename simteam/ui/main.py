import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

import os

from app.data_loader import load_event_log, load_temps
from app.org_builder import build_org_structure
from components.streamlit_register import render_org_chart

def load_css(relative_path):
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, relative_path)
    with open(full_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="SimTeam Org Chart", layout="wide")

load_css("app/styles/futuristic.css")

# --- Sidebar ---
with st.sidebar:
    st.title("📅 Filter")

    # Load data
    with st.spinner("Fetching event log..."):
        df = load_event_log()
        temp_list = load_temps()

    if df.empty:
        st.warning("No data available.")
        st.stop()

    df["date"] = pd.to_datetime(df["date"])
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    # Initialize session state
    if "selected_date" not in st.session_state:
        st.session_state.selected_date = min_date

    # Back and forward buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("BACK", use_container_width=True):
            new_date = st.session_state.selected_date - timedelta(days=1)
            if new_date >= min_date:
                st.session_state.selected_date = new_date
    with col2:
        if st.button("NEXT", use_container_width=True):
            new_date = st.session_state.selected_date + timedelta(days=1)
            if new_date <= max_date:
                st.session_state.selected_date = new_date

    # Date input (sync with session state)
    selected_date = st.date_input(
        "Snapshot date",
        value=st.session_state.selected_date,
        min_value=min_date,
        max_value=max_date,
        key="date_picker"
    )
    st.session_state.selected_date = selected_date

    # Optional preview of data
    # st.subheader("Node Preview")
    # st.json(actives[:3])

# --- Main Body ---
st.title("S.I.M.T.E.A.M")

# Build org data
actives, temps = build_org_structure(df, temp_list=temp_list, date=selected_date.isoformat())

tab1, tab2, tab3 = st.tabs(["Org Chart", "DB Terminal", "AI"])

with tab1:
    st.subheader(f"Organisation as of {selected_date.isoformat()}")
    st.caption(f"Showing {len(actives)} active employees")
    render_org_chart(actives + temps, key="org_chart", height=400)  # 90vh ≈ 900px

with tab2:
    st.subheader("🛠 DB Terminal")
    st.info("Terminal placeholder – coming soon!")

with tab3:
    st.subheader("🤖 AI Assistant")
    st.info("AI interface placeholder – coming soon!")
