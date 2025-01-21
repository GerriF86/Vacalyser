import requests
import json
import re
import faiss
import numpy as np
import os
import PyPDF2
from config import MODEL_NAME, OLLAMA_URL, DATA_DIR, INDEX_PATH, DIMENSION
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.document_loaders import JSONLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM 
import os
import re
import streamlit as st
import base64
from PIL import Image

# --- Constants ---
MODEL_NAME = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"
DATA_DIR = "APP/data/processed"
INDEX_PATH = "vector_databases/faiss_index.index"
DIMENSION = 768

# --- FAISS Index laden ---
index = None  # Initialisiere die Variable index
metadata = [] # Initialisiere die Variable metadata
if os.path.exists(INDEX_PATH):
    try:
        index = faiss.read_index(INDEX_PATH)
        json_files = []
        for root, _, files in os.walk(DATA_DIR):
            for file in files:
                if file.endswith(".json"):
                    json_files.append(os.path.join(root, file))
        json_files.sort()
        
        # Stelle sicher, dass metadata als globale Variable verfügbar ist
        global metadata
        metadata = []
        
        for json_file in json_files:
            with open(json_file, 'r') as f:
                data = json.load(f)
                metadata.append(data)
        print(f"Geladene Metadaten: {len(metadata)}")
    except Exception as e:
        st.error(f"Fehler beim Laden des FAISS-Index: {e}")
        index = None
        metadata = []
else:
    st.warning("FAISS-Index nicht gefunden. Bitte zuerst `populate_vectordb.py` ausführen.")
    index = None
    metadata = []

# --- Helper Functions ---
def styled_button(label, key=None):
    return st.button(label, key=key)

def parse_bullet_points(text):
    items = re.findall(r"[-*•]\s*(.*)", text)
    return items

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def set_bg_hack(main_bg):
    main_bg_ext = "png"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

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
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    except Exception as e:
        print(f"Fehler beim Extrahieren von Text mit PyPDF2: {e}")
    return text

# --- RAG Functions ---
def get_relevant_documents(query, n_results=3):
    global index, metadata  # Verwende die globalen Variablen

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

def extract_additional_fields_from_pdf_text(text):
    fields = {}
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if "company:" in line.lower():
            fields["company"] = lines[i].split(":", 1)[1].strip()
        elif "location:" in line.lower():
            fields["location"] = lines[i].split(":", 1)[1].strip()
        elif "position type:" in line.lower():
            fields["permanent_position"] = "yes" if "permanent" in lines[i].split(":", 1)[1].strip().lower() else "no"
        elif "full time/part time:" in line.lower():
            fields["full_time"] = "yes" if "full time" in lines[i].split(":", 1)[1].strip().lower() else "no"
        elif "phone number:" in line.lower():
            fields["phone_number"] = lines[i].split(":", 1)[1].strip()
        elif "email address:" in line.lower():
            fields["email"] = lines[i].split(":", 1)[1].strip()
        elif "contact person:" in line.lower():
            fields["contact_person"] = lines[i].split(":", 1)[1].strip()
        elif "salary range:" in line.lower():
            fields["salary_range_pdf"] = lines[i].split(":", 1)[1].strip()
    return fields

# Initialize embedding model globally
embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')
vectorstore = None
qa_chain = None

def initialize_rag(model_name=MODEL_NAME, model_url=OLLAMA_URL):
    global vectorstore, qa_chain

    index_folder = "vector_databases"
    index_file = os.path.join(index_folder, "faiss_index.index")

    if not os.path.exists(index_file):
        st.error(f"Index file not found at {index_file}. Please run populate_vectordb.py first.")
        return False

    # Laden des Index direkt mit faiss.read_index und vollständigem Pfad
    try:
        index = faiss.read_index(index_file) # Vollständigen Pfad direkt verwenden
    except Exception as e:
        st.error(f"Error loading index: {e}")
        return False

    vectorstore = FAISS(embedding_model.embed_query, index, {}, {}) # Leeres Dictionary für docstore und index_to_docstore_id

    llm = OllamaLLM(model=model_name, base_url=model_url)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )

    return True
    
