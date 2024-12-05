import logging
logger = logging.getLogger(__name__)
import requests 
import plotly.graph_objs as go

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks() 

st.write("### Major Program Reports 🎓")
st.write("See major-specific skills and compare them to industry skills!")

def get_top_student_skills(major):
    try:
        response = requests.get(f'http://api:4000/depthead/top-student-skills/{major}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching top skills: {e}")
        st.error("Failed to fetch top skills")
        return None
    
def get_top_industry_skills(industry):
    try:
        response = requests.get(f'http://api:4000/depthead/top-skills/industry/{industry}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching top skills: {e}")
        st.error("Failed to fetch top skills")
        return None      
    
def get_all_majors():
    try:
        response = requests.get(f'http://api:4000/depthead/student/major')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching majors: {e}")
        st.error("Failed to fetch majors")
        return None 

all_majors = get_all_majors()
major_names = [major['major'] for major in all_majors]

st.write("# Major Program Reports")
option = st.selectbox(
    "Search major",
    ["Choose a major"] + major_names 
)

def display_top_student_skills():
    if option != "Choose a major":
        st.write("## Top Student Skills:")
        skills = get_top_student_skills(option)
        ranking = 1
        for skill in skills:
            with st.expander(f"{ranking} {skill['skill_name']}"):
                st.markdown(f"Skill type: {skill['skill_type']}")
                st.markdown(f"Frequency: {skill['frequency']}")
                st.markdown(f"Average Proficiency: {skill['avg_student_proficiency']}")
                ranking += 1

def get_all_industries():
    try:
        response = requests.get(f'http://api:4000/depthead/job/industry')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching information: {e}")
        st.error("Failed to fetch information")
        return None 


all_industries = get_all_industries()
industry_names = [industry['industry'] for industry in all_industries]


def display_top_industry_skills():
    if industry != "Choose an industry":
        skills = get_top_industry_skills(industry)
        ranking = 1
        for skill in skills:
            with st.expander(f"{ranking} {skill['skill_name']}"):
                st.markdown(f"Skill type: {skill['skill_type']}")
                st.markdown(f"Frequency: {skill['frequency']}")
                st.markdown(f"Average Weight: {skill['avg_skill_weightage']}")
                ranking += 1
    
def display_radar_chart():
    if industry != "Choose an industry" and option != "Choose a major":  # Use 'and' for logical comparison
        try:
            # Fetch skills
            industry_skills = get_top_industry_skills(industry)
            student_skills = get_top_student_skills(option)

            # Debug responses to ensure correct data
            logger.debug(f"Industry Skills: {industry_skills}")
            logger.debug(f"Student Skills: {student_skills}")

            # Align skills between industry and student data
            all_skills = {skill['skill_name'] for skill in industry_skills} | {skill['skill_name'] for skill in student_skills}
            all_skills = list(all_skills)  # Convert to list for ordering

            # Map skills to weights for radar chart
            student_weights = [
                float(next((s['avg_student_proficiency'] for s in student_skills if s['skill_name'] == skill), 0)) for skill in all_skills
            ]
            industry_weights = [
                float(next((e['avg_skill_weightage'] for e in industry_skills if e['skill_name'] == skill), 0)) for skill in all_skills
            ]

            # Create Radar Chart
            fig = go.Figure()

            # Add industry skills to the radar chart
            fig.add_trace(go.Scatterpolar(
                r=industry_weights,
                theta=all_skills,
                fill='toself',
                name="Industry's Top Skills",
                line=dict(color='black', width=3),
                marker=dict(symbol='circle', size=16)
            ))

            # Add student skills to the radar chart
            fig.add_trace(go.Scatterpolar(
                r=student_weights,
                theta=all_skills,
                fill='toself',
                name="Students' Top Skills",
                line=dict(color='red', width=3),
                marker=dict(symbol='star', size=8)
            ))

            # Update layout
            max_range = max(max(industry_weights), max(student_weights)) if industry_weights or student_weights else 1
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, max_range])
                ),
                showlegend=True,
                title="Radar Chart: Skills Comparison"
            )

            # Display radar chart
            st.plotly_chart(fig)

        except Exception as e:
            st.error(f"An error occurred: {e}")


left, center, right, = st.columns([1, 1, 1.5])

with left:
    display_top_student_skills()

with center:
    st.write("## Top Industry Skills")
    industry = st.selectbox(
        "Search industry",
        ["Choose an industry"] + industry_names
    )
    display_top_industry_skills()

with right: 
    display_radar_chart()