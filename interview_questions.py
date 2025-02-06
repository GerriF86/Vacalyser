import streamlit as st

# Generiere Interviewfragen basierend auf Jobdetails & Skills
def generate_interview_questions():
    questions = []
    
    if "job_title" in st.session_state and st.session_state["job_title"]:
        questions.append(f"Können Sie Ihre Erfahrungen im Bereich '{st.session_state['job_title']}' beschreiben?")
    
    if "selected_tasks" in st.session_state and st.session_state["selected_tasks"]:
        questions.append(f"Wie würden Sie die Aufgabe '{st.session_state['selected_tasks'][0]}' angehen?")

    if "required_skills" in st.session_state and st.session_state["required_skills"]:
        questions.append(f"Wie haben Sie Ihre Fähigkeiten in '{st.session_state['required_skills'][0]}' in der Vergangenheit angewendet?")

    if "experience_level" in st.session_state and st.session_state["experience_level"]:
        questions.append(f"Welche Herausforderungen sind Ihnen auf '{st.session_state['experience_level']}'-Niveau begegnet?")

    if "interview_stages" in st.session_state and st.session_state["interview_stages"]:
        questions.append(f"Warum glauben Sie, dass Sie für eine '{st.session_state['interview_stages']}'-stufige Interviewstruktur geeignet sind?")

    return questions

# UI für Interviewfragen
def interview_questions_ui():
    st.subheader("🎤 Automatisch generierte Interviewfragen")

    questions = generate_interview_questions()
    
    if questions:
        for i, question in enumerate(questions, start=1):
            st.write(f"**{i}. {question}**")
    else:
        st.write("🔹 Keine Interviewfragen gefunden. Bitte füllen Sie mehr Jobdetails aus.")
