from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session, joinedload

from app.domain.entities.aplicacion import Aplicacion
from app.domain.repositories.aplicacion_repository import AplicacionRepository
from app.infrastructure.persistence import models


class AplicacionRepositoryImpl(AplicacionRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def crear(self, aplicacion: Aplicacion) -> Aplicacion:
        db_aplicacion = models.Aplicacion(
            fecha_aplicacion=aplicacion.fecha_aplicacion,
            producto_id=aplicacion.producto_id,
            cultivo_id=aplicacion.cultivo_id,
            dosis_aplicada=aplicacion.dosis_aplicada,
            unidad_medida=aplicacion.unidad_medida,
            area_tratada=aplicacion.area_tratada,
            motivo=aplicacion.motivo,
            observaciones=aplicacion.observaciones,
            fecha_segura_reingreso=aplicacion.fecha_segura_reingreso,
            usuario_id=aplicacion.usuario_id,
            fecha_registro=aplicacion.fecha_registro
        )
        self.db.add(db_aplicacion)
        self.db.commit()
        self.db.refresh(db_aplicacion)
        
        return self._map_to_entity(db_aplicacion)
    
    def obtener_por_id(self, aplicacion_id: int) -> Optional[Aplicacion]:
        db_aplicacion = self.db.query(models.Aplicacion).filter(
            models.Aplicacion.id == aplicacion_id
        ).first()
        
        if db_aplicacion is None:
            return None
        
        return self._map_to_entity(db_aplicacion)
    
    def listar_por_cultivo(self, cultivo_id: int) -> List[Aplicacion]:
        db_aplicaciones = self.db.query(models.Aplicacion).filter(
            models.Aplicacion.cultivo_id == cultivo_id
        ).order_by(models.Aplicacion.fecha_aplicacion.desc()).all()
        
        return [self._map_to_entity(db_aplicacion) for db_aplicacion in db_aplicaciones]
    
    def listar_por_usuario(self, usuario_id: int) -> List[Aplicacion]:
        db_aplicaciones = self.db.query(models.Aplicacion).filter(
            models.Aplicacion.usuario_id == usuario_id
        ).order_by(models.Aplicacion.fecha_aplicacion.desc()).all()
        
        return [self._map_to_entity(db_aplicacion) for db_aplicacion in db_aplicaciones]
    
    def listar_por_fecha(self, fecha_inicio: date, fecha_fin: date, usuario_id: int) -> List[Aplicacion]:
        db_aplicaciones = self.db.query(models.Aplicacion).filter(
            models.Aplicacion.fecha_aplicacion >= fecha_inicio,
            models.Aplicacion.fecha_aplicacion <= fecha_fin,
            models.Aplicacion.usuario_id == usuario_id
        ).order_by(models.Aplicacion.fecha_aplicacion.desc()).all()
        
        return [self._map_to_entity(db_aplicacion) for db_aplicacion in db_aplicaciones]
    
    def actualizar(self, aplicacion: Aplicacion) -> Aplicacion:
        db_aplicacion = self.db.query(models.Aplicacion).filter(
            models.Aplicacion.id == aplicacion.id
        ).first()
        
        if db_aplicacion is None:
            return None
        
        db_aplicacion.fecha_aplicacion = aplicacion.fecha_aplicacion
        db_aplicacion.dosis_aplicada = aplicacion.dosis_aplicada
        db_aplicacion.unidad_medida = aplicacion.unidad_medida
        db_aplicacion.area_tratada = aplicacion.area_tratada
        db_aplicacion.motivo = aplicacion.motivo
        db_aplicacion.observaciones = aplicacion.observaciones
        db_aplicacion.fecha_segura_reingreso = aplicacion.fecha_segura_reingreso
        
        self.db.commit()
        self.db.refresh(db_aplicacion)
        
        return self._map_to_entity(db_aplicacion)
    
    def eliminar(self, aplicacion_id: int) -> bool:
        db_aplicacion = self.db.query(models.Aplicacion).filter(
            models.Aplicacion.id == aplicacion_id
        ).first()
        
        if db_aplicacion is None:
            return False
        
        self.db.delete(db_aplicacion)
        self.db.commit()
        
        return True
    
    def _map_to_entity(self, db_aplicacion: models.Aplicacion) -> Aplicacion:
        return Aplicacion(
            id=db_aplicacion.id,
            fecha_aplicacion=db_aplicacion.fecha_aplicacion,
            producto_id=db_aplicacion.producto_id,
            cultivo_id=db_aplicacion.cultivo_id,
            dosis_aplicada=db_aplicacion.dosis_aplicada,
            unidad_medida=db_aplicacion.unidad_medida,
            area_tratada=db_aplicacion.area_tratada,
            motivo=db_aplicacion.motivo,
            observaciones=db_aplicacion.observaciones,
            fecha_segura_reingreso=db_aplicacion.fecha_segura_reingreso,
            usuario_id=db_aplicacion.usuario_id,
            fecha_registro=db_aplicacion.fecha_registro
        )