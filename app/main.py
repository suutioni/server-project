from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from app.database import engine, SessionLocal
from app.models import Task
from app.schemas import TaskCreate, TaskResponse, TaskUpdate


app = FastAPI()




@app.get("/")
def read_root():
    return {"message": "Hello Docker + FastAPI!"}



@app.get("/db-check")
def db_check():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT version();")
        )

        return {
            "database": result.scalar()
        }



@app.post("/tasks",response_model=TaskResponse)
def create_task(task: TaskCreate):
    with SessionLocal() as db:
        db_task = Task(
            title=task.title,
            description=task.description
        )

        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        return db_task



@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks():
    with SessionLocal() as db:
        tasks = db.query(Task).all()

        return tasks



@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate):
    with SessionLocal() as db:
        db_task = db.get(Task, task_id)

        if db_task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        if task.title is not None:
            db_task.title = task.title

        if task.description is not None:
            db_task.description = task.description

        if task.completed is not None:
            db_task.completed = task.completed

        db.commit()
        db.refresh(db_task)

        return db_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    with SessionLocal() as db:
        db_task = db.get(Task, task_id)

        if db_task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )


        db.delete(db_task)
        db.commit()

        return {
           "message": "Task deleted"
        }
