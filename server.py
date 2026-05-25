from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime, time, sqlite3

app = FastAPI()

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS my_app(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        create_at INTEGER
    )
""")

class NoteRequest(BaseModel):
    text: str

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
def get_list():
    cursor.execute("SELECT text FROM my_app ORDER BY id DESC")
    rows = cursor.fetchall()
    if rows:
        text = [text[0] for text in rows]
        return {"text": '\n'.join(text)}
    return {"text": "Пока пусто"}

@app.post("/notes")
def save_notes(note: NoteRequest):
    text = note.text
    cursor.execute("INSERT INTO my_app (text, create_at) VALUES (?, ?)", (text, int(time.time())))
    conn.commit()
    return {"status": "ok", "message": "Заметка сохранена"}
