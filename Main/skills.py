import streamlit as st

# Function to get emoji based on progress
def get_emoji(progress):
    if progress >= 70:
        return "🚀"
    elif progress >= 50:
        return "✅"
    else:
        return "🔴"

def skills_page():
    st.header("💡 Skills Progress")
    st.markdown("Track your learning progress and access resources to master new skills.")

    # Sample skill categories and their skills
    skill_categories = {
        "Programming": ["Python", "JavaScript", "SQL", "Docker"],
        "Frontend": ["React", "CSS", "HTML"],
        "Cloud": ["AWS"]
    }

    # Sample data for skills progress (could be fetched from a database or a file)
    skills = {
        "Python": {"progress": 80, "resources": [{"name": "Python Docs", "url": "https://docs.python.org/3/", "completed": True}]},
        "JavaScript": {"progress": 60, "resources": [{"name": "JavaScript MDN", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript", "completed": False}]},
        "SQL": {"progress": 40, "resources": [{"name": "SQL Tutorial", "url": "https://www.sqltutorial.org/", "completed": False}]},
        "Docker": {"progress": 70, "resources": [{"name": "Docker Docs", "url": "https://docs.docker.com/", "completed": True}]},
        "React": {"progress": 50, "resources": [{"name": "React Docs", "url": "https://reactjs.org/docs/getting-started.html", "completed": False}]},
        "CSS": {"progress": 75, "resources": [{"name": "CSS Tricks", "url": "https://css-tricks.com/", "completed": True}]},
        "HTML": {"progress": 85, "resources": [{"name": "HTML MDN", "url": "https://developer.mozilla.org/en-US/docs/Web/HTML", "completed": True}]},
        "AWS": {"progress": 30, "resources": [{"name": "AWS Docs", "url": "https://aws.amazon.com/documentation/", "completed": False}]}
    }

    # Iterate through categories and their respective skills
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
                        {"".join([f"<li><a href='{resource['url']}' target='_blank'>{resource['name']}</a> {'✔️' if resource['completed'] else '⏳'}</li>"
                            for resource in details['resources']])}
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        st.divider()
