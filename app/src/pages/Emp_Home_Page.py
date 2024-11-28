import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

## Different employer pages???
st.title(f"Welcome to the Tech Corp Employer Home Page, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button("View Profile Info",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/emp_profile.py')

if st.button('View the List of Students in the System', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/emp_student_list.py')

if st.button('Candidate Match Chart and Info', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/emp_skill_match.py')

if st.button("View Classification Demo",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/emp1_tests.py')

