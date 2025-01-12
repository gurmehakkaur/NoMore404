# calculate_time.py

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
