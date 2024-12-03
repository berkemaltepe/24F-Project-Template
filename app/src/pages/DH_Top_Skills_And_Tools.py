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

def get_notes(faculty_id, skill_id):
    try:
        response = requests.get(f'http://api:4000/depthead/skill_note/{skill_id}/{faculty_id}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching top skills: {e}")
        st.error("Failed to fetch top skills")
        return None

def add_note(faculty_id, skill_id, description):
    try:
        response = requests.post(f'http://api:4000/depthead/skill_note/{faculty_id}/{skill_id}/{description}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error adding note: {e}")
        st.error("Failed to add note")
        return None

def update_note(description, note_id):
    try:
        response = requests.put(f'http://api:4000/depthead/skill_note/{note_id}/{description}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error updating note: {e}")
        st.error("Failed to update note")
        return None

def delete_note(note_id):
    try:
        response = requests.delete(f'http://api:4000/depthead/skill_note/{note_id}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error deleting note: {e}")
        st.error("Failed to delete note")
        return None


def display_notes(notes):
    for note in notes:
        note_col, edit_col, delete_col = st.columns([3, 1, 1])
        with note_col:
            st.markdown(f"{note['description']}")

        with edit_col:
            edit_key = f"edit_mode_{note['note_id']}"
            if st.session_state.get(edit_key, False):  # Check edit mode for this note
                new_desc = st.text_input("Update note", value=note['description'], key=f"desc_input_{note['note_id']}")

                save_col, cancel_col = st.columns([2, 2])
                with save_col:
                    if st.button(f"Save Note", key=f"save_note_{note['note_id']}"):
                            update_note(new_desc, note['note_id'])
                            st.session_state[edit_key] = False
                            st.rerun()
                with cancel_col:
                    if st.button("Cancel", key=f"cancel_desc_{note['note_id']}"):
                        st.session_state[edit_key] = False
                        st.rerun()
            else:
                # Ensure the Edit note button has a unique key for each note
                if st.button(f"Edit note ✏️", key=f"edit_note_{note['note_id']}", use_container_width=True):
                    st.session_state[edit_key] = True
                    st.rerun()

        with delete_col:
            if st.button("Delete note 🗑️", key=f"delete_note_{note['note_id']}", use_container_width=True):
                delete_note(note['note_id'])
                st.rerun()

        

def display_add_notes(skill_id):
                add_key = f"add_mode_{skill_id}"
                if st.session_state.get(add_key, False):
                    new_desc = st.text_input("Add note", value='', key=f"add_desc_input_{skill_id}")

                    save_col, cancel_col = st.columns([2, 2])
                    with save_col:
                        if st.button(f"Save Note", key=f"save_note_{skill_id}"):
                                add_note(st.session_state.faculty_id, skill_id, new_desc)
                                st.session_state[add_key] = False 
                                st.rerun()
                    with cancel_col:
                        if st.button("Cancel", key=f"cancel_desc_{skill_id}"):
                            st.session_state[add_key] = False
                            st.rerun()  
                else:
                    if st.button("Add note ➕", key=f"add_note_btn_{skill_id}", use_container_width=True):
                        st.session_state[add_key] = True
                        st.rerun() 


def display_top_skills():
    top_skills = get_top_skills()
    if option == "Choose an option":
        for ranking, skill in enumerate(top_skills, start=1):
            notes = get_notes(st.session_state.faculty_id, skill['skill_id'])

            with st.expander(f"{ranking} {skill['skill_name']}"):
                st.markdown(f"Skill type: {skill['skill_type']}")
                st.markdown(f"Frequency: {skill['frequency']}")
                st.markdown(f"Average Employer Weight: {skill['avg_skill_weightage']}")
                st.markdown(f"Average Student Proficiency: {skill['avg_student_proficiency']}")
                st.write("### Notes:")
                display_notes(notes)
                display_add_notes(skill['skill_id'])
                ranking += 1

    else:
        filtered_skills = get_top_filtered_skills(option)
        ranking2 = 1
        for skill in filtered_skills:
            notes2 = get_notes(st.session_state.faculty_id, skill['skill_id'])
            with st.expander(f"{ranking2} {skill['skill_name']}"):
                st.markdown(f"Skill type: {skill['skill_type']}")
                st.markdown(f"Frequency: {skill['frequency']}")
                st.markdown(f"Average Employer Weight: {skill['avg_skill_weightage']}")
                st.markdown(f"Average Student Proficiency: {skill['avg_student_proficiency']}")
                display_notes(notes2)
                display_add_notes(skill['skill_id'])

                ranking2 += 1
    

st.write("## Top Skills")
display_top_skills()

