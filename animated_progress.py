import streamlit as st
import time

# Fortschritt basierend auf ausgefüllten Feldern berechnen
def calculate_progress():
    total_keys = [
        "company_name", "industry", "location", "company_values", "team_size", "job_title", "selected_tasks",
        "required_skills", "benefits", "interview_stages"
    ]
    filled_keys = [key for key in total_keys if st.session_state.get(key)]
    return int((len(filled_keys) / len(total_keys)) * 100)

# UI für animierte Fortschrittsanzeige
def animated_progress_ui():
    st.sidebar.subheader("📊 Fortschritt")
    
    progress = calculate_progress()
    
    progress_bar = st.sidebar.progress(0)
    for i in range(progress + 1):
        time.sleep(0.01)
        progress_bar.progress(i / 100)
    
    st.sidebar.write(f"**{progress}% abgeschlossen**")
