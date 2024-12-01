# import libs
import streamlit as st
import pandas as pd
import requests

# page title
st.title("Co-op Advisor: Student List")

# Input field for Advisor ID
advisor_id = st.text_input("Enter your Advisor ID:", value="")

# Fetch students only if an Advisor ID is provided
if advisor_id:
    try:
        # Make API request to fetch students for the provided advisor ID
        response = requests.get(f"http://localhost:4000/advisor/{advisor_id}/students")
        
        if response.status_code == 200:
            # Display students in a table
            students = pd.DataFrame(response.json())
            st.dataframe(students)
        else:
            st.error("Failed to fetch students. Please check the Advisor ID.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please enter your Advisor ID to see the student list.")