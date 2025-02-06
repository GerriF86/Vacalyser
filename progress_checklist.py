import streamlit as st

# Fortschritt basierend auf ausgefüllten Feldern berechnen
def calculate_progress():
    total_keys = [
        "company_name", "industry", "location", "company_values", "company_size", "founded_year", "main_markets", 
        "department", "team_size", "work_mode", "job_title", "selected_tasks", "required_skills", "benefits",
        "interview_stages"
    ]
    filled_keys = [key for key in total_keys if st.session_state.get(key)]
    progress = int((len(filled_keys) / len(total_keys)) * 100)
    
    missing_fields = [key for key in total_keys if not st.session_state.get(key)]
    
    return progress, missing_fields

# UI für Fortschritt & Checkliste
def progress_checklist_ui():
    st.sidebar.subheader("📊 Fortschritt")
    
    progress, missing_fields = calculate_progress()
    st.sidebar.progress(progress / 100)
    st.sidebar.write(f"**{progress}% abgeschlossen**")
    
    if missing_fields:
        st.sidebar.write("🚨 **Noch auszufüllen:**")
        for field in missing_fields:
            st.sidebar.write(f"- {field.replace('_', ' ').title()}")
