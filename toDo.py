import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import json
import os
import base64

#A list of time intervals from 00:00 to 23:45 with 15 minute delta
def time_list():
    start_time = datetime.strptime('00:00', '%H:%M')
    end_time = datetime.strptime('23:45', '%H:%M')
    time_list = []
    while start_time <= end_time:
        time_list.append(start_time.time().strftime('%H:%M'))
        start_time += timedelta(minutes=15)
    return time_list


#Function to change the background of the sidebar
def sidebar_bg(side_bg):

   side_bg_ext = 'gif'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )

#Function to change the background of the main page
def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.
 
    Returns
    -------
    The background.
    '''
    
    main_bg_ext = "png"     # set bg name
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover;
             background-repeat: no-repeat;
             background-attachment: fixed;         }}
         </style>
         """,
         unsafe_allow_html=True
     )

# Main Page
if "__main__" == __name__:

    #Wide mode
    st.set_page_config(layout="wide")
    
    #username = st.sidebar.text_input("Username")
    #password = st.sidebar.text_input("Password", type='password')   
    if 'username' in st.session_state and 'password' in st.session_state:
        # The rest of your code goes here
        pass
    else:
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type='password')
        
        if username and password:
            st.session_state.username = username
            st.session_state.password = password   

    filename = f"{username}_{password}.json"
    

    # Title
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
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as f:
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
        with open(filename, 'w') as f:
            json.dump(days_and_tasks, f)

    # Add Task
    addTask = st.sidebar.text_input("Add Task")

    startTime = st.sidebar.selectbox("Task begins at:", time_list()[0:-1])
    endTime = st.sidebar.selectbox("Task ends at:", time_list()[time_list().index(startTime)+1:])

    if st.sidebar.button("Add"):
        days_and_tasks[currentDay].append([startTime,endTime,addTask,"Incomplete 🙀"])
        st.sidebar.success("Added Task 😺")
        with open(filename, 'w') as f:
            json.dump(days_and_tasks, f)

    # Remove Task
    removeTask = st.sidebar.selectbox("Remove Task/Change Status", [i[2] for i in days_and_tasks[currentDay]])
    if st.sidebar.button("Remove"):
        for task in days_and_tasks[currentDay]:
            if removeTask == task[2]:
                days_and_tasks[currentDay].remove(task)
                st.sidebar.success("Removed Task 😺")
        with open(filename, 'w') as f:
            json.dump(days_and_tasks, f)

    # Change Status
    if st.sidebar.button("Complete"):
        for task in days_and_tasks[currentDay]:
            if removeTask == task[2]:
                task[3] = "Complete 😽"
                st.sidebar.success("Changed Status 😺")
        with open(filename, 'w') as f:
            json.dump(days_and_tasks, f)
    
    #Clear All Tasks for the Week
    if st.sidebar.button("Clear Tasks for the Week"):
        for day in days_and_tasks:
            days_and_tasks[day] = []
        st.sidebar.success("Cleared All Tasks for the Week 😺")
        with open(filename, 'w') as f:
            json.dump(days_and_tasks, f)
    
    # Display Table    
    current_day_table = pd.DataFrame(days_and_tasks[currentDay], columns=["Start Time", "End Time", "Task", "Status"])
    current_day_table = current_day_table.sort_values(by=["Start Time", "End Time"])
    
    current_day_table = current_day_table.reset_index(drop=True)
    if (days_and_tasks[currentDay] == []):
        st.markdown("<h1 style='text-align: center;'>No Tasks for the Day 😿</h1>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align: center;'>🗒️Your To-Do List🗒️</h1>", unsafe_allow_html=True)
        st.table(current_day_table)