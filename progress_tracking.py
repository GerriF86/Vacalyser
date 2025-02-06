import streamlit as st
import json

# Funktion zum Speichern der aktuellen Eingaben
def save_session_state(filename="job_data.json"):
    data = {key: st.session_state[key] for key in st.session_state if not key.startswith("_")}
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    st.success("✅ Daten erfolgreich gespeichert!")

# Funktion zum Laden gespeicherter Eingaben
def load_session_state(filename="job_data.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            for key, value in data.items():
                st.session_state[key] = value
        st.success("✅ Daten erfolgreich geladen!")
    except FileNotFoundError:
        st.warning("⚠ Noch keine gespeicherten Daten gefunden.")
    except json.JSONDecodeError:
        st.error("❌ Fehler beim Laden der Daten.")

# Fortschrittsanzeige basierend auf ausgefüllten Feldern
def calculate_progress():
    total_keys = [
        "company_name", "industry", "location", "company_values", "department", "team_size", "work_mode",
        "job_title", "selected_tasks", "required_skills", "hard_skills", "soft_skills", "certifications",
        "experience_level", "interview_stages", "assessment_required", "hiring_manager", "benefits"
    ]
    filled_keys = sum(1 for key in total_keys if st.session_state.get(key))
    return int((filled_keys / len(total_keys)) * 100)

# UI für Speichern/Laden & Fortschritt anzeigen
def save_load_progress_ui():
    st.sidebar.subheader("💾 Datenverwaltung")
    if st.sidebar.button("💾 Daten speichern"):
        save_session_state()
    if st.sidebar.button("📂 Daten laden"):
        load_session_state()

    # Fortschrittsanzeige
    progress = calculate_progress()
    st.sidebar.subheader("📊 Fortschritt")
    st.sidebar.progress(progress / 100)
    st.sidebar.write(f"**{progress}% abgeschlossen**")
