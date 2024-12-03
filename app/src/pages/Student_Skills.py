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

# Function to get student skills
def get_student_skills(student_id):
    try:
        response = requests.get(f'http://api:4000/s/student/{student_id}/skill/')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching student skills: {e}")
        st.error("Failed to fetch student skills")
        return None

# Function to add student skill
def add_student_skill(student_id, skill_id, weight):
    try:
        response = requests.post(f'http://api:4000/s/student/{student_id}/skill/', json={
            'skill_id': skill_id,
            'weight': weight
        })
        response.raise_for_status()
        st.success("Successfully added student skill")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error adding student skill: {e}")
        st.error("Failed to add student skill")

# Fetch and display student skills
if st.session_state.student_id:
    student_skills = get_student_skills(st.session_state.student_id)
    if student_skills:
        st.write("### Student Skills")
        # Display student skills as text
        for skill in student_skills:
            st.markdown(f"**Skill ID:** {skill['skill_id']} - **Skill Name:** {skill['skill_name']} - **Skill Type:** {skill['skill_type']} - **Proficiency:** {skill['proficiency']}")

    # Add new skill
    st.write("### Add New Skill")
    skill_id = st.number_input("Skill ID", min_value=1, step=1)
    proficiency = st.number_input("Proficiency", min_value=1, max_value=10, step=1)
    if st.button("Add Skill"):
        add_student_skill(st.session_state.student_id, skill_id, proficiency)
else:
    st.write("Please enter a student ID.")