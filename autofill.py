import streamlit as st

# Beispiel-Datenbank mit vorkonfigurierten Job-Profilen für Autofill
JOB_PROFILES = {
    "Data Scientist": {
        "selected_tasks": ["Datenanalysen durchführen", "Machine Learning Modelle trainieren", "Datenvisualisierung erstellen"],
        "required_skills": ["Python", "Statistik", "Machine Learning", "Datenbanken"],
        "salary_range": "60.000 - 90.000 €",
        "benefits": ["Homeoffice", "Weiterbildung", "Firmenwagen"]
    },
    "Software Engineer": {
        "selected_tasks": ["Code entwickeln & optimieren", "Unit-Tests schreiben", "Technische Dokumentation pflegen"],
        "required_skills": ["Python", "JavaScript", "DevOps", "Datenbanken"],
        "salary_range": "55.000 - 85.000 €",
        "benefits": ["Flexible Arbeitszeiten", "Aktienoptionen", "Remote-Work"]
    },
    "Marketing Manager": {
        "selected_tasks": ["Kampagnen entwickeln", "SEO-Strategien umsetzen", "Social Media Analysen durchführen"],
        "required_skills": ["SEO", "Google Ads", "Content Marketing", "Datenanalyse"],
        "salary_range": "50.000 - 75.000 €",
        "benefits": ["Weiterbildung", "Firmenwagen", "Bonuszahlungen"]
    }
}

# UI für die Autofill-Funktion
def autofill_ui():
    st.subheader("⚡ Autofill für Stellenausschreibungen")

    job_title = st.text_input("Gib den Job-Titel ein", key="job_title")

    if job_title in JOB_PROFILES:
        st.write("✨ Automatisches Ausfüllen mit KI-gestützten Vorschlägen verfügbar.")
        if st.button("🔄 Autofill übernehmen"):
            for key, value in JOB_PROFILES[job_title].items():
                st.session_state[key] = value
            st.success("✅ Autofill erfolgreich! Deine Stellenausschreibung wurde vorbefüllt.")
