import streamlit as st
import PyPDF2
import requests
from bs4 import BeautifulSoup
import io

# PDF-Text extrahieren
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

# URL-Text scrapen
def extract_text_from_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")
        job_text = "\n".join([p.get_text() for p in paragraphs])

        return job_text if job_text else "Kein relevanter Text gefunden."
    except Exception as e:
        return f"Fehler beim Abrufen der URL: {e}"

# UI für Job-Import
def job_import_ui():
    st.subheader("📄 Importiere eine bestehende Stellenausschreibung")

    import_option = st.radio("Wähle eine Import-Methode:", ["PDF-Upload", "URL", "Text-Eingabe"])

    extracted_text = ""

    if import_option == "PDF-Upload":
        uploaded_file = st.file_uploader("Lade eine PDF-Stellenanzeige hoch", type=["pdf"])
        if uploaded_file:
            extracted_text = extract_text_from_pdf(uploaded_file)

    elif import_option == "URL":
        url = st.text_input("Gib die URL der Stellenausschreibung ein:")
        if url:
            extracted_text = extract_text_from_url(url)

    elif import_option == "Text-Eingabe":
        extracted_text = st.text_area("Füge den Stellenausschreibungstext ein:")

    if extracted_text:
        st.text_area("Extrahierter Text:", extracted_text, height=200)
        if st.button("Automatisch Felder ausfüllen"):
            st.session_state["imported_job_text"] = extracted_text
            st.success("✅ Die Felder wurden automatisch ausgefüllt!")
