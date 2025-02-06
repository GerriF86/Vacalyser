import streamlit as st

# 🎨 Modernes Farbschema
PRIMARY_COLOR = "#1F2937"  # Dunkles Blau-Grau für die Kopfzeile und das Menü
SECONDARY_COLOR = "#4F46E5"  # Lila-Blau für Akzente und Buttons
BACKGROUND_COLOR = "#F3F4F6"  # Helles Grau für den Hintergrund
TEXT_COLOR = "#111827"  # Dunkelgrau für besseren Kontrast
HIGHLIGHT_COLOR = "#10B981"  # Grün für Fortschrittsanzeige und positive Akzente

# 📌 Globale CSS-Styles für die App
def inject_custom_css():
    st.markdown(f"""
        <style>
            /* Globales Styling */
            body {{
                background-color: {BACKGROUND_COLOR};
                color: {TEXT_COLOR};
                font-family: 'Inter', sans-serif;
            }}

            /* Sidebar Styling */
            .css-1d391kg {{
                background-color: {PRIMARY_COLOR} !important;
                color: white !important;
            }}

            /* Fortschrittsbalken */
            .stProgress > div > div {{
                background-color: {HIGHLIGHT_COLOR} !important;
            }}

            /* Buttons */
            .stButton > button {{
                background-color: {SECONDARY_COLOR};
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 16px;
                font-weight: bold;
            }}

            /* Spacing für bessere Darstellung */
            .block-container {{
                padding-top: 1rem !important;
            }}

            /* Header Styling */
            .css-18e3th9 {{
                font-size: 24px !important;
                font-weight: bold !important;
                color: {SECONDARY_COLOR} !important;
            }}
        </style>
    """, unsafe_allow_html=True)

# 📌 Modernes Navigationsmenü in der Sidebar
def modern_navigation():
    st.sidebar.markdown(f"""
        <div style='padding: 20px; text-align: center;'>
            <h2 style='color: white;'>🚀 AI Need Analysis</h2>
            <p style='color: #D1D5DB;'>Die Zukunft der Job-Analyse</p>
        </div>
    """, unsafe_allow_html=True)

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

    selected_page = st.sidebar.radio("Navigation", list(pages.keys()))
    st.session_state["current_page"] = pages[selected_page]

# 📌 UI-Setup-Funktion
def setup_ui():
    inject_custom_css()
    modern_navigation()
