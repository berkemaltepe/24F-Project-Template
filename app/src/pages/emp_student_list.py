import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

# # add one number input for variable 1 into column 1
# with col1:
#   var_01 = st.number_input('Variable 01:',
#                            step=1)

# # add another number input for variable 2 into column 2
# with col2:
#   var_02 = st.number_input('Variable 02:',
#                            step=1)

# logger.info(f'var_01 = {var_01}')
# logger.info(f'var_02 = {var_02}')
BASE_URL = "http://web-api:4000/employer"

st.title("Student List")

st.header("Get List of Students")
if st.button("Fetch Students", type='primary', use_container_width=True):
    try:
        # Make a GET request to the /students endpoint
        response = requests.get(f"{BASE_URL}/students")
        if response.status_code == 200:
            students = response.json()
            if students:
                st.write("Students List:")
                for student in students:
                    st.write(f"- ID: {student['student_id']}, Name: {student['name']}, Major: {student['major']}")
            else:
                st.info("No students found in the database.")
        else:
            st.error(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {e}")