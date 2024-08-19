import os
import time
import json
import logging
import pymysql

from openai import OpenAI
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
TIDB_HOST = os.getenv("TIDB_HOST")
TIDB_PORT = int(os.getenv("TIDB_PORT"))
TIDB_USER = os.getenv("TIDB_USER")
TIDB_PASSWORD = os.getenv("TIDB_PASSWORD")
TIDB_DATABASE = os.getenv("TIDB_DATABASE")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434/v1/")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize clients
tidb_connection = pymysql.connect(
    host=TIDB_HOST,
    port=TIDB_PORT,
    user=TIDB_USER,
    password=TIDB_PASSWORD,
    database=TIDB_DATABASE
)
ollama_client = OpenAI(base_url=OLLAMA_URL, api_key="ollama")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize model
model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

def tidb_search_text(query, course, table_name="course_questions"):
    search_query = f"""
    SELECT section, question, text
    FROM {table_name}
    WHERE course = %s
    AND (MATCH(question) AGAINST(%s IN BOOLEAN MODE) 
         OR MATCH(text) AGAINST(%s IN BOOLEAN MODE))
    LIMIT 5
    """
    try:
        with tidb_connection.cursor() as cursor:
            cursor.execute(search_query, (course, query, query))
            results = cursor.fetchall()
        return [dict(zip([desc[0] for desc in cursor.description], row)) for row in results]
    except Exception as e:
        logging.error(f"Error during TiDB text search: {e}")
        return []

def tidb_search_knn(vector, course, table_name="course_questions"):
    # Note: TiDB does not natively support KNN search; this is a placeholder
    # Implement custom KNN search logic if needed or use a different tool for vector search
    return []

def build_prompt(query, search_results):
    prompt_template = """
    You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
    Use only the facts from the CONTEXT when answering the QUESTION.

    QUESTION: {question}

    CONTEXT: 
    {context}
    """.strip()

    context = "\n\n".join(
        [
            f"section: {doc['section']}\nquestion: {doc['question']}\nanswer: {doc['text']}"
            for doc in search_results
        ]
    )
    return prompt_template.format(question=query, context=context).strip()

def llm(prompt, model_choice):
    start_time = time.time()
    try:
        if model_choice.startswith('ollama/'):
            response = ollama_client.chat.completions.create(
                model=model_choice.split('/')[-1],
                messages=[{"role": "user", "content": prompt}]
            )
        elif model_choice.startswith('openai/'):
            response = openai_client.chat.completions.create(
                model=model_choice.split('/')[-1],
                messages=[{"role": "user", "content": prompt}]
            )
        else:
            raise ValueError(f"Unknown model choice: {model_choice}")

        answer = response.choices[0].message.content
        tokens = {
            'prompt_tokens': response.usage.prompt_tokens,
            'completion_tokens': response.usage.completion_tokens,
            'total_tokens': response.usage.total_tokens
        }
        end_time = time.time()
        response_time = end_time - start_time

        return answer, tokens, response_time

    except Exception as e:
        logging.error(f"Error during LLM interaction: {e}")
        return "Error", {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}, 0

def evaluate_relevance(question, answer):
    prompt_template = """
    You are an expert evaluator for a Retrieval-Augmented Generation (RAG) system.
    Your task is to analyze the relevance of the generated answer to the given question.
    Based on the relevance of the generated answer, you will classify it
    as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

    Here is the data for evaluation:

    Question: {question}
    Generated Answer: {answer}

    Please analyze the content and context of the generated answer in relation to the question
    and provide your evaluation in parsable JSON without using code blocks:

    {{
      "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
      "Explanation": "[Provide a brief explanation for your evaluation]"
    }}
    """.strip()

    prompt = prompt_template.format(question=question, answer=answer)
    evaluation, tokens, _ = llm(prompt, 'openai/gpt-4o-mini')
    
    try:
        json_eval = json.loads(evaluation)
        return json_eval['Relevance'], json_eval['Explanation'], tokens
    except json.JSONDecodeError:
        logging.error("Failed to parse evaluation response.")
        return "UNKNOWN", "Failed to parse evaluation", tokens

def calculate_openai_cost(model_choice, tokens):
    openai_cost = 0

    if model_choice == 'openai/gpt-3.5-turbo':
        openai_cost = (tokens['prompt_tokens'] * 0.0015 + tokens['completion_tokens'] * 0.002) / 1000
    elif model_choice in ['openai/gpt-4o', 'openai/gpt-4o-mini']:
        openai_cost = (tokens['prompt_tokens'] * 0.03 + tokens['completion_tokens'] * 0.06) / 1000

    return openai_cost

def get_answer(query, course, model_choice, search_type):
    if search_type == 'Vector':
        vector = model.encode(query)
        search_results = tidb_search_knn(vector, course)
    else:
        search_results = tidb_search_text(query, course)

    prompt = build_prompt(query, search_results)
    answer, tokens, response_time = llm(prompt, model_choice)
    
    relevance, explanation, eval_tokens = evaluate_relevance(query, answer)

    openai_cost = calculate_openai_cost(model_choice, tokens)

    return {
        'answer': answer,
        'response_time': response_time,
        'relevance': relevance,
        'relevance_explanation': explanation,
        'model_used': model_choice,
        'prompt_tokens': tokens['prompt_tokens'],
        'completion_tokens': tokens['completion_tokens'],
        'total_tokens': tokens['total_tokens'],
        'eval_prompt_tokens': eval_tokens['prompt_tokens'],
        'eval_completion_tokens': eval_tokens['completion_tokens'],
        'eval_total_tokens': eval_tokens['total_tokens'],
        'openai_cost': openai_cost
    }
