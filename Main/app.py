import streamlit as st
import cohere
from home import home_page
from skills import skills_page
from projects import projects_page
from resume_buddy import resume_buddy_page
from mental_health_check import mental_health_check_page


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


tabs = st.tabs(["🏠 Home", "💡 Skills", "🛠️ Projects", " 🤝 Resume Buddy", "Mental Health Check"])

def main():
    st.sidebar.title("Navigation")
    
    # Create a sidebar or top menu for navigation
    page = st.sidebar.radio("Select a Page", ["Home", "Skills", "Projects", "Resume Buddy", "Mental Health Check"])

    if page == "Home":
        home_page()  # Call home_page() from home.py
    elif page == "Skills":
        skills_page()  # Call skills_page() from skills.py
    elif page == "Projects":
        projects_page()  # Call projects_page() from projects.py
    elif page == "Resume Buddy":
        resume_buddy_page()  # Call resume_buddy_page() from resume_buddy.py
    elif page == "Mental Health Check":
        mental_health_check_page()

if __name__ == "__main__":
    main()