import streamlit as st
from utils import styled_button, define_recruitment_steps

def main():
    job_title = st.session_state.job_details["job_title"]
    st.header(f"Recruitment Process for {job_title}")

    # Lade vorgeschlagene Schritte
    with st.spinner("Lade vorgeschlagene Schritte..."):
        suggested_steps = define_recruitment_steps(job_title)

    if "recruitment_process" not in st.session_state:
        st.session_state.recruitment_process = suggested_steps

    # Vorhandene recruitment_process_steps in Checkboxen anzeigen
    for step in st.session_state.recruitment_process:
        if st.checkbox(step, key=step):
            if step not in st.session_state.selected_recruitment_steps:
                st.session_state.selected_recruitment_steps.append(step)
        else:
            if step in st.session_state.selected_recruitment_steps:
                st.session_state.selected_recruitment_steps.remove(step)

    st.session_state.job_details["current_recruitment_process"] = st.text_area("Current Recruitment Process", value=st.session_state.job_details.get("current_recruitment_process", ""))

    # Button Layout anpassen
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("Next: Benefits"):
            st.session_state.page = "benefits_page"
            st.rerun()