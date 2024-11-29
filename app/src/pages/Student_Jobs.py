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

# Function to get job skill match details
def get_job_skill_match(student_id, job_id):
    try:
        response = requests.get(f'http://api:4000/s/{student_id}/job/{job_id}/skills')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching job skill match: {e}")
        st.error("Failed to fetch job skill match")
        return None

# Fetch and display best job matches
if st.session_state.student_id:
    best_jobs = get_best_jobs(st.session_state.student_id)
    if best_jobs:
        st.write("### Best Job Matches for You")
        # Display best job matches with expanders to show skill matches
        for job in best_jobs:
            with st.expander(f"{job['job_title']} - {job['match_percentage']}% match"):
                st.markdown(f"**Job ID:** {job['job_id']}")
                st.markdown(f"**Job Title:** {job['job_title']}")
                st.markdown(f"**Location:** {job['location']}")
                st.markdown(f"**Description:** {job['description']}")
                st.markdown(f"**Pay Range:** {job['pay_range']}")
                st.markdown(f"**Date Posted:** {job['date_posted']}")
                st.markdown(f"**Status:** {job['status']}")
                st.markdown(f"**Match Percentage:** {job['match_percentage']}%")
                st.markdown(f"**Company:** {job['company']}")

                job_skill_match = get_job_skill_match(st.session_state.student_id, job['job_id'])
                if job_skill_match:
                    st.write("### Job Skill Match Details")
                    # Display job skill match details in a prettier format
                    for skill in job_skill_match:
                        st.markdown(f"**Skill ID:** {skill['skill_id']} - **Skill Name:** {skill['skill_name']} - **Student Proficiency:** {skill['student_proficiency']} - **Job Requirement:** {skill['job_requirement']} - **Job Min Proficiency:** {skill['job_min_proficiency']} - **Level of Fit:** {skill['level_of_fit']}")
                else:
                    st.write("No job skill match details available.")
    else:
        st.write("No job matches available.")
else:
    st.write("Please enter a student ID.")
