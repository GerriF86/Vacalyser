import streamlit as st
import PyPDF2
import requests
from bs4 import BeautifulSoup
import io

def extract_text_from_pdf(uploaded_file):
    """Extrahiert den Text aus einem hochgeladenen PDF-Dokument."""
    reader = PyPDF2.PdfReader(uploaded_file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

def extract_text_from_url(url):
    """Scrapt den Hauptinhalt einer Stellenanzeige von einer angegebenen URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Versuch, relevante Job-Details zu extrahieren
        paragraphs = soup.find_all("p")
        job_text = "\n".join([p.get_text() for p in paragraphs])
        
        return job_text if job_text else "Kein relevanter Text gefunden."
    except Exception as e:
        return f"Fehler beim Abrufen der URL: {e}"

def auto_fill_session_state(extracted_text):
    """Füllt die `st.session_state`-Felder mit den extrahierten Informationen."""
    if extracted_text:
        st.session_state["job_title"] = extracted_text[:50]  # Platzhalter, später NLP-Analyse für Titel
        st.session_state["company_name"] = "Unternehmen XY"  # Später per NLP erkennen
        st.session_state["selected_tasks"] = ["Aufgabe 1", "Aufgabe 2"]  # NLP zur Extraktion notwendig
        st.session_state["required_skills"] = ["Skill 1", "Skill 2"]  # NLP zur Extraktion notwendig

def job_ad_extraction_ui():
    """Streamlit UI-Komponente für das Hochladen und Analysieren von Stellenanzeigen."""
    st.subheader("🔍 Automatische Analyse einer Stellenanzeige")

    option = st.radio("Wähle eine Methode zur Analyse:", ["PDF-Upload", "URL eingeben"])

    extracted_text = ""

    if option == "PDF-Upload":
        uploaded_file = st.file_uploader("Lade eine Stellenanzeige als PDF hoch", type=["pdf"])
        if uploaded_file:
            extracted_text = extract_text_from_pdf(uploaded_file)

    elif option == "URL eingeben":
        url = st.text_input("Gib die URL der Stellenanzeige ein:")
        if url:
            extracted_text = extract_text_from_url(url)

    if extracted_text:
        st.text_area("Extrahierter Text:", extracted_text, height=200)
        if st.button("Automatisch Felder ausfüllen"):
            auto_fill_session_state(extracted_text)
            st.success("Die Felder wurden automatisch ausgefüllt!")

