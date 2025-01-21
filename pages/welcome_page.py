import streamlit as st
from utils import set_bg_hack, query_ollama, extract_text_from_pdf_pypdf2, extract_additional_fields_from_pdf_text, rag_enhanced_query, get_relevant_documents, parse_bullet_points  # Importiere die benötigten Funktionen

def navigate_to_page(page_name):
    st.session_state.page = page_name

def main():
    # Hintergrundbild (angepasst an neues Verzeichnis)
    set_bg_hack("static/screenshot.png")

    # Importiere Roboto Schriftart
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

        /* Alle Textelemente */
        body, p, li, h1, h2, h3, h4, h5, h6, .stTextInput, .stButton, .stSelectbox, .stMultiselect, .stSlider, .stNumberInput, .stTextArea, .stCheckbox {
            font-family: 'Roboto', sans-serif !important;
        }

        /* Code-Elemente */
        code {
            font-family: 'Courier New', Courier, monospace !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Logo zentriert
    st.markdown("<div class='logo-container'><img src='data:image/png;base64," + get_base64_encoded_image('static/color1_logo_transparent_background.png') + "' width='200'></div>", unsafe_allow_html=True)

    # Kurzer Welcome Message
    st.markdown("<div class='welcome-message'>AI-gestützte Analyse ihrer Vakanzbedürfnisse</div>", unsafe_allow_html=True)

    # Job Title Input
    st.markdown("<div class='job-title-label'>Geben Sie eine Stellenbezeichnung ein</div>", unsafe_allow_html=True)
    st.session_state.role_info["job_title"] = st.text_input(
        label="Stellenbezeichnung",
        value=st.session_state.role_info.get("job_title", ""),
        placeholder="z.B. Data Scientist, Marketing Manager",
        key="job_title_input",
        label_visibility='collapsed'
    )

    # Button (zentriert)
    st.markdown("<div class='center'>", unsafe_allow_html=True)
    if st.session_state.role_info["job_title"] and st.button("**Profil erstellen**", key="start_button_manual"):
        navigate_to_page("data_extraction_page") # Hier muss die richtige Folgeseite angegeben werden
    st.markdown("</div>", unsafe_allow_html=True)

    # PDF Upload (unauffälliger)
    st.markdown("<div class='pdf-uploader'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Oder laden Sie eine Stellenbeschreibung als PDF hoch", type="pdf")
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file is not None:
        text = extract_text_from_pdf_pypdf2(uploaded_file)
        if text:
            st.success("PDF erfolgreich hochgeladen und Text extrahiert!")

            # Daten extrahieren (RAG-basiert)
            try:
                extracted_data = extract_data_from_pdf_rag(uploaded_file)

                # Session state aktualisieren
                st.session_state.pdf_text = text
                # Hier werden die Werte aus extracted_data dem Session State zugewiesen,
                # wobei ein leerer String als Standardwert verwendet wird, falls ein Schlüssel nicht vorhanden ist.
                st.session_state.role_info["job_title"] = extracted_data.get("job_title", "")
                st.session_state.role_info["location"] = extracted_data.get("location", "")
                st.session_state.company_info["Company Name"] = extracted_data.get("company", "") # Feld "company" zu "company_name" korrigiert.
                st.session_state.tasks = extracted_data.get("tasks", [])
                st.session_state.benefits = extracted_data.get("benefits", [])
                st.session_state.company_info["company_description"] = extracted_data.get("company_description", "")
                st.session_state.role_info["required_skills"] = extracted_data.get("required_skills", [])

                # Button, um zur nächsten Seite zu navigieren
                if st.button("Proceed to Data Review", key="start_button"):
                    navigate_to_page("data_extraction_page")  # Hier den Namen deiner Folgeseite einsetzen
                    st.rerun() # Nicht ideal, aber notwendig, um die Daten auf der Folgeseite direkt anzuzeigen

            except Exception as e:
                st.error(f"Fehler bei der Datenextraktion: {e}")
        else:
            st.error("Text konnte nicht aus der PDF extrahiert werden.")

if __name__ == "__main__":
    main()
