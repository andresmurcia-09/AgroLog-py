from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class CultivoBase(BaseModel):
    nombre: str
    variedad: Optional[str] = None
    fecha_siembra: Optional[date] = None
    fecha_cosecha_estimada: Optional[date] = None
    parcela_id: int


class CultivoCreate(CultivoBase):
    pass


class CultivoUpdate(BaseModel):
    nombre: Optional[str] = None
    variedad: Optional[str] = None
    fecha_siembra: Optional[date] = None
    fecha_cosecha_estimada: Optional[date] = None


class CultivoResponse(CultivoBase):
    id: int
    fecha_registro: datetime
    activo: bool

    class Config:
        from_attributes = True