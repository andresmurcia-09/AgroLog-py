from datetime import datetime
from typing import List, Optional

from app.domain.entities.usuario import Usuario
from app.domain.repositories.usuario_repository import UsuarioRepository
from app.application.security import get_password_hash, verify_password


class UsuarioService:
    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository
    
    def crear_usuario(self, nombre: str, apellido: str, email: str, password: str) -> Usuario:
        usuario_existente = self.usuario_repository.obtener_por_email(email)
        if usuario_existente:
            raise ValueError("El email ya está registrado")
        
        hashed_password = get_password_hash(password)
        nuevo_usuario = Usuario(
            id=None,
            nombre=nombre,
            apellido=apellido,
            email=email,
            hashed_password=hashed_password,
            fecha_registro=datetime.now(),
            activo=True
        )
        
        return self.usuario_repository.crear(nuevo_usuario)
    
    def autenticar_usuario(self, email: str, password: str) -> Optional[Usuario]:
        usuario = self.usuario_repository.obtener_por_email(email)
        if not usuario:
            return None
        
        if not verify_password(password, usuario.hashed_password):
            return None
        
        return usuario
    
    def obtener_usuario(self, usuario_id: int) -> Optional[Usuario]:
        return self.usuario_repository.obtener_por_id(usuario_id)
    
    def listar_usuarios(self) -> List[Usuario]:
        return self.usuario_repository.listar()
    
    def actualizar_usuario(self, usuario_id: int, nombre: str = None, apellido: str = None, 
                          email: str = None, password: str = None) -> Usuario:
        usuario = self.usuario_repository.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        if nombre:
            usuario.nombre = nombre
        if apellido:
            usuario.apellido = apellido
        if email and email != usuario.email:
            usuario_existente = self.usuario_repository.obtener_por_email(email)
            if usuario_existente and usuario_existente.id != usuario_id:
                raise ValueError("El email ya está registrado por otro usuario")
            usuario.email = email
        if password:
            usuario.hashed_password = get_password_hash(password)
        
        return self.usuario_repository.actualizar(usuario)
    
    def eliminar_usuario(self, usuario_id: int) -> bool:
        return self.usuario_repository.eliminar(usuario_id)