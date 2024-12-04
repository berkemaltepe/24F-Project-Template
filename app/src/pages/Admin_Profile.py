import logging
logger = logging.getLogger(__name__)
import requests
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

URL = "http://web-api:4000/system_admin/1"

def get_admin():
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            return response.json()[0]
        else:
            st.error(f"Failed to fetch admins: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while fetching admins: {e}")
        return None

admin = get_admin()

def display_info():
    st.title(f"{admin['name']}'s Employer Profile")
    st.markdown(
        f'''
        <small>
           ID Number
         </small>
        <div style="background-color:whitesmoke; padding:10px; border-radius: 5px;">
           {admin['admin_id']}
        </div>
        <span style="display: block; margin-bottom: 10px;"></span>
        <small> 
            Name
        </small>
        <div style="background-color:whitesmoke; padding:10px; border-radius: 5px; height:40px">
            {admin['name']}
        </div>
        <span style="display: block; margin-bottom: 10px;"></span>
        <small> 
            Email
        </small>
        <div style="background-color:whitesmoke; padding:10px; border-radius: 5px;">
            {admin['email']}
        </div>
        <span style="display: block; margin-bottom: 10px;"></span>
        <small> 
            Industry
        </small>
        <div style="background-color:whitesmoke; padding:10px; border-radius: 5px;">
            {admin['industry']}
        </div>
        <span style="display: block; margin-bottom: 10px;"></span>
        <small> 
            Number of Applications
        </small>
        <div style="background-color:whitesmoke; padding:10px; border-radius: 5px;">
            {admin['num_applications']}
        </div>
        ''',
        unsafe_allow_html=True
    )

# Display the profile or the form based on the session state
if "edit" not in st.session_state:
    st.session_state["edit"] = False

if st.session_state["edit"]:
    st.title("Edit Employer Profile")
    name = st.text_input("Name", value=f"{admin['name']}")
    email = st.text_input("Email", value=f"{admin['email']}")
    industry = st.text_input("Industry", value=f"{admin['industry']}")
    num_apps = st.number_input("Number of Applications", min_value=0, value=admin['num_applications'], step=1)
    
    if st.button("Save Changes"):
        admin_data = {"name": name, "email": email, "industry": industry, "num_applications": num_apps}
        try:
            response = requests.put(f"{URL}", json=admin_data)
            if response.status_code == 200:
                st.session_state["update_success"] = f"Successfully updated admin {name}."
                st.session_state["edit"] = False
                st.rerun()
            else:
                st.error(f"Failed to update admin: {response.text}")
        except Exception as e:
            st.error(f"Error occurred while update admin: {e}")
    
    if st.button("Cancel"):
        st.session_state["edit"] = False
        st.rerun()

else:
    # Display the admin info
    display_info()
    st.write('')
    if st.button("Edit"):
        st.session_state["edit"] = True
        st.rerun()
    if "update_success" in st.session_state:
        st.success(st.session_state["update_success"])
        del st.session_state["update_success"]