def query_with_rag(query):
    """
    Führt eine RAG-Anfrage mit LangChain durch.
    """
    global qa_chain
    if qa_chain is None:
        print("RAG components not initialized. Call initialize_rag first.")
        return ""
    try:
        result = qa_chain({"query": query})
        return result["result"]
    except Exception as e:
        print(f"Error during RAG query: {e}")
        return ""

def parse_bullet_points(text):
    items = re.findall(r"[-*•]\s*(.*)", text)
    return items

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

def extract_text_from_pdf_pypdf2(pdf_file):
    """Extrahiert Text aus einem PDF mit PyPDF2."""
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    except Exception as e:
        print(f"Fehler beim Extrahieren von Text mit PyPDF2: {e}")
    return text

# Verbesserte Extraktion mit RAG und Fallback-Lösung
def extract_data_from_pdf_rag(pdf_file):
    """
    Extrahiert Daten aus einem PDF mithilfe von RAG.
    Wenn die Extraktion fehlschlägt, wird eine Fallback-Logik mit regulären Ausdrücken verwendet.
    """
    text = extract_text_from_pdf_pypdf2(pdf_file)
    
    extracted_data = {}
    
    # RAG-Anfrage, um alle relevanten Informationen zu extrahieren.
    rag_prompt = f"""
        Extract the following information from the provided PDF text:
        - job_title
        - location
        - contact_person
        - contact_email
        - salary range
        - contract type (full-time/part-time/etc.)
        - tasks (as a bullet point list)
        - benefits (as a bullet point list)
        - company description
        - required_skills (as a bullet point list)
        - number of vacancies
        - desired start date
        - department specific keywords
        - desired certifications
        - level of experience (years)
        - required languages
        - desired education level
        - internal contact person
        - priority of the position (e.g., low, medium, high)
        - travel requirements
        - training budget
        - direct supervisor
        - team size
        - reporting line
        - reason for vacancy
        - current recruitment process description
        - competitor companies
        - tools and technologies used
        - desired soft skills

        If any information is not found, leave it blank.

        Here is the PDF text:
        ---
        {text}
        ---
        Give your answer in JSON Format:
    """
    #st.write(rag_prompt)
    rag_response = query_with_rag(rag_prompt)
    

    # Parse die JSON-Antwort
    try:
        extracted_data = json.loads(rag_response)
        
        # Ensure certain keys are initialized even if not found in extracted_data
        for key in ["tasks", "benefits", "required_skills"]:
          if key not in extracted_data:
            extracted_data[key] = []

        # Konvertiere die Aufgaben und Vorteile in Listen, falls sie als Strings vorliegen
        if isinstance(extracted_data["tasks"], str):
            extracted_data["tasks"] = parse_bullet_points(extracted_data["tasks"])
        if isinstance(extracted_data["benefits"], str):
            extracted_data["benefits"] = parse_bullet_points(extracted_data["benefits"])
        if isinstance(extracted_data["required_skills"], str):
            extracted_data["required_skills"] = parse_bullet_points(extracted_data["required_skills"])


    except json.JSONDecodeError:
        print("Failed to parse RAG response as JSON. Response is not a valid JSON")
        print(rag_response)
        extracted_data = {}  # Setze extracted_data auf ein leeres Dictionary

    return extracted_data

def get_relevant_documents(query, n_results=3):
    global vectorstore
    if vectorstore is None:
        st.warning("Vectorstore not initialized!")
        return []

    try:
        # Verwenden Sie die similarity_search_with_score Methode, um die relevantesten Dokumente zu finden
        results = vectorstore.similarity_search_with_score(query, k=n_results)
        
        # Extrahieren Sie die Inhalte aus den Suchergebnissen und fügen Sie sie relevant_documents hinzu
        relevant_documents = []
        for doc, score in results:
            relevant_documents.append(doc.page_content)  # Verwenden Sie page_content, nicht content
        
        return relevant_documents
    except Exception as e:
        st.error(f"Error during similarity search: {e}")
        return []

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

