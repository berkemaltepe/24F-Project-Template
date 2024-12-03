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

# Ensure session state contains the necessary data
if "advisor_id" not in st.session_state:
    st.error("Advisor ID not found. Please log in as an advisor.")
    st.stop()

st.write(f"Advisor ID: {st.session_state.get('advisor_id', 'Not set')}")

BASE_URL = "http://web-api:4000/a"  # Base URL for API endpoints
advisor_id = st.session_state["advisor_id"]

# Page Title
st.markdown(
    """
    <div style="padding: 20px; border-radius: 10px; border: 3px solid #FF0000; background-color: #000000; color: white; text-align: center;">
        <h1 style="font-size: 40px;">Advisor - Job Postings</h1>
        <p style="font-size: 18px;">Review job postings and match students to roles</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Fetch job postings
try:
    job_response = requests.get(f"{BASE_URL}/advisor/employer/")
    if job_response.status_code == 200:
        jobs = job_response.json()
        if not jobs:
            st.warning("No job postings available.")
        else:
            # Convert job data into a DataFrame
            job_data = pd.DataFrame(jobs)

            # Search and Filter
            search_term = st.text_input("Search for job postings by title or location:", "").strip().lower()
            if search_term:
                job_data = job_data[
                    job_data["job_title"].str.lower().str.contains(search_term) |
                    job_data["location"].str.lower().str.contains(search_term)
                ]

            # Sorting options
            sort_by = st.selectbox("Sort by:", ["Job Title", "Location", "Pay Range", "Date Posted"])
            if sort_by == "Job Title":
                job_data = job_data.sort_values("job_title")
            elif sort_by == "Location":
                job_data = job_data.sort_values("location")
            elif sort_by == "Pay Range":
                job_data = job_data.sort_values("pay_range")
            elif sort_by == "Date Posted":
                job_data = job_data.sort_values("date_posted", ascending=False)

            # Display job postings in a table
            st.write("### Job Postings")
            st.dataframe(job_data[["job_title", 
                                   "employer_name", 
                                   "location", 
                                   "pay_range", 
                                   "status", 
                                   "date_posted"]], use_container_width=True)
            
            # Select a job for more details
            selected_job_title = st.selectbox(
                "Select a job to view more details:",
                options=["None"] + job_data["job_title"].tolist()
            )

            if selected_job_title != "None":
                job_details = job_data[job_data["job_title"] == selected_job_title].iloc[0]
                st.markdown("### Job Details")
                st.write(f"**Title:** {job_details['job_title']}")
                st.write(f"**Employer:** {job_details['employer_name']}")
                st.write(f"**Location:** {job_details['location']}")
                st.write(f"**Pay Range:** {job_details['pay_range']}")
                st.write(f"**Date Posted:** {job_details['date_posted']}")
                st.write(f"**Status:** {job_details['status']}")
                st.write(f"**Description:** {job_details['description']}")

                # Additional actions for the selected job
                st.markdown("### Actions")
                if st.button("Match a Student to this Job"):
                    st.session_state["job_id"] = job_details["job_id"]
                    st.success(f"Job '{job_details['job_title']}' selected for matching.")
                    st.switch_page("pages/advisor_skill_match.py")  # Redirect to skill match page
    else:
        st.error("Failed to fetch job postings. Please try again later.")

except Exception as e:
    st.error(f"An error occurred while fetching job postings: {e}")