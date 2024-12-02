import logging
import requests
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks

# Configure logging
logger = logging.getLogger(__name__)

# Set up the page layout
st.set_page_config(layout="wide")

# Show sidebar links for the logged-in user
SideBarLinks()

# Define the base API URL for advisors
BASE_URL = "http://web-api:4000/a"

# Ensure session state contains the necessary data
if "advisor_id" not in st.session_state:
    st.error("Advisor ID not found. Please log in as an advisor.")
    st.stop()

st.write(f"Advisor ID: {st.session_state.get('advisor_id', 'Not set')}")

# Title of the page
st.markdown(
    """
    <div style="padding: 20px; border-radius: 10px; border: 3px solid #FF0000; background-color: #000000; color: white; text-align: center;">
        <h1 style="font-size: 40px;">Advisor - Student List</h1>
        <p style="font-size: 18px;">View and manage the students assigned to you</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Fetch the list of students assigned to the advisor
advisor_id = st.session_state["advisor_id"]
response = requests.get(f"{BASE_URL}/advisor/{advisor_id}/list-of-students/")

if response.status_code == 200:
    students = response.json()
    if not students:
        st.warning("No students are currently assigned to you.")
    else:
        # Convert the student data into a Pandas DataFrame
        student_data = pd.DataFrame([
            {
                "Student ID": student["student_id"],
                "Name": student["name"],
                "Email": student["email"],
                "Major": student["major"],
                "GPA": student["gpa"],
                "Co-op Status": student["coop_status"],
            }
            for student in students
        ])
        
        st.write("")
        st.dataframe(student_data, use_container_width=True)

        # Add functionality to view more details or remove a student
        selected_student = st.selectbox(
            "Select a student to view details or manage:",
            options=["None"] + list(student_data["Name"]),
        )

        if selected_student != "None":
            # Retrieve the selected student's details
            student = next(s for s in students if s["name"] == selected_student)
            st.markdown(f"### Details for {student['name']}")
            st.json(student)

            # Action buttons for the selected student
            col1, col2 = st.columns(2)
            with col1:
                if st.button("View Skills"):
                    st.session_state["student_id"] = student["student_id"]
                    st.switch_page("pages/advisor_skill_match.py")
            with col2:
                if st.button("Remove Student"):
                    delete_response = requests.delete(
                        f"{BASE_URL}/advisor/{advisor_id}/student/{student['student_id']}/"
                    )
                    if delete_response.status_code == 200:
                        st.success(f"Student {student['name']} removed successfully.")
                        st.experimental_rerun()
                    else:
                        st.error(f"Failed to remove student: {delete_response.text}")
else:
    st.error(f"Failed to fetch students. Error {response.status_code}: {response.text}")

# Add functionality to assign a student by student ID
st.markdown("### Add a Student by Student ID")
student_id_to_add = st.number_input("Enter Student ID to Add", min_value=1, step=1)
if st.button("Add Student"):
    try:
        response = requests.put(
            f"{BASE_URL}/advisor/{advisor_id}/student/{student_id_to_add}/"
        )
        if response.status_code == 200:
            st.success(f"Student with ID {student_id_to_add} successfully assigned to Advisor {advisor_id}.")
            st.experimental_rerun()  # Refresh the page to show the updated student list
        else:
            st.error(f"Failed to add student: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error adding student: {e}")
        st.error("An error occurred while adding the student.")

# Footer
st.markdown(
    """
    <hr>
    <footer style="text-align: center; margin-top: 30px; color: #777;">
        <p>Powered by NU SkillMatch Platform | © 2024 SkillMatch, Inc.</p>
    </footer>
    """,
    unsafe_allow_html=True,
)