from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import PermissionDB
from app.schemas import PermissionResponse

router = APIRouter(prefix="/permisos", tags=["Permisos"])

@router.get("/", response_model=List[PermissionResponse])
def listar_permisos(db: Session = Depends(get_db)):
    return db.query(PermissionDB).all()
