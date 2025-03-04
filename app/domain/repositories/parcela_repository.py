from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.parcela import Parcela


class ParcelaRepository(ABC):
    @abstractmethod
    def crear(self, parcela: Parcela) -> Parcela:
        pass
    
    @abstractmethod
    def obtener_por_id(self, parcela_id: int) -> Optional[Parcela]:
        pass
    
    @abstractmethod
    def listar_por_usuario(self, usuario_id: int) -> List[Parcela]:
        pass
    
    @abstractmethod
    def actualizar(self, parcela: Parcela) -> Parcela:
        pass
    
    @abstractmethod
    def eliminar(self, parcela_id: int) -> bool:
        pass