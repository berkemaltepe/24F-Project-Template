import logging
import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Configure logging
logger = logging.getLogger(__name__)

# Set up the page layout
st.set_page_config(layout="wide")

# Ensure session state contains the necessary data
if "student_id" not in st.session_state or "advisor_id" not in st.session_state:
    st.error("Missing required data. Please navigate back and select a student or advisor.")
    st.stop()

BASE_URL = "http://web-api:4000/a"  # Base URL for API endpoints
student_id = st.session_state["student_id"]
advisor_id = st.session_state["advisor_id"]

# Page title
st.markdown(
    """
    <div style="padding: 20px; border-radius: 10px; border: 3px solid #FF0000; background-color: #000000; color: white; text-align: center;">
        <h1 style="font-size: 40px;">Skill Match Analysis</h1>
        <p style="font-size: 18px;">View the skill gap between your student and job requirements</p>
    </div>
    """,
    unsafe_allow_html=True,
)