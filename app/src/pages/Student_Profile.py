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

# Function to get student information
def get_student(student_id):
    try:
        response = requests.get(f'http://api:4000/s/student/{student_id}/')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching student information: {e}")
        st.error("Failed to fetch student information")
        return None

# Function to update student profile
def update_student_profile(student_id, profile_data):
    try:
        response = requests.put(f'http://api:4000/s/student/{student_id}/', json=profile_data)
        response.raise_for_status()
        st.success("Successfully updated student profile")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating student profile: {e}")
        st.error("Failed to update student profile")

# Fetch and display student information
if st.session_state.student_id:
    student_info = get_student(st.session_state.student_id)
    if student_info:
        st.write("### Student Information")

        # Display student information in a prettier format
        st.markdown(f"**Name:** {student_info[0]['name']}")
        st.markdown(f"**Email:** {student_info[0]['email']}")
        st.markdown(f"**Location:** {student_info[0]['location']}")
        st.markdown(f"**Major:** {student_info[0]['major']}")
        st.markdown(f"**Co-op Status:** {student_info[0]['coop_status']}")
        st.markdown(f"**Resume:** {student_info[0]['resume']}")
        st.markdown(f"**Level:** {student_info[0]['level']}")
        st.markdown(f"**LinkedIn Profile:** {student_info[0]['linkedin_profile']}")
        st.markdown(f"**GPA:** {student_info[0]['gpa']}")

        # Button to navigate to Student Skills page
        if st.button("Go to Student Skills"):
            st.switch_page('pages/Student_Skills.py')

        # Edit profile section
        with st.expander("Edit Profile"):
            name = st.text_input("Name", value=student_info[0]['name'])
            email = st.text_input("Email", value=student_info[0]['email'])
            location = st.text_input("Location", value=student_info[0]['location'])
            major = st.text_input("Major", value=student_info[0]['major'])
            coop_status = st.text_input("Co-op Status", value=student_info[0]['coop_status'])
            resume = st.text_area("Resume", value=student_info[0]['resume'])
            level = st.text_input("Level", value=student_info[0]['level'])
            linkedin_profile = st.text_input("LinkedIn Profile", value=student_info[0]['linkedin_profile'])
            gpa = st.number_input("GPA", min_value=0, max_value=4, step=1, value=int(student_info[0]['gpa']))

            if st.button("Update Profile"):
                profile_data = {
                    'name': name,
                    'email': email,
                    'location': location,
                    'major': major,
                    'coop_status': coop_status,
                    'resume': resume,
                    'level': level,
                    'linkedin_profile': linkedin_profile,
                    'gpa': gpa
                }
                update_student_profile(st.session_state.student_id, profile_data)
    else:
        st.write("No student information available.")
else:
    st.write("Please enter a student ID.")