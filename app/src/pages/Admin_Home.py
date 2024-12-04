import logging
import requests
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

def get_admin():
    try:
        response = requests.get("http://web-api:4000/system_admin/1")
        if response.status_code == 200:
            return response.json()[0]
        else:
            st.error(f"Failed to fetch admins: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching admins: {e}")
        return None

admin = get_admin()

st.title(f"Welcome to the Admin Home Page, {admin['name']}.")
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