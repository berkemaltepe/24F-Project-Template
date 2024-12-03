import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide')

SideBarLinks()

# Set the page header
st.title("All Advisors Information")

URL = "http://api:4000/system_admin" 

def get_advisors():
    try:
        response = requests.get(f"{URL}/advisor")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch advisors: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching advisors: {e}")
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

def display_all_advisors():
    advisors = get_advisors()

    if advisors:
        admins = get_admin_names_ids()
        
        for advisor in advisors:
            admin_name = next((k for k, v in admins.items() if v == advisor["admin_id"]), "Unknown")
            advisor['admin_id'] = admin_name
        columns = ["advisor_id", "name", "email", "department", "admin_id"]
        df = pd.DataFrame(advisors, columns=columns)
        df.rename(columns={
            "advisor_id": "ID",
            "admin_id": "Admin",
            "name": "Name",
            "email": "Email",
            "department": "Department"}, inplace=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.warning("No advisor data available.")

def add_advisor(): 
    id = st.number_input("Advisor ID", min_value=1, step=1) 
    admins = get_admin_names_ids()
    selected_admin = st.selectbox("Admin", options=["Select an Admin"] + list(admins.keys())) 
    name = st.text_input("Name")
    email = st.text_input("Email")
    department = st.text_input("Department")
    
    if st.button("Add advisor", type='primary', use_container_width=True):
        advisors = get_advisors()
        if (not all([name, email, department]) or
        selected_admin == "Select an Admin"):
            st.warning("Please fill out all the fields.")
        elif any(advisor['advisor_id'] == id for advisor in advisors):
            st.warning(f"Advisor ID {id} already exists. Enter a unique advisor ID.")
        else:
            advisor_data = {"advisor_id": id, "admin_id": admins[selected_admin], "name": name, "email": email, "department": department}
            try:
                response = requests.post(f"{URL}/advisor", json=advisor_data)
                if response.status_code == 200:
                    st.session_state["add_success"] = f"Successfully added new advisor {name}."
                    st.rerun()
                else:
                    st.error(f"Failed to add advisor: {response.text}")
            except Exception as e:
                st.error(f"Error occurred while adding advisor: {e}")

    if "add_success" in st.session_state:
        st.success(st.session_state["add_success"])
        del st.session_state["add_success"]

display_all_advisors()
st.divider()
st.write("## Add an advisor")
add_advisor()