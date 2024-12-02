import streamlit as st
import requests
from modules.nav import SideBarLinks

# Set up the page layout
st.set_page_config(layout="wide")

# Show sidebar links for the logged-in user
SideBarLinks()