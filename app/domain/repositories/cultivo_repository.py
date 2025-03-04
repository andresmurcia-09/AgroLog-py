from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.cultivo import Cultivo


class CultivoRepository(ABC):
    @abstractmethod
    def crear(self, cultivo: Cultivo) -> Cultivo:
        pass
    
    @abstractmethod
    def obtener_por_id(self, cultivo_id: int) -> Optional[Cultivo]:
        pass
    
    @abstractmethod
    def listar_por_parcela(self, parcela_id: int) -> List[Cultivo]:
        pass
    
    @abstractmethod
    def listar_por_usuario(self, usuario_id: int) -> List[Cultivo]:
        pass
    
    @abstractmethod
    def actualizar(self, cultivo: Cultivo) -> Cultivo:
        pass
    
    @abstractmethod
    def eliminar(self, cultivo_id: int) -> bool:
        pass