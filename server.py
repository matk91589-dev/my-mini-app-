from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime, time, sqlite3

app = FastAPI()

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS mini-app-pj(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        text TEXT,
        create_at INTEGER
    )
""")

class NoteRequest(BaseModel):
    text: str
    user_id: int

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"status": "ok", "message": "Сервер жив!"}

@app.get("/time")
def get_time():
    return {"time": datetime.datetime.now().isoformat()}

@app.get("/list")
def get_list(user_id: int):
    cursor.execute("SELECT text FROM mini-app-pj WHERE user_id = ? ORDER BY id DESC", (user_id, ))
    rows = cursor.fetchall()
    if rows:
        text = [text[0] for text in rows]
        return {"text": '\n'.join(text)}
    return {"text": "Пока пусто"}

@app.post("/notes")
def save_notes(note: NoteRequest):
    text = note.text
    user_id = note.user_id
    cursor.execute("INSERT INTO mini-app-pj (user_id, text, create_at) VALUES (?, ?, ?)", (user_id, text, int(time.time())))
    conn.commit()
    return {"status": "ok", "message": "Заметка сохранена"}
