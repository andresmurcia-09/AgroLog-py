from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ParcelaBase(BaseModel):
    nombre: str
    ubicacion: Optional[str] = None
    superficie: Optional[float] = None


class ParcelaCreate(ParcelaBase):
    pass


class ParcelaUpdate(BaseModel):
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    superficie: Optional[float] = None


class ParcelaResponse(ParcelaBase):
    id: int
    usuario_id: int
    fecha_registro: datetime
    activo: bool

    class Config:
        from_attributes = True