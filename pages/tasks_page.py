import streamlit as st
from utils import *
from config import *

def main():
    job_title = st.session_state.role_info["job_title"]
    st.header(f"Tasks for {job_title}")
    if "task_frequencies" not in st.session_state:
        st.session_state.task_frequencies = {}

    # Wenn die Aufgabenliste leer ist, initialisiere sie mit den extrahierten Aufgaben oder RAG-basiert
    if not st.session_state.tasks and "pdf_text" in st.session_state:
        st.session_state.tasks = extract_data_from_pdf_rag(st.session_state.pdf_text).get("tasks", [])
    elif not st.session_state.tasks:
        st.session_state.tasks = analyze_role(st.session_state.role_info["job_title"]).get("tasks", [])

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
        st.session_state.task_frequencies[manual_task] = "Often"
    if st.button("Next: Skillset Selection"):
        st.session_state.page = "skills_page"
        st.rerun()

if __name__ == "__main__":
    main()