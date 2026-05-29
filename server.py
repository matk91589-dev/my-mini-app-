from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
import time, sqlite3

app = FastAPI()

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS ping_combat(
        user_id INTEGER PRIMARY KEY,
        best_score INTEGER,
        total_score INTEGER,
        create_at INTEGER
    )
""")
conn.commit()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/save")
async def save(request: Request):
    data = await request.json()
    user_id = data["user_id"]
    clicks = data["clicks"]

    cursor.execute("SELECT best_score, total_score FROM ping_combat WHERE user_id = ?", (user_id, ))
    row = cursor.fetchone()

    if row:
        if clicks > row[0]:
            cursor.execute("UPDATE ping_combat SET best_score = ? WHERE user_id = ?", (clicks, user_id))
            conn.commit()
        
        score = clicks + row[1]
        cursor.execute("UPDATE ping_combat SET total_score = ? WHERE user_id = ?", (score, user_id))
        conn.commit()

    else:
        cursor.execute("INSERT INTO ping_combat (user_id, best_score, total_score, create_at) VALUES (?, ?, ?, ?)", (user_id, clicks, clicks, int(time.time())))
        conn.commit()

    return {"status": "ok"}

@app.get("/score")
async def score(user_id: int):
    cursor.execute("SELECT total_score FROM ping_combat WHERE user_id = ?", (user_id, ))
    row = cursor.fetchone()
    return {"total": row[0] if row else 0}
