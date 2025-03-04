from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductoFitosanitarioBase(BaseModel):
    nombre: str
    tipo: str
    fabricante: Optional[str] = None
    principio_activo: Optional[str] = None
    dosis_recomendada: Optional[str] = None
    periodo_carencia: Optional[int] = None


class ProductoFitosanitarioCreate(ProductoFitosanitarioBase):
    pass


class ProductoFitosanitarioUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    fabricante: Optional[str] = None
    principio_activo: Optional[str] = None
    dosis_recomendada: Optional[str] = None
    periodo_carencia: Optional[int] = None


class ProductoFitosanitarioResponse(ProductoFitosanitarioBase):
    id: int
    usuario_id: int
    fecha_registro: datetime
    activo: bool

    class Config:
        from_attributes = True