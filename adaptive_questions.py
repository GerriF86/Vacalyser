import streamlit as st

# Priorisierte Fragen nach Kategorie & Zeitaufwand
QUESTION_SETS = {
    "Unternehmen": [
        {"key": "company_name", "question": "Wie heißt dein Unternehmen?", "priority": 10},
        {"key": "industry", "question": "In welcher Branche ist dein Unternehmen tätig?", "priority": 8},
        {"key": "company_size", "question": "Wie groß ist dein Unternehmen?", "priority": 7},
        {"key": "work_mode", "question": "Wie wird in deinem Unternehmen gearbeitet? (Remote, Hybrid, Vor-Ort)", "priority": 6},
    ],
    "Jobrolle": [
        {"key": "job_title", "question": "Wie lautet der Job-Titel?", "priority": 10},
        {"key": "selected_tasks", "question": "Welche sind die wichtigsten Aufgaben dieser Rolle?", "priority": 9},
        {"key": "required_skills", "question": "Welche Skills sind für diese Position erforderlich?", "priority": 9},
        {"key": "experience_level", "question": "Welche Erfahrung wird erwartet?", "priority": 8},
    ],
    "Recruiting-Prozess": [
        {"key": "interview_stages", "question": "Wie viele Interviewrunden gibt es?", "priority": 7},
        {"key": "assessment_needed", "question": "Gibt es Assessments oder Case Studies?", "priority": 6},
        {"key": "application_timeline", "question": "Wie lange dauert der Bewerbungsprozess?", "priority": 6},
    ],
    "Flexibilität & Anforderungen": [
        {"key": "salary_range", "question": "Welche Gehaltsspanne wird angeboten?", "priority": 8},
        {"key": "remote_policy", "question": "Gibt es Homeoffice-Optionen?", "priority": 7},
        {"key": "training_willingness", "question": "Welche Weiterbildungsmöglichkeiten gibt es?", "priority": 7},
    ]
}

# Dynamische Fragegenerierung basierend auf Priorität
def generate_adaptive_questions():
    st.subheader("📝 Beantworte die wichtigsten Fragen")

    total_time_available = 20  # Maximale Zeit in Minuten
    estimated_time_per_question = 1.5  # Durchschnittliche Beantwortungsdauer pro Frage in Minuten
    max_questions = int(total_time_available / estimated_time_per_question)

    all_questions = []
    for category in QUESTION_SETS.values():
        all_questions.extend(category)

    # Fragen nach Priorität sortieren und die Top-N auswählen
    sorted_questions = sorted(all_questions, key=lambda x: x["priority"], reverse=True)[:max_questions]

    for q in sorted_questions:
        if q["key"] not in st.session_state or not st.session_state[q["key"]]:
            st.text_input(q["question"], key=q["key"])

    st.success("✅ Dein Profil wird automatisch optimiert, basierend auf den wichtigsten Antworten.")
