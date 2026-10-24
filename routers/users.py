from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError
from security import create_access_token

from schemas import UserCreate, UserLogin
from services.users import create_user, authenticate_user

router = APIRouter()


@router.post("/register", status_code=201)
def register_user(user: UserCreate):
    user_data = user.model_dump()

    try:
        return create_user(user_data)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists"
        )

@router.post("/login")
def login_user(user_data: UserLogin):
    user = authenticate_user(
        user_data.username,
        user_data.password
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    access_token = create_access_token(str(user["_id"]))

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Login successful",
        "user_id": str(user["_id"]),
        "username": user["username"],
    }
