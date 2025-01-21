import streamlit as st
from utils import *
from config import *
import streamlit as st
from utils import *

# --- Constants (if needed specifically for this page) ---
# MODEL_NAME = "llama3.2:3b"  # Consider removing if already defined in the main script
# OLLAMA_URL = "http://localhost:11434/api/generate"  # Consider removing if already defined in the main script

# --- Helper Functions (if needed specifically for this page) ---
# def styled_button(label, key=None):
#     return st.button(label, key=key)

# def parse_bullet_points(text):
#     items = re.findall(r"[-*•]\s*(.*)", text)
#     return items

# --- Page Functions ---
def main():
    job_title = st.session_state.role_info["job_title"]
    st.subheader("Role Deep Dive", f"Unpacking the {job_title} Position")

    # Extrahiere Infos aus PDF, falls vorhanden
    if "pdf_text" in st.session_state:
        with st.expander("Uploaded Job Description (PDF)", expanded=True):
            st.text_area("Extracted Text", st.session_state.pdf_text, height=300, label_visibility="collapsed")

        # Nutze die extrahierten Infos aus dem PDF für die RAG-Funktionalität
        relevant_docs = [st.session_state.pdf_text]

        rag_prompt = rag_enhanced_query(
            query=f"""
            Analyze the role of {job_title} in detail:
            * Provide a comprehensive list of common tasks and responsibilities, be very specific.
            * List essential skills and qualifications, both hard and soft skills.
            * Outline potential challenges and opportunities associated with this role.
            """,
            context_documents=relevant_docs
        )

        response = query_ollama(MODEL_NAME, rag_prompt)

        # ... (Verarbeite die Response wie in analyze_role()) ...
        tasks_section = re.search(r"Common tasks and responsibilities:\n(.*?)(?=Essential skills and qualifications:)", response, re.DOTALL)
        st.session_state.tasks = parse_bullet_points(tasks_section.group(1).strip()) if tasks_section else []

        skills_section = re.search(r"Essential skills and qualifications:\n(.*?)(?=Potential challenges and opportunities:)", response, re.DOTALL)
        skills = skills_section.group(1).strip().split("\n\n") if skills_section else []
        st.session_state.technical_skills = {skill: {"must_have": False, "nice_to_have": False} for skill in parse_bullet_points(skills[0])} if len(skills) > 0 else {}
        st.session_state.soft_skills = {skill: {"must_have": False, "nice_to_have": False} for skill in parse_bullet_points(skills[1])} if len(skills) > 1 else {}

        challenges_section = re.search(r"Potential challenges and opportunities:\n(.*)", response, re.DOTALL)
        st.session_state.challenges = parse_bullet_points(challenges_section.group(1).strip()) if challenges_section else []

    # Zwei-Spalten-Layout
    col1, col2 = st.columns(2)

    with col1:
        st.session_state.role_info["location"] = st.text_input(label="Location", value=st.session_state.role_info["location"], placeholder="e.g., Berlin, Germany")
        st.session_state.role_info["work_arrangement"] = st.selectbox(
            "Work Arrangement",
            ["Full-Time", "Part-Time", "Contract", "Internship"],
            index=["Full-Time", "Part-Time", "Contract", "Internship"].index(
                st.session_state.role_info["work_arrangement"]
            ),
        )
        st.session_state.role_info["onsite_remote_hybrid"] = st.selectbox(
            "Onsite / Remote / Hybrid",
            ["Onsite", "Remote", "Hybrid"],
            index=["Onsite", "Remote", "Hybrid"].index(st.session_state.role_info["onsite_remote_hybrid"]),
        )
        if st.session_state.role_info["onsite_remote_hybrid"] == "Hybrid":
            st.session_state.role_info["onsite_percentage"] = st.slider(
                "Onsite Percentage", 0, 100, st.session_state.role_info["onsite_percentage"]
            )

        st.session_state.role_info["department"] = st.text_input("Department", st.session_state.role_info["department"], placeholder="e.g., Engineering")

    with col2:
        min_salary, max_salary = st.session_state.role_info["salary_range"]

        if min_salary is None or min_salary < 0 or min_salary > 200000:
            min_salary = 0

        if max_salary is None or max_salary < 0 or max_salary > 200000:
            max_salary = 0

        salary_range = st.slider(
            "Salary Range (in thousands)",
            0,
            200,
            (min_salary, max_salary),
            10,
            format="%d",
        )
        st.session_state.role_info["salary_range"] = salary_range

        st.session_state.role_info["responsible_money"] = st.text_input(
            "Budget Authority", st.session_state.role_info["responsible_money"], placeholder="e.g., Department Head"
        )
        st.session_state.role_info["responsible_authority"] = st.text_input(
            "Hiring Authority", st.session_state.role_info["responsible_authority"], placeholder="e.g., Hiring Manager"
        )
        st.session_state.role_info["responsible_need"] = st.text_input(
            "Who defines the need?", st.session_state.role_info["responsible_need"], placeholder="e.g., Team Lead"
        )

        # --- Gehaltsvorschlag ---
        if st.session_state.role_info["location"]:
            with st.expander("Gehaltsvorschlag (geschätzt)"):
                experience_level = st.selectbox("Erfahrungslevel", ["Junior", "Mid-Level", "Senior"])
                experience_years = {"Junior": 1, "Mid-Level": 3, "Senior": 6}.get(experience_level, 1)

                if st.button("Gehaltsspanne schätzen", key="salary_estimate"):
                    with st.spinner("Schätze Gehaltsspanne..."):
                        salary_range = determine_salary(
                            job_title, st.session_state.role_info["location"], experience_years
                        )
                        if salary_range != (None, None):
                            st.write(f"Geschätzte Gehaltsspanne: {salary_range[0]}k - {salary_range[1]}k")
                        else:
                            st.write("Konnte keine Gehaltsspanne schätzen.")
        # --- Ende Gehaltsvorschlag ---

    # --- Required Languages ---
    print(f"Languages from session_state before multiselect: {st.session_state.role_info.get('languages')}")
    # Filter out empty strings from the default values
    default_languages = [lang for lang in st.session_state.role_info.get("languages", []) if lang]
    st.session_state.role_info["languages"] = st.multiselect(
        "Required Languages",
        options=["English", "German", "Spanish", "French"],
        default=default_languages
    )
    print(f"Languages from session_state after multiselect: {st.session_state.role_info.get('languages')}")
    # --- End Required Languages ---
    
    if st.button("Next: Tasks Time"):
        # Call functions using the collected information
        if "pdf_text" not in st.session_state:
            st.session_state.tasks = analyze_role(job_title).get("tasks", [])
        st.session_state.selected_tasks = []
        st.session_state.task_frequencies = {}  # Initialize task frequencies
        st.session_state.page = "tasks_page"
        st.rerun()

# Make sure to set the default value for 'languages' in st.session_state when initializing the session state
if "page" not in st.session_state:
    st.session_state.page = "welcome_page"
    # ... other initializations ...
    st.session_state.role_info = {
        "job_title": "",
        "location": "",
        "work_arrangement": "Full-Time",
        "onsite_remote_hybrid": "Onsite",
        "onsite_percentage": 100,
        "salary_range": (0, 0),
        "department": "",
        "responsible_money": "",
        "responsible_authority": "",
        "responsible_need": "",
        "languages": [],  # Initialize 'languages' to an empty list
    }

if __name__ == "__main__":
    main()