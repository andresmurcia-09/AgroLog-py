from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class AplicacionBase(BaseModel):
    fecha_aplicacion: date
    producto_id: int
    cultivo_id: int
    dosis_aplicada: float
    unidad_medida: str
    area_tratada: Optional[float] = None
    motivo: Optional[str] = None
    observaciones: Optional[str] = None


class AplicacionCreate(AplicacionBase):
    pass


class AplicacionUpdate(BaseModel):
    fecha_aplicacion: Optional[date] = None
    dosis_aplicada: Optional[float] = None
    unidad_medida: Optional[str] = None
    area_tratada: Optional[float] = None
    motivo: Optional[str] = None
    observaciones: Optional[str] = None


class AplicacionResponse(AplicacionBase):
    id: int
    fecha_segura_reingreso: Optional[date] = None
    usuario_id: int
    fecha_registro: datetime

    class Config:
        from_attributes = True


class AplicacionDetalleResponse(AplicacionResponse):
    producto_nombre: str
    cultivo_nombre: str
    parcela_nombre: str

    class Config:
        from_attributes = True