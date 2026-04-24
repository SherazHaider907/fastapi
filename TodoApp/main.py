from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from . import models
from .database import engine
from .routers import auth, todos, admin, users,api
import jinja2


app = FastAPI()
app.include_router(api.router, prefix="/api")

models.Base.metadata.create_all(bind=engine)

base_dir = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=base_dir / "static"), name="static")

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(base_dir / "Templates")),
    autoescape=jinja2.select_autoescape(["html", "xml"]),
)


def render_template(template_name: str, context: dict = None):
    context = context or {}
    template = jinja_env.get_template(template_name)
    return HTMLResponse(content=template.render(**context))


@app.get("/")
def root():
    return RedirectResponse(url="/home")


@app.get("/home")
def home(request: Request):
    return render_template("home.html")


@app.get("/login")
def login(request: Request):
    return render_template("login.html")


@app.get("/register")
def register(request: Request):
    return render_template("register.html")


@app.get("/todos")
def todos_page(request: Request):
    return render_template("todos.html")


@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

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
