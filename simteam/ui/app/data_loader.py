# app/data_loader.py

import json
import pandas as pd
import requests
import streamlit as st
from urllib.parse import urlparse, urljoin

API_ENDPOINT = "/api/v1/eventlog/"
LOCAL_FILE = "res_output.json"

def get_base_url() -> str:
    
    host = urlparse(st.context.url).hostname
    if host in ["localhost", "127.0.0.1"]:
        base_url = "http://localhost:10000"
    else:
        base_url = "https://simteam-backend-fastapi-299036431019.asia-northeast1.run.app"
    return base_url

def load_event_log() -> pd.DataFrame:
    """
    Load event log from API or fallback to local file.
    """
    base_url = get_base_url()
    api_url = urljoin(base_url, API_ENDPOINT)

    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except Exception:
        with open(LOCAL_FILE, "r") as f:
            return pd.DataFrame(json.load(f))
