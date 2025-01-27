import json
from langchain_community.vectorstores import FAISS
import os
from tqdm import tqdm
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

DATA_DIR = "data/processed"
INDEX_PATH = "vector_databases"  # Still just the directory
DB_NAME = "index" # The desired name of the index file
DIMENSION = 768

def load_data(data_dir):
    """
    Loads data from JSON files and returns it as a list of dictionaries.
    """
    print(f"Loading data from: {data_dir}")
    data = []
    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".json"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding='utf-8') as f:
                    try:
                        job_data = json.load(f)
                        job_data['job_description'] = job_data.get('job_description', '')
                        if data_dir in root:
                            relative_root = os.path.relpath(root, data_dir)
                        else:
                            relative_root = ""
                        job_data['id'] = os.path.join(relative_root, file[:-5])
                        data.append(job_data)
                    except json.JSONDecodeError:
                        print(f"Error parsing {filepath}")
    print(f"Found data records: {len(data)}")
    return data

def create_and_save_faiss_index(data, index_path=INDEX_PATH, db_name=DB_NAME):
    """
    Creates a FAISS index using LangChain, adds data, and saves it.
    """
    try:
        # Instantiate embedding model
        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )

        # Create a list of Documents (required by LangChain's FAISS)
        documents = [
            Document(page_content=item["job_description"], metadata={"id": item["id"]})
            for item in data
        ]

        # Create the FAISS index using from_documents
        print(f"Creating FAISS index: {db_name} with dimension {DIMENSION}")
        faiss_index = FAISS.from_documents(documents, embedding)

        # Save the index using save_local (LangChain's method)
        faiss_index.save_local(index_path, index_name=db_name)
        print(f"FAISS index saved to {index_path}/{db_name}")

        return faiss_index

    except Exception as e:
        print(f"Error creating or saving the index: {e}")
        return None

def main():
    """
    Loads the data, creates the FAISS index using LangChain, and saves it.
    """
    data = load_data(DATA_DIR)
    print(f"Number of loaded data records in main(): {len(data)}")
    if not data:
        print("No data found. Exiting script.")
        return

    # Sort the data alphabetically by job title
    data.sort(key=lambda x: x.get('job_title', ''))

    faiss_index = create_and_save_faiss_index(data, INDEX_PATH)
    if faiss_index:
        print("Index successfully created.")
    else:
        print("Error creating the index.")

if __name__ == "__main__":
    main()