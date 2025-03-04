from datetime import datetime, date
from typing import List, Optional

from app.domain.entities.recordatorio import Recordatorio
from app.domain.repositories.recordatorio_repository import RecordatorioRepository
from app.domain.repositories.aplicacion_repository import AplicacionRepository
from app.domain.repositories.usuario_repository import UsuarioRepository


class RecordatorioService:
    def __init__(self, recordatorio_repository: RecordatorioRepository, 
                aplicacion_repository: AplicacionRepository,
                usuario_repository: UsuarioRepository):
        self.recordatorio_repository = recordatorio_repository
        self.aplicacion_repository = aplicacion_repository
        self.usuario_repository = usuario_repository
    
    def crear_recordatorio(self, aplicacion_id: int, fecha_recordatorio: date, 
                          tipo: str, mensaje: str) -> Recordatorio:
        aplicacion = self.aplicacion_repository.obtener_por_id(aplicacion_id)
        if not aplicacion:
            raise ValueError("Aplicación no encontrada")
        
        nuevo_recordatorio = Recordatorio(
            id=None,
            aplicacion_id=aplicacion_id,
            fecha_recordatorio=fecha_recordatorio,
            tipo=tipo,
            mensaje=mensaje,
            completado=False,
            fecha_registro=datetime.now()
        )
        
        return self.recordatorio_repository.crear(nuevo_recordatorio)
    
    def obtener_recordatorio(self, recordatorio_id: int) -> Optional[Recordatorio]:
        return self.recordatorio_repository.obtener_por_id(recordatorio_id)
    
    def listar_recordatorios_por_aplicacion(self, aplicacion_id: int) -> List[Recordatorio]:
        aplicacion = self.aplicacion_repository.obtener_por_id(aplicacion_id)
        if not aplicacion:
            raise ValueError("Aplicación no encontrada")
        
        return self.recordatorio_repository.listar_por_aplicacion(aplicacion_id)
    
    def listar_recordatorios_pendientes_por_usuario(self, usuario_id: int) -> List[Recordatorio]:
        usuario = self.usuario_repository.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        return self.recordatorio_repository.listar_pendientes_por_usuario(usuario_id)
    
    def listar_recordatorios_por_fecha(self, fecha: date, usuario_id: int) -> List[Recordatorio]:
        usuario = self.usuario_repository.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        return self.recordatorio_repository.listar_por_fecha(fecha, usuario_id)
    
    def marcar_recordatorio_completado(self, recordatorio_id: int) -> Recordatorio:
        recordatorio = self.recordatorio_repository.obtener_por_id(recordatorio_id)
        if not recordatorio:
            raise ValueError("Recordatorio no encontrado")
        
        return self.recordatorio_repository.marcar_completado(recordatorio_id)
    
    def eliminar_recordatorio(self, recordatorio_id: int) -> bool:
        recordatorio = self.recordatorio_repository.obtener_por_id(recordatorio_id)
        if not recordatorio:
            raise ValueError("Recordatorio no encontrado")
        
        return self.recordatorio_repository.eliminar(recordatorio_id)