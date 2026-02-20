import os
import streamlit as st
from supabase import create_client

def get_supabase():
    # First try environment variables (Render)
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    # Fallback to Streamlit secrets (local)
    if not url or not key:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")

    return create_client(url, key)