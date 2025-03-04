from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


@dataclass
class Aplicacion:
    id: Optional[int]
    fecha_aplicacion: date
    producto_id: int
    cultivo_id: int
    dosis_aplicada: float
    unidad_medida: str
    area_tratada: Optional[float]
    motivo: Optional[str]
    observaciones: Optional[str]
    fecha_segura_reingreso: Optional[date]
    usuario_id: int
    fecha_registro: datetime