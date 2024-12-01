# Import necessary libraries
import streamlit as st

# Set wide layout for the page
st.set_page_config(layout="wide")

# Sidebar navigation setup
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Go to:",
    ["Home", "Student List", "Skill Match Analysis", "Active Job Postings", "Manage Students"]
)

# Handle sidebar navigation
if menu == "Student List":
    st.session_state["advisor_id"] = 1  # Ensure advisor_id is set (replace 1 with dynamic ID if needed)
    st.switch_page("advisor_students.py")
elif menu == "Skill Match Analysis":
    st.switch_page("advisor_skill_match.py")
elif menu == "Active Job Postings":
    st.switch_page("advisor_job_postings.py")
elif menu == "Manage Students":
    st.switch_page("advisor_manage_students.py")

# Page title and description
st.markdown(
    """
    <div style="padding: 20px; border-radius: 10px; border: 3px solid #FF0000; background-color: #000000; text-align: center; color: white;">
        <h1 style="font-size: 40px; margin-bottom: 10px;">Welcome to the Co-op Advisor Dashboard</h1>
        <p style="font-size: 20px;">Hello, {name}! Here are your options:</p>
    </div>
    """.format(name=st.session_state.get("first_name", "Advisor")),
    unsafe_allow_html=True,
)

# Add spacing
st.write("")
st.write("")

# Style for buttons
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
            color: #000000;
        }
    </style>
"""
st.markdown(button_style, unsafe_allow_html=True)

# Buttons for navigation
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("Student List"):
        st.switch_page("advisor_students.py")
with col2:
    if st.button("Skill Match Analysis"):
        st.switch_page("advisor_skill_match.py")
with col3:
    if st.button("Active Job Postings"):
        st.switch_page("advisor_job_postings.py")
with col4:
    if st.button("Manage Students"):
        st.switch_page("advisor_manage_students.py")

# Footer for branding
st.markdown(
    """
    <hr>
    <footer style="text-align: center; margin-top: 30px; color: #777;">
        <p style="font-size: 14px;">Powered by NU SkillMatch Platform | © 2024 SkillMatch, Inc.</p>
    </footer>
    """,
    unsafe_allow_html=True,
)