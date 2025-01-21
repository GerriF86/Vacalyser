import streamlit as st
from utils import *

def main():
    job_title = st.session_state.job_details["job_title"]
    st.header(f"Tasks for {job_title}")

    if "task_frequencies" not in st.session_state:
        st.session_state.task_frequencies = {}

    # Stelle sicher, dass st.session_state.tasks initialisiert ist
    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    for task in st.session_state.tasks:
        col1, col2 = st.columns([2, 1])

        with col1:
            if st.checkbox(task, key=f"{task}_checkbox"):
                if task not in st.session_state.selected_tasks:
                    st.session_state.selected_tasks.append(task)

                    if task not in st.session_state.task_frequencies:
                        st.session_state.task_frequencies[task] = "Often"
            else:
                if task in st.session_state.selected_tasks:
                    st.session_state.selected_tasks.remove(task)
                    if task in st.session_state.task_frequencies:
                        del st.session_state.task_frequencies[task]

        with col2:
            if task in st.session_state.selected_tasks:
                frequency = st.selectbox(
                    label=f"Frequency of {task}",
                    options=["Often", "Occasionally", "Rarely"],
                    index=["Often", "Occasionally", "Rarely"].index(st.session_state.task_frequencies.get(task, "Often")),
                    key=f"{task}_frequency"
                )
                st.session_state.task_frequencies[task] = frequency

    manual_task = st.text_input(label="Add a custom task:", placeholder="e.g., Organize team events")
    if manual_task:
        st.session_state.selected_tasks.append(manual_task)
        st.session_state.task_frequencies[manual_task] = "Often"  # Standardmäßig auf "Often" setzen

    # Button Layout anpassen
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("Next: Recruitment Process"):
            st.session_state.page = "recruitment_process_page"
            st.rerun()

if __name__ == "__main__":
    main()