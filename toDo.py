import streamlit as st
from datetime import datetime, timedelta
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

    days_and_tasks = {"Monday": st.session_state.monday_list,
                       "Tuesday": st.session_state.tuesday_list,
                         "Wednesday": st.session_state.wednesday_list,
                           "Thursday": st.session_state.thursday_list,
                             "Friday": st.session_state.friday_list,
                               "Saturday": st.session_state.saturday_list,
                                 "Sunday": st.session_state.sunday_list}
    # Add Task
    addTask = st.sidebar.text_input("Add Task")
    startTime = st.sidebar.selectbox("Task begins at:", time_list()[0:-1])
    endTime = st.sidebar.selectbox("Task ends at:", time_list()[time_list().index(startTime)+1:])
    if st.sidebar.button("Add"):
        days_and_tasks[currentDay].append([startTime,endTime,addTask])
        st.sidebar.success("Added Task")
    for i in days_and_tasks[currentDay]:
        st.markdown(f"##### {i[0]} -> {i[1]} : {i[2]}")

    # Remove Task
    removeTask = st.sidebar.selectbox("Remove Task", [i[2] for i in days_and_tasks[currentDay]])
    if st.sidebar.button("Remove"):
        for task in days_and_tasks[currentDay]:
            if removeTask == task[2]:
                days_and_tasks[currentDay].remove(task)
                st.sidebar.success("Removed Task")
