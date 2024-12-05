import streamlit as st
import plotly.graph_objs as go
import requests
from modules.nav import SideBarLinks

# Set Streamlit layout
st.set_page_config(layout="wide")
st.markdown(
                    f"""
                    <div style="padding: 20px; border-radius: 10px; border: 3px solid #FF0000; background-color: #000000; margin-bottom: 20px;">
                        <h2 style="text-align: center; color: #FFFFFF;"> <strong>SkillMatch Comparison</h2>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

SideBarLinks()

# Define base URLs
BASE_URL = "http://web-api:4000/employer"



job_id = st.session_state['job_id']
student_id = st.session_state['student_id']


# Fetch data when a button is clicked
if job_id and student_id:
    try:
        # Fetch student skills
        student_response = requests.get(f"{BASE_URL}/students/{student_id}/skills")
        student_info = requests.get(f"{BASE_URL}/students/{student_id}")
        employer_response = requests.get(f"{BASE_URL}/jobs/{job_id}/skills")
        
        if student_response.status_code == 200 and employer_response.status_code == 200:
            student_skills = student_response.json()
            employer_skills = employer_response.json()
            student = student_info.json()[0]

            
            st.header("Student's Skillset")
            for skill in student_skills:
                st.write(f"Skill: {skill['skill_name']} | Weight: {skill['weight']}")
            st.header("Required Skillset")
            for skill in employer_skills:
                st.write(f"Skill: {skill['skill_name']} | Weight: {skill['weight']}")    
            # Ensure skills are aligned
            all_skills = {skill['skill_name'] for skill in employer_skills} | {skill['skill_name'] for skill in student_skills}
            
            all_skills = list(all_skills)  # Convert to list for ordering

            # Map skills to weights for radar chart
            student_weights = [next((s['weight'] for s in student_skills if s['skill_name'] == skill), 0) for skill in all_skills]
            employer_weights = [next((e['weight'] for e in employer_skills if e['skill_name'] == skill), 0) for skill in all_skills]

            # Create Radar Chart
            fig = go.Figure()

            # Add employer skills to the radar chart
            fig.add_trace(go.Scatterpolar(
                r=employer_weights,
                theta=all_skills,
                fill='toself',
                name="Employer's Required Skills",
                line=dict(color='black', width=3),
                marker=dict(symbol='circle', size=16)
            ))

            # Add student skills to the radar chart
            fig.add_trace(go.Scatterpolar(
                r=student_weights,
                theta=all_skills,
                fill='toself',
                name="Student's Skills",
                line=dict(color='red', width=3),
                marker=dict(symbol='star', size=8)
            ))

            # Update layout
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, max(max(employer_weights), max(student_weights))])
                ),
                showlegend=True,
                title="Radar Chart: Skills Comparison"
            )

            # Display radar chart
            st.plotly_chart(fig)

            # Fetch and display skill gap
            skill_gap_response = requests.get(f"{BASE_URL}/job/{job_id}/{student_id}/student_matches")
            if skill_gap_response.status_code == 200:
                skill_gap_data = skill_gap_response.json()
                for gap in skill_gap_data:
                    if gap['student_id'] == student_id:
                        st.header(f"**Total Skill Match:** {gap['total_skill_gap']}%")
                        break
                else:
                    st.warning("No skill gap data found for the selected student and job.")
            else:
                st.error("Failed to fetch skill gap data.")
        else:
            st.error("Failed to fetch data for student or job. Please check the inputs and try again.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
