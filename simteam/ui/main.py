import asyncio
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go
import os
import time
from typing import Iterator

from app.data_loader import load_event_log, load_temps
from app.org_builder import build_org_structure
from components.streamlit_register import render_org_chart
from pydanticai.async_call import get_sql_response

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

    # --- Load data ---
    with st.spinner("Fetching event log..."):
        df = load_event_log()
        temp_list = load_temps()

    if df.empty:
        st.warning("No data available.")
        st.stop()

    df["date"] = pd.to_datetime(df["date"])
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    # --- Initialise date state ---
    if "selected_date" not in st.session_state:
        st.session_state.selected_date = min_date
    if "previous_selected_date" not in st.session_state:
        st.session_state.previous_selected_date = None
    if "selected_date" not in st.session_state or st.session_state.selected_date is None:
        st.session_state.selected_date = min_date

    # --- Date navigation ---
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

    # --- Date input ---
    selected_date = st.date_input(
        label="",
        value=st.session_state.selected_date,
        min_value=min_date,
        max_value=max_date,
        key="date_picker"
    )
    st.session_state.selected_date = selected_date

    # --- Filter for selected date ---
    df_day = df[df["date"].dt.date == selected_date]

    # --- Event Console Text Generator ---
    def console_stream_chars() -> Iterator[str]:
        time.sleep(1.0)
        divider = "─" * 20 + "\n"

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
            time.sleep(0.012)

    # --- Event Console Display ---
    st.markdown("---")
    st.markdown("#### 🧠 Event Console")
    st.markdown('<div id="sidebar-console">', unsafe_allow_html=True)

    if st.session_state.previous_selected_date != selected_date:
        st.write_stream(console_stream_chars)
        st.session_state.previous_selected_date = selected_date
    else:
        if df_day.empty:
            st.markdown("No events recorded today.")
        else:
            divider = "─" * 20
            lines = [f"[{row['date'].strftime('%H:%M:%S')}] EMP {row['employee_id']} ➝ {row['event_type']} ({row['role']})" for _, row in df_day.iterrows()]
            text = f"{len(df_day)} event(s) on {selected_date}...\n{divider}\n" + f"\n{divider}\n".join(lines)
            st.markdown(text)

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
    st.markdown("Ask questions about the employee database using natural language.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask me something about your org..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with st.spinner("Thinking..."):
            output = asyncio.run(get_sql_response(prompt))
            try:
                output = asyncio.run(get_sql_response(prompt))
                answer = output.result.encode("utf-8", errors="replace").decode("utf-8")
                sql_code = output.sql
            except Exception as e:
                answer = f"❌ Error: {e}"
                sql_code = ""

        with st.chat_message("assistant"):
            st.markdown(answer)
            if sql_code:
                with st.expander("🧠 Show generated SQL"):
                    st.code(sql_code, language="sql")

        st.session_state.chat_history.append({"role": "assistant", "content": answer})


with tab3:
    st.subheader("⌨️ Meta Model")

    with st.form("meta_model_form"):
        st.markdown("#### Input Configuration")
        col1, col2 = st.columns(2)

        with col1:
            weight_employed = st.number_input("Weight: EMPLOYED", min_value=1, max_value=10, value=4)
            weight_promoted = st.number_input("Weight: PROMOTED", min_value=1, max_value=10, value=2)
            weight_change = st.number_input("Weight: CHANGE", min_value=1, max_value=10, value=1)
            weight_left = st.number_input("Weight: LEFT", min_value=1, max_value=10, value=1)
            seed = st.number_input("Random Seed", min_value=0, value=42)

        with col2:
            min_employees_for_leaving = st.number_input("Min Employees for Leaving", min_value=10, max_value=100, value=20)
            min_events_per_week = st.number_input("Min Events per Week", min_value=1, max_value=10, value=1)
            max_events_per_day = st.number_input("Max Events per Day", min_value=1, max_value=20, value=8)
            max_events_per_type = st.number_input("Max Events per Type", min_value=1, max_value=5, value=3)

        submit = st.form_submit_button("Run Simulation & Predict")

    if submit:
        with st.spinner("Running simulation and predicting..."):
            import requests

            api_url = "https://simteam-backend-fastapi-299036431019.asia-northeast1.run.app/api/v1/simulate"
            payload = {
                "weight_employed": weight_employed,
                "weight_promoted": weight_promoted,
                "weight_change": weight_change,
                "weight_left": weight_left,
                "min_employees_for_leaving": min_employees_for_leaving,
                "min_events_per_week": min_events_per_week,
                "max_events_per_day": max_events_per_day,
                "max_events_per_type": max_events_per_type,
                "seed": seed
            }

            try:
                response = requests.get(api_url, params=payload)
                response.raise_for_status()
                data = response.json()

                merged_df = pd.DataFrame({
                    "Simulated": data["actual_sim"]["stats"],
                    "Predicted": data["predicted_stats"]
                })

                st.success("Simulation and prediction complete.")
                
                # Only show if simulation has been run
                sim_timeseries = data["actual_sim"]["time_series"]

                # Convert to DataFrame
                df_ts = pd.DataFrame.from_dict(sim_timeseries, orient="index").reset_index()
                df_ts.columns = ["date", "hire", "promote", "leave", "total_employees"]
                df_ts["date"] = pd.to_datetime(df_ts["date"])
                df_ts = df_ts.sort_values("date")

                # Plot
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df_ts["date"],
                    y=df_ts["total_employees"],
                    mode="lines",
                    name="Total Employees",
                    line=dict(color="#00F0FF", width=2),
                ))

                fig.update_layout(
                    title="Total Employees Over Time",
                    xaxis_title=None,
                    yaxis_title="Employees",
                    plot_bgcolor="#0c1117",
                    paper_bgcolor="#0c1117",
                    font=dict(color="#FFFFFF"),
                    hovermode="x unified",
                    margin=dict(t=40, r=20, l=20, b=40)
                )

                st.plotly_chart(fig, use_container_width=True)

                st.markdown("#### 📊 Simulated Summary Stats")
                st.dataframe(merged_df)

            except requests.RequestException as e:
                st.error(f"API call failed: {e}")

# --- Post-render delayed re-run to start console stream ---
if not st.session_state.ready_to_stream:
    time.sleep(0.5)  # allow main body to load first
    st.session_state.ready_to_stream = True
    st.rerun()
