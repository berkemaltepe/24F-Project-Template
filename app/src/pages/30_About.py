import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About NU SkillMatch")

st.markdown (
    """
    NU SkillMatch is a platform that connects students with job opportunities based on their skills.
    """
        )
