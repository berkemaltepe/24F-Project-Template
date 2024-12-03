import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks

# Set up logging
logger = logging.getLogger(__name__)

# Set page layout for Streamlit
st.set_page_config(layout='wide')

# Show appropriate sidebar links
SideBarLinks()

def get_all_skills():
    try:
        response = requests.get(f'http://api:4000/depthead/skill/skill_name')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching information: {e}")
        st.error("Failed to fetch information")
        return None

# Get skills
all_skills = get_all_skills()
if all_skills:
    skill_names = [skill['skill_name'] for skill in all_skills]
else:
    skill_names = []

# Select skill option
option = st.selectbox("Filter by skill", ["Choose a skill"] + skill_names)

# Functions to fetch jobs and students
def get_jobs():
    try:
        response = requests.get(f'http://api:4000/depthead/all-job-skills')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching information: {e}")
        st.error("Failed to fetch information")
        return None

def get_job_skills(job_id):
    try:
        response = requests.get(f'http://api:4000/depthead/jobs/{job_id}/skills')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching information: {e}")
        st.error("Failed to fetch information")
        return None

def get_student_skills(student_id):
    try:
        response = requests.get(f'http://api:4000/depthead/student/{student_id}/skills')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching information: {e}")
        st.error("Failed to fetch information")
        return None
    
def get_filtered_jobs(skill_name):
    try:
        response = requests.get(f'http://api:4000/depthead/all-job-skills/{skill_name}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching information: {e}")
        st.error("Failed to fetch information")
        return None
    
def get_filtered_students(skill_name):
    try:
        response = requests.get(f'http://api:4000/depthead/all-student-skills/{skill_name}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching information: {e}")
        st.error("Failed to fetch information")
        return None
    
def get_students():
    try:
        response = requests.get(f'http://api:4000/depthead/all-student-skills')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching information: {e}")
        st.error("Failed to fetch information")
        return None
    
##### def get_student_skills() like the job one to get their skills separately 
    

# Display jobs and their skills
def display_jobs():
    jobs = get_jobs()
    if option == "Choose a skill":
        for job in jobs:
            job_skills = get_job_skills(job['job_id'])
            if job_skills:
                with st.expander(f"**{job['job_title']}**, {job['employer_name']}"):
                    st.markdown(f"Description: {job['description']}")
                    st.markdown(f"Industry: {job['industry']}")
                    st.markdown(f"Pay range: {job['pay_range']}")
                    st.markdown(f"Date posted: {job['date_posted']}")
                    st.markdown(f"Status: {job['status']}")

                    st.write("##### Required skills:")
                    for skill in job_skills:
                        st.markdown(f"{skill['skill_name']}, {skill['weight']}")
            else:
                st.warning(f"No skills found for job {job['job_title']}")
    else:
        jobs = get_filtered_jobs(option)
        for job in jobs:
            job_skills = get_job_skills(job['job_id'])
            if job_skills:
                with st.expander(f"**{job['job_title']}**, {job['employer_name']}"):
                    st.markdown(f"Description: {job['description']}")
                    st.markdown(f"Industry: {job['industry']}")
                    st.markdown(f"Pay range: {job['pay_range']}")
                    st.markdown(f"Date posted: {job['date_posted']}")
                    st.markdown(f"Status: {job['status']}")

                    st.write("##### Required skills:")
                    for skill in job_skills:
                        st.markdown(f"{skill['skill_name']}, {skill['weight']}")

            else:
                st.warning(f"No skills found for job {job['job_title']}")

# Display jobs and their skills
def display_students():
    students = get_students()
    if option == "Choose a skill":
        for student in students:
            student_skills = get_student_skills(student['student_id'])
            with st.expander(f"{student['student_name']}, {student['major']}, {student['level']}"):
                    st.markdown(f"Email: {student['email']}")
                    st.markdown(f"GPA: {student['gpa']}")
                    st.markdown(f"Co-op Status: {student['coop_status']}")

                    st.write("##### Skills:")
                    for skill in student_skills:
                        st.markdown(f"{skill['skill_name']}, {skill['weight']}")

    else:
        students = get_filtered_students(option)
        for student in students:
            student_skills = get_student_skills(student['student_id'])
            with st.expander(f"{student['student_name']}, {student['major']}, {student['level']}"):
                    st.markdown(f"Email: {student['email']}")
                    st.markdown(f"GPA: {student['gpa']}")
                    st.markdown(f"Co-op Status: {student['coop_status']}")

                    st.write("##### Skills:")
                    for skill in student_skills:
                        st.markdown(f"{skill['skill_name']}, {skill['weight']}")



# Display jobs
left, right = st.columns(2)

with left:
    st.write("## Job Listings")
    display_jobs()

with right:
    st.write('## Students')
    display_students()