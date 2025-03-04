from typing import List, Optional
from sqlalchemy.orm import Session

from app.domain.entities.parcela import Parcela
from app.domain.repositories.parcela_repository import ParcelaRepository
from app.infrastructure.persistence import models


class ParcelaRepositoryImpl(ParcelaRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def crear(self, parcela: Parcela) -> Parcela:
        db_parcela = models.Parcela(
            nombre=parcela.nombre,
            ubicacion=parcela.ubicacion,
            superficie=parcela.superficie,
            usuario_id=parcela.usuario_id,
            fecha_registro=parcela.fecha_registro,
            activo=parcela.activo
        )
        self.db.add(db_parcela)
        self.db.commit()
        self.db.refresh(db_parcela)
        
        return self._map_to_entity(db_parcela)
    
    def obtener_por_id(self, parcela_id: int) -> Optional[Parcela]:
        db_parcela = self.db.query(models.Parcela).filter(models.Parcela.id == parcela_id).first()
        if db_parcela is None:
            return None
        
        return self._map_to_entity(db_parcela)
    
    def listar_por_usuario(self, usuario_id: int) -> List[Parcela]:
        db_parcelas = self.db.query(models.Parcela).filter(
            models.Parcela.usuario_id == usuario_id,
            models.Parcela.activo == True
        ).all()
        
        return [self._map_to_entity(db_parcela) for db_parcela in db_parcelas]
    
    def actualizar(self, parcela: Parcela) -> Parcela:
        db_parcela = self.db.query(models.Parcela).filter(models.Parcela.id == parcela.id).first()
        if db_parcela is None:
            return None
        
        db_parcela.nombre = parcela.nombre
        db_parcela.ubicacion = parcela.ubicacion
        db_parcela.superficie = parcela.superficie
        db_parcela.activo = parcela.activo
        
        self.db.commit()
        self.db.refresh(db_parcela)
        
        return self._map_to_entity(db_parcela)
    
    def eliminar(self, parcela_id: int) -> bool:
        db_parcela = self.db.query(models.Parcela).filter(models.Parcela.id == parcela_id).first()
        if db_parcela is None:
            return False
        
        db_parcela.activo = False
        self.db.commit()
        
        return True
    
    def _map_to_entity(self, db_parcela: models.Parcela) -> Parcela:
        return Parcela(
            id=db_parcela.id,
            nombre=db_parcela.nombre,
            ubicacion=db_parcela.ubicacion,
            superficie=db_parcela.superficie,
            usuario_id=db_parcela.usuario_id,
            fecha_registro=db_parcela.fecha_registro,
            activo=db_parcela.activo
        )