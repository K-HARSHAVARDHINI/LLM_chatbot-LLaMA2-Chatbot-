from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3, re, os, datetime
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import requests
import traceback
import tempfile

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "order_management.db"
chat_memory = {}
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# 🛠 Create embedded DB chat log table
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp TEXT,
                user_query TEXT,
                bot_response TEXT
            )
        """)

init_db()

def load_faq_embeddings():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT question, keywords, answer FROM faq")
    faq_raw = cursor.fetchall()
    conn.close()

    faq_list = []
    for question, keywords, answer in faq_raw:
        combined = f"{question} {keywords}".strip()
        embedding = embed_model.encode(combined)
        faq_list.append({
            "question": question,
            "keywords": keywords,
            "answer": answer,
            "embedding": embedding
        })
    return faq_list

faq_embeddings = load_faq_embeddings()

def rag_retrieve_faq(user_query, threshold=0.7):
    user_embedding = embed_model.encode(user_query)
    similarities = [
        (faq, cosine_similarity([user_embedding], [faq["embedding"]])[0][0])
        for faq in faq_embeddings
    ]
    best_match, best_score = max(similarities, key=lambda x: x[1])
    return best_match["answer"] if best_score >= threshold else None

def query_llama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama2", "prompt": prompt, "stream": False}
    )
    return response.json()["response"]

def classify_intent(user_input):
    system_prompt = "Classify the user's intent as one of the following: product_info, order_status, faq, greeting, goodbye, unknown. Only return the label."
    prompt = f"{system_prompt}\nUser: {user_input}\nIntent:"
    return query_llama(prompt).strip().lower()

def generate_sql_from_prompt(user_prompt, intent):
    prompt = f"""You're an expert SQL assistant. Generate a clean SQLite SQL query for table `{intent}` based on the user's question. Do NOT include markdown or formatting.

User: {user_prompt}
SQL:"""
    raw_sql = query_llama(prompt)
    cleaned_sql = re.sub(r"```(?:sql)?", "", raw_sql).strip("` \n")
    return cleaned_sql

def run_sql(query, table):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        print("Executing SQL:", query)
        cursor.execute(query)
        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        return [dict(zip(col_names, row)) for row in rows]
    except Exception as e:
        print("SQL Error:", e)
        if table == "product_info":
            return run_fallback_product_search(query)
        elif table == "order_status":
            return run_fallback_order_search(query)
        return [{"error": f"SQL execution failed: {str(e)}"}]
    finally:
        conn.close()

def run_fallback_product_search(prompt):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    keywords = re.findall(r'\b\w+\b', prompt.lower())
    cursor.execute("SELECT * FROM product_info")
    results = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]
    matched = [dict(zip(cols, r)) for r in results if any(k in str(r).lower() for k in keywords)]
    conn.close()
    return matched

def run_fallback_order_search(prompt):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    order_id = re.search(r'\bORD\d+\b', prompt, re.IGNORECASE)
    if order_id:
        order_id_val = order_id.group().upper()
        cursor.execute("SELECT * FROM order_status WHERE UPPER(order_id) = ?", (order_id_val,))
        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        conn.close()
        return [dict(zip(col_names, row)) for row in rows]
    conn.close()
    return []

def format_response_naturally(results):
    if not results:
        return "Sorry, I couldn't find any results."
    if "error" in results[0]:
        return results[0]["error"]
    table_headers = results[0].keys()
    lines = [" | ".join(table_headers)]
    lines.append("-" * len(lines[0]))
    for row in results:
        lines.append(" | ".join(str(v) for v in row.values()))
    return "\n".join(lines)

def log_chat(user, query, response):
    now = datetime.datetime.now().isoformat()
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO chat_log (session_id, timestamp, user_query, bot_response) VALUES (?, ?, ?, ?)",
            (user, now, query, response)
        )

class ChatRequest(BaseModel):
    session_id: str
    prompt: str
    language: str = "en"

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        user_input = req.prompt
        user_id = req.session_id

        if re.search(r'\b(hi|hello|hey)\b', user_input.lower()):
            reply = "Hello! How can I assist you today?"
        else:
            rag_answer = rag_retrieve_faq(user_input)
            if rag_answer:
                reply = rag_answer
            else:
                intent = classify_intent(user_input)
                if intent == "unknown":
                    reply = "I'm not sure how to help with that. Could you please rephrase?"
                else:
                    sql = generate_sql_from_prompt(user_input, intent)
                    results = run_sql(sql, intent)
                    reply = format_response_naturally(results)

        chat_memory.setdefault(user_id, []).append((user_input, reply))
        log_chat(user_id, user_input, reply)

        return {"response": reply}
    except Exception:
        traceback.print_exc()
        return {"response": "⚠️ Internal error occurred."}

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Service is running ✅"}

@app.get("/test-db")
async def test_database():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("SELECT 1")
        return {"db_status": "connected ✅"}
    except Exception as e:
        return {"db_status": f"error ❌ - {str(e)}"}

@app.get("/chat-log/{session_id}")
async def get_chat_log(session_id: str):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, user_query, bot_response FROM chat_log WHERE session_id = ?", (session_id,))
        rows = cursor.fetchall()
    if not rows:
        return {"log": "No logs found for this session."}
    log_text = "\n".join(f"[{ts}] USER: {uq}\nBOT: {br}\n" for ts, uq, br in rows)
    return {"log": log_text}

@app.get("/download-chat/{session_id}")
async def download_chat_log(session_id: str):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, user_query, bot_response FROM chat_log WHERE session_id = ?", (session_id,))
        rows = cursor.fetchall()

    if not rows:
        return {"message": "No chat found for this session ID."}

    content = "\n".join(f"[{ts}] USER: {uq}\nBOT: {br}\n" for ts, uq, br in rows)
    
    # Create a temp file for download
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as tmpfile:
        tmpfile.write(content)
        tmpfile_path = tmpfile.name

    return FileResponse(tmpfile_path, filename=f"chat_log_{session_id}.txt", media_type='text/plain')
