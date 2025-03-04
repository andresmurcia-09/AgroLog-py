from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


@dataclass
class Cultivo:
    id: Optional[int]
    nombre: str
    variedad: Optional[str]
    fecha_siembra: Optional[date]
    fecha_cosecha_estimada: Optional[date]
    parcela_id: int
    fecha_registro: datetime
    activo: bool = True