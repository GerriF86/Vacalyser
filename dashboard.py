import streamlit as st

# Definiere die Seitenstruktur
pages = {
    "🏠 Home": "welcome_page",
    "🏢 Unternehmensdetails": "company_details_page",
    "👥 Abteilung": "department_info_page",
    "📝 Rolle & Aufgaben": "role_info_page",
    "📌 Aufgaben": "tasks_page",
    "🎯 Skills": "skills_page",
    "🎁 Benefits": "benefits_page",
    "🛠 Recruiting-Prozess": "recruitment_process_page",
    "📊 Zusammenfassung": "summary_page",
}

# UI für Dashboard mit direktem Zugriff auf jede Sektion
def dashboard_ui():
    st.sidebar.subheader("📌 Dashboard – Schnellzugriff")
    
    cols = st.columns(3)
    i = 0

    for page_name, page_key in pages.items():
        with cols[i % 3]:
            if st.button(page_name):
                st.session_state["current_page"] = page_key
                st.rerun()
        i += 1
