from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Tabla de asociación para Usuario y Roles
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("usuarios.id")),
    Column("role_id", Integer, ForeignKey("roles.id")),
)

# Tabla de asociación para Roles y Permisos
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id")),
    Column("permission_id", Integer, ForeignKey("permisos.id")),
)

class UserDB(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="lector")
    avatar_url = Column(String)

    # Relación con Roles
    roles = relationship("RoleDB", secondary=user_roles, back_populates="users")

class RoleDB(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)

    users = relationship("UserDB", secondary=user_roles, back_populates="roles")
    permissions = relationship("PermissionDB", secondary=role_permissions, back_populates="roles")

class PermissionDB(Base):
    __tablename__ = "permisos"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)

    roles = relationship("RoleDB", secondary=role_permissions, back_populates="permissions")

class BookDB(Base):
    __tablename__ = "libros"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    page = Column(Integer)
    read = Column(String)
    cover_url = Column(String)
    synopsis = Column(String, nullable=True)
    read_url = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    genre = Column(String, default="Novela")
    series = Column(String, nullable=True) # Para colecciones como "Dragon Ball"
