from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.usuario import Usuario


class UsuarioRepository(ABC):
    @abstractmethod
    def crear(self, usuario: Usuario) -> Usuario:
        pass
    
    @abstractmethod
    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        pass
    
    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        pass
    
    @abstractmethod
    def listar(self) -> List[Usuario]:
        pass
    
    @abstractmethod
    def actualizar(self, usuario: Usuario) -> Usuario:
        pass
    
    @abstractmethod
    def eliminar(self, usuario_id: int) -> bool:
        pass