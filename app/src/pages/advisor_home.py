import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# Set wide layout for the page
st.set_page_config(layout = 'wide')

# Sidebar navigation setup
SideBarLinks()

# Page title
st.title('Co-op Advisor Home Page')

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

