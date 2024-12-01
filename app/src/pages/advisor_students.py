# import libs
import streamlit as st
import pandas as pd
import requests

# Define the base URL for the API
BASE_URL = "http://web-api:4000/advisor"

# Title and description for the page
st.markdown(
    """
    <div style="padding: 20px; border-radius: 10px; border: 3px solid #FF0000; background-color: #000000; color: white; text-align: center;">
        <h1>Student List</h1>
        <p>View and manage students assigned to you.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

