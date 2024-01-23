import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import json
import os
import requests



#A list of time intervals from 00:00 to 23:45 with 15 minute delta
def time_list():
    start_time = datetime.strptime('00:00', '%H:%M')
    end_time = datetime.strptime('23:45', '%H:%M')
    time_list = []
    while start_time <= end_time:
        time_list.append(start_time.time().strftime('%H:%M'))
        start_time += timedelta(minutes=15)
    return time_list
ip_address = requests.get('https://api.ipify.org').text
unique_json_file = f'{ip_address}_unique_json_file'


# Main Page
if "__main__" == __name__:

    #Wide mode
    st.set_page_config(layout="wide")

    # Title
    st.title("Your To-Do List :spiral_note_pad:")

    #Days of the week
    currentDay = st.sidebar.selectbox("Select Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    
    if 'init' not in st.session_state:
        st.session_state.init = True
        st.session_state.monday_list = []
        st.session_state.tuesday_list = []
        st.session_state.wednesday_list = []
        st.session_state.thursday_list = []
        st.session_state.friday_list = []
        st.session_state.saturday_list = []
        st.session_state.sunday_list = []
    
    
    #Load Tasks from JSON
    if os.path.exists('unique_json_file') and os.path.getsize('unique_json_file') > 0:
        with open('unique_json_file', 'r') as f:
            days_and_tasks = json.load(f)
    else:
        days_and_tasks = {"Monday": st.session_state.monday_list,
                            "Tuesday": st.session_state.tuesday_list,
                            "Wednesday": st.session_state.wednesday_list,
                            "Thursday": st.session_state.thursday_list,
                            "Friday": st.session_state.friday_list,
                            "Saturday": st.session_state.saturday_list,
                            "Sunday": st.session_state.sunday_list}
    
    #Clear All Tasks for the Day
    if st.sidebar.button("Clear Tasks for the Day"):
        days_and_tasks[currentDay] = []
        st.sidebar.success(f"Cleared All Tasks for {currentDay} 😺")
        with open('unique_json_file', 'w') as f:
            json.dump(days_and_tasks, f)

    # Add Task
    addTask = st.sidebar.text_input("Add Task")


    startTime = st.sidebar.selectbox("Task begins at:", time_list()[0:-1])
    endTime = st.sidebar.selectbox("Task ends at:", time_list()[time_list().index(startTime)+1:])

    if st.sidebar.button("Add"):
        days_and_tasks[currentDay].append([startTime,endTime,addTask,"Incomplete 🙀"])
        st.sidebar.success("Added Task 😺")
        with open('unique_json_file', 'w') as f:
            json.dump(days_and_tasks, f)

    

    # Remove Task
    removeTask = st.sidebar.selectbox("Remove Task/Change Status", [i[2] for i in days_and_tasks[currentDay]])
    if st.sidebar.button("Remove"):
        for task in days_and_tasks[currentDay]:
            if removeTask == task[2]:
                days_and_tasks[currentDay].remove(task)
                st.sidebar.success("Removed Task 😺")
        with open('unique_json_file', 'w') as f:
            json.dump(days_and_tasks, f)

    # Change Status
    if st.sidebar.button("Complete"):
        for task in days_and_tasks[currentDay]:
            if removeTask == task[2]:
                task[3] = "Complete 😽"
                st.sidebar.success("Changed Status 😺")
        with open('unique_json_file', 'w') as f:
            json.dump(days_and_tasks, f)
    

    
    #Clear All Tasks for the Week
    if st.sidebar.button("Clear Tasks for the Week"):
        for day in days_and_tasks:
            days_and_tasks[day] = []
        st.sidebar.success("Cleared All Tasks for the Week 😺")
        with open('unique_json_file', 'w') as f:
            json.dump(days_and_tasks, f)
    
    # Display Table    
    current_day_table = pd.DataFrame(days_and_tasks[currentDay], columns=["Start Time", "End Time", "Task", "Status"])
    current_day_table = current_day_table.sort_values(by=["Start Time", "End Time"])
    st.table(current_day_table)

