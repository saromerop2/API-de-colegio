from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

import models
from database import engine, get_db
from schemas import UserCreate, Token, UserOut, TokenData
from auth import verify_password, get_password_hash, create_access_token, decode_token
from config import settings

# crear tablas
models.Base = models  # (no hace nada, solo para evitarflake — ignore)
models.Base = None    # no necesario, las tablas las crearemos manualmente abajo

# --- ajustar: import real de Base desde database
from database import Base as DBBase
DBBase.metadata.create_all(bind=engine)

app = FastAPI(title="School Auth API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# --- utilidades
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# Dependencia que retorna el usuario actual o lanza 401
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_data = decode_token(token)
    if not token_data or not token_data.username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    user = get_user_by_username(db, token_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    return user

# Depencencia para admin
def require_admin(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Se requiere rol admin")
    return current_user

# --- RUTAS

@app.post("/register", response_model=UserOut, status_code=201)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_username(db, user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    hashed = get_password_hash(user_in.password)
    user = models.User(username=user_in.username, hashed_password=hashed, full_name=user_in.full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token({"sub": user.username, "role": user.role}, expires_delta=access_token_expires)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me", response_model=UserOut)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# Solo admin: listar usuarios
@app.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), admin: models.User = Depends(require_admin)):
    users = db.query(models.User).all()
    return users

# Solo admin: asignar rol a un usuario
@app.put("/users/{user_id}/role", response_model=UserOut)
def set_role(user_id: int, role: str, db: Session = Depends(get_db), admin: models.User = Depends(require_admin)):
    if role not in ("admin", "student"):
        raise HTTPException(status_code=400, detail="role debe ser 'admin' o 'student'")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user.role = role
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Ejemplo de ruta protegida solo estudiantes (o admin también, si quieres)
@app.get("/student-area")
def student_area(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "student" and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Solo estudiantes o administradores pueden acceder")
    return {"msg": f"Hola {current_user.username}, bienvenido al área de estudiantes", "role": current_user.role}
