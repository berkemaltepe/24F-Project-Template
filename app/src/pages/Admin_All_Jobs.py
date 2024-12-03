import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide')

SideBarLinks()

# Set the page header
st.title("All Jobs Information")

URL = "http://api:4000/system_admin" 

def get_jobs():
    try:
        response = requests.get(f"{URL}/job")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch jobs: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching jobs: {e}")
        return None

def get_emp_name_ids():
    try:
        response = requests.get(f"{URL}/employer")
        if response.status_code == 200:
            emps = response.json()
            return {emp['name']: emp['emp_id'] for emp in emps}
        else:
            st.error(f"Failed to fetch employers: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching employers: {e}")
        return None

def display_all_jobs():
    jobs = get_jobs()

    if jobs:
        emps = get_emp_name_ids()
        
        for job in jobs:
            emp_name = next((k for k, v in emps.items() if v == job["emp_id"]), "Unknown")
            job['emp_id'] = emp_name

        columns = ["job_id", "title", "emp_id", "description", "location", "pay_range", "status"]
        df = pd.DataFrame(jobs, columns=columns)
        df.rename(columns={
            "job_id": "ID",
            "title": "Title",
            "emp_id": "Employer",
            "description": "Description",
            "location": "Location",
            "pay_range": "Pay Range",
            "status": "Status"}, inplace=True)
        df.rename(columns={"job_id": "id"}, inplace=True)
        st.dataframe(df, hide_index=True)
    else:
        st.warning("No job data available.")

def add_job():  
    id = st.number_input("Job ID", min_value=1, step=1) 
    title = st.text_input("Title")
    emps = get_emp_name_ids()
    selected_emp = st.selectbox("Employer", options=["Select an Employer"] + list(emps.keys()))
    description = st.text_input("Description")
    location = st.text_input("Location")
    pay_range = st.text_input("Pay Range")
    status = st.selectbox("Status", ["Open", "Not Open"])

    jobs = get_jobs()
    
    if st.button("Add Job", type='primary', use_container_width=True):
        if (not all([title, description, location, pay_range]) or
        selected_emp == "Select an Employer"):
            st.warning("Please fill out all the fields.")
        elif any(job['job_id'] == id for job in jobs):
            st.warning(f"Job ID {id} already exists. Enter a unique job ID.")
        else:
            job_data = {"job_id": id, "title": title, "emp_id": emps[selected_emp], "description": description, 
            "location": location, "pay_range": pay_range, "status": status}
            
            try:
                response = requests.post(f"{URL}/job", json=job_data)
                if response.status_code == 200:
                    st.session_state["add_success"] = f"Successfully added new job {title}."
                    st.rerun()
                else:
                    st.error(f"Failed to add job: {response.text}")
            except Exception as e:
                st.error(f"Error occurred while adding job: {e}")

    if "add_success" in st.session_state:
        st.success(st.session_state["add_success"])
        del st.session_state["add_success"]

def delete_job():
    jobs = get_jobs()
    job_ids = [job['job_id'] for job in jobs]
    selected_job = st.selectbox("Job ID", options=["Select a job"] + job_ids)

    if st.button("Delete", type='primary', use_container_width=True):
        if selected_job == "Select a job":
            st.warning("Please select a valid job to delete.")
        else:
            for job in jobs:
                if job['job_id'] == selected_job:
                    job_title = job['title']
                    break
            try:
                delete_response = requests.delete(f"{URL}/job/{selected_job}")
                if delete_response.status_code == 200:
                    st.session_state["delete_success"] = f"Successfully deleted {job_title}."
                    st.rerun()
                else:
                    st.error(f"Failed to delete {job_title}: {delete_response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error deleting job: {e}")

    if "delete_success" in st.session_state:
        st.success(st.session_state["delete_success"])
        del st.session_state["delete_success"]

display_all_jobs()
st.divider()
left, right = st.columns(2, gap="large")

with left:
    st.write("## Add a job")
    add_job()

with right:
    st.write('## Delete a job')
    delete_job()