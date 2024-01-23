import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import json
import os

#A list of time intervals from 00:00 to 23:45 with 15 minute delta
def time_list():
    start_time = datetime.strptime('00:00', '%H:%M')
    end_time = datetime.strptime('23:45', '%H:%M')
    time_list = []
    while start_time <= end_time:
        time_list.append(start_time.time().strftime('%H:%M'))
        start_time += timedelta(minutes=15)
    return time_list

# Main Page
if "__main__" == __name__:
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
    if os.path.exists('toDo.json') and os.path.getsize('toDo.json') > 0:
        with open('toDo.json', 'r') as f:
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
        with open('toDo.json', 'w') as f:
            json.dump(days_and_tasks, f)

    # Add Task
    addTask = st.sidebar.text_input("Add Task")


    startTime = st.sidebar.selectbox("Task begins at:", time_list()[0:-1])
    endTime = st.sidebar.selectbox("Task ends at:", time_list()[time_list().index(startTime)+1:])

    if st.sidebar.button("Add"):
        days_and_tasks[currentDay].append([startTime,endTime,addTask,"Incomplete 🙀"])
        st.sidebar.success("Added Task 😺")
        with open('toDo.json', 'w') as f:
            json.dump(days_and_tasks, f)

    

    # Remove Task
    removeTask = st.sidebar.selectbox("Remove Task/Change Status", [i[2] for i in days_and_tasks[currentDay]])
    if st.sidebar.button("Remove"):
        for task in days_and_tasks[currentDay]:
            if removeTask == task[2]:
                days_and_tasks[currentDay].remove(task)
                st.sidebar.success("Removed Task 😺")
        with open('toDo.json', 'w') as f:
            json.dump(days_and_tasks, f)

    # Change Status
    #changeStatus = st.sidebar.selectbox("Change Status", [i[2] for i in days_and_tasks[currentDay]])
    if st.sidebar.button("Complete"):
        for task in days_and_tasks[currentDay]:
            if removeTask == task[2]:
                task[3] = "Complete 😽"
                st.sidebar.success("Changed Status 😺")
        with open('toDo.json', 'w') as f:
            json.dump(days_and_tasks, f)
    

    
    #Clear All Tasks for the Week
    if st.sidebar.button("Clear Tasks for the Week"):
        for day in days_and_tasks:
            days_and_tasks[day] = []
        st.sidebar.success("Cleared All Tasks for the Week 😺")
        with open('toDo.json', 'w') as f:
            json.dump(days_and_tasks, f)
    
    # Display Table    
    current_day_table = pd.DataFrame(days_and_tasks[currentDay], columns=["Start Time", "End Time", "Task", "Status"])
    current_day_table = current_day_table.sort_values(by=["Start Time", "End Time"])
    st.table(current_day_table)

