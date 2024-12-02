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