# config.py
MODEL_NAME = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"
DATA_DIR = "data/processed"  # Pfad zu den Daten für den FAISS-Index relativ zu app.py
INDEX_PATH = "vector_databases/faiss_index.index"  # Pfad zur FAISS-Indexdatei relativ zu app.py
DIMENSION = 768