##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.markdown(
                    f"""
                    <div style="padding: 20px; border-radius: 10px; border: 3px solid #FF0000; background-color: #000000; margin-bottom: 20px;">
                        <h2 style="text-align: center; color: #FFFFFF;"> <strong>Welcome to NU SkillMatch 👋</h2>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
st.write('\n\n')
st.write('## Select a user: ')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

if st.button("Act as Jane, a Student", 
            type = 'primary', 
            use_container_width=True):
    # when user clicks the button, they are now considered authenticated
    st.session_state['authenticated'] = True
    # we set the role of the current user
    st.session_state['role'] = 'student'
    # we add the first name of the user (so it can be displayed on 
    # subsequent pages). 
    st.session_state['first_name'] = 'Jane'
    # add student id to session state
    st.session_state['student_id'] = 1
    # finally, we ask streamlit to switch to another page, in this case, the 
    # landing page for this particular user type
    logger.info("Logging in as Student Persona")
    st.switch_page('pages/Student_Home_Page.py')

if st.button("Act as John, a Student", 
            type = 'primary', 
            use_container_width=True):
    # when user clicks the button, they are now considered authenticated
    st.session_state['authenticated'] = True
    # we set the role of the current user
    st.session_state['role'] = 'student'
    # we add the first name of the user (so it can be displayed on 
    # subsequent pages). 
    st.session_state['first_name'] = 'John'
    # add student id to session state
    st.session_state['student_id'] = 2
    # finally, we ask streamlit to switch to another page, in this case, the 
    # landing page for this particular user type
    logger.info("Logging in as Student Persona")
    # CHANGE TO STUDENT HOME PAGE (make a new page or something like that)
    st.switch_page('pages/Student_Home_Page.py')

# (Nick) currently working on pls don't change
if st.button('Act as Nick, an Employer at Tech Corp', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'employer'
    st.session_state['first_name'] = 'Nick'
    st.session_state['emp_id'] = 1
    st.switch_page('pages/Emp_Home_Page.py')

if st.button('Act as Steven, an Employer at EduWorld', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'employer'
    st.session_state['first_name'] = 'Steven'
    st.session_state['emp_id'] = 2
    st.switch_page('pages/Emp_Home_Page.py')

if st.button('Act as Yuta, Co-Op Advisor', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'advisor'
    st.session_state['first_name'] = 'Yuta'
    st.session_state['advisor_id'] = 1
    st.switch_page('pages/advisor_home.py')

if st.button("Act as Lea, the Head of Khoury College of CS", 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'dept_head'
    st.session_state['first_name'] = 'Lea'
    st.session_state['faculty_id'] = '1'

    logger.info("Logging in as Khoury Dept. Head")
    # CHANGE TO DEPT HEAD HOME PAGE (make a new page or something like that)
    st.switch_page('pages/Dept_Head_Home.py')

if st.button("Act as Alice, the System Admin", 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'sysadmin'
    st.session_state['first_name'] = 'Alice'
    logger.info("Logging in as System Admin")
    st.switch_page('pages/Admin_Home.py')



