import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide')

SideBarLinks()

# Set the page header
st.title("All Skills Information")

URL = "http://api:4000/system_admin" 

def get_skills():
    try:
        response = requests.get(f"{URL}/skill")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch skills: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching skills: {e}")
        return None

def display_all_skills():
    skills = get_skills()
    
    if skills:
        columns = ["skill_id", "skill_name", "skill_type", "weight"]
        df = pd.DataFrame(skills, columns=columns)
        df.rename(columns={
            "skill_id": "ID",
            "skill_name": "Name",
            "skill_type": "Type",
            "weight": "Weight"}, inplace=True)
        st.dataframe(df, use_container_width=True, hide_index=True, 
        column_config=st.column_config.Column("ID", width="large"))
    else:
        st.warning("No skill data available.")

def add_skill(): 
    id = st.number_input("Skill ID", min_value=1, step=1)  
    name = st.text_input("Name")
    type = st.text_input("Type")
    weight = st.number_input("Weight", min_value=1, step=1)
    
    if st.button("Add skill", type='primary', use_container_width=True):
        skills = get_skills()
        if not all([name, type]):
            st.warning("Please fill out all the fields.")
        elif any(skill['skill_id'] == id for skill in skills):
            st.warning(f"Skill ID {id} already exists. Enter a unique skill ID.")
        else:
            skill_data = {"skill_id": id, "skill_name": name, "skill_type": type, "weight": weight}
            
            try:
                response = requests.post(f"{URL}/skill", json=skill_data)
                if response.status_code == 200:
                    st.session_state["add_success"] = f"Successfully added new skill {name}."
                    st.rerun()
                else:
                    st.error(f"Failed to add skill: {response.text}")
            except Exception as e:
                st.error(f"Error occurred while adding skill: {e}")

    if "add_success" in st.session_state:
        st.success(st.session_state["add_success"])
        del st.session_state["add_success"]

def delete_skill():
    skills = get_skills()
    skill_ids = [skill['skill_id'] for skill in skills]
    selected_skill = st.selectbox("Skill ID", options=["Select a skill"] + skill_ids)

    if st.button("Delete", type='primary', use_container_width=True):
        if selected_skill == "Select a skill":
            st.warning("Please select a valid skill to delete.")
        else:
            for skill in skills:
                if skill['skill_id'] == selected_skill:
                    skill_name = skill['skill_name']
            try:
                delete_response = requests.delete(f"{URL}/skill/{selected_skill}")
                if delete_response.status_code == 200:
                    st.session_state["delete_success"] = f"Successfully deleted {skill_name}."
                    st.rerun()
                else:
                    st.error(f"Failed to delete {skill_name}: {delete_response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error deleting skill: {e}")

    if "delete_success" in st.session_state:
        st.success(st.session_state["delete_success"])
        del st.session_state["delete_success"]

display_all_skills()
st.divider()
left, right = st.columns(2, gap="large")

with left:
    st.write("## Add a skill")
    add_skill()

with right:
    st.write('## Delete a skill')
    delete_skill()