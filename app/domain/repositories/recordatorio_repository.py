from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date

from app.domain.entities.recordatorio import Recordatorio


class RecordatorioRepository(ABC):
    @abstractmethod
    def crear(self, recordatorio: Recordatorio) -> Recordatorio:
        pass
    
    @abstractmethod
    def obtener_por_id(self, recordatorio_id: int) -> Optional[Recordatorio]:
        pass
    
    @abstractmethod
    def listar_por_aplicacion(self, aplicacion_id: int) -> List[Recordatorio]:
        pass
    
    @abstractmethod
    def listar_pendientes_por_usuario(self, usuario_id: int) -> List[Recordatorio]:
        pass
    
    @abstractmethod
    def listar_por_fecha(self, fecha: date, usuario_id: int) -> List[Recordatorio]:
        pass
    
    @abstractmethod
    def marcar_completado(self, recordatorio_id: int) -> Recordatorio:
        pass
    
    @abstractmethod
    def eliminar(self, recordatorio_id: int) -> bool:
        pass