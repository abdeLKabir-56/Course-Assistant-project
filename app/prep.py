import os
import requests
import pandas as pd
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text
from tqdm.auto import tqdm
from dotenv import load_dotenv

load_dotenv()

# Load configuration from environment variables
TIDB_HOST = os.getenv("TIDB_HOST")
TIDB_PORT = os.getenv("TIDB_PORT")
TIDB_USER = os.getenv("TIDB_USER")
TIDB_PASSWORD = os.getenv("TIDB_PASSWORD")
TIDB_DATABASE = os.getenv("TIDB_DATABASE")
MODEL_NAME = os.getenv("MODEL_NAME")
TABLE_NAME = os.getenv("TABLE_NAME")

# TiDB connection URL
TIDB_URL = f"mysql+pymysql://{TIDB_USER}:{TIDB_PASSWORD}@{TIDB_HOST}:{TIDB_PORT}/{TIDB_DATABASE}"

BASE_URL = "https://github.com/DataTalksClub/llm-zoomcamp/blob/main"

def fetch_documents():
    print("Fetching documents...")
    relative_url = "03-vector-search/eval/documents-with-ids.json"
    docs_url = f"{BASE_URL}/{relative_url}?raw=1"
    docs_response = requests.get(docs_url)
    documents = docs_response.json()
    print(f"Fetched {len(documents)} documents")
    return documents

def fetch_ground_truth():
    print("Fetching ground truth data...")
    relative_url = "03-vector-search/eval/ground-truth-data.csv"
    ground_truth_url = f"{BASE_URL}/{relative_url}?raw=1"
    df_ground_truth = pd.read_csv(ground_truth_url)
    df_ground_truth = df_ground_truth[
        df_ground_truth.course == "machine-learning-zoomcamp"
    ]
    ground_truth = df_ground_truth.to_dict(orient="records")
    print(f"Fetched {len(ground_truth)} ground truth records")
    return ground_truth

def load_model():
    print(f"Loading model: {MODEL_NAME}")
    return SentenceTransformer(MODEL_NAME)

def setup_tidb():
    print("Setting up TiDB...")
    engine = create_engine(TIDB_URL)
    with engine.connect() as connection:
        connection.execute(text(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id VARCHAR(255) PRIMARY KEY,
                question TEXT,
                text TEXT,
                course VARCHAR(255),
                question_text_vector BLOB
            )
        """))
    print(f"TiDB table '{TABLE_NAME}' created")
    return engine

def index_documents(engine, documents, model):
    print("Indexing documents...")
    with engine.connect() as connection:
        for doc in tqdm(documents):
            question = doc["question"]
            text = doc["text"]
            doc["question_text_vector"] = model.encode(question + " " + text).tolist()
            
            # Convert list to binary format
            question_text_vector = bytes(doc["question_text_vector"])
            
            connection.execute(text(f"""
                INSERT INTO {TABLE_NAME} (id, question, text, course, question_text_vector)
                VALUES (:id, :question, :text, :course, :question_text_vector)
                ON DUPLICATE KEY UPDATE
                question = VALUES(question),
                text = VALUES(text),
                course = VALUES(course),
                question_text_vector = VALUES(question_text_vector)
            """), {
                "id": doc["id"],
                "question": question,
                "text": text,
                "course": doc["course"],
                "question_text_vector": question_text_vector
            })
    print(f"Indexed {len(documents)} documents")

def main():
    print("Starting the indexing process...")

    documents = fetch_documents()
    ground_truth = fetch_ground_truth()
    model = load_model()
    engine = setup_tidb()
    index_documents(engine, documents, model)

    print("Indexing process completed successfully!")

if __name__ == "__main__":
    main()
