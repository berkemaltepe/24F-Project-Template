import logging
import requests
import pandas as pd
import streamlit as st

# Configure logging
logger = logging.getLogger(__name__)

# Set up the page layout
st.set_page_config(layout="wide")

# Ensure session state contains the necessary data
if "advisor_id" not in st.session_state:
    st.error("Advisor ID not found. Please log in as an advisor.")
    st.stop()

BASE_URL = "http://web-api:4000/a"  # Base URL for API endpoints
advisor_id = st.session_state["advisor_id"]

# Page Title
st.markdown(
    """
    <div style="padding: 20px; border-radius: 10px; border: 3px solid #FF0000; background-color: #000000; color: white; text-align: center;">
        <h1 style="font-size: 40px;">Advisor - Job Postings</h1>
        <p style="font-size: 18px;">Review job postings and match students to roles</p>
    </div>
    """,
    unsafe_allow_html=True,
)