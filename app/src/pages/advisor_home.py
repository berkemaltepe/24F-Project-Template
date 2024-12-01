import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# Set wide layout for the page
st.set_page_config(layout = 'wide')

# Sidebar navigation setup
SideBarLinks()

# Page title
st.title('Co-op Advisor Home Page')

# Buttons for navigation


