from fastapi import APIRouter, Body, Depends, Path
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated
from models import Task
from schema import *
from db import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/tasks/", response_model=TaskResponse)
async def create_task(
    task: Annotated[TaskCreate, Body()], db: Session = Depends(get_db)
):
    """
    Endpoint to create a task
    """
    created_task = Task(**task.model_dump())
    db.add(created_task)
    db.commit()
    return created_task


@router.get("/tasks", response_model=list[TaskResponse])
async def fetch_tasks(db: Session = Depends(get_db)):
    """
    Endpoint to fetch all tasks
    """
    query = select(Task)
    tasks = db.execute(query).scalars().all()
    return tasks


@router.get("/tasks/{task_id}", response_model=TaskResponse | None)
async def fetch_single_task(
    task_id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)
):
    """
    Endpoint to fetch a single task
    """
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=400, detail="Galat number diye ho")
    return task


@router.patch("/tasks/{task_id}/update/", response_model=TaskResponse)
async def update_task(
    task_id: Annotated[int, Path(gt=0)], task: TaskUpdate, db: Session = Depends(get_db)
):
    """
    Endpoint to update a given task
    """
    user_task_data = task.model_dump()
    updated_task = db.get(Task,task_id)
    if updated_task is None:
        raise HTTPException(status_code=400, detail="Galat number diye ho")
    updated_task.completed = user_task_data['completed']
    updated_task.name = user_task_data['name']
    db.commit()
    return updated_task

@router.delete("/tasks/{task_id}/delete/")
async def update_task(
    task_id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)
):
    """
    Endpoint to delete a given task
    """
    to_be_deleted_task = db.get(Task,task_id)
    if to_be_deleted_task is None:
        raise HTTPException(status_code=400, detail="Galat number diye ho")
    db.delete(to_be_deleted_task)
    db.commit()
    return JSONResponse(status_code=204)