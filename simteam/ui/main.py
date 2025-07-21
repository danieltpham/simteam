# main.py

import pandas as pd
import streamlit as st
from datetime import datetime
from app.data_loader import load_event_log
from app.org_builder import build_org_structure
# from components.org_chart_component import render_org_chart

st.set_page_config(page_title="SimTeam Org Chart", layout="wide")
st.title("SimTeam Org Chart Viewer")

with st.spinner("Loading data..."):
    df = load_event_log()

if df.empty:
    st.warning("No data available.")
    st.stop()

# Date input
df["date"] = pd.to_datetime(df["date"])
min_date = df["date"].min().date()
max_date = df["date"].max().date()

selected_date = st.date_input("Select snapshot date", max_date, min_value=min_date, max_value=max_date)

# Build org chart structure
nodes = build_org_structure(df, date=selected_date.isoformat())

st.subheader("Org Chart")
st.caption(f"Snapshot as of {selected_date.isoformat()}")
# render_org_chart(nodes)