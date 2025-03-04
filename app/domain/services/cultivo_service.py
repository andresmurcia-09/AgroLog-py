from datetime import datetime, date
from typing import List, Optional

from app.domain.entities.cultivo import Cultivo
from app.domain.repositories.cultivo_repository import CultivoRepository
from app.domain.repositories.parcela_repository import ParcelaRepository


class CultivoService:
    def __init__(self, cultivo_repository: CultivoRepository, parcela_repository: ParcelaRepository):
        self.cultivo_repository = cultivo_repository
        self.parcela_repository = parcela_repository
    
    def crear_cultivo(self, nombre: str, variedad: str, fecha_siembra: date, 
                     fecha_cosecha_estimada: date, parcela_id: int) -> Cultivo:
        parcela = self.parcela_repository.obtener_por_id(parcela_id)
        if not parcela:
            raise ValueError("Parcela no encontrada")
        
        nuevo_cultivo = Cultivo(
            id=None,
            nombre=nombre,
            variedad=variedad,
            fecha_siembra=fecha_siembra,
            fecha_cosecha_estimada=fecha_cosecha_estimada,
            parcela_id=parcela_id,
            fecha_registro=datetime.now(),
            activo=True
        )
        
        return self.cultivo_repository.crear(nuevo_cultivo)
    
    def obtener_cultivo(self, cultivo_id: int) -> Optional[Cultivo]:
        return self.cultivo_repository.obtener_por_id(cultivo_id)
    
    def listar_cultivos_por_parcela(self, parcela_id: int) -> List[Cultivo]:
        parcela = self.parcela_repository.obtener_por_id(parcela_id)
        if not parcela:
            raise ValueError("Parcela no encontrada")
        
        return self.cultivo_repository.listar_por_parcela(parcela_id)
    
    def listar_cultivos_por_usuario(self, usuario_id: int) -> List[Cultivo]:
        return self.cultivo_repository.listar_por_usuario(usuario_id)
    
    def actualizar_cultivo(self, cultivo_id: int, nombre: str = None, variedad: str = None,
                          fecha_siembra: date = None, fecha_cosecha_estimada: date = None) -> Cultivo:
        cultivo = self.cultivo_repository.obtener_por_id(cultivo_id)
        if not cultivo:
            raise ValueError("Cultivo no encontrado")
        
        if nombre:
            cultivo.nombre = nombre
        if variedad:
            cultivo.variedad = variedad
        if fecha_siembra:
            cultivo.fecha_siembra = fecha_siembra
        if fecha_cosecha_estimada:
            cultivo.fecha_cosecha_estimada = fecha_cosecha_estimada
        
        return self.cultivo_repository.actualizar(cultivo)
    
    def eliminar_cultivo(self, cultivo_id: int) -> bool:
        cultivo = self.cultivo_repository.obtener_por_id(cultivo_id)
        if not cultivo:
            raise ValueError("Cultivo no encontrado")
        
        return self.cultivo_repository.eliminar(cultivo_id)