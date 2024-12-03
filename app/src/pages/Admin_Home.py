import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome to the Admin Home Page, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Profile', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Admin_Profile.py')

if st.button('View All Jobs', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Admin_All_Jobs.py')

if st.button('View All Skills', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Admin_All_Skills.py')

if st.button('View All Employers', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Admin_All_Employers.py')

if st.button('View All Department Faculties', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Admin_All_Faculties.py')

if st.button('View All Co-op Advisors', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Admin_All_Advisors.py')

if st.button('View All Students', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Admin_All_Students.py')