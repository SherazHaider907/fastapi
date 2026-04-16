from fastapi import APIRouter, Depends,HTTPException
from pydantic import BaseModel
from models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import timedelta,datetime,timezone
from starlette import status


router = APIRouter(
    prefix ='/auth',
    tags=['auth']
)


SECRET_KEY = "a53525ce8455ef0d9ce976d463e1d011085c2a5c0703fbe355175baa931a484f"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')



class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role : str
    phone_number : str


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

def create_access_token(username: str,user_id:int,role:str,expires_delta:timedelta):
    encode = {'sub':username,'id':user_id,'role':role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)


async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail ='Could not validate user')
        return {'username':username,'id':user_id,'user_role':user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail ='Could not validate user')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, CreateUserRequest: CreateUserRequest):
    create_user_model = User(
        email=CreateUserRequest.email,
        username=CreateUserRequest.username,
        first_name=CreateUserRequest.first_name,
        last_name=CreateUserRequest.last_name,
        role=CreateUserRequest.role,
        hashed_password=bcrypt_context.hash(CreateUserRequest.password),
        is_active=True,
        phone_number=CreateUserRequest.phone_number
    )
    db.add(create_user_model)
    db.commit()
    return {"message": "User created successfully"}


@router.post("/token",response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail ='Could not validate user')
    token = create_access_token(user.username,user.id,user.role,timedelta(minutes=20))
    return {'access_token':token,'token_type': 'bearer'}