from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from app.domain.entities.cultivo import Cultivo
from app.domain.repositories.cultivo_repository import CultivoRepository
from app.infrastructure.persistence import models


class CultivoRepositoryImpl(CultivoRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def crear(self, cultivo: Cultivo) -> Cultivo:
        db_cultivo = models.Cultivo(
            nombre=cultivo.nombre,
            variedad=cultivo.variedad,
            fecha_siembra=cultivo.fecha_siembra,
            fecha_cosecha_estimada=cultivo.fecha_cosecha_estimada,
            parcela_id=cultivo.parcela_id,
            fecha_registro=cultivo.fecha_registro,
            activo=cultivo.activo
        )
        self.db.add(db_cultivo)
        self.db.commit()
        self.db.refresh(db_cultivo)
        
        return self._map_to_entity(db_cultivo)
    
    def obtener_por_id(self, cultivo_id: int) -> Optional[Cultivo]:
        db_cultivo = self.db.query(models.Cultivo).filter(models.Cultivo.id == cultivo_id).first()
        if db_cultivo is None:
            return None
        
        return self._map_to_entity(db_cultivo)
    
    def listar_por_parcela(self, parcela_id: int) -> List[Cultivo]:
        db_cultivos = self.db.query(models.Cultivo).filter(
            models.Cultivo.parcela_id == parcela_id,
            models.Cultivo.activo == True
        ).all()
        
        return [self._map_to_entity(db_cultivo) for db_cultivo in db_cultivos]
    
    def listar_por_usuario(self, usuario_id: int) -> List[Cultivo]:
        db_cultivos = self.db.query(models.Cultivo).join(
            models.Parcela
        ).filter(
            models.Parcela.usuario_id == usuario_id,
            models.Cultivo.activo == True
        ).all()
        
        return [self._map_to_entity(db_cultivo) for db_cultivo in db_cultivos]
    
    def actualizar(self, cultivo: Cultivo) -> Cultivo:
        db_cultivo = self.db.query(models.Cultivo).filter(models.Cultivo.id == cultivo.id).first()
        if db_cultivo is None:
            return None
        
        db_cultivo.nombre = cultivo.nombre
        db_cultivo.variedad = cultivo.variedad
        db_cultivo.fecha_siembra = cultivo.fecha_siembra
        db_cultivo.fecha_cosecha_estimada = cultivo.fecha_cosecha_estimada
        db_cultivo.activo = cultivo.activo
        
        self.db.commit()
        self.db.refresh(db_cultivo)
        
        return self._map_to_entity(db_cultivo)
    
    def eliminar(self, cultivo_id: int) -> bool:
        db_cultivo = self.db.query(models.Cultivo).filter(models.Cultivo.id == cultivo_id).first()
        if db_cultivo is None:
            return False
        
        db_cultivo.activo = False
        self.db.commit()
        
        return True
    
    def _map_to_entity(self, db_cultivo: models.Cultivo) -> Cultivo:
        return Cultivo(
            id=db_cultivo.id,
            nombre=db_cultivo.nombre,
            variedad=db_cultivo.variedad,
            fecha_siembra=db_cultivo.fecha_siembra,
            fecha_cosecha_estimada=db_cultivo.fecha_cosecha_estimada,
            parcela_id=db_cultivo.parcela_id,
            fecha_registro=db_cultivo.fecha_registro,
            activo=db_cultivo.activo
        )