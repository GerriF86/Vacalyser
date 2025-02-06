import streamlit as st

# Beispiel-Datenbank mit typischen Aufgaben & Skills basierend auf Job-Titeln
TASK_SKILL_DB = {
    "Data Scientist": {
        "tasks": ["Datenanalysen durchführen", "Machine Learning Modelle trainieren", "Datenvisualisierung erstellen"],
        "skills": ["Python", "Statistik", "Machine Learning", "Datenbanken"]
    },
    "Software Engineer": {
        "tasks": ["Code entwickeln & optimieren", "Unit-Tests schreiben", "Technische Dokumentation pflegen"],
        "skills": ["Python", "JavaScript", "DevOps", "Datenbanken"]
    },
    "Marketing Manager": {
        "tasks": ["Kampagnen entwickeln", "SEO-Strategien umsetzen", "Social Media Analysen durchführen"],
        "skills": ["SEO", "Google Ads", "Content Marketing", "Datenanalyse"]
    }
}

# UI für automatische Vorschläge basierend auf Job-Titel
def ki_suggestions_ui():
    st.subheader("🤖 KI-gestützte Vorschläge für Aufgaben & Skills")

    job_title = st.text_input("Gib den Job-Titel ein", key="job_title")

    if job_title in TASK_SKILL_DB:
        suggested_tasks = TASK_SKILL_DB[job_title]["tasks"]
        suggested_skills = TASK_SKILL_DB[job_title]["skills"]

        st.write("📌 Basierend auf deinem Job-Titel könnten folgende Aufgaben relevant sein:")
        for task in suggested_tasks:
            st.write(f"- {task}")
            if st.button(f"✅ {task} übernehmen", key=f"task_{task}"):
                st.session_state["selected_tasks"].append(task)

        st.write("🎯 Empfohlene Skills für diese Rolle:")
        for skill in suggested_skills:
            st.write(f"- {skill}")
            if st.button(f"✅ {skill} übernehmen", key=f"skill_{skill}"):
                st.session_state["required_skills"].append(skill)
