import streamlit as st
from utils import get_base64_encoded_image, extract_text_from_pdf_pypdf2, extract_data_from_pdf_rag, set_bg_hack

def main():
    # --- STYLING ---
    # Importiere Roboto Schriftart
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

        /* Alle Textelemente */
        body, p, li, h1, h2, h3, h4, h5, h6, .stTextInput, .stButton, .stSelectbox, .stMultiselect, .stSlider, .stNumberInput, .stTextArea, .stCheckbox, .stFileUploader {
            font-family: 'Roboto', sans-serif !important;
        }

        /* Code-Elemente */
        code {
            font-family: 'Courier New', Courier, monospace !important;
        }

        /* Header-Styling */
        .header-container {
            background-color: #D3D3D3;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }

        /* Logo-Styling */
        .logo-container {
            text-align: center;
            margin-bottom: 20px;
        }

        /* Welcome Message Styling */
        .welcome-message {
            font-size: 1.5em;
            color: #222222;
            text-align: center;
            margin-top: 10px;
            margin-bottom: 30px;
        }

        /* Job Title Input Styling */
        .job-title-label {
            font-size: 1.2em;
            color: #222222;
            font-weight: 600;
            text-align: center;
            margin-bottom: 10px;
        }

        /* Zentrierung von Elementen */
        .center {
            text-align: center;
        }

        /* PDF Uploader Styling */
        .pdf-uploader {
            margin-top: 20px;
            margin-bottom: 20px;
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
    st.session_state.job_details["job_title"] = st.text_input(
        label="Stellenbezeichnung",
        value=st.session_state.job_details.get("job_title", ""),
        placeholder="z.B. Data Scientist, Marketing Manager",
        key="job_title_input",
        label_visibility='collapsed'
    )

    # Button (zentriert)
    st.markdown("<div class='center'>", unsafe_allow_html=True)
    if st.session_state.job_details["job_title"] and st.button("**Profil erstellen**", key="start_button_manual"):
        st.session_state.page = "company_details_page"
        st.rerun()
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
                with st.spinner('Daten werden extrahiert...'):
                    extracted_data = extract_data_from_pdf_rag(uploaded_file)

                # Session state aktualisieren
                st.session_state.pdf_text = text
                st.session_state.job_details["job_title"] = extracted_data.get("job_title", "")
                st.session_state.job_details["location"] = extracted_data.get("job_location", "")
                st.session_state.company_info["company_name"] = extracted_data.get("company_name", "")
                st.session_state.tasks = extracted_data.get("tasks", [])
                st.session_state.benefits = extracted_data.get("benefits", [])
                st.session_state.company_info["company_description"] = extracted_data.get("company_description", "")
                st.session_state.job_details["required_skills"] = extracted_data.get("required_skills", [])

                # Navigiere zur nächsten Seite nach erfolgreicher Extraktion
                st.session_state.page = "company_details_page"
                st.rerun()

            except Exception as e:
                st.error(f"Fehler bei der Datenextraktion: {e}")
        else:
            st.error("Text konnte nicht aus der PDF extrahiert werden.")

if __name__ == "__main__":
    main()