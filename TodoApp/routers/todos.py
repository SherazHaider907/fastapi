from typing import Annotated
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Path ,Query ,HTTPException
from starlette import status
from .auth import get_current_user


from models import Todo
from database import SessionLocal



router = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

# Pydantic model for request body validation
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=1 , max_length=300) 
    priority: int = Field(gt=0, lt=6)
    complete: bool 


# get all todos
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail ="Authentications Failed")
    return db.query(Todo).filter(Todo.owner_id==user.get('id')).all()

# get todo by id using path parameter
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user:user_dependency,db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail ="Authentications Failed")
    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")

# create todo using post method
@router.post("/todo/", status_code=status.HTTP_201_CREATED)
async def create_todo(user:user_dependency,db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401,detail ="Authentications Failed")
    todo_model = Todo(**todo_request.dict(),owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()

# update todo by id using put method
@router.put("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(
    user:user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0)
    
):
    if user is None:
        raise HTTPException(status_code=401,detail ="Authentications Failed")
    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


# delete todo by id using delete method
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency,db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail ="Authentications Failed")
    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).delete()

    db.commit()
