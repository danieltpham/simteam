import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import os
import time
from typing import Iterator

from app.data_loader import load_event_log, load_temps
from app.org_builder import build_org_structure
from components.streamlit_register import render_org_chart

# --- Load custom CSS ---
def load_css(relative_path):
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, relative_path)
    with open(full_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="SimTeam Org Chart", layout="wide")
load_css("app/styles/futuristic.css")

# --- Session State Initialization ---
if "selected_date" not in st.session_state:
    st.session_state.selected_date = None

if "ready_to_stream" not in st.session_state:
    st.session_state.ready_to_stream = False

# --- Sidebar ---
with st.sidebar:
    st.title("📅 DATE")

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

    if st.session_state.selected_date is None:
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
        "",
        value=st.session_state.selected_date,
        min_value=min_date,
        max_value=max_date,
        key="date_picker"
    )
    st.session_state.selected_date = selected_date

    # --- Event Console ---
    df_day = df[df["date"].dt.date == selected_date]

    def console_stream_chars() -> Iterator[str]:
        time.sleep(1.0)  # Delay before typing starts

        divider = "─" * 20 + "\n"  # Sci-fi-style line

        if df_day.empty:
            text = "No events recorded today.\n"
        else:
            text = f"{len(df_day)} event(s) on {selected_date}...\n"
            text += divider
            for _, row in df_day.iterrows():
                line = f"[{row['date'].strftime('%H:%M:%S')}] EMP {row['employee_id']} ➝ {row['event_type']} ({row['role']})\n"
                text += line + divider

        for char in text:
            yield char
            time.sleep(0.015)


    st.markdown("---")
    st.markdown("#### 🧠 Event Console")

    # Begin styled container
    st.markdown('<div id="sidebar-console">', unsafe_allow_html=True)

    if st.session_state.ready_to_stream:
        st.write_stream(console_stream_chars)
    else:
        st.code(">>> Initialising...", language="bash")

    # End styled container
    st.markdown('</div>', unsafe_allow_html=True)

# --- Main Body ---
st.title("S.I.M.T.E.A.M")

# Build org data
actives, temps = build_org_structure(df, temp_list=temp_list, date=selected_date.isoformat())

tab1, tab2, tab3 = st.tabs(["ORG CHART", "AI CHATBOT", "META MODEL"])

with tab1:
    st.subheader(f"Organisation as of {selected_date.isoformat()}")
    st.caption(f"Showing {len(actives)} active employees")
    render_org_chart(actives + temps, key="org_chart", height=400)

with tab2:
    st.subheader("🤖 AI Assistant")
    st.info("AI interface placeholder – coming soon!")

with tab3:
    st.subheader("⌨️ Meta Model")
    st.info("ML model placeholder – coming soon!")

# --- Post-render delayed re-run to start console stream ---
if not st.session_state.ready_to_stream:
    time.sleep(0.5)  # allow main body to load first
    st.session_state.ready_to_stream = True
    st.rerun()
