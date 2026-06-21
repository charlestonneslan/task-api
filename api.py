from fastapi import FastAPI, HTTPException, Depends
import db
from schemas import TaskIn
from contextlib import asynccontextmanager

def get_db():
    conn = db.get_database_connection()
    try:
        yield conn
    finally:
        conn.close()

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
def list_tasks(conn = Depends(get_db)):
    rows = db.list_tasks(conn)
    return [
        {"id": r[0], 
         "title": r[1], 
         "description": r[2], 
         "done": bool(r[3])}
        for r in rows
    ]

@app.post("/tasks", status_code=201)
def add_task(task: TaskIn, conn = Depends(get_db)):
    new_id = db.add_task(conn, task.title, task.description)
    return {
        "id": new_id, 
        "title": task.title, 
        "description": task.description,
        "done": False
    }
    
@app.patch("/tasks/{task_id}")
def mark_done(task_id: int, conn = Depends(get_db)):
    rowcount = db.mark_done(conn, task_id)
    if rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "id": task_id,
        "done": True
    }

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, conn = Depends(get_db)):
    rowcount = db.delete_task(conn, task_id)
    if rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")