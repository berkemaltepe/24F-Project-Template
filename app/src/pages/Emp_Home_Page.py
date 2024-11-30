import logging
logger = logging.getLogger(__name__)
import requests

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

# Show appropriate sidebar links for the role of the currently logged-in user
SideBarLinks()

BASE_URL = "http://web-api:4000/employer"

# Fetch employer data
response = requests.get(f"{BASE_URL}/employer/{st.session_state['emp_id']}")
if response.status_code == 200:
    emp = response.json()[0]
else:
    st.error(f"Error {response.status_code}: {response.text}")

employer_id = st.session_state['emp_id']

# Hero banner with border
st.markdown(
    f"""
    <div style="padding: 20px; border-radius: 10px; border: 3px solid #FF0000; background-color: #000000; text-align: center; color: white;">
        <h1 style="font-size: 40px; margin-bottom: 10px;">Welcome to the {emp['name']} Employer Portal</h1>
        <p style="font-size: 20px;">Hello, {st.session_state['first_name']}! What would you like to do today?</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Add spacing
st.write("")
st.write("")
st.write("")

# Buttons with borders and improved styling
button_style = """
    <style>
        .stButton>button {
            background-color: #000000;
            color: white;
            border: 2px solid #FF0000;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease, border-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #FFFFF;
            border-color: #FF0000;
        }
    </style>
"""
st.markdown(button_style, unsafe_allow_html=True)

# Buttons grid
st.markdown(
    """
    <div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;">
        <div style="width: 300px;">
    """,
    unsafe_allow_html=True,
)

if st.button(f"View {emp['name']} Info (How Others See You!)", use_container_width=True):
    st.switch_page('pages/emp_profile.py')

st.markdown("</div><div style='width: 300px;'>", unsafe_allow_html=True)

if st.button(f"{emp['name']} Candidate Match Chart and Info", use_container_width=True):
    st.switch_page('pages/emp_skill_match.py')

st.markdown("</div><div style='width: 300px;'>", unsafe_allow_html=True)

if st.button(f"{emp['name']} Job Listing Editor", use_container_width=True):
    st.switch_page('pages/emp_job_creation.py')

st.markdown("</div><div style='width: 300px;'>", unsafe_allow_html=True)

if st.button("View the List of Students in the System", use_container_width=True):
    st.switch_page('pages/emp_student_list.py')

st.markdown("</div></div>", unsafe_allow_html=True)

# Add footer for branding or additional info
st.markdown(
    """
    <hr>
    <footer style="text-align: center; margin-top: 30px; color: #777;">
        <p style="font-size: 14px;">Powered by SkillMatch Platform | © 2024 SkillMatch, Inc.</p>
    </footer>
    """,
    unsafe_allow_html=True,
)
