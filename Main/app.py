import streamlit as st
import cohere

COHERE_API_KEY = 'DpwtCmXovLiCOgKae0sa1TLxcw5PoZ7aTK9D9Egk'
cohere_client = cohere.Client(COHERE_API_KEY)


st.set_page_config(page_title="NoMore404", layout="wide", page_icon="📚")

from streamlit_lottie import st_lottie
import numpy as np
import matplotlib.pyplot as plt
import requests

# Load Lottie animations
def load_lottie_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()


def calculate_time_allocation(months_left, completed_resources, total_resources, completed_projects, total_projects):
    time_per_resource = 10  # hours per resource
    time_per_project = 15  # hours per project
    days_left = months_left * 30  # Approximate days in a month


    # Calculations
    remaining_resources = total_resources - completed_resources
    remaining_projects = total_projects - completed_projects
    time_needed_for_resources = remaining_resources * time_per_resource
    time_needed_for_projects = remaining_projects * time_per_project
    daily_time_for_resources = time_needed_for_resources / days_left
    daily_time_for_projects = time_needed_for_projects / days_left


    return (time_needed_for_resources, time_needed_for_projects, daily_time_for_resources, daily_time_for_projects)

def filter_and_optimize_projects(job_description):
    relevant_projects = []
    for project in projects:
        # Check for keyword matches (basic filtering)
        if any(skill.lower() in job_description.lower() for skill in project["skills"]):
            # Optimize the project description using Cohere
            response = cohere_client.generate(
                model='command-xlarge-nightly',
                prompt=f"Job Description: {job_description}\nProject Description: {project['description']}\n"
                       f"Optimize the project description to align with the job description:",
                max_tokens=150
            )
            optimized_description = response.generations[0].text.strip()
            relevant_projects.append({
                "name": project["name"],
                "description": optimized_description
            })
    return relevant_projects


# Animations
completion_animation = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_jcikwtux.json")


# Progress Emojis
def get_emoji(progress):
    if progress == 100:
        return "🎉 Mastered!"
    elif progress >= 70:
        return "🚀 Almost There!"
    elif progress >= 50:
        return "👏 Great Progress!"
    else:
        return "💡 Keep Going!"


