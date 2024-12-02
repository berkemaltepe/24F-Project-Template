import logging
logger = logging.getLogger(__name__)
import requests
import streamlit as st
from modules.nav import SideBarLinks

# Set up the page layout
st.set_page_config(layout="wide")

# Show sidebar links for the logged-in user
SideBarLinks()

# Define the base API URL for advisors
BASE_URL = "http://web-api:4000/advisor"

# Ensure session state contains the necessary data
if "advisor_id" not in st.session_state:
    st.error("Advisor ID not found. Please log in as an advisor.")
    st.stop()

st.write(f"Advisor ID: {st.session_state.get('advisor_id', 'Not set')}")

# # Fetch advisor details using the stored advisor_id
# response = requests.get(f"{BASE_URL}/{st.session_state['advisor_id']}")
# if response.status_code == 200:
#     advisor_data = response.json()[0]
# else:
#     st.error(f"Error {response.status_code}: {response.text}")

advisor_id = st.session_state["advisor_id"]
advisor_name = st.session_state.get("first_name", "Advisor")

# Display the page content with a styled header
st.markdown(
    f"""
    <div style="padding: 20px; border-radius: 10px; border: 3px solid #FF0000; background-color: #000000; text-align: center; color: white;">
        <h1 style="font-size: 40px; margin-bottom: 10px;">Welcome to the Co-op Advisor Dashboard</h1>
        <p style="font-size: 20px;">Hello, {advisor_name}! What would you like to do today?</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Add spacing
st.write("")
st.write("")

# Styling for buttons
button_style = """
    <style>
        .stButton>button {
            background-color: #000000;
            color: white;
            border: 2px solid #FF0000;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease, border-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #FFFFFF;
            border-color: #FF0000;
        }
    </style>
"""
st.markdown(button_style, unsafe_allow_html=True)

# Centered buttons with spacing
st.markdown(
    """
    <div style="display: flex; flex-direction: column; align-items: center; gap: 20px; max-width: 400px; margin: 0 auto;">
    """,
    unsafe_allow_html=True,
)

# Buttons for navigation
if st.button("View Student List", use_container_width=True):
    st.switch_page("pages/advisor_students.py")
st.markdown("</div></div>", unsafe_allow_html=True)
if st.button("Skill Match Analysis", use_container_width=True):
    st.switch_page("pages/advisor_skill_match.py")
st.markdown("</div></div>", unsafe_allow_html=True)
if st.button("Active Job Postings", use_container_width=True):
    st.switch_page("pages/advisor_job_postings.py")
st.markdown("</div></div>", unsafe_allow_html=True)
if st.button("Manage Students", use_container_width=True):
    st.switch_page("pages/advisor_manage_students.py")
st.markdown("</div></div>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <hr>
    <footer style="text-align: center; margin-top: 30px; color: #777;">
        <p style="font-size: 14px;">Powered by NU SkillMatch Platform | © 2024 SkillMatch, Inc.</p>
    </footer>
    """,
    unsafe_allow_html=True,
)
