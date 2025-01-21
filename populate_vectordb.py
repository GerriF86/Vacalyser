import faiss
import json
import os
import numpy as np
from tqdm import tqdm  # Korrektur: Importiere tqdm direkt
from langchain_huggingface import HuggingFaceEmbeddings

DATA_DIR = "data/processed"  # Pfad zu den Daten für den FAISS-Index relativ zu app.py
INDEX_PATH = "vector_databases/faiss_index.index"  # Pfad zur FAISS-Indexdatei relativ zu app.py
DIMENSION = 768

def load_data(data_dir):
    """
    Lädt die Daten aus den JSON-Dateien und gibt sie als Liste von Dictionaries zurück.
    """
    print(f"Lade Daten aus: {data_dir}")
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
                        print(f"Fehler beim Parsen von {filepath}")
    print(f"Gefundene Datensätze: {len(data)}")
    return data

def create_embedding_vector_db(chunks, db_name="faiss_index"):
    """
    Erstellt einen FAISS-Index, fügt die Vektoren der Daten hinzu und speichert den Index.
    """
    try:
        # Instantiate embedding model (without GPU)
        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
        )

        # Erstelle einen leeren Index
        print(f"Erstelle Index: {db_name} mit Dimension {DIMENSION}")
        index = faiss.IndexFlatL2(DIMENSION)

        batch_size = 16

        with tqdm(total=len(chunks), desc=f"Erstelle Index {db_name}") as pbar:
            for i in range(0, len(chunks), batch_size):
                chunk_batch = chunks[i:i + batch_size]

                # Embeddings für den aktuellen Batch von Chunks berechnen
                embeddings = embedding.embed_documents([chunk['job_description'] for chunk in chunk_batch])

                # Konvertiere die Liste der Embeddings in ein NumPy-Array
                vectors_array = np.array(embeddings).astype('float32')

                # Füge die Vektoren zum Index hinzu
                print(f"Füge {len(vectors_array)} Vektoren zum Index hinzu.")
                index.add(vectors_array)
                pbar.update(len(chunk_batch))

        # Erstelle das Verzeichnis, falls es nicht existiert
        index_dir = os.path.dirname(INDEX_PATH)
        os.makedirs(index_dir, exist_ok=True)

        # Speichere den Index (korrigierter Dateiname)
        index_path = os.path.join(index_dir, f"{db_name}.index")  # Speichere als .index
        print(f"Speichere Index in {index_path}")
        faiss.write_index(index, index_path)
        print(f"FAISS-Index wurde in {index_path} gespeichert.")
        return index

    except Exception as e:
        print(f"Fehler beim Erstellen oder Speichern des Index: {e}")
        return None

def main():
    """
    Lädt die Daten, erstellt den FAISS-Index und speichert ihn.
    """
    data = load_data(DATA_DIR)
    print(f"Anz. der geladenen Datensätze in main(): {len(data)}")
    if not data:
        print("Keine Daten gefunden. Beende Skript.")
        return

    # Sortiere die Daten alphabetisch nach dem Jobtitel
    data.sort(key=lambda x: x.get('job_title', ''))

    index = create_embedding_vector_db(chunks=data, db_name="faiss_index") #Statt create_and_populate_index(data)
    print(f"Index: {index}")
    if index:
        print("Index erfolgreich erstellt.")
    else:
        print("Fehler beim Erstellen des Index.")

if __name__ == "__main__":
    main()