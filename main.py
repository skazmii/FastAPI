from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class TaskCreate(BaseModel):
    title: str

def get_db_connection():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

create_table()

@app.get("/")
def home():
    return {"message": "Task Manager API running"}

@app.get("/tasks")
def get_tasks():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return [dict(task) for task in tasks]

@app.post("/tasks")
def create_task(task: TaskCreate):
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO tasks (title, completed) VALUES (?, ?)",
        (task.title, 0)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {
        "id": new_id,
        "title": task.title,
        "completed": False
    }

@app.patch("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    conn = get_db_connection()
    conn.execute(
        "UPDATE tasks SET completed = 1 WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    conn.close()

    return {"message": "Task marked as complete"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    conn.close()

    return {"message": "Task deleted"}