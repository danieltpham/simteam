import streamlit as st
import pandas as pd
import requests

# Streamlit App Title and Description
st.title("SimTeam Event Logs")
st.write("Below is a live view of all recorded employee events from the FastAPI backend.")

# Backend API base URL (adjust if running on separate host/port)
API_URL = "http://localhost:10000/api/v1/eventlog/"

# Fetch data
with st.spinner("Fetching event log data..."):
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        # Normalize into DataFrame
        df = pd.DataFrame(data)

        if df.empty:
            st.info("No event log records found.")
        else:
            # Optional: Format datetime nicely
            df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d %H:%M:%S")
            st.dataframe(df)
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching event logs: {e}")
