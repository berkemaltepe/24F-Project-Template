# import libs
import streamlit as st
import pandas as pd
import requests

# page title
st.title("Co-op Advisor: Student List")

# Input field for Advisor ID
advisor_id = st.text_input("Enter your Advisor ID:", value="")