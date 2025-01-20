import streamlit as st
from utils import define_recruitment_steps

def main():
    job_title = st.session_state.role_info["job_title"]
    st.header(f"Recruitment Process for {job_title}")
    # Lade vorgeschlagene Schritte
    with st.spinner("Lade vorgeschlagene Schritte..."):
        suggested_steps = define_recruitment_steps(job_title)
    if "recruitment_process" not in st.session_state:
        st.session_state.recruitment_process = suggested_steps  # Initialisiere mit den vorgeschlagenen Schritten
    if "selected_steps" not in st.session_state:
        st.session_state.selected_steps = []
    for step in st.session_state.recruitment_process:
        if st.checkbox(step, key=step):
            if step not in st.session_state.selected_steps:
                st.session_state.selected_steps.append(step)
        else:
            if step in st.session_state.selected_steps:
                st.session_state.selected_steps.remove(step)
    manual_step = st.text_input(label="Add a custom step:", placeholder="e.g., Culture fit interview")
    if manual_step:
        st.session_state.selected_steps.append(manual_step)
    if st.button("Next: Summary & Ad Generation"):
        st.session_state.page = "summary_page"
        st.rerun()

if __name__ == "__main__":
    main()