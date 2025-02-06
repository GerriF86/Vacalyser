import streamlit as st

# Bewertungskriterien für Stellenausschreibung (Skala 1-10)
def evaluate_job_posting():
    score = 10
    feedback = []

    # Bewertung basierend auf ausgefüllten Feldern
    if not st.session_state.get("selected_tasks"):
        score -= 2
        feedback.append("🔴 Es fehlen Aufgaben für die Rolle.")
    if not st.session_state.get("required_skills"):
        score -= 2
        feedback.append("🔴 Es fehlen erforderliche Skills.")
    if len(st.session_state.get("selected_tasks", [])) < 3:
        score -= 1
        feedback.append("🟠 Weniger als 3 Aufgaben angegeben.")
    if len(st.session_state.get("required_skills", [])) < 3:
        score -= 1
        feedback.append("🟠 Weniger als 3 Skills angegeben.")
    if not st.session_state.get("salary_range"):
        score -= 1
        feedback.append("🟠 Keine Gehaltsspanne angegeben.")
    if not st.session_state.get("benefits"):
        score -= 1
        feedback.append("🟠 Keine Benefits angegeben.")

    return max(score, 1), feedback

# UI für die Bewertung & visuelle Verbesserungsvorschläge
def job_evaluation_ui():
    st.subheader("📊 Echtzeit-Bewertung der Stellenausschreibung")

    score, feedback = evaluate_job_posting()
    
    # Farbliche Anzeige des Scores
    if score >= 8:
        st.success(f"⭐ {score}/10 - Sehr gute Stellenausschreibung!")
    elif score >= 5:
        st.warning(f"⚠ {score}/10 - Einige Verbesserungen nötig.")
    else:
        st.error(f"❌ {score}/10 - Viele Verbesserungen erforderlich.")

    # Verbesserungen als interaktive Vorschläge
    if feedback:
        st.write("🔧 Verbesserungsvorschläge:")
        for item in feedback:
            st.write(f"- {item}")
