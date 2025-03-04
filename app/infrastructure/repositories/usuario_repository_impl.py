from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.entities.usuario import Usuario
from app.domain.repositories.usuario_repository import UsuarioRepository
from app.infrastructure.persistence import models


class UsuarioRepositoryImpl(UsuarioRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def crear(self, usuario: Usuario) -> Usuario:
        db_usuario = models.Usuario(
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            email=usuario.email,
            hashed_password=usuario.hashed_password,
            fecha_registro=usuario.fecha_registro,
            activo=usuario.activo
        )
        self.db.add(db_usuario)
        self.db.commit()
        self.db.refresh(db_usuario)
        
        return self._map_to_entity(db_usuario)
    
    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        db_usuario = self.db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
        if db_usuario is None:
            return None
        
        return self._map_to_entity(db_usuario)
    
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        db_usuario = self.db.query(models.Usuario).filter(models.Usuario.email == email).first()
        if db_usuario is None:
            return None
        
        return self._map_to_entity(db_usuario)
    
    def listar(self) -> List[Usuario]:
        db_usuarios = self.db.query(models.Usuario).all()
        return [self._map_to_entity(db_usuario) for db_usuario in db_usuarios]
    
    def actualizar(self, usuario: Usuario) -> Usuario:
        db_usuario = self.db.query(models.Usuario).filter(models.Usuario.id == usuario.id).first()
        if db_usuario is None:
            return None
        
        db_usuario.nombre = usuario.nombre
        db_usuario.apellido = usuario.apellido
        db_usuario.email = usuario.email
        db_usuario.hashed_password = usuario.hashed_password
        db_usuario.activo = usuario.activo
        
        self.db.commit()
        self.db.refresh(db_usuario)
        
        return self._map_to_entity(db_usuario)
    
    def eliminar(self, usuario_id: int) -> bool:
        db_usuario = self.db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
        if db_usuario is None:
            return False
        
        db_usuario.activo = False
        self.db.commit()
        
        return True
    
    def _map_to_entity(self, db_usuario: models.Usuario) -> Usuario:
        return Usuario(
            id=db_usuario.id,
            nombre=db_usuario.nombre,
            apellido=db_usuario.apellido,
            email=db_usuario.email,
            hashed_password=db_usuario.hashed_password,
            fecha_registro=db_usuario.fecha_registro,
            activo=db_usuario.activo
        )