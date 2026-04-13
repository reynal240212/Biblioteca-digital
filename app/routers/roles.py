from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import RoleDB
from app.schemas import RoleResponse

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=List[RoleResponse])
def listar_roles(db: Session = Depends(get_db)):
    return db.query(RoleDB).all()

@router.get("/{id}/permisos")
def listar_permisos_del_rol(id: int, db: Session = Depends(get_db)):
    rol = db.query(RoleDB).filter(RoleDB.id == id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol.permissions
