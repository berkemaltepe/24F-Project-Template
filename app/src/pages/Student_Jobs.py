import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

SideBarLinks()

# Initialize session state for student_id if not already set
if 'student_id' not in st.session_state:
    st.session_state.student_id = ''

# Function to get best job matches for the student
def get_best_jobs(student_id):
    try:
        response = requests.get(f'http://api:4000/s/job/best_match/{student_id}/')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching best jobs: {e}")
        st.error("Failed to fetch best jobs")
        return None

# Fetch and display best job matches
if st.session_state.student_id:
    best_jobs = get_best_jobs(st.session_state.student_id)
    if best_jobs:
        st.write("### Best Job Matches for You")
        # Display best job matches in a prettier format
        for job in best_jobs:
            st.markdown(f"**Job ID:** {job['job_id']} - **Job Title:** {job['job_title']} - **Match Percentage:** {job['match_percentage']}%")
    else:
        st.write("No job matches available.")
else:
    st.write("Please enter a student ID.")
