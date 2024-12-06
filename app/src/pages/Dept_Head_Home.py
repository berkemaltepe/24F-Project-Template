import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome to the Department Head Homepage, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Top Industry Skills', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/DH_Top_Skills_And_Tools.py')

if st.button('View Major Program Reports', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/DH_Major_Pages.py')

if st.button('Search jobs and students by skill', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/DH_Search_By_Skill.py')