from fastapi import FastAPI
import db
from schemas import TaskIn
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = db.get_database_connection()
    db.init_db(conn)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Task API "}

@app.get("/tasks")
def list_tasks():
    conn = db.get_database_connection()
    rows = db.list_tasks(conn)
    return [
        {"id": r[0], 
         "title": r[1], 
         "description": r[2], 
         "done": bool(r[3])}
        for r in rows
    ]

@app.post("/tasks", status_code=201)
def add_task(task: TaskIn):
    conn = db.get_database_connection()
    new_id = db.add_task(conn, task.title, task.description)
    return {
        "id": new_id, 
        "title": task.title, 
        "description": task.description,
        "done": False
    }
    
