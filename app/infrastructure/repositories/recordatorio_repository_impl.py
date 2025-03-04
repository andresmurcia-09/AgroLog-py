from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session, joinedload

from app.domain.entities.recordatorio import Recordatorio
from app.domain.repositories.recordatorio_repository import RecordatorioRepository
from app.infrastructure.persistence import models


class RecordatorioRepositoryImpl(RecordatorioRepository):
    def __init__(self, db: Session):
        self.db = db

    def crear(self, recordatorio: Recordatorio) -> Recordatorio:
        db_recordatorio = models.Recordatorio(
            aplicacion_id=recordatorio.aplicacion_id,
            fecha_recordatorio=recordatorio.fecha_recordatorio,
            tipo=recordatorio.tipo,
            mensaje=recordatorio.mensaje,
            completado=recordatorio.completado,
            fecha_registro=recordatorio.fecha_registro
        )
        self.db.add(db_recordatorio)
        self.db.commit()
        self.db.refresh(db_recordatorio)

        return self._map_to_entity(db_recordatorio)

    def obtener_por_id(self, recordatorio_id: int) -> Optional[Recordatorio]:
        db_recordatorio = self.db.query(models.Recordatorio).filter(
            models.Recordatorio.id == recordatorio_id
        ).first()

        if db_recordatorio is None:
            return None

        return self._map_to_entity(db_recordatorio)

    def listar_por_aplicacion(self, aplicacion_id: int) -> List[Recordatorio]:
        db_recordatorios = self.db.query(models.Recordatorio).filter(
            models.Recordatorio.aplicacion_id == aplicacion_id
        ).all()

        return [self._map_to_entity(db_recordatorio) for db_recordatorio in db_recordatorios]

    def listar_pendientes_por_usuario(self, usuario_id: int) -> List[Recordatorio]:
        db_recordatorios = self.db.query(models.Recordatorio).join(
            models.Aplicacion
        ).filter(
            models.Aplicacion.usuario_id == usuario_id,
            models.Recordatorio.completado == False
        ).order_by(models.Recordatorio.fecha_recordatorio.asc()).all()

        return [self._map_to_entity(db_recordatorio) for db_recordatorio in db_recordatorios]

    def listar_por_fecha(self, fecha: date, usuario_id: int) -> List[Recordatorio]:
        db_recordatorios = self.db.query(models.Recordatorio).join(
            models.Aplicacion
        ).filter(
            models.Aplicacion.usuario_id == usuario_id,
            models.Recordatorio.fecha_recordatorio == fecha
        ).all()

        return [self._map_to_entity(db_recordatorio) for db_recordatorio in db_recordatorios]

    def marcar_completado(self, recordatorio_id: int) -> Recordatorio:
        db_recordatorio = self.db.query(models.Recordatorio).filter(
            models.Recordatorio.id == recordatorio_id
        ).first()

        if db_recordatorio is None:
            return None

        db_recordatorio.completado = True
        self.db.commit()
        self.db.refresh(db_recordatorio)

        return self._map_to_entity(db_recordatorio)

    def actualizar(self, recordatorio: Recordatorio) -> Recordatorio:
        db_recordatorio = self.db.query(models.Recordatorio).filter(
            models.Recordatorio.id == recordatorio.id
        ).first()

        if db_recordatorio is None:
            return None

        db_recordatorio.fecha_recordatorio = recordatorio.fecha_recordatorio
        db_recordatorio.tipo = recordatorio.tipo
        db_recordatorio.mensaje = recordatorio.mensaje
        db_recordatorio.completado = recordatorio.completado

        self.db.commit()
        self.db.refresh(db_recordatorio)

        return self._map_to_entity(db_recordatorio)

    def eliminar(self, recordatorio_id: int) -> bool:
        db_recordatorio = self.db.query(models.Recordatorio).filter(
            models.Recordatorio.id == recordatorio_id
        ).first()

        if db_recordatorio is None:
            return False

        self.db.delete(db_recordatorio)
        self.db.commit()

        return True

    def _map_to_entity(self, db_recordatorio: models.Recordatorio) -> Recordatorio:
        return Recordatorio(
            id=db_recordatorio.id,
            aplicacion_id=db_recordatorio.aplicacion_id,
            fecha_recordatorio=db_recordatorio.fecha_recordatorio,
            tipo=db_recordatorio.tipo,
            mensaje=db_recordatorio.mensaje,
            completado=db_recordatorio.completado,
            fecha_registro=db_recordatorio.fecha_registro
        )