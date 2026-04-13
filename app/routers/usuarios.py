from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import UserDB
from app.schemas import UserCreate, UserResponse
from app.utils import get_password_hash
import random

AVATARS = [
    f"https://api.dicebear.com/7.x/adventurer/svg?seed={name}" 
    for name in ["Felix", "Aura", "Jasper", "Luna", "Orion", "Nova", "Silas", "Lyra", "Finn", "Maya", 
                 "Kai", "Zoe", "Bastian", "Clara", "Dante", "Elena", "Hugo", "Iris", "Jude", "Kira",
                 "Leo", "Mira", "Nico", "Olive", "Puck", "Quinn", "Rory", "Sasha", "Theo", "Vera"]
]

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UserResponse)
def crear_usuario(usuario: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == usuario.username).first()
    if db_user:
        raise HTTPException(
            status_code=400, detail="El nombre de usuario ya está registrado"
        )

    db_email = db.query(UserDB).filter(UserDB.email == usuario.email).first()
    if db_email:
        raise HTTPException(
            status_code=400, detail="El correo electrónico ya está registrado"
        )

    hashed_pass = get_password_hash(usuario.password)

    nuevo_usuario = UserDB(
        username=usuario.username,
        email=usuario.email,
        full_name=usuario.full_name,
        hashed_password=hashed_pass,
        role="lector",
        avatar_url=random.choice(AVATARS)
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.get("/", response_model=List[UserResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(UserDB).all()
    return usuarios


@router.get("/{id}", response_model=UserResponse)
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(UserDB).filter(UserDB.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.put("/{id}/avatar")
def actualizar_avatar(id: int, avatar_url: str, db: Session = Depends(get_db)):
    usuario = db.query(UserDB).filter(UserDB.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario.avatar_url = avatar_url
    db.commit()
    return {"mensaje": "Avatar actualizado", "avatar_url": avatar_url}

@router.get("/{id}/roles")
def listar_roles_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(UserDB).filter(UserDB.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario.roles

@router.get("/{id}/permisos")
def listar_permisos_usuario(id: int, db: Session = Depends(get_db)):
    usuario = db.query(UserDB).filter(UserDB.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Aplanar todos los permisos de todos sus roles
    permisos = []
    for rol in usuario.roles:
        for permiso in rol.permissions:
            if permiso not in permisos:
                permisos.append(permiso)
    return permisos
