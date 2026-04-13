from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import Optional, List

class StatusRead(str, Enum):
    PENDING = "pendiente"
    READ = "leído"
    NOT_READ = "no leído"

# Esquemas para Permisos
class PermissionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

# Esquemas para Roles
class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    permissions: List[PermissionResponse] = []

    class Config:
        from_attributes = True

# Esquemas para Libros
class BookSchema(BaseModel):
    id: Optional[int] = None
    title: str
    author: str
    page: int
    read: StatusRead = StatusRead.NOT_READ
    cover_url: Optional[str] = None
    synopsis: Optional[str] = None
    read_url: Optional[str] = None
    file_path: Optional[str] = None
    genre: str = "Novela"
    series: Optional[str] = None

    class Config:
        from_attributes = True

# Esquemas para Usuarios
class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    avatar_url: Optional[str] = None
    roles: List[RoleResponse] = [] # Lista de roles estructurados

    class Config:
        from_attributes = True

class UserSecret(UserBase):
    hashed_password: str
