from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.services.auth_service import get_current_user
from app.schemas.user_schema import UserResponse
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.utils.security import verify_password, create_access_token, hash_password
from app.database.db import get_db
from app.utils.security import is_strong_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    email_normalized = user_in.email.lower().strip()
    if db.query(User).filter(User.email == email_normalized).first():
        raise HTTPException(status_code=400, detail="Nao é possível registrar um usuário com este e-mail")
    
    if not is_strong_password(user_in.password):
        raise HTTPException(
            status_code=400,
            detail="A senha deve ter pelo menos 8 caracteres, incluindo maiúsculas, minúsculas, números e caracteres especiais."
        )
    
    user = User(
    
        name=user_in.name,
        email=email_normalized,
        password_hash=hash_password(user_in.password),
        role=user_in.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user