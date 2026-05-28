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

@app.post("/save")
def save():
    pass
