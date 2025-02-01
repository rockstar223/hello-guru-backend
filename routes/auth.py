from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from pydantic import BaseModel

router = APIRouter()

# Define Request Body Model
class UserRequest(BaseModel):
    username: str
    password: str

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User Signup API (Fixes "Field required" error)
@router.post("/signup")
def signup(user: UserRequest, db: Session = Depends(get_db)):
    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

# User Login API (Fixes "Field required" error)
@router.post("/login")
def login(user: UserRequest, db: Session = Depends(get_db)):
    user_record = db.query(User).filter(User.username == user.username, User.password == user.password).first()
    if user_record:
        return {"message": "Login successful"}
    raise HTTPException(status_code=400, detail="Invalid credentials")
