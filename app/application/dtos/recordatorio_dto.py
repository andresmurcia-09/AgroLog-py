from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class RecordatorioBase(BaseModel):
    aplicacion_id: int
    fecha_recordatorio: date
    tipo: str
    mensaje: str


class RecordatorioCreate(RecordatorioBase):
    pass


class RecordatorioUpdate(BaseModel):
    fecha_recordatorio: Optional[date] = None
    tipo: Optional[str] = None
    mensaje: Optional[str] = None


class RecordatorioResponse(RecordatorioBase):
    id: int
    completado: bool
    fecha_registro: datetime

    class Config:
        from_attributes = True


class RecordatorioDetalleResponse(RecordatorioResponse):
    aplicacion_fecha: date
    producto_nombre: str
    cultivo_nombre: str

    class Config:
        from_attributes = True