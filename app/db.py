import os
import mysql.connector
from mysql.connector import DictCursor
from datetime import datetime
from zoneinfo import ZoneInfo
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

tz = ZoneInfo("Europe/Berlin")

def get_db_connection():
    try:
        host = os.getenv('TIDB_HOST')
        port = int(os.getenv('TIDB_PORT'))
        database = os.getenv('TIDB_DB')
        user = os.getenv('TIDB_USER')
        password = os.getenv('TIDB_PASSWORD')
        
        return mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to database: {err}")
        raise

def init_db():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS feedback")
            cur.execute("DROP TABLE IF EXISTS conversations")

            cur.execute("""
                CREATE TABLE conversations (
                    id VARCHAR(255) PRIMARY KEY,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    course TEXT NOT NULL,
                    model_used TEXT NOT NULL,
                    response_time FLOAT NOT NULL,
                    relevance TEXT NOT NULL,
                    relevance_explanation TEXT NOT NULL,
                    prompt_tokens INT NOT NULL,
                    completion_tokens INT NOT NULL,
                    total_tokens INT NOT NULL,
                    eval_prompt_tokens INT NOT NULL,
                    eval_completion_tokens INT NOT NULL,
                    eval_total_tokens INT NOT NULL,
                    openai_cost FLOAT NOT NULL,
                    timestamp TIMESTAMP NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE feedback (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    conversation_id VARCHAR(255),
                    feedback INT NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                )
            """)
        conn.commit()
        logging.info("Database initialized successfully.")
    except mysql.connector.Error as err:
        logging.error(f"Error initializing database: {err}")
    finally:
        conn.close()

def save_conversation(conversation_id, question, answer_data, course, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now(tz)

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO conversations 
                (id, question, answer, course, model_used, response_time, relevance, 
                relevance_explanation, prompt_tokens, completion_tokens, total_tokens, 
                eval_prompt_tokens, eval_completion_tokens, eval_total_tokens, openai_cost, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    conversation_id,
                    question,
                    answer_data["answer"],
                    course,
                    answer_data["model_used"],
                    answer_data["response_time"],
                    answer_data["relevance"],
                    answer_data["relevance_explanation"],
                    answer_data["prompt_tokens"],
                    answer_data["completion_tokens"],
                    answer_data["total_tokens"],
                    answer_data["eval_prompt_tokens"],
                    answer_data["eval_completion_tokens"],
                    answer_data["eval_total_tokens"],
                    answer_data["openai_cost"],
                    timestamp,
                ),
            )
        conn.commit()
        logging.info("Conversation saved successfully.")
    except mysql.connector.Error as err:
        logging.error(f"Error saving conversation: {err}")
    finally:
        conn.close()

def save_feedback(conversation_id, feedback, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now(tz)

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO feedback (conversation_id, feedback, timestamp) VALUES (%s, %s, %s)",
                (conversation_id, feedback, timestamp),
            )
        conn.commit()
        logging.info("Feedback saved successfully.")
    except mysql.connector.Error as err:
        logging.error(f"Error saving feedback: {err}")
    finally:
        conn.close()

def get_recent_conversations(limit=5, relevance=None):
    conn = get_db_connection()
    try:
        with conn.cursor(dictionary=True) as cur:
            query = """
                SELECT c.*, f.feedback
                FROM conversations c
                LEFT JOIN feedback f ON c.id = f.conversation_id
            """
            if relevance:
                query += " WHERE c.relevance = %s"
                params = (relevance, limit)
            else:
                params = (limit,)

            query += " ORDER BY c.timestamp DESC LIMIT %s"

            cur.execute(query, params)
            return cur.fetchall()
    except mysql.connector.Error as err:
        logging.error(f"Error fetching recent conversations: {err}")
        return []
    finally:
        conn.close()

def get_feedback_stats():
    conn = get_db_connection()
    try:
        with conn.cursor(dictionary=True) as cur:
            cur.execute("""
                SELECT 
                    SUM(CASE WHEN feedback > 0 THEN 1 ELSE 0 END) as thumbs_up,
                    SUM(CASE WHEN feedback < 0 THEN 1 ELSE 0 END) as thumbs_down
                FROM feedback
            """)
            return cur.fetchone()
    except mysql.connector.Error as err:
        logging.error(f"Error fetching feedback stats: {err}")
        return {'thumbs_up': 0, 'thumbs_down': 0}
    finally:
        conn.close()
