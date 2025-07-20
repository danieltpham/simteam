import streamlit as st
import pandas as pd
import requests
from urllib.parse import urljoin, urlparse

# Streamlit App Title and Description
st.title("SimTeam Event Logs")
st.write("Below is a live view of all recorded employee events from the FastAPI backend.")

import streamlit as st
import requests
from urllib.parse import urlparse, urljoin

API_ENDPOINT = "/api/v1/eventlog/"

API_ENDPOINT = "/api/v1/eventlog/"

# Parse current URL from Streamlit context
parsed = urlparse(st.context.url)
host = parsed.hostname  # e.g. 'localhost' or 'yourdomain.com'

# Decide which base to use
if host in ["localhost", "127.0.0.1"]:
    base_url = "http://localhost:10000"
else:
    # base_url = f"{parsed.scheme}://{parsed.netloc}"
    base_url = "https://simteam-backend-fastapi-299036431019.asia-northeast1.run.app"

# Final API URL
API_URL = urljoin(base_url, API_ENDPOINT)
    
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
