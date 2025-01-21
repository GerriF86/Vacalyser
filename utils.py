import streamlit as st
import requests
import json
import re
from PIL import Image
import base64
import faiss
import numpy as np
import os
import PyPDF2
from langchain_huggingface import HuggingFaceEmbeddings

# --- Constants ---
MODEL_NAME = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"
DATA_DIR = "data/processed"
INDEX_PATH = "vector_databases/faiss_index.index"
DIMENSION = 768

# --- FAISS Index laden ---
index = None
metadata = []  # Initialisiere metadata außerhalb der if-Bedingung

if os.path.exists(INDEX_PATH):
    try:
        index = faiss.read_index(INDEX_PATH)
        json_files = []
        for root, _, files in os.walk(DATA_DIR):
            for file in files:
                if file.endswith(".json"):
                    json_files.append(os.path.join(root, file))
        json_files.sort()
        metadata = []
        for json_file in json_files:
            with open(json_file, 'r', encoding='utf-8') as f:  # encoding='utf-8' hinzugefügt
                data = json.load(f)
                metadata.append(data)
        print(f"Geladene Metadaten: {len(metadata)}")
    except Exception as e:
        st.error(f"Fehler beim Laden des FAISS-Index: {e}")
        index = None
        metadata = []  # Setze metadata auf eine leere Liste im Fehlerfall
else:
    st.warning("FAISS-Index nicht gefunden. Bitte zuerst `populate_vectordb.py` ausführen.")
    index = None
    metadata = []  # Setze metadata auf eine leere Liste, wenn der Index nicht gefunden wird


# --- Helper Functions ---
def styled_button(label, key=None):
    return st.button(label, key=key)

# Navigation Function 
def navigate_to_page(page_name):
    st.session_state.page = page_name

def parse_bullet_points(text):
    items = re.findall(r"[-*•]\s*(.*)", text)
    return items

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

    
def query_ollama(model_name, input_text):
    try:
        with requests.post(
            OLLAMA_URL,
            json={"model": model_name, "prompt": input_text},
            stream=True,
        ) as response:
            response.raise_for_status()

            full_response = ""
            for line in response.iter_lines(decode_unicode=True):
                if line.strip():
                    try:
                        json_line = json.loads(line)
                        full_response += json_line.get("response", "")
                    except json.JSONDecodeError:
                        print(f"JSON Decode Error: {line}")
                        continue
            return full_response
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return ""

# --- PDF Extraction Functions ---
def extract_text_from_pdf_pypdf2(pdf_file):
    """Extrahiert Text aus einem PDF mit PyPDF2."""
    text = ""
    try:
        # Öffne die Datei im Binärmodus:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
        for page in pdf_reader.pages:
            text += page.extract_text()
    except Exception as e:
        print(f"Fehler beim Extrahieren von Text mit PyPDF2: {e}")
    return text

# --- RAG Functions ---
def get_relevant_documents(query, n_results=3):
    global index, metadata

    if index is None or not metadata:
        st.warning("FAISS-Index oder Metadaten nicht geladen.")
        return []

    query_vector = np.zeros((1, DIMENSION), dtype=np.float32)
    distances, indices = index.search(query_vector, n_results)

    relevant_documents = []
    for i in indices[0]:
        if i < len(metadata):
            relevant_documents.append(metadata[i]['job_description'])
        else:
            print(f"Index {i} ist außerhalb des gültigen Bereichs.")
    return relevant_documents

def rag_enhanced_query(query, context_documents):
    context_string = " ".join(context_documents)
    enhanced_query = f"""
    Basierend auf dem folgenden Kontext:
    ---
    {context_string}
    ---
    Beantworte die folgende Frage:
    {query}
    """
    return enhanced_query

