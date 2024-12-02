import logging
import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Configure logging
logger = logging.getLogger(__name__)

# Set up the page layout
st.set_page_config(layout="wide")

# Ensure session state contains the necessary data
if "student_id" not in st.session_state or "advisor_id" not in st.session_state:
    st.error("Missing required data. Please navigate back and select a student or advisor.")
    st.stop()

BASE_URL = "http://web-api:4000/a"  # Base URL for API endpoints
student_id = st.session_state["student_id"]
advisor_id = st.session_state["advisor_id"]

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

# Select job ID
st.write("### Select a Job to Compare")
job_response = requests.get(f"{BASE_URL}/advisor/employer/")
if job_response.status_code == 200:
    jobs = job_response.json()
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
            st.write("### Skill Comparison Table")
            st.dataframe(comparison_df)

            # Create a bar chart for visualization
            st.write("### Skill Gap Visualization")
            plt.figure(figsize=(10, 6))
            plt.bar(
                comparison_df["skill_name"], 
                comparison_df["job_requirement"] - comparison_df["student_proficiency"], 
                color="red", 
                alpha=0.7,
            )
            plt.xlabel("Skills")
            plt.ylabel("Skill Gap")
            plt.title("Skill Gaps Between Student Proficiency and Job Requirements")
            plt.xticks(rotation=45, ha="right")
            st.pyplot(plt)
    else:
        st.error("Failed to fetch skill comparison data.")