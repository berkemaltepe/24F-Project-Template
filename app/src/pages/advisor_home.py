import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# Set wide layout for the page
st.set_page_config(layout = 'wide')

# Sidebar navigation setup
SideBarLinks()
BASE_URL = "http://web-api:4000/advisor"

# Fetch advisor data
response = requests.get(f"{BASE_URL}/{st.session_state['advisor_id']}/students")
if response.status_code == 200:
    students = response.json()
else:
    st.error(f"Error {response.status_code}: {response.text}")

advisor_id = st.session_state['advisor_id']

# Hero banner with border
st.markdown(
    f"""
    <div style="padding: 20px; border-radius: 10px; border: 3px solid #FF0000; background-color: #000000; text-align: center; color: white;">
        <h1 style="font-size: 40px; margin-bottom: 10px;">Welcome to the Co-op Advisor Dashboard</h1>
        <p style="font-size: 20px;">Hello, {st.session_state['first_name']}! Here are your options:</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Buttons for navigation
if st.button('Student List', use_container_width=True):
    st.switch_page('pages/advisor_students.py')  # Redirect to Student List page
if st.button('Skill Match Analysis', use_container_width=True):
    st.switch_page('pages/advisor_skill_match.py')  # Redirect to Skill Match Analysis page
if st.button('Active Job Postings', use_container_width=True):
    st.switch_page('pages/advisor_job_postings.py')  # Redirect to Job Postings page
if st.button('Manage Students', use_container_width=True):
    st.switch_page('pages/advisor_manage_students.py')  # Redirect to Manage Students page

# Add sidebar navigation
menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Student List", "Skill Match Analysis", "Active Job Postings", "Manage Students"]
)

if menu == "Student List":
    st.switch_page('pages/advisor_students.py')
elif menu == "Skill Match Analysis":
    st.switch_page('pages/advisor_skill_match.py')
elif menu == "Active Job Postings":
    st.switch_page('pages/advisor_job_postings.py')
elif menu == "Manage Students":
    st.switch_page('pages/advisor_manage_students.py')