# --- Core Functions ---
def analyze_role(job_title):
    if not job_title:
        print("Job title: Vanished! Please provide one, I need it.")
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
def generate_job_ad_variations(role_info, company_info, benefits, recruitment_process, audiences, language, styles):
    variations = {}
    for audience in audiences:
        for style in styles:
            relevant_docs = get_relevant_documents(
                query=f"Stellenanzeige für {role_info.get('job_title', '')} für Zielgruppe {audience} im Stil {style}",
                n_results=2
            )
            rag_prompt = rag_enhanced_query(
                query=f"""
                Write a {style} job ad in {language} for a {role_info.get('job_title', '')}.
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
            response = query_ollama(MODEL_NAME, rag_prompt)
            variations[f"{audience}_{style}"] = response
    return variations
def suggest_interview_questions(job_title, focus_areas, n_questions=5):
    questions = []
    for area in focus_areas:
        relevant_docs = get_relevant_documents(
            query=f"Interviewfragen für {job_title} im Bereich {area}",
            n_results=2
        )
        rag_prompt = rag_enhanced_query(
            query=f"""
            Generate {n_questions} interview questions for a {job_title} position focusing on {area}.
            """,
            context_documents=relevant_docs
        )
        response = query_ollama(MODEL_NAME, rag_prompt)
        questions.extend(parse_bullet_points(response))
    return questions[:n_questions]
def generate_onboarding_plan(job_title, department, company_info):
    relevant_docs = get_relevant_documents(
        query=f"Onboarding-Plan für {job_title} in {department}",
        n_results=2
    )
    rag_prompt = rag_enhanced_query(
        query=f"""
        Create a comprehensive onboarding plan for a new {job_title} in the {department} department.
        Company Information: {company_info}
        Include tasks, goals, and resources for the first week, first month, and first three months.
        """,
        context_documents=relevant_docs
    )
    response = query_ollama(MODEL_NAME, rag_prompt)
    return response
def suggest_training_measures(job_title, required_skills):
    relevant_docs = get_relevant_documents(
        query=f"Weiterbildung für {job_title} mit Fokus auf {', '.join(required_skills)}",
        n_results=2
    )
    rag_prompt = rag_enhanced_query(
        query=f"""
        Suggest training measures for a {job_title} to enhance the following skills: {', '.join(required_skills)}.
        """,
        context_documents=relevant_docs
    )
    response = query_ollama(MODEL_NAME, rag_prompt)
    return response
def analyze_company_culture(company_name):
    relevant_docs = get_relevant_documents(
        query=f"Unternehmenskultur von {company_name}",
        n_results=3
    )
    rag_prompt = rag_enhanced_query(
        query=f"""
        Analyze the company culture of {company_name} based on publicly available information.
        """,
        context_documents=relevant_docs
    )
    response = query_ollama(MODEL_NAME, rag_prompt)
    return response
def identify_talent_pools(job_title, required_skills):
    relevant_docs = get_relevant_documents(
        query=f"Talentpools für {job_title} mit Skills {', '.join(required_skills)}",
        n_results=2
    )
    rag_prompt = rag_enhanced_query(
        query=f"""
        Identify promising talent pools for the {job_title} position, considering the required skills: {', '.join(required_skills)}.
        """,
        context_documents=relevant_docs
    )
    response = query_ollama(MODEL_NAME, rag_prompt)
    return response
def analyze_competitors(company_name, job_title):
    relevant_docs = get_relevant_documents(
        query=f"Stellenanzeigen von Konkurrenten von {company_name} für {job_title}",
        n_results=3
    )
    rag_prompt = rag_enhanced_query(
        query=f"""
        Analyze job ads from competitors of {company_name} for the {job_title} position.
        Identify common requirements, benefits, and salary ranges.
        """,
        context_documents=relevant_docs
    )
    response = query_ollama(MODEL_NAME, rag_prompt)
    return response
def check_diversity_inclusion(job_ad):
    relevant_docs = get_relevant_documents(
        query=f"Formulierungen in Stellenanzeigen, die Diversität und Inklusion fördern",
        n_results=2
    )
    rag_prompt = rag_enhanced_query(
        query=f"""
        Analyze the following job ad for language that could be perceived as non-inclusive or discriminatory:
        ---
        {job_ad}
        ---
        Suggest improvements to promote diversity and inclusion.
        """,
        context_documents=relevant_docs
    )
    response = query_ollama(MODEL_NAME, rag_prompt)
    return response
def check_legal_compliance(job_ad, country="Deutschland"):
    relevant_docs = get_relevant_documents(
        query=f"Arbeitsrechtliche Bestimmungen für Stellenanzeigen in {country}",  # Korrektur hier
        n_results=2
    )
    rag_prompt = rag_enhanced_query(
        query=f"""
        Analyze the following job ad for compliance with labor laws in {country}:
        ---
        {job_ad}
        ---
        Identify any potential legal issues.
        """,
        context_documents=relevant_docs
    )
    response = query_ollama(MODEL_NAME, rag_prompt)
    return response

def analyze_trends(industry, job_title):
    relevant_docs = get_relevant_documents(
        query=f"Aktuelle Trends im Recruiting für {job_title} in der Branche {industry}",
        n_results=2
    )
    rag_prompt = rag_enhanced_query(
        query=f"""
        Identify current trends in recruiting for {job_title} in the {industry} industry.
        """,
        context_documents=relevant_docs
    )
    response = query_ollama(MODEL_NAME, rag_prompt)
    return response
def generate_social_media_posts(job_ad, platform="LinkedIn"):
    relevant_docs = get_relevant_documents(
        query=f"Beispiele für Social Media Posts für Stellenanzeigen auf {platform}",
        n_results=2
    )
    rag_prompt = rag_enhanced_query(
        query=f"""
        Generate engaging social media posts for the following job ad on {platform}:
        ---
        {job_ad}
        ---
        """,
        context_documents=relevant_docs
    )
    response = query_ollama(MODEL_NAME, rag_prompt)
    return response
def prepare_interview(role, focus_areas):
    focus_text = ", ".join(focus_areas)
    prompt = f"""
    Generate interview questions for a {role}. Focus on these areas: {focus_text}.
    Provide a mix of behavioral, technical, and situational questions.
    """
    response = query_ollama(MODEL_NAME, prompt)
    return parse_bullet_points(response)

def create_onboarding_checklist(role, department):
    prompt = f"""
    Create a comprehensive onboarding checklist for a {role} in {department}.
    Include tasks, goals, and resources for the first week, first month, and first three months.
    """
    response = query_ollama(MODEL_NAME, prompt)
    return parse_bullet_points(response)
def suggest_retention_strategies(role):
    prompt = f"""
    Suggest effective retention strategies for a {role}.
    Consider factors like career growth, work-life balance, recognition, and compensation.
    """
    response = query_ollama(MODEL_NAME, prompt)
    return parse_bullet_points(response)
def identify_benefits(role, region=None):
    prompt = f"""
    What are some attractive benefits for a {role}?
    """
    if region:
        prompt += f" Consider the region: {region}."
    response = query_ollama(MODEL_NAME, prompt)
    return parse_bullet_points(response)
def define_recruitment_steps(role):
    prompt = f"""
    Define the steps in the recruitment process for a {role}.
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
                info["Industry"] = value
            elif key.lower() == "company location":
                info["Company Location"] = value
            elif key.lower() == "company size":
                info["Company Size"] = value.lower()
            elif key.lower() == "website":
                info["Website"] = value
    return info
# --- Navigation Function ---
def navigate_to_page(page_name):
    st.session_state.page = page_name
# --- Welcome Message Generation ---
def generate_welcome_message():
    if 'welcome_message' not in st.session_state:
        with st.spinner('Generating welcome message...'):
            message = query_ollama(MODEL_NAME, "Generate a concise and welcoming message for users of Cognitive Staffing Vacancy Need Analysis App, an AI-powered recruitment app. Keep it under two sentences. output should contain welcome message only")
            st.session_state.welcome_message = message
    st.sidebar.markdown(st.session_state.welcome_message)

#Seitenstruktur:
def set_bg_hack(main_bg):
    main_bg_ext = "png"
    try:
        with open(main_bg, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: url(data:image/{main_bg_ext};base64,{encoded_string});
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        print(f"Warning: Background image file not found at {main_bg}")

def hide_sidebar_content():
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                .css-1cpxqw2 {display: none;} /* Welcome Message */
                .css-j463ke {display: none;} /* About the app */
                .css-1siy2j7 {display: none;} /* Generate Description */
                .css-pkbazv {display: none;} /* About us */
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
# --- Page Functions ---
def welcome_page():
    st.markdown(
        """
        <style>
        .stApp.max-width-0 .main {
            margin-left: 0;
            margin-right: 0;
            padding: 1em;
        }
        .stApp.max-width-0 .main .block-container {
            max-width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        <style>
        .stApp.max-width-0 .main {
            margin-left: 0;
            margin-right: 0;
            padding: 1em;
        }
        .stApp.max-width-0 .main .block-container {
            max-width: 100%;
        }
        .stApp [data-testid="stText"] {
            text-align: center;
        }
        .stApp [data-testid="stHeader"] {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <div style='color: #0d47a1; font-size: 4em; font-weight: 900; line-height: 1.2; text-align: center;'>{st.session_state.get('welcome_message', 'Welcome to RecruitSmarts')}</div>
            <div style='color: #0d47a1; font-size: 2.5em; font-weight: 600; line-height: 1.2; text-align: center;'>Revolutionize Your Hiring with AI</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <p style="font-size: 1.1em; color: #0d47a1; margin-bottom: 1.5em; line-height: 1.6; text-align: center;">
        Stop losing critical information in the early stages of recruitment.
        <b>RecruitSmarts</b> leverages the power of <b>local AI</b> to help you capture every essential detail about your open positions.
        </p>
        """,
        unsafe_allow_html=True,
    )
    # PDF Upload
    uploaded_file = st.file_uploader("Upload a PDF job description", type="pdf")
    if uploaded_file is not None:
        # Extrahieren des Textes
        text = extract_text_from_pdf_pypdf2(uploaded_file)
        if text:
            st.success("PDF uploaded and text extracted successfully!")
            # Daten extrahieren
            extracted_data = extract_data_from_pdf_rag(uploaded_file)
            # Session state aktualisieren
            st.session_state.pdf_text = text
            st.session_state.role_info["job_title"] = extracted_data.get("job_title", "")
            st.session_state.role_info["location"] = extracted_data.get("location", "")
            st.session_state.company_info["Company Name"] = extracted_data.get("company_name", "")
            st.session_state.tasks = extracted_data.get("tasks", [])
            st.session_state.benefits = extracted_data.get("benefits", [])
            st.session_state.company_info["company_description"] = extracted_data.get("company_description", "")
            st.session_state.role_info["required_skills"] = extracted_data.get("required_skills", [])
            st.session_state.role_info["Number of Vacancies"] = extracted_data.get("number_of_vacancies", 1)
            st.session_state.role_info["Start Date"] = extracted_data.get("start_date", None)
            st.session_state.role_info["department_specific_keywords"] = extracted_data.get("department_specific_keywords", "")
            st.session_state.role_info["desired_certifications"] = extracted_data.get("desired_certifications", "")
            st.session_state.role_info["level_experience_min"] = extracted_data.get("level_experience_min", 0)
            st.session_state.role_info["level_experience_max"] = extracted_data.get("level_experience_max", 10)
            st.session_state.role_info["languages"] = extracted_data.get("languages", "")
            st.session_state.role_info["education_level"] = extracted_data.get("education_level", "")
            st.session_state.role_info["internal_contact_person"] = extracted_data.get("internal_contact_person", "")
            st.session_state.role_info["priority"] = extracted_data.get("priority", "")
            st.session_state.role_info["travel_requirements"] = extracted_data.get("travel_requirements", "")
            st.session_state.role_info["training_budget"] = extracted_data.get("training_budget", 0)
            st.session_state.role_info["direct_supervisor"] = extracted_data.get("direct_supervisor", "")
            st.session_state.role_info["team_size"] = extracted_data.get("team_size", 0)
            st.session_state.role_info["reporting_line"] = extracted_data.get("reporting_line", "")
            st.session_state.role_info["reason_vacancy"] = extracted_data.get("reason_vacancy", "")
            st.session_state.role_info["current_recruitment_process"] = extracted_data.get("current_recruitment_process", "")
            st.session_state.role_info["competitor_companies"] = extracted_data.get("competitor_companies", "")
            st.session_state.role_info["tools_technologies"] = extracted_data.get("tools_technologies", "")
            st.session_state.role_info["soft_skills"] = extracted_data.get("soft_skills", "")
            st.session_state.role_info["contract_type"] = extracted_data.get("contract_type", "")
            st.session_state.role_info["salary_range"] = extracted_data.get("salary_range", "")
            st.session_state.role_info["contact_person"] = extracted_data.get("contact_person", "")
            st.session_state.role_info["contact_email"] = extracted_data.get("contact_email", "")
            # ... (weitere Felder hier einfügen, z.B. contact_person, contact_email, etc.)
            # Button, um die Analyse zu starten
            if st.button("Proceed to Data Review", key="start_button"):
                navigate_to_page("data_extraction_page")
        else:
            st.error("Could not extract text from PDF. Please try another file or use the manual input.")
    # --- MANUELLER INPUT ---
    st.markdown('<p style="font-size: 1.1em; color: #0d47a1; font-weight: 600; margin-bottom: 0.5em; margin-top: 1em; text-align: center;">...or enter job title manually</p>', unsafe_allow_html=True)
    st.session_state.job_title = st.text_input(
        label="Enter Your Vacancy Title to Begin",
        value=st.session_state.role_info.get("job_title", ""),
        placeholder="e.g., Data Scientist, Marketing Guru, Python Developer",
        key="job_title_input",
        label_visibility='collapsed'
    )
    st.session_state.role_info["job_title"] = st.session_state.job_title
    st.markdown(
        """
        <div style="display: flex; justify-content: center;">
        """,
        unsafe_allow_html=True
    )
    if st.session_state.job_title and st.button("**Start Building Your Ideal Candidate Profile**", key="start_button_manual"):
        navigate_to_page("data_extraction_page")
    
    st.markdown("</div>", unsafe_allow_html=True)
def about_us_page():
    st.markdown(
        """
        <p style="font-size: 1.1em; color: #e6edf3; margin-bottom: 1.5em; line-height: 1.6;">
        RecruitSmarts is an AI-powered talent acquisition app designed to streamline the hiring process. 
        </p>
        """,
        unsafe_allow_html=True,
    )
def data_extraction_page():
    st.header("Review and Edit Extracted Data")
    if "pdf_text" in st.session_state:
        st.subheader("Data Extracted from PDF")
        # Example for job_title
        st.session_state.role_info["job_title"] = st.text_input("Job Title", value=st.session_state.role_info.get("job_title", ""), key="job_title_extracted")
        # Example for location
        st.session_state.role_info["location"] = st.text_input("Location", value=st.session_state.role_info.get("location", ""), key="location_extracted")
        # Example for tasks
        st.session_state.tasks = st.text_area("Tasks", value="\n".join(st.session_state.tasks), key="tasks_extracted")
        # Example for company name
        st.session_state.company_info["Company Name"] = st.text_input("Company Name", value=st.session_state.company_info.get("Company Name", ""), key="company_name_extracted")
        # Füge alle anderen relevanten Felder hier hinzu, z.B.:
        st.session_state.role_info["contact_person"] = st.text_input("Contact Person", value=st.session_state.role_info.get("contact_person", ""), key="contact_person_extracted")
        st.session_state.role_info["contact_email"] = st.text_input("Contact Email", value=st.session_state.role_info.get("contact_email", ""), key="contact_email_extracted")
        st.session_state.role_info["salary_range"] = st.text_input("Salary Range", value=st.session_state.role_info.get("salary_range", ""), key="salary_range_extracted")
        st.session_state.role_info["contract_type"] = st.text_input("Contract Type", value=st.session_state.role_info.get("contract_type", ""), key="contract_type_extracted")
        st.session_state.benefits = st.text_area("Benefits", value="\n".join(st.session_state.benefits), key="benefits_extracted")
        st.session_state.company_info["company_description"] = st.text_area("Company Description", value=st.session_state.company_info.get("company_description", ""), key="company_description_extracted")
        st.session_state.role_info["required_skills"] = st.text_area("Required Skills", value="\n".join(st.session_state.role_info.get("required_skills", [])), key="required_skills_extracted")
        st.session_state.role_info["Number of Vacancies"] = st.number_input("Number of Vacancies", value=st.session_state.role_info.get("Number of Vacancies", 1), key="vacancies_extracted")
        st.session_state.role_info["Start Date"] = st.date_input("Desired Start Date", value=st.session_state.role_info.get("Start Date"), key="start_date_extracted")
        st.session_state.role_info["department_specific_keywords"] = st.text_input("Department-Specific Keywords", value=st.session_state.role_info.get("department_specific_keywords", ""), key="keywords_extracted")
        st.session_state.role_info["desired_certifications"] = st.text_input("Desired Certifications", value=st.session_state.role_info.get("desired_certifications", ""), key="certifications_extracted")
        st.session_state.role_info["level_experience_min"] = st.number_input("Minimum Years of Experience", value=st.session_state.role_info.get("level_experience_min", 0), key="experience_min_extracted")
        st.session_state.role_info["level_experience_max"] = st.number_input("Maximum Years of Experience", value=st.session_state.role_info.get("level_experience_max", 10), key="experience_max_extracted")
        st.session_state.role_info["languages"] = st.text_input("Required Languages", value=st.session_state.role_info.get("languages", ""), key="languages_extracted")
        st.session_state.role_info["education_level"] = st.text_input("Desired Education Level", value=st.session_state.role_info.get("education_level", ""), key="education_extracted")
        st.session_state.role_info["internal_contact_person"] = st.text_input("Internal Contact Person", value=st.session_state.role_info.get("internal_contact_person", ""), key="internal_contact_extracted")
        st.session_state.role_info["priority"] = st.text_input("Priority of the Position", value=st.session_state.role_info.get("priority", ""), key="priority_extracted")
        st.session_state.role_info["travel_requirements"] = st.text_input("Travel Requirements", value=st.session_state.role_info.get("travel_requirements", ""), key="travel_extracted")
        st.session_state.role_info["training_budget"] = st.number_input("Training Budget", value=st.session_state.role_info.get("training_budget", 0), key="training_budget_extracted")
        st.session_state.role_info["direct_supervisor"] = st.text_input("Direct Supervisor", value=st.session_state.role_info.get("direct_supervisor", ""), key="supervisor_extracted")
        st.session_state.role_info["team_size"] = st.number_input("Team Size", value=st.session_state.role_info.get("team_size", 0), key="team_size_extracted")
        st.session_state.role_info["reporting_line"] = st.text_input("Reporting Line", value=st.session_state.role_info.get("reporting_line", ""), key="reporting_line_extracted")
        st.session_state.role_info["reason_vacancy"] = st.text_input("Reason for Vacancy", value=st.session_state.role_info.get("reason_vacancy", ""), key="reason_extracted")
        st.session_state.role_info["current_recruitment_process"] = st.text_area("Current Recruitment Process Description", value=st.session_state.role_info.get("current_recruitment_process", ""), key="recruitment_process_extracted")
        st.session_state.role_info["competitor_companies"] = st.text_input("Competitor Companies", value=st.session_state.role_info.get("competitor_companies", ""), key="competitors_extracted")
        st.session_state.role_info["tools_technologies"] = st.text_input("Tools and Technologies Used", value=st.session_state.role_info.get("tools_technologies", ""), key="tools_extracted")
        st.session_state.role_info["soft_skills"] = st.text_input("Desired Soft Skills", value=st.session_state.role_info.get("soft_skills", ""), key="soft_skills_extracted")

    
    else:
        st.subheader("Manually Entered Data")
        # Job Title (already entered on welcome_page)
        st.write(f"Job Title: {st.session_state.role_info['job_title']}")
        # Example for location
        st.session_state.role_info["location"] = st.text_input("Location", value=st.session_state.role_info.get("location", ""), key="location_manual")
        # ... (Add fields for other data to be entered manually)
    if st.button("Next"):
        st.session_state.page = "company_details_page"
        st.rerun()

if __name__ == "__main__":
    main()