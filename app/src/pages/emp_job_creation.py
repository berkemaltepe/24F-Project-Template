import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

# Display the appropriate sidebar links for the role of the logged-in user
SideBarLinks()

BASE_URL = "http://web-api:4000/employer"

try:
    # Fetch employer info
    response = requests.get(f"{BASE_URL}/employer/{st.session_state['emp_id']}")
    if response.status_code == 200:
        emp = response.json()[0]

    employer_id = st.session_state['emp_id']

    if employer_id:
        # Fetch jobs for the employer
        jobs_response = requests.get(f"{BASE_URL}/employers/{employer_id}/jobs")
        if jobs_response.status_code == 200:
            jobs = jobs_response.json()
            if jobs:
                st.markdown(
                    f"""
                    <div style="padding: 20px; border-radius: 10px; border: 3px solid #FF0000; background-color: #000000; margin-bottom: 20px;">
                        <h2 style="text-align: center; color: #FFFFFF;"> <strong>{emp['name']}</strong> Job Listings and Edit Options</h2>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Display each job in an expandable section
                for job in jobs:
                    job_id = job['job_id']
                    with st.expander(f"Edit Job: {job['title']} (Job ID: {job_id})", expanded=False):
                        # Fetch job details
                        job_details_response = requests.get(f"{BASE_URL}/jobs/{job_id}")
                        if job_details_response.status_code == 200:
                            job_details = job_details_response.json()[0]  # Assuming single object in list

                            # Editable fields for job details
                            new_title = st.text_input("Job Title", value=job_details['title'], key=f"title_{job_id}")
                            new_description = st.text_area("Job Description", value=job_details['description'], key=f"description_{job_id}")
                            new_location = st.text_input("Location", value=job_details['location'], key=f"location_{job_id}")
                            new_pay_range = st.text_input("Pay Range", value=job_details['pay_range'], key=f"pay_{job_id}")
                            new_status = st.selectbox(
                                "Status", 
                                options=["Open", "Closed"], 
                                index=0 if job_details['status'] == "Open" else 1, 
                                key=f"status_{job_id}"
                            )

                            # Editable skills for the job
                            st.markdown("### Required Skills")
                            skills_response = requests.get(f"{BASE_URL}/jobs/{job_id}/skills")
                            if skills_response.status_code == 200:
                                skills = skills_response.json()
                                all_skills_response = requests.get(f"{BASE_URL}/skills")
                                if all_skills_response.status_code == 200:
                                    all_skills = all_skills_response.json()
                                    skill_options = {skill['skill_name']: skill['skill_id'] for skill in all_skills}

                                    skill_updates = []
                                    new_skills_to_add = []
                                    skills_to_remove = []

                                    # Display current skills with options to update or delete
                                    st.markdown("#### Current Skills")
                                    for skill in skills:
                                        col1, col2, col3 = st.columns([4, 2, 1])
                                        with col1:
                                            selected_skill = st.selectbox(
                                                f"Skill ({skill['skill_name']})", 
                                                options=list(skill_options.keys()),
                                                index=list(skill_options.keys()).index(skill['skill_name']),
                                                key=f"select_skill_{skill['skill_id']}_{job_id}"
                                            )
                                            selected_skill_id = skill_options[selected_skill]
                                        with col2:
                                            weight = st.number_input(
                                                f"Weight for {selected_skill}", 
                                                value=skill['weight'], 
                                                step=1, 
                                                key=f"skill_weight_{skill['skill_id']}_{job_id}"
                                            )
                                        with col3:
                                            remove = st.checkbox(
                                                "Remove", 
                                                key=f"remove_skill_{skill['skill_id']}_{job_id}"
                                            )
                                            if remove:
                                                skills_to_remove.append(skill['skill_id'])

                                        skill_updates.append({"skill_id": selected_skill_id, "weight": weight, "job_id": job_id})

                                    # Option to add new skills
                                    # Add New Skills Section
                                    st.markdown("#### Add New Skills")
                                    col1, col2 = st.columns([4, 2])
                                    with col1:
                                        new_skill_name = st.selectbox(
                                            "Select a New Skill to Add", 
                                            options=list(skill_options.keys()),
                                            key=f"add_new_skill_{job_id}"
                                        )
                                        new_skill_id = skill_options[new_skill_name]
                                    with col2:
                                        new_skill_weight = st.number_input(
                                            "Weight", 
                                            min_value=1, 
                                            step=1, 
                                            key=f"add_new_skill_weight_{job_id}"
                                        )

                                    # Ensure button triggers correct POST request WHY ISN'T THIS WORKING (EDIT: i fixed it >:))
                                    if st.button(f"Add New Skill to Job ID {job_id}", key=f"add_skill_btn_{job_id}"):
                                        try:
                                            # Ensure payload matches route expectations
                                            payload = {"skill_id": new_skill_id, "weight": new_skill_weight}
                                            add_skill_response = requests.post(
                                                f"{BASE_URL}/jobs/{job_id}/skills",
                                                json=payload
                                            )
                                            if add_skill_response.status_code == 200:
                                                st.success(f"Skill '{new_skill_name}' added successfully!")
                                            else:
                                                st.error(f"Failed to add skill '{new_skill_name}': {add_skill_response.json()['error']}")
                                        except Exception as e:
                                            st.error(f"An error occurred while adding skill '{new_skill_name}': {e}")


                                    # Save all changes together
                                    if st.button(f"Save Changes for Job ID {job_id}", key=f"save_all_{job_id}"):
                                        try:
                                            # Update job details
                                            job_update_payload = {
                                                "title": new_title,
                                                "description": new_description,
                                                "location": new_location,
                                                "pay_range": new_pay_range,
                                                "status": new_status,
                                            }
                                            job_update_response = requests.put(f"{BASE_URL}/jobs/{job_id}", json=job_update_payload)
                                            if job_update_response.status_code != 200:
                                                st.error(f"Failed to update job details for Job ID {job_id}: {job_update_response.text}")
                                            # Update existing skills
                                            for skill_update in skill_updates:
                                                skill_update_response = requests.put(
                                                    f"{BASE_URL}/jobs/{job_id}/skills/{skill_update['skill_id']}",
                                                    json={"weight": skill_update['weight']}
                                                )
                                                if skill_update_response.status_code != 200:
                                                    st.error(f"Failed to update skill '{skill_update['skill_id']}': {skill_update_response.text}")

                                            # Add new skills
                                            for new_skill in new_skills_to_add:
                                                add_skill_response = requests.post(
                                                    f"{BASE_URL}/jobs/{job_id}/skills",
                                                    json=new_skill
                                                )
                                                if add_skill_response.status_code != 200:
                                                    st.error(f"Failed to add skill '{new_skill['skill_id']}': {add_skill_response.text}")

                                            # Remove skills
                                            for skill_id in skills_to_remove:
                                                remove_skill_response = requests.delete(
                                                    f"{BASE_URL}/jobs/{job_id}/skills/{skill_id}"
                                                )
                                                if remove_skill_response.status_code != 200:
                                                    st.error(f"Failed to remove skill ID '{skill_id}': {remove_skill_response.text}")

                                            st.success(f"All changes for Job ID {job_id} saved successfully!")
                                        except Exception as e:
                                            st.error(f"An error occurred while saving changes for Job ID {job_id}: {e}")
                                else:
                                    st.warning("Failed to fetch all available skills.")
                            else:
                                st.warning("No skills listed for this job.")



                            # Delete job button
                            if st.button(f"Delete Job ID {job_id}", key=f"delete_{job_id}"):
                                try:
                                    delete_response = requests.delete(f"{BASE_URL}/jobs/{job_id}")
                                    if delete_response.status_code == 200:
                                        st.success(f"Job ID {job_id} deleted successfully!")
                                    else:
                                        st.error(f"Failed to delete Job ID {job_id}: {delete_response.text}")
                                except Exception as e:
                                    st.error(f"An error occurred while deleting Job ID {job_id}: {e}")

            # Add a new job 
            st.markdown("### Add a New Job")
            with st.form(key="add_job_form"):
                title = st.text_input("Job Title")
                description = st.text_area("Job Description")
                location = st.text_input("Location")
                pay_range = st.text_input("Pay Range")
                status = st.selectbox("Status", options=["Open", "Closed"])
                submit_button = st.form_submit_button(label="Add Job")
                industry = emp['industry']

                if submit_button:
                    try:
                        add_job_payload = {
                            "title": title,
                            "description": description,
                            "location": location,
                            "pay_range": pay_range,
                            "status": status,
                            "emp_id": employer_id,
                            "industry": industry
                        }
                        add_response = requests.post(f"{BASE_URL}/jobs", json=add_job_payload)
                        if add_response.status_code == 200:
                            st.success("Job added successfully!")
                        else:
                            st.error(f"Failed to add job: {add_response.text}")
                    except Exception as e:
                        st.error(f"An error occurred while adding the job: {e}")
        else:
            st.error("Failed to fetch jobs for the employer.")
except Exception as e:
    st.error(f"An error occurred: {e}")
