import streamlit as st

# Beispiel-Datenbank mit vorgefertigten Aufgaben
JOB_TASKS_DB = {
    "Data Scientist": ["Datenanalysen durchführen", "Machine Learning Modelle trainieren", "Datenvisualisierung erstellen"],
    "Software Engineer": ["Code entwickeln & optimieren", "Unit-Tests schreiben", "Technische Dokumentation pflegen"],
    "Marketing Manager": ["Kampagnen entwickeln", "SEO-Strategien umsetzen", "Social Media Analysen durchführen"],
}

# UI für Job-Titel mit automatischen Aufgaben-Vorschlägen
def job_title_autocomplete_ui():
    st.subheader("🔍 Job-Titel & Aufgaben")
    job_title = st.text_input("Gib den Job-Titel ein", key="job_title")

    if job_title in JOB_TASKS_DB:
        suggested_tasks = JOB_TASKS_DB[job_title]
        st.write("📌 Basierend auf deinem Job-Titel könnten folgende Aufgaben relevant sein:")
        for task in suggested_tasks:
            st.write(f"- {task}")
            if st.button(f"✅ {task} übernehmen", key=f"task_{task}"):
                st.session_state["selected_tasks"].append(task)
