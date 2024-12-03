# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st

#### ------------------------ Student Navigation ------------------------
def StudentHomePageNav():
    st.sidebar.page_link("pages/Student_Home_Page.py", label="Student Home", icon="🎓")

def StudentProfileNav():
    st.sidebar.page_link("pages/Student_Profile.py", label="Student Profile", icon="📝")

def StudentSkillsNav():
    st.sidebar.page_link("pages/Student_Skills.py", label="Student Skills", icon="🧠")

def StudentJobsNav():
    st.sidebar.page_link("pages/Student_Jobs.py", label="Student Jobs", icon="💼")

#### ------------------------ Employer Navigation ------------------------

def EmpProfileNav():
    st.sidebar.page_link("pages/emp_profile.py", label="Employer Profile", icon="📝")

def EmpSkillMatchNav():
    st.sidebar.page_link("pages/emp_skill_match.py", label="SkillMatch", icon="📈")

def EditJobsNav():
    st.sidebar.page_link("pages/emp_job_creation.py", label="Edit Jobs", icon="💼")

def StudentListNav():
    st.sidebar.page_link("pages/emp_student_list.py", label="See List of Students", icon="🎓")

# --------------------------------Advisor Navigation --------------------------------

def AdvisorStudentListNav():
    st.sidebar.page_link("pages/advisor_students.py", label="My Students", icon="🎓")


def AdvisorSkillMatchNav():
    st.sidebar.page_link(
        "pages/advisor_skill_match.py", label="Skill Match Analysis", icon="📈"
    )


def AdvisorJobPostingsNav():
    st.sidebar.page_link(
        "pages/advisor_job_postings.py", label="Active Job Postings", icon="💼"
    )


def AdvisorManageNav():
    st.sidebar.page_link(
        "pages/advisor_manage.py", label="Manage Account", icon="🛠️"
    )
#### ------------------------ Department Head Navigation ---------------------------- ####

def TopSkillsNav():
    st.sidebar.page_link("pages/DH_Top_Skills_And_Tools.py", label="Top Skills", icon="💼")

def MajorReportNav():
    st.sidebar.page_link("pages/DH_Major_Pages.py", label="Major Program Reports", icon="🎓")

def SearchBySkillNav():
    st.sidebar.page_link("pages/DH_Search_By_Skill.py", label="Search by Skill", icon="🔍")

#### ------------------------ Admin Navigation ------------------------

def AdminHomeNav():
    st.sidebar.page_link("pages/Admin_Home.py", label="Admin Home", icon="🖥️")

def AdminProfileNav():
    st.sidebar.page_link("pages/Admin_Profile.py", label="Admin Profile", icon="📝")

def AdminJobsNav():
    st.sidebar.page_link("pages/Admin_All_Jobs.py", label="Jobs", icon="💼")

def AdminSkillsNav():
    st.sidebar.page_link("pages/Admin_All_Skills.py", label="Skills", icon="📚")

def AdminEmployersNav():
    st.sidebar.page_link("pages/Admin_All_Employers.py", label="Employers", icon="🏢")

def AdminFacultiesNav():
    st.sidebar.page_link("pages/Admin_All_Faculties.py", label="Faculties", icon="🏫")

def AdminAdvisorsNav():
    st.sidebar.page_link("pages/Admin_All_Advisors.py", label="Advisors", icon="💬")

def AdminStudentsNav():
    st.sidebar.page_link("pages/Admin_All_Students.py", label="Students", icon="🎓")

#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home Page", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


#### ------------------------ Examples for Role of pol_strat_advisor ------------------------
def PolStratAdvHomeNav():
    st.sidebar.page_link(
        "pages/00_Pol_Strat_Home.py", label="Political Strategist Home", icon="👤"
    )


def WorldBankVizNav():
    st.sidebar.page_link(
        "pages/01_World_Bank_Viz.py", label="World Bank Visualization", icon="🏦"
    )


def MapDemoNav():
    st.sidebar.page_link("pages/02_Map_Demo.py", label="Map Demonstration", icon="🗺️")


## ------------------------ Examples for Role of usaid_worker ------------------------
def ApiTestNav():
    st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon="🛜")


def PredictionNav():
    st.sidebar.page_link(
        "pages/11_Prediction.py", label="Regression Prediction", icon="📈"
    )


def ClassificationNav():
    st.sidebar.page_link(
        "pages/13_Classification.py", label="Classification Demo", icon="🌺"
    )

# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=True):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # If the user is a student, show the student links
        if st.session_state["role"] == "student":
            StudentHomePageNav()
            StudentProfileNav()
            StudentSkillsNav()
            StudentJobsNav()

        # If the user is an emp, show the emp links
        if st.session_state["role"] == "employer":
            EmpProfileNav()
            EmpSkillMatchNav()
            EditJobsNav()
            StudentListNav()
        
        # If the user is an advisor, show the advisor links
        if st.session_state["role"] == "advisor":
            AdvisorStudentListNav()
            AdvisorJobPostingsNav()
            AdvisorSkillMatchNav()
            AdvisorManageNav()

        # If the user is a department head, show the dept head links 
        if st.session_state["role"] == "dept_head":
            TopSkillsNav()
            MajorReportNav()
            SearchBySkillNav()
            
        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "sysadmin":
            AdminHomeNav()
            AdminProfileNav()
            AdminJobsNav()
            AdminSkillsNav()
            AdminEmployersNav()
            AdminFacultiesNav()
            AdminAdvisorsNav()
            AdminStudentsNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "usaid_worker":
            PredictionNav()
            ApiTestNav()
            ClassificationNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")