def set_bg_hack(main_bg):
    """
    Sets the background image of the Streamlit app.

    Args:
        main_bg: The filename of the image in the 'static' directory (e.g., 'screenshot.png').
    """
    main_bg_ext = main_bg.split(".")[-1]  # Get the file extension
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(f"static/{main_bg}", "rb").read()).decode()});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def extract_additional_fields_from_pdf_text(text):
    fields = {}
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if "company:" in line.lower():
            fields["company_name"] = lines[i].split(":", 1)[1].strip()
        elif "location:" in line.lower():
            fields["job_location"] = lines[i].split(":", 1)[1].strip()
        elif "position type:" in line.lower():
            fields["permanent_position"] = "yes" if "permanent" in lines[i].split(":", 1)[1].strip().lower() else "no"
        elif "full time/part time:" in line.lower():
            fields["full_time"] = "yes" if "full time" in lines[i].split(":", 1)[1].strip().lower() else "no"
        elif "phone number:" in line.lower():
            fields["phone_number"] = lines[i].split(":", 1)[1].strip()
        elif "email address:" in line.lower():
            fields["contact_email"] = lines[i].split(":", 1)[1].strip()
        elif "contact person:" in line.lower():
            fields["contact_person"] = lines[i].split(":", 1)[1].strip()
        elif "salary range:" in line.lower():
            fields["salary_range_pdf"] = lines[i].split(":", 1)[1].strip()
    return fields

#Core Functions#

def analyze_role(job_title):
    if not job_title:
        st.error("Job title: Vanished! Please provide one, I need it.")
        return {
            "tasks": [],
            "technical_skills": [],
            "soft_skills": [],
            "challenges": [],
        }
    
    relevant_docs = get_relevant_documents(
        query=f"Aufgaben und Verantwortlichkeiten für {job_title}",
        n_results=2
    )

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

    tasks_section = re.search(r"Common tasks and responsibilities:\n(.*?)(?=Essential skills and qualifications:)", response, re.DOTALL)
    tasks = parse_bullet_points(tasks_section.group(1).strip()) if tasks_section else []

    skills_section = re.search(r"Essential skills and qualifications:\n(.*?)(?=Potential challenges and opportunities:)", response, re.DOTALL)
    skills = skills_section.group(1).strip().split("\n\n") if skills_section else []
    technical_skills = parse_bullet_points(skills[0]) if len(skills) > 0 else []
    soft_skills = parse_bullet_points(skills[1]) if len(skills) > 1 else []

    challenges_section = re.search(r"Potential challenges and opportunities:\n(.*)", response, re.DOTALL)
    challenges = parse_bullet_points(challenges_section.group(1).strip()) if challenges_section else []

    return {
        "tasks": tasks,
        "technical_skills": technical_skills,
        "soft_skills": soft_skills,
        "challenges": challenges,
    }

def analyze_company_and_team(job_title):
    relevant_docs = get_relevant_documents(
        query=f"Fragen zur Unternehmenskultur für {job_title}",
        n_results=1
    )
    rag_prompt = rag_enhanced_query(
        query=f"""
        Develop 3 insightful questions to help a new {job_title} understand the company and team culture, values, and work style.
        """,
        context_documents=relevant_docs
    )
    response = query_ollama(MODEL_NAME, rag_prompt)
    return {question: "" for question in parse_bullet_points(response)}

def determine_salary(job_title, region, experience):
    relevant_docs = get_relevant_documents(
        query=f"Gehaltsspanne für {job_title} in {region} mit {experience} Jahren Erfahrung",
        n_results=1
    )
    rag_prompt = rag_enhanced_query(
        query=f"""
        Estimate the salary range for a {job_title} with {experience} years of experience in {region}. 
        Provide a realistic salary range and note that this is just an estimate.
        """,
        context_documents=relevant_docs
    )
    response = query_ollama(MODEL_NAME, rag_prompt)
    match = re.search(r"(\d+)\s*-\s*(\d+)", response) if response else None
    return (int(match.group(1)), int(match.group(2))) if match else (None, None)

def generate_job_ad(
    job_details,
    company_info,
    benefits,
    recruitment_process,
    audience="general",
    language="english",
    style="formal",
):
    relevant_docs = get_relevant_documents(
        query=f"Stellenanzeige für {job_details.get('job_title', '')}",
        n_results=3
    )
    rag_prompt = rag_enhanced_query(
        query=f"""
        Write a {style} job ad in {language} for a {job_details.get('job_title', '')}.

        Target audience: {audience}
        About the company: {company_info}
        Benefits: {benefits}
        Recruitment process: {recruitment_process}

        Include:
        * An engaging company description
        * A clear job description with responsibilities
        * Required skills and qualifications
        * A list of benefits
        * A compelling call to action
        """,
        context_documents=relevant_docs
    )
    return query_ollama(MODEL_NAME, rag_prompt)

def prepare_interview(job_title, focus_areas):
    focus_text = ", ".join(focus_areas)
    prompt = f"""
    Generate interview questions for a {job_title}. Focus on these areas: {focus_text}.
    Provide a mix of behavioral, technical, and situational questions.
    """
    response = query_ollama(MODEL_NAME, prompt)
    return parse_bullet_points(response)

