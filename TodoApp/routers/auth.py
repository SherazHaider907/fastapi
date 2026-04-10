from fastapi import APIRouter
from pydantic import BaseModel
from models import User
router = APIRouter()

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role : str

@router.post("/auth/")
async def create_user(CreateUserRequest: CreateUserRequest):
    create_user_model = User(
        email=CreateUserRequest.email,
        username=CreateUserRequest.username,
        first_name=CreateUserRequest.first_name,
        last_name=CreateUserRequest.last_name,
        role=CreateUserRequest.role,
        hashed_password=CreateUserRequest.password,
        is_active=True
    )

    return create_user_model
    


