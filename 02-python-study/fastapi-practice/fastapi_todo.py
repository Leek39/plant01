import os
from datetime import datetime, timezone
from urllib import request

from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from models import Todo, get_db


app = FastAPI()

@app.get("/api/todos")
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return {
        'status' : 'success',
        'data' : [todo.to_dict() for todo in todos],
        'count' : len(todos)
    }

@app.get("/api/todos/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    return{
        'status' : 'success',
        'data' : [todo.to_dict()]
    }

@app.post('/api/todos')
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
