# pages/6_tasks_page.py
import streamlit as st
from ui_elements import centered_title
from core_functions import get_tasks_for_job_title

def main():
    """Functions of the tasks page of the Streamlit application."""
    centered_title("Tasks")

    # Initialize Session State if not existing
    if "job_details" not in st.session_state:
        st.session_state.job_details = {}
    if "task_frequencies" not in st.session_state:
        st.session_state.task_frequencies = {}
    if "selected_tasks" not in st.session_state:
        st.session_state.selected_tasks = []

    # Load predefined tasks for the job title if available
    job_title = st.session_state.job_details.get("job_title", "")
    if job_title:
        try:
            predefined_tasks = get_tasks_for_job_title(job_title)
        except Exception as e:
            st.error(f"Error loading predefined tasks: {e}")
            predefined_tasks = []
    else:
        predefined_tasks = []

    # Select tasks with checkboxes in two columns
    col1, col2 = st.columns(2)
    for i, task in enumerate(predefined_tasks):
        with col1 if i % 2 == 0 else col2:
            is_selected = st.checkbox(
                task,
                key=f"task_{task}",
                value=task in st.session_state.selected_tasks,
            )
            if is_selected:
                if task not in st.session_state.selected_tasks:
                    st.session_state.selected_tasks.append(task)
            else:
                if task in st.session_state.selected_tasks:
                    st.session_state.selected_tasks.remove(task)

    # Task frequencies
    if st.session_state.selected_tasks:
        for task in st.session_state.selected_tasks:
            st.session_state.task_frequencies[task] = st.selectbox(
                f"Frequency for '{task}'",
                ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly", "On Demand"],
                key=f"frequency_{task}",
                index=get_index_for_value(
                    st.session_state.task_frequencies.get(task),
                    ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly", "On Demand"],
                ),
            )

    if st.button("Next: Skills"):
        st.session_state.current_page = "skills_page"
        st.rerun()

if __name__ == "__main__":
    main()