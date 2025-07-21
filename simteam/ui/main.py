import pandas as pd
import streamlit as st
from datetime import datetime

from app.data_loader import load_event_log, load_temps
from app.org_builder import build_org_structure
from components.streamlit_register import render_org_chart

st.set_page_config(page_title="SimTeam Org Chart", layout="wide")
st.title("📊 SimTeam Org Chart")

# Load and display the event log
with st.spinner("Fetching event log..."):
    df = load_event_log()
    temp_list = load_temps()

if df.empty:
    st.warning("No data available.")
    st.stop()

# Convert dates
df["date"] = pd.to_datetime(df["date"])
min_date = df["date"].min().date()
max_date = df["date"].max().date()

# Select snapshot date
selected_date = st.date_input(
    "Snapshot date",
    value=min_date,
    min_value=min_date,
    max_value=max_date,
    key="date_picker"
)

actives, temps = [], []
# Build full org chart node structure (Bumbeishvili format)
actives, temps = build_org_structure(df, temp_list = temp_list, date=selected_date.isoformat())

st.subheader(f"Organisation as of {selected_date.isoformat()}")
st.caption(f"Showing {len(actives)} active employees")

# Preview raw data
with st.expander("🔍 Preview node data"):
    st.json(actives[:3])

# Render component
render_org_chart(actives+temps, key="org_chart", height=300)


