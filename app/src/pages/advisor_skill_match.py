import logging
import requests
import pandas as pd
import streamlit as st
import plotly.graph_objs as go
from modules.nav import SideBarLinks

# Configure logging
logger = logging.getLogger(__name__)

# Set up the page layout
st.set_page_config(layout="wide")

# Show sidebar links for the logged-in user
SideBarLinks()

# Ensure session state contains the necessary data
if "advisor_id" not in st.session_state:
    st.error("Advisor ID not found. Please log in as an advisor.")
    st.stop()

st.write(f"Advisor ID: {st.session_state.get('advisor_id', 'Not set')}")

# Page title
st.markdown(
    """
    <div style="padding: 20px; border-radius: 10px; border: 3px solid #FF0000; background-color: #000000; color: white; text-align: center;">
        <h1 style="font-size: 40px;">Skill Match Analysis</h1>
        <p style="font-size: 18px;">View the skill gap between your student and job requirements</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write('')

BASE_URL = "http://web-api:4000/a"  # Base URL for API endpoints
advisor_id = st.session_state["advisor_id"]

# Fetch the list of students assigned to the advisor
response = requests.get(f"{BASE_URL}/advisor/{advisor_id}/list-of-students/")
if response.status_code == 200:
    students = response.json()
    if not students:
        st.error("No students are currently assigned to you.")
        st.stop()
    else:
        # Convert student list into a DataFrame
        student_data = pd.DataFrame(students)
        # Map student IDs to names for the dropdown
        student_options = {str(row["student_id"]): row["name"] for _, row in student_data.iterrows()}
        
        # Dropdown to select a student
        selected_student_id = st.selectbox(
            "Select a student from your list:",
            options=["None"] + list(student_options.keys()),
            format_func=lambda x: student_options.get(x, "None"),
        )

        if selected_student_id != "None":
            # Set the selected student_id in session state
            st.session_state["student_id"] = int(selected_student_id)
            st.success(f"Student {student_options[selected_student_id]} selected.")
else:
    st.error(f"Failed to fetch students. Error {response.status_code}: {response.text}")
    st.stop()

# If student_id exists in session state, continue with skill match
if "student_id" in st.session_state:
    student_id = st.session_state["student_id"]

    # Select job ID
    st.write("##### Select a Job to Compare")
    job_response = requests.get(f"{BASE_URL}/advisor/employer/")
    if job_response.status_code == 200:
        jobs = job_response.json()
        if not jobs:
            st.error("No jobs found.")
            st.stop()
        job_data = pd.DataFrame(jobs)
        selected_job = st.selectbox(
            "Available Jobs:",
            options=["Select a job"] + job_data["job_title"].tolist(),
        )
    else:
        st.error("Failed to fetch jobs. Please try again later.")
        st.stop()

    if selected_job != "Select a job":
        job_id = job_data[job_data["job_title"] == selected_job]["job_id"].values[0]

        # Fetch skill comparison data
        comparison_response = requests.get(f"{BASE_URL}/advisor/job/{job_id}/skills/compare/{student_id}/")
        if comparison_response.status_code == 200:
            skill_comparison = comparison_response.json()
            if not skill_comparison:
                st.warning("No skill comparison data available for this job.")
            else:
                # Convert skill comparison data into a DataFrame
                comparison_df = pd.DataFrame(skill_comparison)

                # Display a DataFrame of skill gaps
                st.write("##### Skill Comparison Table")
                st.dataframe(comparison_df)

                # Create Radar Chart using Plotly
                st.write("##### Radar Chart: Skills Comparison")
                all_skills = comparison_df["skill_name"].tolist()
                student_skills = comparison_df["student_proficiency"].tolist()
                job_skills = comparison_df["job_requirement"].tolist()

                fig = go.Figure()

                # Add job requirements
                fig.add_trace(go.Scatterpolar(
                    r=job_skills,
                    theta=all_skills,
                    fill='toself',
                    name="Employer's Required Skills",
                    line=dict(color='black', width=3),
                    marker=dict(symbol='circle', size=8)
                ))

                # Add student proficiency
                fig.add_trace(go.Scatterpolar(
                    r=student_skills,
                    theta=all_skills,
                    fill='toself',
                    name="Student's Skills",
                    line=dict(color='red', width=3),
                    marker=dict(symbol='star', size=8)
                ))

                # Update layout
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, max(max(job_skills), max(student_skills))])
                    ),
                    showlegend=True
                )

                st.plotly_chart(fig)
        else:
            st.error("Failed to fetch skill comparison data.")
