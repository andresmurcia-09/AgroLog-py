from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date

from app.domain.entities.aplicacion import Aplicacion


class AplicacionRepository(ABC):
    @abstractmethod
    def crear(self, aplicacion: Aplicacion) -> Aplicacion:
        pass
    
    @abstractmethod
    def obtener_por_id(self, aplicacion_id: int) -> Optional[Aplicacion]:
        pass
    
    @abstractmethod
    def listar_por_cultivo(self, cultivo_id: int) -> List[Aplicacion]:
        pass
    
    @abstractmethod
    def listar_por_usuario(self, usuario_id: int) -> List[Aplicacion]:
        pass
    
    @abstractmethod
    def listar_por_fecha(self, fecha_inicio: date, fecha_fin: date, usuario_id: int) -> List[Aplicacion]:
        pass
    
    @abstractmethod
    def actualizar(self, aplicacion: Aplicacion) -> Aplicacion:
        pass
    
    @abstractmethod
    def eliminar(self, aplicacion_id: int) -> bool:
        pass