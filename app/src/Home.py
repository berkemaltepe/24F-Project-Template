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
st.title('Welcome to NU SkillMatch')
st.write('\n\n')
st.write('## Select a user: ')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

if st.button("Act as Berke, a Student", 
            type = 'primary', 
            use_container_width=True):
    # when user clicks the button, they are now considered authenticated
    st.session_state['authenticated'] = True
    # we set the role of the current user
    st.session_state['role'] = 'student'
    # we add the first name of the user (so it can be displayed on 
    # subsequent pages). 
    st.session_state['first_name'] = 'Berke'
    # finally, we ask streamlit to switch to another page, in this case, the 
    # landing page for this particular user type
    logger.info("Logging in as Student Persona")
    # CHANGE TO STUDENT HOME PAGE (make a new page or something like that)
    st.switch_page('pages/00_Pol_Strat_Home.py')

# (Nick) currently working on pls don't change
if st.button('Act as Nick, an Employer', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'employer'
    st.session_state['first_name'] = 'Nick'
    st.switch_page('pages/Emp_Home_Page.py')

if st.button('Act as Yuta, Co-Op Advisor', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'advisor'
    st.session_state['first_name'] = 'Yuta'
    # CHANGE TO ADVISOR HOME PAGE (make a new page or something like that)
    st.switch_page('pages/20_Admin_Home.py')

if st.button("Act as Lea, the Head of Khoury College of CS", 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'dept_head'
    st.session_state['first_name'] = 'Lea'
    logger.info("Logging in as Khoury Dept. Head")
    # CHANGE TO DEPT HEAD HOME PAGE (make a new page or something like that)
    st.switch_page('pages/00_Pol_Strat_Home.py')

if st.button("Act as Colin, the System Admin", 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'sysadmin'
    st.session_state['first_name'] = 'Colin'
    logger.info("Logging in as System Admin")
    # CHANGE TO SYS ADMIN HOME PAGE (make a new page or something like that)
    st.switch_page('pages/00_Pol_Strat_Home.py')



