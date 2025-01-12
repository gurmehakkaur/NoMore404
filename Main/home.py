import streamlit as st
from calculate_time import calculate_time_allocation  # Assuming you have this function

def home_page():
    st.header("Welcome to Your Learning Dashboard, Gurmehak!")
    st.markdown("Use this dashboard to track your skills progress, access learning resources, and manage your projects.")

    # Remove this line to eliminate the animation
    # st_lottie(completion_animation, height=300, key="welcome_animation")

    # Display text area and pre-fill with session state
    coop_descriptions = st.text_area(
        "Copy-paste your targeted co-op descriptions",
        value="\n".join(st.session_state["user_input"]["descriptions"])
    )

    # Slider for time range
    time_range = st.slider(
        "Time Available (Months)",
        2, 12,
        value=st.session_state["user_input"]["time_range"]
    )

    # Save button to update session state
    if st.button("Save"):
        st.session_state["user_input"]["descriptions"] = (
            coop_descriptions.strip().split("\n") if coop_descriptions.strip() else []
        )
        st.session_state["user_input"]["time_range"] = time_range
        st.success("Co-op details updated successfully!")

    # Hardcoded Inputs
    months_left = time_range
    completed_resources = 4  # Example value for completed skill resources
    total_resources = 10  # Example value for total skill resources
    completed_projects = 2  # Example value for completed projects
    total_projects = 5  # Example value for total projects

    # Calculations
    time_needed_for_resources, time_needed_for_projects, daily_time_for_resources, daily_time_for_projects = calculate_time_allocation(
        months_left, completed_resources, total_resources, completed_projects, total_projects
    )

    # Outputs
    st.subheader("📈 Results")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Total time for resources:** {time_needed_for_resources} hours")
        st.info(f"**Daily time for resources:** {daily_time_for_resources:.2f} hours/day")
    with col2:
        st.info(f"**Total time for projects:** {time_needed_for_projects} hours")
        st.info(f"**Daily time for projects:** {daily_time_for_projects:.2f} hours/day")
