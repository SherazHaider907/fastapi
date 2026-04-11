from fastapi import APIRouter, Depends
from pydantic import BaseModel
from models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
import starlette.status as status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from datetime import timedelta,datetime,timezone


router = APIRouter()


SECRET_KEY = "a53525ce8455ef0d9ce976d463e1d011085c2a5c0703fbe355175baa931a484f"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role : str


class Token(BaseModel):
    access_token:str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username:str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user

def create_access_token(username: str,user_id:int,expires_delta:timedelta):
    encode = {'sub':username,'id':user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, CreateUserRequest: CreateUserRequest):
    create_user_model = User(
        email=CreateUserRequest.email,
        username=CreateUserRequest.username,
        first_name=CreateUserRequest.first_name,
        last_name=CreateUserRequest.last_name,
        role=CreateUserRequest.role,
        hashed_password=bcrypt_context.hash(CreateUserRequest.password),
        is_active=True
    )
    db.add(create_user_model)
    db.commit()
    


@router.post("/token",response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        return "Failed Authentication"
    token = create_access_token(user.username,user.id,timedelta(minutes=20))
    return {'access_token':token,'token_type': 'bearer'}