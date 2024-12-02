import streamlit as st
import requests
from modules.nav import SideBarLinks

# Set up the page layout
st.set_page_config(layout="wide")

# Show sidebar links for the logged-in user
SideBarLinks()

# Ensure session state contains the necessary data
if "advisor_id" not in st.session_state:
    st.error("Advisor ID not found. Please log in as an advisor.")
    st.stop()

st.write(f"Advisor ID: {st.session_state.get('advisor_id', 'Not set')}")

# Base API URL for advisor-related actions
BASE_URL = "http://web-api:4000/a"
advisor_id = st.session_state["advisor_id"]

# Page title
st.markdown(
    """
    <div style="padding: 20px; border-radius: 10px; border: 3px solid #FF0000; background-color: #000000; color: white; text-align: center;">
        <h1 style="font-size: 40px;">Manage Your Account</h1>
        <p style="font-size: 18px;">Update your account details</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Fetch advisor details
response = requests.get(f"{BASE_URL}/advisor/{advisor_id}/")
if response.status_code == 200:
    advisor_details = response.json()[0]
else:
    st.error(f"Failed to fetch advisor details. Error {response.status_code}: {response.text}")
    st.stop()

# Display advisor details in a form
with st.form("update_account_form"):
    st.subheader("Account Information")

    # Pre-fill the form with current details
    name = st.text_input("Name", value=advisor_details["name"])
    email = st.text_input("Email", value=advisor_details["email"])
    department = st.text_input("Department", value=advisor_details["department"])

    # Submit button
    submitted = st.form_submit_button("Update Account")