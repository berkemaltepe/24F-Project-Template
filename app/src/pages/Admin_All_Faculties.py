import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide')

SideBarLinks()

# Set the page header
st.title("All Faculties Information")

URL = "http://api:4000/system_admin" 

def get_faculty_names_ids():
    try:
        response = requests.get(f"{URL}/faculty")
        if response.status_code == 200:
            faculties = response.json()
            return {faculty['name']: faculty['faculty_id'] for faculty in faculties}
        else:
            st.error(f"Failed to fetch faculties: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching faculties: {e}")
        return None

def get_admin_names_ids():
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            admins = response.json()
            return {admin['name']: admin['admin_id'] for admin in admins}
        else:
            st.error(f"Failed to fetch admins: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching admins: {e}")
        return None

def display_all_faculties():
    try:
        response = requests.get(f"{URL}/faculty") 
        faculties = response.json()  
    except Exception as e:
        st.error(f"Error fetching faculty data: {e}")
        faculties = []

    if faculties:
        admins = get_admin_names_ids()
        
        for faculty in faculties:
            admin_name = next((k for k, v in admins.items() if v == faculty["admin_id"]), "Unknown")
            faculty['admin_id'] = admin_name
        columns = ["faculty_id", "name", "email", "department", "admin_id"]
        df = pd.DataFrame(faculties, columns=columns)
        df.rename(columns={
            "faculty_id": "ID",
            "admin_id": "Admin",
            "name": "Name",
            "email": "Email",
            "department": "Department"}, inplace=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("No faculty data available.")

def add_faculty(): 
    id = st.number_input("Faculty ID", min_value=1, step=1) 
    admins = get_admin_names_ids()
    selected_admin = st.selectbox("Admin", options=["Select an Admin"] + list(admins.keys())) 
    name = st.text_input("Name")
    email = st.text_input("Email")
    department = st.text_input("Department")
    
    if st.button("Add Faculty", type='primary', use_container_width=True):
        faculties = get_faculty_names_ids()
        if (not all([name, email, department]) or
        selected_admin == "Select an Admin"):
            st.warning("Please fill out all the fields.")
        elif id in faculties.values():
            st.warning(f"Faculty ID {id} already exists. Enter a unique faculty ID.")
        else:
            faculty_data = {"faculty_id": id, "admin_id": admins[selected_admin], "name": name, "email": email, "department": department}
            try:
                response = requests.post(f"{URL}/faculty", json=faculty_data)
                if response.status_code == 200:
                    st.session_state["add_success"] = f"Successfully added new faculty {name}."
                    st.rerun()
                else:
                    st.error(f"Failed to add faculty: {response.text}")
            except Exception as e:
                st.error(f"Error occurred while adding faculty: {e}")

    if "add_success" in st.session_state:
        st.success(st.session_state["add_success"])
        del st.session_state["add_success"]

display_all_faculties()
st.divider()
st.write("## Add a Faculty")
add_faculty()