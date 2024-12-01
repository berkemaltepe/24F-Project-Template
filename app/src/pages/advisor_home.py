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
    st.switch_page('student_list.py')  # Redirect to Student List page
if st.button('Skill Match Analysis', use_container_width=True):
    st.switch_page('skill_match.py')  # Redirect to Skill Match Analysis page
if st.button('Active Job Postings', use_container_width=True):
    st.switch_page('job_postings.py')  # Redirect to Job Postings page
if st.button('Manage Students', use_container_width=True):
    st.switch_page('manage_students.py')  # Redirect to Manage Students page

