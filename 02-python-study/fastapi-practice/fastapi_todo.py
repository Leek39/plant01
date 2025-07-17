import os
from datetime import datetime, timezone
from typing import List
from urllib import request

from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from models import Todo, get_db
from schemas import TodoCreate, TodoUpdate, TodoResponse


app = FastAPI()

@app.get("/api/todos", response_model=List[TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return todos

@app.get("/api/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo :
        raise HTTPException(status_code=404, detail="Todo not found")
    """return{
        'status' : 'success',
        'data' : [todo.to_dict()]
    }"""
    return todo

@app.post('/api/todos')
def create_todo(todo_data: TodoCreate, db:Session = Depends(get_db)):
    new_todo = Todo(
        title = todo_data.title,
        completed = todo_data.completed
    )

    try:
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="DB ERROR")
"""
async def create_todo(request: Request, db: Session = Depends(get_db)):
    data = await request.json()

    if not data or 'title' not in data:
        raise HTTPException(status_code=400, detail='Missing title')

    new_todo = Todo(
        title = data['title'],
        completed = data.get('completed', False)
    )

    try:
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)

        return {
            'status' : 'success',
            'data' : new_todo.to_dict()
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="DB ERROR")
"""

@app.put('/api/todos/{todo_id}')
#async def update_todo(todo_id: int, request: Request, db: Session = Depends(get_db)):
def update_todo(todo_id: int, todo_data: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    #data = await request.json()

    """if not data or 'title' not in data:
        raise HTTPException(status_code=400, detail='Missing title')

    if 'title' in data:
        todo.title = data['title']
    if 'completed' in data:
        todo.completed = data['completed']"""

    if todo_data.title is not None:
        todo.title = todo_data.title
    if todo_data.completed is not None:
        todo.completed = todo_data.completed

    try:
        db.commit()
        """return {
            'status' : 'success',
            'data' : todo.to_dict()
        }"""
        return todo
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="DB ERROR")

@app.delete('/api/todos/{todo_id}')
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    try:
        db.delete(todo)
        db.commit()
        return {
            'status' : 'success',
            'message' : 'TODO deleted'
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="DB ERROR")

