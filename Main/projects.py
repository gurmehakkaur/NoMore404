import streamlit as st

def projects_page():
    st.header("🛠️ Project Tracking")

    # Ensure the session state contains the "projects" list
    if "projects" not in st.session_state:
        st.session_state["projects"] = []

    total_projects = len(st.session_state["projects"])
    completed_projects = sum(p["status"] == "Complete" for p in st.session_state["projects"])
    overall_progress = (completed_projects / total_projects) * 100 if total_projects > 0 else 0

    st.write(f"### Overall Progress: {completed_projects}/{total_projects} Projects Completed")
    st.progress(overall_progress / 100)

    for project in st.session_state["projects"]:
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.subheader(project["name"])
            st.write(f"**Skills:** {', '.join(project['skills'])}")
            st.write(f"**Relevant to:** {', '.join(project['companies'])}")
        with col2:
            st.write(f"**Status:** {project['status']}")
        with col3:
            if project["status"] == "Incomplete":
                if st.button(f"Mark '{project['name']}' Complete", key=project["name"]):
                    project["status"] = "Complete"
            else:
                st.write("🎉 Completed!")
        
        # Add a description field for completed projects
        if project["status"] == "Complete":
            # Display a text area to edit the project description
            description = st.text_area(
                f"Add/Edit description for '{project['name']}':",
                value=project.get("description", ""),  # Pre-fill if a description exists
                height=100,
                key=f"description_{project['name']}"
            )

            # Save the edited description to the project
            if st.button(f"Save description for '{project['name']}'", key=f"save_{project['name']}"):
                # Update the description in the project
                project["description"] = description.strip()
                st.success(f"Description for '{project['name']}' saved successfully!")

        st.divider()
