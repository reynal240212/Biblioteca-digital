from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserDB
from app.utils import verify_password
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Autenticación"])


class LoginSchema(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(datos: LoginSchema, db: Session = Depends(get_db)):
    usuario = db.query(UserDB).filter(UserDB.username == datos.username).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )

    if not verify_password(datos.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )

    return {
        "mensaje": "Inicio de sesión exitoso",
        "usuario": {
            "id": usuario.id,
            "username": usuario.username,
            "full_name": usuario.full_name,
            "role": usuario.role,
            "avatar_url": usuario.avatar_url
        },
    }
