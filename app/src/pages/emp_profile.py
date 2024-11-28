import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

# Display the appropriate sidebar links for the role of the logged-in user
SideBarLinks()

BASE_URL = "http://web-api:4000/employer"

try:
    # Fetch employer information
    response = requests.get(f"{BASE_URL}/employer/{st.session_state['emp_id']}")
    if response.status_code == 200:
        emp = response.json()[0]
        if emp:
            st.title("Your Company Information:")
            st.write(f"Name: {emp['name']}")
            st.write(f"Industry: {emp['industry']}")
            st.write(f"EMP_ID: {emp['emp_id']}")
            st.write(f"Contact: {emp['email']}")

            # Input field for updating email
            new_email = st.text_input("Update Email Address", value=emp['email'])

            # Button to update email
            if st.button("Update Email"):
                try:
                    # Make a PUT request to update the email
                    update_response = requests.put(
                        f"{BASE_URL}/employers/{emp['emp_id']}/email",
                        json={"id": emp['emp_id'], "email": new_email}
                    )
                    if update_response.status_code == 200:
                        st.success("Email updated successfully!")
                    else:
                        st.error(f"Failed to update email: {update_response.text}")
                except Exception as update_error:
                    st.error(f"An error occurred: {update_error}")
        else:
            st.info("No employer data found in the database.")
    else:
        st.error(f"Error {response.status_code}: {response.text}")
except Exception as e:
    st.error(f"An error occurred: {e}")
