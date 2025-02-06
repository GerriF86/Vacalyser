import streamlit as st

# Definiere die Reihenfolge der Seiten
pages = [
    "welcome_page", "company_details_page", "department_info_page", "role_info_page", "tasks_page",
    "skills_page", "benefits_page", "recruitment_process_page", "summary_page"
]

# Navigation steuern
def navigation_ui():
    current_page = st.session_state.get("current_page", "welcome_page")

    col1, col2 = st.columns([1, 1])
    
    # Zurück-Button
    if pages.index(current_page) > 0:
        if col1.button("⬅ Zurück"):
            prev_page = pages[pages.index(current_page) - 1]
            st.session_state["current_page"] = prev_page
            st.rerun()

    # Weiter-Button
    if pages.index(current_page) < len(pages) - 1:
        if col2.button("Weiter ➡"):
            next_page = pages[pages.index(current_page) + 1]
            st.session_state["current_page"] = next_page
            st.rerun()
