import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd

st.set_page_config(layout = 'wide')

SideBarLinks()

# Set the page header
st.title("All Students Information")

URL = "http://api:4000/system_admin" 

def get_students(): 
    try:
        response = requests.get(f"{URL}/student")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch students: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching students: {e}")
        return None

def get_advisor_names_ids():
    try:
        response = requests.get(f"{URL}/advisor")
        if response.status_code == 200:
            advisors = response.json()
            return {advisor['name']: advisor['advisor_id'] for advisor in advisors}
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

def display_all_students():
    students = get_students()
    if students:
        advisors = get_advisor_names_ids()
        admins = get_admin_names_ids()
        
        for student in students:
            advisor_name = next((k for k, v in advisors.items() if v == student["advisor_id"]), "Unknown")
            admin_name = next((k for k, v in admins.items() if v == student["admin_id"]), "Unknown")
            student['advisor_id'] = advisor_name
            student['admin_id'] = admin_name

        columns = ["student_id", "name", "email", "location", "major", "coop_status",
        "resume", "level", "linkedin_profile", "gpa", "advisor_id", "admin_id"]
        df = pd.DataFrame(students, columns=columns)
        df.rename(columns={
            "student_id": "ID",
            "name": "Name",
            "email": "Email Address",
            "location": "Location",
            "major": "Major",
            "coop_status": "Co-op Status",
            "resume": "Resume",
            "level": "Level",
            "linkedin_profile": "LinkedIn",
            "gpa": "GPA",
            "advisor_id": "Advisor",
            "admin_id": "Admin"}, inplace=True)
        st.dataframe(df, hide_index=True)
    else:
        st.warning("No student data available.")

def add_student(): 
    id = st.number_input("Student ID", min_value=1, step=1)  
    name = st.text_input("Name")
    email = st.text_input("Email")
    location = st.text_input("Location")
    major = st.text_input("Major")
    coop_status = st.selectbox("Co-op Status", ["Select a Status", "Seeking", "Accepted"])
    resume = st.text_input("Resume Link")
    level = st.selectbox("Level", ["Select a Level", "Sophomore", "Junior", "Senior"])
    linkedin_profile = st.text_input("LinkedIn Profile")
    gpa = st.number_input("GPA", min_value=0, max_value=4)

    advisors = get_advisor_names_ids()
    selected_advisor = st.selectbox("Advisor", options=["Select an Advisor"] + list(advisors.keys()))

    admins = get_admin_names_ids()
    selected_admin = st.selectbox("Admin", options=["Select an Admin"] + list(admins.keys()))

    students = get_students()
    
    if st.button("Add Student", type='primary', use_container_width=True):
        if (not all([name, email, location, major, resume, linkedin_profile]) or
        coop_status == "Select a Status" or level == "Select a Level" or 
        selected_advisor == "Select an Advisor" or selected_admin == "Select an Admin"):
            st.warning("Please fill out all the fields.")
        elif any(student['student_id'] == id for student in students):
            st.warning(f"Student ID {id} already exists. Enter a unique student ID.")
        else:
            student_data = {"student_id": id, "name": name, "email": email, "location": location, "major": major, 
            "coop_status": coop_status, "resume": resume, "level": level, "linkedin_profile": linkedin_profile, "gpa": gpa, 
            "advisor_id": advisors[selected_advisor], "admin_id": admins[selected_admin]}
            
            try:
                add_response = requests.post(f"{URL}/student", json=student_data)
                if add_response.status_code == 200:
                    st.session_state["add_success"] = f"Successfully added new student {name}."
                    st.rerun()
                else:
                    st.error(f"Failed to add student: {add_response.text}")
            except Exception as e:
                st.error(f"Error occurred while adding student: {e}")

    if "add_success" in st.session_state:
        st.success(st.session_state["add_success"])
        del st.session_state["add_success"]

def delete_student():
    students = get_students()
    student_ids = [student['student_id'] for student in students]
    selected_student = st.selectbox("Student ID", options=["Select a Student"] + student_ids)

    if st.button("Delete", type='primary', use_container_width=True):
        if selected_student == "Select a student":
            st.warning("Please select a valid student to delete.")
        else:
            for student in students:
                if student['student_id'] == selected_student:
                    student_name = student['name']
                    break
            try:
                delete_response = requests.delete(f"{URL}/student/{selected_student}")
                if delete_response.status_code == 200:
                    st.session_state["delete_success"] = f"Successfully deleted {student_name}."
                    st.rerun()
                else:
                    st.error(f"Failed to delete {student_name}: {delete_response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error deleting student: {e}")

    if "delete_success" in st.session_state:
        st.success(st.session_state["delete_success"])
        del st.session_state["delete_success"]

display_all_students()
st.divider()
left, right = st.columns(2, gap="large")

with left:
    st.write("## Add a student")
    add_student()

with right:
    st.write('## Delete a student')
    delete_student()