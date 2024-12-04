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

# Function to get all jobs with skill match details
def get_all_jobs(student_id):
    try:
        response = requests.get(f'http://api:4000/s/jobs/{student_id}/')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching all jobs: {e}")
        st.error("Failed to fetch all jobs")
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
    st.write("## Best Job Matches for You")
    best_jobs = get_best_jobs(st.session_state.student_id)
    if best_jobs:
        for job in best_jobs:
            with st.expander(f"{job['job_title']} - {job['match_percentage']}% match"):
                st.markdown(f"**Job ID:** {job['job_id']}")
                st.markdown(f"**Job Title:** {job['job_title']}")
                st.markdown(f"**Company:** {job['company']}")
                st.markdown(f"**Location:** {job['location']}")
                st.markdown(f"**Description:** {job['description']}")
                st.markdown(f"**Pay Range:** {job['pay_range']}")
                st.markdown(f"**Date Posted:** {job['date_posted']}")
                st.markdown(f"**Status:** {job['status']}")
                st.markdown(f"**Match Percentage:** {job['match_percentage']}%")

                if st.button("Compare Skills",
                             type='primary',
                             use_container_width=True,
                             key=f"compare_skills_{job['job_id']}"):
                    st.session_state.job_id = job['job_id']
                    logger.info(f"Viewing job skill match for job ID: {job['job_id']}")
                    st.switch_page('pages/Student_Skill_Match.py')
    else:
        st.write("No job matches available.")

    st.write("## All Job Listings")
    all_jobs = get_all_jobs(st.session_state.student_id)
    if all_jobs:
        for job in all_jobs:
            with st.expander(f"{job['job_title']} - {job['match_percentage']}% match"):
                st.markdown(f"**Job ID:** {job['job_id']}")
                st.markdown(f"**Job Title:** {job['job_title']}")
                st.markdown(f"**Company:** {job['company']}")
                st.markdown(f"**Location:** {job['location']}")
                st.markdown(f"**Description:** {job['description']}")
                st.markdown(f"**Pay Range:** {job['pay_range']}")
                st.markdown(f"**Date Posted:** {job['date_posted']}")
                st.markdown(f"**Status:** {job['status']}")
                st.markdown(f"**Match Percentage:** {job['match_percentage']}%")

                if st.button("Compare Skills",
                             type='primary',
                             use_container_width=True,
                             key=f"all_compare_skills_{job['job_id']}"):
                    st.session_state.job_id = job['job_id']
                    logger.info(f"Viewing job skill match for job ID: {job['job_id']}")
                    st.switch_page('pages/Student_Skill_Match.py')
    else:
        st.write("No job matches available.")