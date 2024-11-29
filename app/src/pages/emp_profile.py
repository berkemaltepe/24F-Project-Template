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
    # Fetch employer info
    response = requests.get(f"{BASE_URL}/employer/{st.session_state['emp_id']}")
    if response.status_code == 200:
        emp = response.json()[0]
        if emp:
            # Styled header
            st.markdown(
                f"""
                <div style="padding: 20px; border-radius: 10px; background-color: #f7f7f7; margin-bottom: 20px;">
                    <h1 style="text-align: center; color: #333;">Information on Your Company: {emp['name']}</h1>
                    <p style="text-align: center; font-size: 16px; color: #333;">Industry: <strong>{emp['industry']}</strong></p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # im going insane rn but here's details in a styled card
            st.markdown(
                f"""
                <div style="padding: 20px; border-radius: 10px; background-color: #ffffff; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                    <h3 style="color: #FF0000;">Employer Details</h3>
                    <ul style="font-size: 16px; line-height: 1.8;">
                        <li><strong>Copmany Name:</strong> {emp['name']}</li>
                        <li><strong>EMP_ID:</strong> {emp['emp_id']}</li>
                        <li>
                            <strong>Contact:</strong> {emp['email']}
                            <form action="#" method="post" style="display:inline;">
                            </form>
                        </li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # If pencil clicked, open email input for editing
            if st.session_state.get('edit_mode', False):
                new_email = st.text_input("Update Email Address", value=emp['email'], key="email_input")
                save_col, cancel_col = st.columns([2, 2])
                with save_col:
                    if st.button("Save Email", key="save_email"):
                        try:
                            update_response = requests.put(
                                f"{BASE_URL}/employers/{emp['emp_id']}/email",
                                json={"id": emp['emp_id'], "email": new_email}
                            )
                            if update_response.status_code == 200:
                                st.success("Email updated successfully!")
                                st.session_state.edit_mode = False
                            else:
                                st.error(f"Failed to update email: {update_response.text}")
                        except Exception as update_error:
                            st.error(f"An error occurred: {update_error}")
                with cancel_col:
                    if st.button("Cancel", key="cancel_email"):
                        st.session_state.edit_mode = False
            else:
                # Set edit mode when pencil is clicked
                if st.button("Edit Email ✏️", key="edit_email_btn", use_container_width=True):
                    st.session_state.edit_mode = True

        else:
            st.info("No employer data found in the database.")
    else:
        st.error(f"Error {response.status_code}: {response.text}")
    
    employer_id = st.session_state['emp_id']

    
    if employer_id:
    # Fetch jobs for the employer
        try:
            jobs_response = requests.get(f"{BASE_URL}/employers/{employer_id}/jobs")
            if jobs_response.status_code == 200:
                jobs = jobs_response.json()
                if jobs:
                    # Display job listings with improved styling
                    st.markdown(
                        f"""
                        <div style="padding: 20px; border-radius: 10px; background-color: #f7f7f7; margin-bottom: 20px;">
                            <h2 style="text-align: center; color: #333;"> <strong>{emp['name']}</strong> Job Listings and Required Skills</h2>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    for job in jobs:
                        job_id = job['job_id']
                        
                        # card time
                        st.markdown(
                            f"""
                            <div style="padding: 15px; margin-bottom: 20px; border-radius: 8px; background-color: #ffffff; 
                                        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                                <h3 style="color: #FF0000; margin: 0;">{job['title']}</h3>
                                <p style="margin: 5px 0;"><strong>Job ID:</strong> {job_id}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        # need the required skills
                        skills_response = requests.get(f"{BASE_URL}/jobs/{job_id}/skills")
                        if skills_response.status_code == 200:
                            skills = skills_response.json()
                            if skills:
                                st.markdown(
                                    """
                                    <div style="margin-left: 20px;">
                                        <h4 style="color: #4a90e2;">Required Skills:</h4>
                                        <ul style="font-size: 16px; line-height: 1.8;">
                                    """,
                                    unsafe_allow_html=True,
                                )
                                for skill in skills:
                                    st.markdown(
                                        f"""
                                        <li>{skill['skill_name']} (Weight: {skill['weight']})</li>
                                        """,
                                        unsafe_allow_html=True,
                                    )
                                st.markdown("</ul></div>", unsafe_allow_html=True)
                            else:
                                st.markdown(
                                    """
                                    <div style="margin-left: 20px;">
                                        <p style="font-size: 16px;">No skills listed for this job.</p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                        else:
                            st.error(f"Failed to fetch skills for Job ID {job_id}.")
                else:
                    st.warning("No jobs found for this employer.")
            else:
                st.error("Failed to fetch jobs for the employer.")
        except Exception as e:
            st.error(f"An error occurred while fetching jobs: {e}")



except Exception as e:
    st.error(f"An error occurred: {e}")