# Data: Skills and Projects
skills = {
    "Python": {
        "progress": 75,
        "resources": [
            {"name": "Automate the Stuff with Python", "url": "https://automatetheboringstuff.com", "completed": True},
            {"name": "Python Crash Course", "url": "https://nostarch.com/pythoncrashcourse2e", "completed": False},
            {"name": "LeetCode Practice", "url": "https://leetcode.com", "completed": False}
        ]
    },
    "React": {
        "progress": 50,
        "resources": [
            {"name": "React Docs", "url": "https://react.dev", "completed": True},
            {"name": "Scrimba React Course", "url": "https://scrimba.com", "completed": False},
            {"name": "Frontend Masters", "url": "https://frontendmasters.com", "completed": False}
        ]
    },
    "AWS": {
        "progress": 30,
        "resources": [
            {"name": "AWS Essentials", "url": "https://aws.amazon.com/training/intro_series", "completed": False},
            {"name": "AWS Free Tier Labs", "url": "https://aws.amazon.com/free", "completed": False},
            {"name": "AWS Cloud Practitioner", "url": "https://aws.amazon.com/certification/certified-cloud-practitioner", "completed": False}
        ]
    },
    "JavaScript": {
        "progress": 60,
        "resources": [
            {"name": "Eloquent JavaScript", "url": "https://eloquentjavascript.net", "completed": False},
            {"name": "MDN JavaScript Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "completed": True},
            {"name": "JavaScript 30", "url": "https://javascript30.com", "completed": False}
        ]
    },
    "HTML": {
        "progress": 80,
        "resources": [
            {"name": "MDN HTML", "url": "https://developer.mozilla.org/en-US/docs/Web/HTML", "completed": True},
            {"name": "HTML Crash Course", "url": "https://www.youtube.com/watch?v=UB1O30fR-EE", "completed": False},
            {"name": "HTML5 Rocks", "url": "https://www.html5rocks.com", "completed": True}
        ]
    },
    "CSS": {
        "progress": 65,
        "resources": [
            {"name": "CSS Tricks", "url": "https://css-tricks.com", "completed": True},
            {"name": "Flexbox Froggy", "url": "https://flexboxfroggy.com", "completed": False},
            {"name": "Grid Garden", "url": "https://cssgridgarden.com", "completed": False}
        ]
    },
    "SQL": {
        "progress": 40,
        "resources": [
            {"name": "SQL Zoo", "url": "https://sqlzoo.net", "completed": False},
            {"name": "PostgreSQL Docs", "url": "https://www.postgresql.org/docs/", "completed": True},
            {"name": "Mode Analytics SQL Tutorial", "url": "https://mode.com/sql-tutorial", "completed": False}
        ]
    },
    "Docker": {
        "progress": 20,
        "resources": [
            {"name": "Docker Hub", "url": "https://hub.docker.com", "completed": False},
            {"name": "Docker Essentials", "url": "https://docker-curriculum.com", "completed": False},
            {"name": "Docker Mastery", "url": "https://www.udemy.com/course/docker-mastery", "completed": False}
        ]
    }
}




projects = [
    {"name": "Build a Portfolio Website", "status": "Incomplete", "skills": ["React", "CSS"], "companies": ["RBC", "TD"], "description": ""},
    {"name": "Data Analysis with Pandas", "status": "Incomplete", "skills": ["Python", "Pandas"], "companies": ["Scotiabank"], "description": ""},
    {"name": "React Todo App", "status": "Complete", "skills": ["React", "JavaScript"], "companies": ["Google"], "description": ""},
]

def add_descriptions():
    """
    Allow users to add descriptions for completed projects.
    """
    for project in projects:
        if project["status"] == "Complete":
            st.subheader(project["name"])
            project["description"] = st.text_area(
                f"Enter a description for '{project['name']}' (if applicable):",
                value=project["description"],
                height=100,
            )

def filter_and_optimize_projects(job_description):
    """
    Filters projects based on their completion status and generates AI-optimized descriptions using Cohere.
    """
    relevant_projects = []
    for project in projects:
        if project["status"] == "Complete":
            # Check for keyword matches (basic filtering)
            if any(skill.lower() in job_description.lower() for skill in project["skills"]):
                # Generate an optimized description using Cohere for resume use
                response = cohere_client.generate(
                    model='command-r-plus-08-2024',
                    prompt=f"Job Description: {job_description}\n"
                           f"Skills: {', '.join(project['skills'])}\n"
                           f"Project Name: {project['name']}\n"
                           f"Technologies used: {', '.join(project['skills'])}\n"
                           f"Project Summary: {project.get('description', '')}\n"
                           f"Generate a concise, result-oriented resume description for this project, "
                           f"focusing on achievements, responsibilities, and key skills used. Use bullet points if appropriate.\n",
                    max_tokens=200
                )
                optimized_description = response.generations[0].text.strip()
                relevant_projects.append({
                    "name": project["name"],
                    "description": optimized_description
                })
    return relevant_projects




# Initialize session state
if "projects" not in st.session_state:
    st.session_state["projects"] = projects


if "user_input" not in st.session_state:
    st.session_state["user_input"] = {"descriptions": [""] * 8, "time_range": 2}


# Streamlit App Layout
st.title("📚 NoMore404")
st.markdown("### Learn all the mentioned skills and complete the pending projects to successfully land your dream co-op job!")


tabs = st.tabs(["🏠 Home", "💡 Skills", "🛠️ Projects", " 🤝 Resume Buddy"])


with tabs[0]:
    st.header("Welcome to Your Learning Dashboard, Gurmehak!")
    st.markdown("Use this dashboard to track your skills progress, access learning resources, and manage your projects.")
    st_lottie(completion_animation, height=300, key="welcome_animation")


    # Display text area and pre-fill with session state
    coop_descriptions = st.text_area(
        "Copy paste your targeted co-op descriptions",
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




# Tab 2: Skills with Enhanced UI
with tabs[1]:
    st.header("💡 Skills Progress")
    st.markdown("Track your learning progress and access resources to master new skills.")


    skill_categories = {
        "Programming": ["Python", "JavaScript", "SQL", "Docker"],
        "Frontend": ["React", "CSS", "HTML"],
        "Cloud": ["AWS"]
    }


    for category, category_skills in skill_categories.items():
        st.subheader(f"📂 {category}")
        col1, col2, col3, col4 = st.columns(4)
        columns = [col1, col2, col3, col4]
       
        for idx, skill_name in enumerate(category_skills):
            details = skills.get(skill_name, {"progress": 0, "resources": []})
            with columns[idx % 4]:
                st.markdown(
                    f"""
                    <div style="
                        background-color: #f9f9f9;
                        border-radius: 10px;
                        padding: 15px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        text-align: center;
                        margin-bottom: 15px;
                        transition: transform 0.3s;
                        hover: scale(1.02);
                    ">
                        <h4 style="margin: 0;">{skill_name}</h4>
                        <div style="
                            margin: 10px 0;
                            height: 10px;
                            background-color: #e0e0e0;
                            border-radius: 5px;
                            position: relative;">
                            <div style="
                                width: {details['progress']}%;
                                height: 100%;
                                background-color: {'#4CAF50' if details['progress'] >= 70 else '#FFC107' if details['progress'] >= 50 else '#F44336'};
                                border-radius: 5px;">
                            </div>
                        </div>
                        <p style="margin: 5px 0;">{get_emoji(details['progress'])}</p>
                        <p><strong>Resources:</strong></p>
                        <ul style="list-style-type: none; padding: 0;">
                        {"".join([
                            f"<li><a href='{resource['url']}' target='_blank'>{resource['name']}</a> {'✔️' if resource['completed'] else '⏳'}</li>"
                            for resource in details['resources']
                        ])}
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        st.divider()


# Tab 3: Projects (No changes)
with tabs[2]:
    st.header("🛠️ Project Tracking")
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



with tabs[3]:  # The fourth tab (index 3)
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
# Ensure `st.session_state` is properly initialized
if "user_input" not in st.session_state:
    st.session_state["user_input"] = {
        "descriptions": [],
        "time_range": 2
    }




