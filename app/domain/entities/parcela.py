from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Parcela:
    id: Optional[int]
    nombre: str
    ubicacion: Optional[str]
    superficie: Optional[float]
    usuario_id: int
    fecha_registro: datetime
    activo: bool = True