def create_onboarding_checklist(job_title, department):
    prompt = f"""
    Create a comprehensive onboarding checklist for a {job_title} in {department}.
    Include tasks, goals, and resources for the first week, first month, and first three months.
    """
    response = query_ollama(MODEL_NAME, prompt)
    return parse_bullet_points(response)

def suggest_retention_strategies(job_title):
    prompt = f"""
    Suggest effective retention strategies for a {job_title}.
    Consider factors like career growth, work-life balance, recognition, and compensation.
    """
    response = query_ollama(MODEL_NAME, prompt)
    return parse_bullet_points(response)

def identify_benefits(job_title, region=None):
    prompt = f"""
    What are some attractive benefits for a {job_title}?
    """
    if region:
        prompt += f" Consider the region: {region}."
    response = query_ollama(MODEL_NAME, prompt)
    return parse_bullet_points(response)

def define_recruitment_steps(job_title):
    prompt = f"""
    Define the steps in the recruitment process for a {job_title}.
    Be thorough and include all stages from initial application to offer.
    """
    response = query_ollama(MODEL_NAME, prompt)
    return parse_bullet_points(response)

def get_company_info(company_name):
    relevant_docs = get_relevant_documents(
        query=f"Informationen über das Unternehmen {company_name}",
        n_results=2
    )
    rag_prompt = rag_enhanced_query(
        query=f"""
        Provide information about {company_name}:
        - Industry
        - Company Location
        - Company Size
        - Website
        """,
        context_documents=relevant_docs
    )
    response = query_ollama(MODEL_NAME, rag_prompt)

    info = {}
    lines = response.split("\n")
    for line in lines:
        if "-" in line:
            key, value = line.split("-", 1)
            key = key.strip()
            value = value.strip()
            if key.lower() == "industry":
                info["industry"] = value
            elif key.lower() == "company location":
                info["company_location"] = value
            elif key.lower() == "company size":
                info["company_size"] = value.lower()
            elif key.lower() == "website":
                info["website"] = value

    return info

# Funktion zum Extrahieren von Daten aus PDF mit RAG
def extract_data_from_pdf_rag(pdf_file):
    # Extrahiere Text aus PDF
    text = extract_text_from_pdf_pypdf2(pdf_file)
    if not text:
        print("Fehler: Konnte Text nicht aus PDF extrahieren.")
        return {}

    # Extrahiere zusätzliche Felder mit Regex
    extracted_fields = extract_additional_fields_from_pdf_text(text)

    # RAG initialisieren, falls noch nicht geschehen
    if 'rag_chain' not in st.session_state:
        initialize_rag_chain()  # oder wie auch immer deine Initialisierungsfunktion heißt

    # Verwende die RAG-Kette, um die extrahierten Informationen anzureichern
    rag_results = {}

    # Beispielhafte RAG-Anfragen (passe diese an deine Bedürfnisse an)
    if "company_name" in extracted_fields:
        rag_results['company_description'] = query_rag_chain(f"Can you provide an overview of the company {extracted_fields['company_name']}?")

    rag_results['tasks'] = query_rag_chain(
        f"What are the main tasks and responsibilities for the role: {extracted_fields.get('job_title', '')}?"
    )

    rag_results['required_skills'] = query_rag_chain(
        f"What skills are required for the role: {extracted_fields.get('job_title', '')}?"
    )

    rag_results['benefits'] = query_rag_chain(
        f"What are common benefits offered for the role: {extracted_fields.get('job_title', '')}?"
    )

    # Kombiniere extrahierte Felder und RAG-Ergebnisse
    extracted_data = {**extracted_fields, **rag_results}

    return extracted_data

def query_rag_chain(query):
    if 'rag_chain' in st.session_state:
        # Stelle sicher, dass die Frage korrekt formatiert ist, z. B. als vollständiger Satz
        if not query.endswith("?"):
            query += "?"
        response = st.session_state.rag_chain.invoke({"input": query})
        # Überprüfe, ob die Antwort ein 'output' Attribut hat
        if hasattr(response, 'output'):
            return response.output
        else:
            # Hier könntest du versuchen, die Antwort anders zu extrahieren oder eine Fehlermeldung zurückgeben
            return "Antwort konnte nicht extrahiert werden."
    else:
        return "RAG-Kette ist nicht initialisiert."