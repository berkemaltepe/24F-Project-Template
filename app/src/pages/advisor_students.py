# import libs
import streamlit as st
import pandas as pd
import requests

# Define the base URL for the API
BASE_URL = "http://web-api:4000/advisor"

# Title and description for the page
st.markdown(
    """
    <div style="padding: 20px; border-radius: 10px; border: 3px solid #FF0000; background-color: #000000; color: white; text-align: center;">
        <h1>Student List</h1>
        <p>View and manage students assigned to you.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Fetch the student list for the current advisor
advisor_id = st.session_state.get("advisor_id", 1)  # Default to 1 if session state is missing
response = requests.get(f"{BASE_URL}/{advisor_id}/students")

if response.status_code == 200:
    students = response.json()
    if not students:
        st.warning("No students are currently assigned to you.")
    else:
        # Display the student list in a table
        st.write("## Assigned Students")
        st.write("Below is the list of students assigned to you:")

        # Convert the student data into a more readable format for display
        student_data = [
            {
                "Student ID": student["student_id"],
                "Name": student["name"],
                "Email": student["email"],
                "Major": student["major"],
                "GPA": student["gpa"],
                "Co-op Status": student["coop_status"],
            }
            for student in students
        ]

        # Display the data using Streamlit's table functionality
        st.table(student_data)

        # Select a student for more actions
        selected_student = st.selectbox(
            "Select a student to view details or manage:",
            options=[None] + [student["name"] for student in student_data],
        )

        if selected_student:
            student = next(
                (s for s in students if s["name"] == selected_student), None
            )
            if student:
                st.write("### Selected Student Details")
                st.json(student)

                # Provide action buttons for the selected student
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("View Skills"):
                        # Redirect to the skill list page for this student
                        st.session_state["student_id"] = student["student_id"]
                        st.switch_page("advisor_skill_match.py")
                with col2:
                    if st.button("Remove Student"):
                        # Call the API to remove the student
                        delete_response = requests.delete(
                            f"{BASE_URL}/student/",
                            json={"student_id": student["student_id"]},
                        )
                        if delete_response.status_code == 200:
                            st.success(f"Student {student['name']} removed successfully.")
                            st.experimental_rerun()
                        else:
                            st.error(f"Error removing student: {delete_response.text}")

else:
    st.error(f"Failed to fetch students. Error: {response.status_code}")