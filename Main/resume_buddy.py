import streamlit as st

def filter_and_optimize_projects(job_description):
    # This is a placeholder for the actual filtering logic.
    # In a real-world scenario, you'd want to match skills or keywords from job_description with your projects.
    relevant_projects = []
    for project in st.session_state["projects"]:
        # Sample matching logic: match any skill in the project with the job description
        if any(skill.lower() in job_description.lower() for skill in project["skills"]):
            relevant_projects.append(project)
    return relevant_projects

def resume_buddy_page():
    st.header("Resume Buddy")
    st.write("Optimize your projects for the co-op job description!")

    # Input for job description
    job_description = st.text_area("Enter the Co-op Job Description:", height=200)
    
    # Button to find relevant projects
    if st.button("Find Relevant Projects"):
        if job_description.strip():
            filtered_projects = filter_and_optimize_projects(job_description)
            if filtered_projects:
                st.success("Here are your relevant and optimized projects!")
                for project in filtered_projects:
                    st.subheader(project["name"])
                    st.write(project["description"])
            else:
                st.warning("No relevant projects found. Try adding more skills or descriptions to your projects!")
        else:
            st.error("Please enter a job description.")
