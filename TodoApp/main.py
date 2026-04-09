from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
import models
from models import Todo
from database import engine,SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

bd_dependency = Annotated[Session, Depends(get_db)]

@app.post("/")
async def read_all(db: bd_dependency):
    return db.query(Todo).all()
