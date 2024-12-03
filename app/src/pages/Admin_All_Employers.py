import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide')

SideBarLinks()

# Set the page header
st.title("All Employers Information")

URL = "http://api:4000/system_admin" 

def get_employer_names_ids():
    try:
        response = requests.get(f"{URL}/employer")
        if response.status_code == 200:
            employers = response.json()
            return {employer['name']: employer['emp_id'] for employer in employers}
        else:
            st.error(f"Failed to fetch employers: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching employers: {e}")
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

def display_all_employers():
    try:
        response = requests.get(f"{URL}/employer") 
        employers = response.json()  
    except Exception as e:
        st.error(f"Error fetching employer data: {e}")
        employers = []
    
    if employers:
        admins = get_admin_names_ids()
        
        for employer in employers:
            admin_name = next((k for k, v in admins.items() if v == employer["admin_id"]), "Unknown")
            employer['admin_id'] = admin_name

        columns = ["emp_id", "name", "email", "industry", "num_applications", "admin_id"]
        df = pd.DataFrame(employers, columns=columns)
        df.rename(columns={
            "emp_id": "ID",
            "admin_id": "Admin",
            "name": "Name",
            "email": "Email",
            "industry": "Industry",
            "num_applications": "Applications"}, inplace=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("No employer data available.")

def add_employer(): 
    id = st.number_input("Employer ID", min_value=1, step=1)  
    admins = get_admin_names_ids()
    selected_admin = st.selectbox("Admin", options=["Select an Admin"] + list(admins.keys())) 
    name = st.text_input("Name")
    email = st.text_input("Email")
    industry = st.text_input("Industry")
    num_apps = st.number_input("Number of Applications", min_value=0, step=1)
    
    if st.button("Add Employer", type='primary', use_container_width=True):
        employers = get_employer_names_ids()

        if (not all([selected_admin, name, email, industry]) or
        selected_admin == "Select an Admin"):
            st.warning("Please fill out all the fields.")
        elif id in employers.values():
            st.warning(f"Employer ID {id} already exists. Enter a unique employer ID.")
        else:
            employer_data = {"emp_id": id, "admin_id": admins[selected_admin], "name": name, "email": email, 
            "industry": industry, "num_applications": num_apps}
            
            try:
                response = requests.post(f"{URL}/employer", json=employer_data)
                if response.status_code == 200:
                    st.session_state["add_success"] = f"Successfully added new employer {name}."
                    st.rerun()
                else:
                    st.error(f"Failed to add employer: {response.text}")
            except Exception as e:
                st.error(f"Error occurred while adding employer: {e}")

    if "add_success" in st.session_state:
        st.success(st.session_state["add_success"])
        del st.session_state["add_success"]

display_all_employers()
st.divider()
st.write("## Add an employer")
add_employer()