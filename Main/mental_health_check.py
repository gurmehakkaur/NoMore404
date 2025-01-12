import streamlit as st
from datetime import date, timedelta
import calendar
import json
import os
import requests

# File to store user check-in data
DATA_FILE = "checkin_data.json"

# Load or initialize data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Save data to the JSON file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Function to fetch the quote of the day
def fetch_quote():
    try:
        response = requests.get("https://zenquotes.io/api/today")
        if response.status_code == 200:
            quote = response.json()[0]['q']
            author = response.json()[0]['a']
            return f'"{quote}" - {author}'
        else:
            return "Unable to fetch quote. Please try again later."
    except Exception as e:
        return f"Error fetching quote: {e}"

# Generate a calendar with checkmarks for completed dates
def generate_calendar(data, selected_month, selected_year):
    cal = calendar.Calendar()
    month_days = list(cal.itermonthdays(selected_year, selected_month))
    today = date.today()
    month_data = data.get(f"{selected_year}-{selected_month}", {})

    st.subheader(f"{calendar.month_name[selected_month]} {selected_year}")

    # Arrange days into rows (weeks)
    rows = []
    week = []
    for day in month_days:
        if day == 0:  # Empty placeholder for days not in the month
            week.append(None)
        else:
            week.append(date(selected_year, selected_month, day))
        if len(week) == 7:
            rows.append(week)
            week = []
    if week:  # Add the remaining days in the last week
        rows.append(week)

    # Render the calendar
    selected_date = None
    st.markdown("<style>.completed {background-color: #d4edda; border-radius: 50%; color: black;}</style>", unsafe_allow_html=True)
    for week in rows:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day is None:
                cols[i].empty()  # Empty cell for placeholders
            else:
                key = str(day)
                if month_data.get(key, False):
                    # Render date with green background
                    cols[i].markdown(
                        f"<div class='completed' style='text-align: center;'><strong>{day.day}</strong></div>",
                        unsafe_allow_html=True,
                    )
                else:
                    # Render the plain date as clickable
                    if cols[i].button(f"{day.day}", key=f"day_{key}"):
                        selected_date = day
    return selected_date

# Main Streamlit app
def mental_health_check_page():
    st.title("Developer Daily Check-In")
    st.sidebar.header("Monthly Overview")

    # Load user data
    data = load_data()

    # Get today's date and current month
    today = date.today()
    selected_year = today.year
    selected_month = today.month

    # Select month and year for calendar view
    selected_month = st.sidebar.selectbox("Select Month", list(range(1, 13)), index=today.month - 1)
    selected_year = st.sidebar.number_input("Year", value=today.year, min_value=2000, max_value=2100)

    # Generate the calendar and get the selected date
    selected_date = generate_calendar(data, selected_month, selected_year)

    if selected_date:
        # Check-in form
        st.header(f"Check-In for {selected_date}")
        with st.form(f"checkin_form_{selected_date}"):
            st.markdown("**Friendly reminder:** Take 5-minute breaks every 20 minutes to recharge your mind!")
            
            # Existing questions
            coding_status = st.radio("How's your coding going today?", ["Great", "Okay", "Challenging"], index=1)
            happiness = st.radio("How are you feeling today?", ["Happy", "Sad", "Mad"], index=0)
            description = st.text_area("Describe your day", placeholder="Write about your coding journey!")
            jobs_applied = st.number_input("How many jobs have you applied for today?", min_value=0, step=1)
            
            # New questions
            leetcode_count = st.number_input("How many LeetCode questions did you complete today?", min_value=0, step=1)
            breaks_taken = st.radio("Did you take any breaks today?", ["Yes", "No", "Planning to"], index=0)
            hobbies = st.multiselect(
                "What kind of hobbies did you focus on today?",
                ["Reading", "Music", "Gaming", "Exercise", "Art", "Meditation", "Other"]
            )
            daily_accomplishment = st.text_area("What was one thing you accomplished today that you're proud of?")
            gratitude = st.text_area("What is one thing you're grateful for today?")
            positive_thought = st.text_area("Take a moment to think about one thing you enjoyed today and write it here:")
            tomorrow_focus = st.text_area("What's one thing you're looking forward to tomorrow?")

            # Submit button
            submitted = st.form_submit_button("Submit")
            if submitted:
                # Save the check-in data
                key = str(selected_date)
                month_key = f"{selected_year}-{selected_month}"
                if month_key not in data:
                    data[month_key] = {}
                data[month_key][key] = {
                    "coding_status": coding_status,
                    "happiness": happiness,
                    "description": description,
                    "jobs_applied": jobs_applied,
                    "leetcode_count": leetcode_count,
                    "breaks_taken": breaks_taken,
                    "hobbies": hobbies,
                    "daily_accomplishment": daily_accomplishment,
                    "gratitude": gratitude,
                    "positive_thought": positive_thought,
                    "tomorrow_focus": tomorrow_focus,
                }
                save_data(data)
                st.success(f"Check-in for {selected_date} saved successfully!")
                # Refresh the calendar immediately after submission
                selected_date = generate_calendar(data, selected_month, selected_year)

    # Display quote of the day
    st.header("Quote of the Day")
    quote = fetch_quote()
    st.info(quote)

if __name__ == "__main__":
    main()
