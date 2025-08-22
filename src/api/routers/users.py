from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user
from ..schemas.user import UserCreate, UserOut
from ..models.user import User
from ..auth.password import get_password_hash
router = APIRouter(prefix="/users", tags=["users"])
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing: raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=payload.email, full_name=payload.full_name, hashed_password=get_password_hash(payload.password))
    db.add(user); db.commit(); db.refresh(user); return user
@router.get("/me", response_model=UserOut)
def read_me(current=Depends(get_current_user)): return current
