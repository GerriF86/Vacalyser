# config.py
import os

# General Configuration
DEFAULT_LANGUAGE = "en"  # Changed to English

# URL Validation Pattern
URL_PATTERN = r"^(https?://)?(www\.)?([a-zA-Z0-9-]+)\.([a-z]{2,6})(\.[a-z]{2,6})?([/?].*)?$"

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "filename": "app.log",
}

# Model Configuration
MODEL_NAME = "llama3.2:3b"  # Model name for Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"  # URL to the Ollama API

# FAISS Configuration
DATA_DIR = "data/processed"
INDEX_PATH = "vector_databases"
DIMENSION = 768  # Dimension of embeddings (adjust if necessary)

# Job Categories for FAISS Specialization
FAISS_JOB_CATEGORIES = [
    "Accountant",
    "Agriculture",
    "Apparel",
    "Arts",
    "Automotive",
    "Aviation",
    "Banking",
    "Business-Development",
    "Construction",
    "Engineering",
    "Finance",
    "Healthcare",
    "HR",
    "IT",
    "PR",
    "Sales",
    "Teacher",
]