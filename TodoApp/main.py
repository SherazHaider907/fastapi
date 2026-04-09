from fastapi import FastAPI
import models
from database import engine
from routers import auth,todos


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# db_dependency = Annotated[Session, Depends(get_db)]

# # Pydantic model for request body validation
# class TodoRequest(BaseModel):
#     title: str = Field(min_length=3)
#     description: str = Field(min_length=1 , max_length=300) 
#     priority: int = Field(gt=0, lt=6)
#     complete: bool 


# # get all todos
# @app.get("/", status_code=status.HTTP_200_OK)
# async def read_all(db: db_dependency):
#     return db.query(Todo).all()

# # get todo by id using path parameter
# @app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
# async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
#     todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
#     if todo_model is not None:
#         return todo_model
#     raise HTTPException(status_code=404, detail="Todo not found")

# # create todo using post method
# @app.post("/todo/", status_code=status.HTTP_201_CREATED)
# async def create_todo(db: db_dependency, todo_request: TodoRequest):
#     todo_model = Todo(**todo_request.dict())

#     db.add(todo_model)
#     db.commit()

# # update todo by id using put method
# @app.put("/todo/{todo_id}", status_code=status.HTTP_200_OK)
# async def update_todo(
#     db: db_dependency,
#     todo_request: TodoRequest,
#     todo_id: int = Path(gt=0)
    
# ):
#     todo_model = db.query(Todo).filter(Todo.id == todo_id).first()

#     if todo_model is None:
#         raise HTTPException(status_code=404, detail="Todo not found")

#     todo_model.title = todo_request.title
#     todo_model.description = todo_request.description
#     todo_model.priority = todo_request.priority
#     todo_model.complete = todo_request.complete

#     db.add(todo_model)
#     db.commit()


# # delete todo by id using delete method
# @app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
#     todo_model = db.query(Todo).filter(Todo.id == todo_id).first()

#     if todo_model is None:
#         raise HTTPException(status_code=404, detail="Todo not found")
#     db.query(Todo).filter(Todo.id == todo_id).delete()

#     db.commit()
