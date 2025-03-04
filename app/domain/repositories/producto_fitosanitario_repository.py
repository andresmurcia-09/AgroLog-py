from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.producto_fitosanitario import ProductoFitosanitario


class ProductoFitosanitarioRepository(ABC):
    @abstractmethod
    def crear(self, producto: ProductoFitosanitario) -> ProductoFitosanitario:
        pass
    
    @abstractmethod
    def obtener_por_id(self, producto_id: int) -> Optional[ProductoFitosanitario]:
        pass
    
    @abstractmethod
    def listar_por_usuario(self, usuario_id: int) -> List[ProductoFitosanitario]:
        pass
    
    @abstractmethod
    def listar_por_tipo(self, tipo: str, usuario_id: int) -> List[ProductoFitosanitario]:
        pass
    
    @abstractmethod
    def actualizar(self, producto: ProductoFitosanitario) -> ProductoFitosanitario:
        pass
    
    @abstractmethod
    def eliminar(self, producto_id: int) -> bool:
        pass