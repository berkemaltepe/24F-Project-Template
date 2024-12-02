import logging
import requests 
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

def get_all_skills():
    try:
        response = requests.get(f'http://api:4000/depthead/skill/skill_type')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching best jobs: {e}")
        st.error("Failed to fetch best jobs")
        return None
    
# Fetch all skills
all_skills = get_all_skills()
skill_names = [skill['skill_type'] for skill in all_skills]

# Display drop-down menu of all skills
option = st.selectbox(
    "Filter by skill type",  # Label for the dropdown
    ["Choose an option"] + skill_names  # Concatenate the default option with the skill_names list
)

def get_top_skills():
    try:
        response = requests.get(f'http://api:4000/depthead/top-skills')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching top skills: {e}")
        st.error("Failed to fetch top skills")
        return None
    
def get_top_filtered_skills(skill_type):
    try:
        response = requests.get(f'http://api:4000/depthead/top-tools/{skill_type}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching top skills: {e}")
        st.error("Failed to fetch top skills")
        return None
    
def display_top_skills():
    top_skills = get_top_skills()
    if option == "Choose an option":
        ranking = 1
        for skill in top_skills:

            with st.expander(f"{ranking} {skill['skill_name']}"):
                st.markdown(f"Skill type: {skill['skill_type']}")
                st.markdown(f"Frequency: {skill['frequency']}")
                st.markdown(f"Average Employer Weight: {skill['avg_skill_weightage']}")
                st.markdown(f"Average Student Proficiency: {skill['avg_student_proficiency']}")

                ranking += 1
    else:
        filtered_skills = get_top_filtered_skills(option)
        ranking2 = 1
        for skill in filtered_skills:
            with st.expander(f"{ranking2} {skill['skill_name']}"):
                st.markdown(f"Skill type: {skill['skill_type']}")
                st.markdown(f"Frequency: {skill['frequency']}")
                st.markdown(f"Average Employer Weight: {skill['avg_skill_weightage']}")
                st.markdown(f"Average Student Proficiency: {skill['avg_student_proficiency']}")

                ranking2 += 1
    

# Assuming get_top_skills() is working fine and returns data like [{'skill_name': 'Skill1', 'skill_type': 'Programming', 'frequency': 5}, ...]

display_top_skills()

