import logging
logger = logging.getLogger(__name__)
import requests

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

BASE_URL = "http://web-api:4000/employer"

response = requests.get(f"{BASE_URL}/employer/{st.session_state['emp_id']}")
if response.status_code == 200:
    emp = response.json()[0]
else:
    st.error(f"Error {response.status_code}: {response.text}")

employer_id = st.session_state['emp_id']

## Different employer pages???
st.title(f"Welcome to the {emp['name']} Employer Home Page, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button(f"View {emp['name']} Info (How Others See You!)",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/emp_profile.py')

if st.button('View the List of Students in the System', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/emp_student_list.py')

if st.button(f"{emp['name']} Candidate Match Chart and Info", 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/emp_skill_match.py')

if st.button(f"{emp['name']} Job Listing Editor",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/emp_job_creation.py')

