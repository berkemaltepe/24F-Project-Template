# import libs
import streamlit as st
import pandas as pd
import requests

# page title
st.title("Co-op Advisor: Student List")

# Fetch students assigned to the advisor
advisor_id = 1  # Example advisor ID; replace with actual logic
response = requests.get(f"http://localhost:4000/advisor/{advisor_id}/students")