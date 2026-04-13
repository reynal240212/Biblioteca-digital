from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import BookDB
from app.schemas import BookSchema, StatusRead

router = APIRouter(prefix="/libros", tags=["Libros"])


@router.post("/", response_model=BookSchema)
def crear_libro(libro: BookSchema, db: Session = Depends(get_db)):
    nuevo_libro = BookDB(
        title=libro.title,
        author=libro.author,
        page=libro.page,
        read=libro.read.value,
        cover_url=libro.cover_url,
        synopsis=libro.synopsis,
        read_url=libro.read_url,
        file_path=libro.file_path,
        genre=libro.genre,
        series=libro.series
    )
    db.add(nuevo_libro)
    db.commit()
    db.refresh(nuevo_libro)
    return nuevo_libro


@router.get("/", response_model=List[BookSchema])
def obtener_libros(status: Optional[StatusRead] = None, db: Session = Depends(get_db)):
    query = db.query(BookDB)
    if status:
        query = query.filter(BookDB.read == status.value)
    return query.all()


@router.get("/{libro_id}", response_model=BookSchema)
def obtener_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(BookDB).filter(BookDB.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro


@router.put("/{libro_id}")
def actualizar_libro(
    libro_id: int, libro_actualizado: BookSchema, db: Session = Depends(get_db)
):
    db_libro = db.query(BookDB).filter(BookDB.id == libro_id).first()
    if not db_libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado en la DB")

    db_libro.title = libro_actualizado.title
    db_libro.author = libro_actualizado.author
    db_libro.page = libro_actualizado.page
    db_libro.read = libro_actualizado.read.value
    db_libro.cover_url = libro_actualizado.cover_url
    db_libro.synopsis = libro_actualizado.synopsis
    db_libro.read_url = libro_actualizado.read_url
    db_libro.file_path = libro_actualizado.file_path
    db_libro.genre = libro_actualizado.genre

    db.commit()
    return {"mensaje": "Libro actualizado en disco"}


@router.delete("/{libro_id}")
def eliminar_libro(libro_id: int, db: Session = Depends(get_db)):
    db_libro = db.query(BookDB).filter(BookDB.id == libro_id).first()
    if not db_libro:
        raise HTTPException(status_code=404, detail="No existe ese ID")

    db.delete(db_libro)
    db.commit()
    return {"mensaje": "Eliminado permanentemente"}
