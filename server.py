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
conn.commit()

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

@app.post("/notes")
def save_notes(note: NoteRequest):
    try:
        text = note.text
        cursor.execute("INSERT INTO my_app (text, create_at) VALUES (?, ?)", (text, int(time.time())))
        conn.commit()
        return {"status": "ok", "message": "Заметка сохранена"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
