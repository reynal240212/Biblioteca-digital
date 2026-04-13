from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.routers import libros, usuarios, auth, dashboard, roles, permisos
from app.models import RoleDB, PermissionDB
from mangum import Mangum

def seed_data():
    db = SessionLocal()
    try:
        # Permisos requeridos
        permisos_nombres = [
            "LIBROS/LEER", "LIBROS/CREAR", "LIBROS/ACTUALIZAR", "LIBROS/ELIMINAR"
        ]
        db_permisos = {}
        for nombre in permisos_nombres:
            p = db.query(PermissionDB).filter(PermissionDB.name == nombre).first()
            if not p:
                p = PermissionDB(name=nombre, description=f"Permiso para {nombre.lower()}")
                db.add(p)
                db.commit()
                db.refresh(p)
            db_permisos[nombre] = p

        # Roles requeridos
        roles_data = [
            {"name": "Rol_1: Solo lectura", "perms": ["LIBROS/LEER"]},
            {"name": "Rol_2: Solo escritura", "perms": ["LIBROS/CREAR"]},
            {"name": "Rol_3: Actualizar y eliminar", "perms": ["LIBROS/ACTUALIZAR", "LIBROS/ELIMINAR"]}
        ]

        for r_data in roles_data:
            rol = db.query(RoleDB).filter(RoleDB.name == r_data["name"]).first()
            if not rol:
                rol = RoleDB(name=r_data["name"], description=f"Rol con acceso a {', '.join(r_data['perms'])}")
                db.add(rol)
                db.commit()
                db.refresh(rol)
            
            # Asignar permisos si el rol es nuevo o no los tiene
            for p_name in r_data["perms"]:
                permiso = db_permisos[p_name]
                if permiso not in rol.permissions:
                    rol.permissions.append(permiso)
        
        db.commit()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas
    Base.metadata.create_all(bind=engine)
    # Sembrar datos
    seed_data()
    yield

app = FastAPI(
    title="Mi Biblioteca API - Parcial II",
    description="API para la gestión de libros, usuarios, roles y permisos",
    version="1.1.0",
    lifespan=lifespan
)

app.include_router(libros.router)
app.include_router(usuarios.router)
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(roles.router)
app.include_router(permisos.router)

# Configuración de archivos estáticos
static_path = os.path.join(os.path.dirname(__file__), "app", "static")

# Mount static files
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/", tags=["Inicio"])
def inicio():
    index_file = os.path.join(static_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "mensaje": "Bienvenido a la API de Mi Biblioteca",
        "doc_url": "/docs",
    }

# Adaptador para Vercel
handler = Mangum(app)
